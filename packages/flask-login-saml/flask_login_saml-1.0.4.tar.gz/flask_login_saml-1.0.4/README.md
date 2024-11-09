# flask-login-saml
Flask SAML2 with flask-login

## Installation

```bash
pip install flask-login-saml
```

## Setup

- Base login configuration

```python 
import flask

from flask_login import LoginManager, login_required, current_user
from flask_login_saml import FlaskSAML

app = flask.Flask('flask')
saml = FlaskSAML()


def redirect_login():
    return flask.redirect(flask.url_for('saml.login'))


@app.route('/saml/login/', endpoint='saml.login', methods=['GET'])
def login():
    return saml.saml_login()


@app.route('/saml/metadata/', endpoint='saml.metadata', methods=['GET'])
def metadata():
    return saml.metadata()


@app.route('/saml/authorize/', endpoint='saml.authorize', methods=['POST'])
def authorize():
    return saml.authorize()


@app.route('/saml/logout/', endpoint='saml.logout', methods=['GET'])
@login_required
def logout():
    return saml.saml_logout()


@app.route('/', methods=['GET'])
@login_required
def index():
    return current_user.subject


if __name__ == '__main__':
    lm = LoginManager(app)
    lm.unauthorized_handler(redirect_login)
    lm.user_loader(saml.user)
    app.config.setdefault(
        'SAML_METADATA_URL',
        'https://<idp>/descriptor'
    )
    app.config['SECRET_KEY'] = 'secret'
    app.config['SESSION_TYPE'] = 'filesystem'
    saml.init_app(app)
    app.run()

```

- Custom login configuration

```python
import flask

from flask_login import LoginManager, login_required, current_user
from flask_login_saml import FlaskSAML

app = flask.Flask('flask')
saml = FlaskSAML(prefix='SSO')


def redirect_login():
    return flask.redirect(flask.url_for('sso.login'))


@app.route('/sso/login/', endpoint='sso.login', methods=['GET'])
def login():
    return saml.saml_login()


@app.route('/sso/metadata/', endpoint='sso.metadata', methods=['GET'])
def metadata():
    return saml.metadata()


@app.route('/sso/authorize/', endpoint='sso.authorize', methods=['POST'])
def authorize():
    return saml.authorize()


@app.route('/sso/logout/', endpoint='sso.logout', methods=['GET'])
@login_required
def logout():
    return saml.saml_logout()


@app.route('/', methods=['GET'])
@login_required
def index():
    return current_user.subject


if __name__ == '__main__':
    lm = LoginManager(app)
    lm.unauthorized_handler(redirect_login)
    lm.user_loader(saml.user)
    app.config.setdefault(
        'SSO_METADATA_URL',
        'https://<idp>/protocol/saml/descriptor'
    )
    app.config['SECRET_KEY'] = 'secret'
    app.config['SESSION_TYPE'] = 'filesystem'
    saml.init_app(app)
    app.run()
```

## Using custom user model

Must be used after FlaskSAML.init_app() or FlaskSAML() if you are not using it

```python
saml.user_model(UserModel)
```

See [user.py](https://github.com/frederickney/flask-login-saml/blob/main/flask_login_saml/user.py) for more information about user model

## Custom login

Must be used after FlaskSAML.init_app() or FlaskSAML() if you are not using it

```python
def login(model, sender, subject, attributes, assertion, auth):
    """
    
    :param model:  
    :param sender: application identifier
    :type sender: str
    :param subject: email address of the logged user
    :type subject: str
    :param attributes: list of user attributes
    :type attributes: list
    :param assertion: saml user assertion
    :type assertion: str
    :param auth: saml authn response used for remembering
    :type auth: str
    :return: if user logged in or not
    :rtype: bool
    
    """
    pass

saml.login_user(login)
```

## Custom logout

Must be used after FlaskSAML.init_app() or FlaskSAML() if you are not using it

```python

def logout(sender):
    """
    :param sender: application identifier
    :type sender: str
    
    """
    pass

saml.logout_user(logout)
```

## Custom error

Must be used after FlaskSAML.init_app() or FlaskSAML() if you are not using it

```python
def error(sender, exception):
    """
    :param sender: application identifier
    :type sender: str
    :param exception: application exception
    :type exception: Exception
    
    """
    pass

saml.error(error)
```

## Custom client

Must be used after FlaskSAML.init_app() or FlaskSAML() if you are not using it

```python
def client(prefix, metadata, allow_unknown_attributes=True):
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
    pass

saml.client(client)
```

Enjoy

# LICENSE

#### See [License file](LICENSE)