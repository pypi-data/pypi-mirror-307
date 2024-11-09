# coding: utf-8

__author__ = "Frédérick NEY"


import logging
import inspect
import saml2
import saml2.client
import saml2.config
import saml2.metadata
import saml2.entity

from flask import current_app, flash, signals, request, redirect, url_for
from flask_login import login_user, logout_user
from .user import SAMLUser
signals = signals.Namespace()


def _saml_error(sender, exception):
    logging.error("{}: {}".format(sender, exception))


def _login_saml_user(model, sender, subject, attributes, assertion, auth):
        """

        :param sender: application identifier
        :type sender: str
        :param subject: email address of the logged user
        :type subject: str
        :param attributes: list of user attributes
        :type attributes: list
        :param auth: saml authn response used for remembering
        :type auth: str
        :return:
        """
        user = model(sender=sender, subject=subject, attributes=attributes, assertion=assertion, auth=auth)
        logging.debug("{}: {}".format(__name__, user.__dict__))
        flash('Successfully logged in')
        return login_user(user)


def _logout_saml_user(sender):
    logging.debug("{}: logged out".format(__name__))
    flash('logged out')
    logout_user()


def _get_metadata(metadata_url):  # pragma: no cover
    """

    :param metadata_url:
    :type metadata_url: str
    :return:
    """
    if metadata_url.startswith('http'):
        import requests
        response = requests.get(metadata_url)
        if response.status_code != 200:
            exc = RuntimeError(
                'Unexpected Status Code: {0}'.format(response.status_code))
            exc.response = response
            raise exc
        return response.text
    else:
        file = open(metadata_url, 'r')
        text = file.read()
        file.close()
        return text


def _get_client(prefix, metadata, allow_unknown_attributes=True):
    """
    :param prefix:
    :type prefix: str
    :param metadata:
    :type metadata: str
    :param allow_unknown_attributes:
    :type allow_unknown_attributes: bool
    :return:
    :rtype: saml2.client.Saml2Client
    """
    acs_url = url_for('{}.authorize'.format(prefix.lower()), _external=True)
    metadata_url = url_for('{}.metadata'.format(prefix.lower()), _external=True)
    settings = {
        'entityid': metadata_url,
        'metadata': {
            'inline': [metadata],
        },
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (acs_url, saml2.BINDING_HTTP_POST),
                    ],
                },
                # Don't verify that the incoming requests originate from us via
                # the built-in cache for authn request ids in pysaml2
                'allow_unsolicited': True,
                # Don't sign authn requests, since signed requests only make
                # sense in a situation where you control both the SP and IdP
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': True,
                'want_response_signed': False,
            },
        },
    }
    config = saml2.config.Config()
    config.load(settings)
    config.allow_unknown_attributes = allow_unknown_attributes
    client = saml2.client.Saml2Client(config=config)
    return client


