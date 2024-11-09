# coding: utf-8

import logging
from datetime import datetime
import saml2.saml

from flask import current_app


class SAMLUser(object):

    @staticmethod
    def load_from_assertion(xml):
        """

        :param xml:
        :return:
        :rtype: SAMLUser
        """
        assertion = saml2.saml.assertion_from_string(xml)
        attributes = {'Role': []}
        for attribute_statement in assertion.attribute_statement:
            for attribute in attribute_statement.attribute:
                for val in attribute.attribute_value:
                    attributes['Role'].append(val.text)
        return SAMLUser(
            sender=current_app.name,
            subject=assertion.subject.name_id.text,
            attributes=attributes,
            assertion=assertion
        )

    def __init__(self, **kwargs):
        for key, attr in kwargs.items():
            logging.debug("{}: SAML {} -> {}".format(__name__, key, attr))
            setattr(self, key, str(attr))

    def get_id(self):
        if hasattr(self, 'assertion'):
            return getattr(self, 'assertion')

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        if hasattr(self, "assertion"):
            return datetime.fromisoformat(
                saml2.saml.assertion_from_string(getattr(self, 'assertion')).authn_statement[0].session_not_on_or_after
            ).strftime('%Y-%m-%dT%H:%M:%S.%fZ') > datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    @property
    def is_anonymous(self):
        return False