class FlaskSAML(object):

    _logout_user = None
    _login_user = None
    _error = None

    def __init__(self, app=None, prefix='SAML'):
        self._logout_user = _logout_saml_user
        self._login_user = _login_saml_user
        self._get_client = _get_client
        self._error = _saml_error
        self.app = app
        self._prefix = prefix
        self._user_model = SAMLUser
        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        """

        :param app:
        :type app: flask.Flask
        :return:
        """
        app.config.setdefault('{}_PREFIX'.format(self._prefix), self._prefix)
        app.config.setdefault('{}_DEFAULT_REDIRECT'.format(self._prefix), '/')
        config = {
            'metadata': _get_metadata(
                metadata_url=app.config['{}_METADATA_URL'.format(self._prefix)],
            ),
            'prefix': app.config['{}_PREFIX'.format(self._prefix)],
            'default_redirect': app.config['{}_DEFAULT_REDIRECT'.format(self._prefix)],
        }
        # Register configuration on app so we can retrieve it later on
        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}
        if self._prefix.lower() not in app.extensions.keys():
            app.extensions[self._prefix.lower()] = self, config
        else:
            _, config = app.extensions[self._prefix.lower()]

    def saml_prepare(self):
        """

        :return:
        :rtype: saml2.client.Saml2Client
        """
        ext, config = current_app.extensions[self._prefix.lower()]
        client = self._get_client(self._prefix, config['metadata'])
        return client

    def metadata(self):
        """
        metadata base view
        :return:
        """
        saml_client = self.saml_prepare()
        metadata_str = saml2.metadata.create_metadata_string(
            configfile=None,
            config=saml_client.config,
        )
        return metadata_str, {'Content-Type': 'text/xml'}

    def saml_logout(self):
        saml_client = self.saml_prepare()
        logging.debug('Received logout request')
        self._logout_user(
            current_app.name
        )
        ext, config = current_app.extensions[self._prefix.lower()]
        url = request.url_root[:-1] + config['default_redirect']
        return redirect(url)

    def saml_login(self):
        saml_client = self.saml_prepare()
        logging.debug('Received login request')
        return_to = request.args.get('next', '')
        ext, config = current_app.extensions[self._prefix.lower()]
        if not return_to.startswith(request.url_root):
            return_to = config['default_redirect']
        reqid, info = saml_client.prepare_for_authenticate(
            relay_state=return_to,
        )
        headers = dict(info['headers'])
        response = redirect(headers.pop('Location'), code=302)
        for name, value in headers.items():
            response.headers[name] = value
        response.headers['Cache-Control'] = 'no-cache, no-store'
        response.headers['Pragma'] = 'no-cache'
        return response

    def user(self, xml_assertion):
        """

        :param xml_assertion:
        :return: logged in user
        """
        if hasattr(self._user_model, 'load_from_assertion'):
            return self._user_model.load_from_assertion(xml_assertion)
        else:
            logging.warning("{}.{}.user_model: {} has no attribute load_from_assertion".format(
                __name__,
                __class__.__name__,
                self._user_model
            ))
            return SAMLUser.load_from_assertion(xml_assertion)

    def authorize(self):
        if 'SAMLResponse' in request.form:
            logging.debug('Received SAMLResponse for login')
            try:
                saml_client = self.saml_prepare()
                authn_response = saml_client.parse_authn_request_response(
                    request.form['SAMLResponse'],
                    saml2.entity.BINDING_HTTP_POST,
                )
                if authn_response is None:
                    raise RuntimeError('Unknown SAML error, please check logs')
            except Exception as exc:
                self._error(
                    current_app.name,
                    exception=exc,
                )
            else:
                self._login_user(
                    self._user_model,
                    current_app.name,
                    subject=authn_response.get_subject().text,
                    attributes=authn_response.get_identity(),
                    assertion=authn_response.assertion,
                    auth=authn_response
                )
                logging.info('{}: User loged in'.format(__name__))
            relay_state = request.form.get('RelayState')
            ext, config = current_app.extensions[self._prefix.lower()]
            if not relay_state:
                relay_state = config['default_redirect']
            redirect_to = relay_state
            if not relay_state.startswith(request.url_root):
                redirect_to = request.url_root[:-1] + redirect_to
            return redirect(redirect_to)
        return 'Missing SAMLResponse POST data', 500

    def login_user(self, callback):
        if callable(callback) and not inspect.isclass(callback):
            self._login_user = callback
        else:
            raise Exception("{}.{}.login_user: {} not callable".format(__name__, __class__.__name__, callback))

    def logout_user(self, callback):
        if callable(callback) and  not inspect.isclass(callback):
            self._logout_user = callback
        else:
            raise Exception("{}.{}.logout_user: {} not callable".format(__name__, __class__.__name__, callback))

    def client(self, callback):
        if callable(callback) and not inspect.isclass(callback):
            self._get_client = callback
        else:
            raise Exception("{}.{}.client: {} not callable".format(__name__, __class__.__name__, callback))

    def error(self, callback):
        if callable(callback) and not inspect.isclass(callback):
            self._error = callback
        else:
            raise Exception("{}.{}.error: {} not callable".format(__name__, __class__.__name__, callback))

    def user_model(self, model):
        if inspect.isclass(model):
            self._user_model = model
        else:
            raise Exception("{}.{}.user_model: {} not a class".format(__name__, __class__.__name__, model))
