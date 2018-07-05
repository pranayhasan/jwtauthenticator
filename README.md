# JupyterHub tokenauthenticator - A Data Valut Token Authenticator for JupyterHub

Authenticate to Jupyterhub using a query parameter for the Data Vault Token, or by an authenticating proxy that can set the Authorization header with the content of a JSONWebToken.

## Installation

This package can be installed with pip:

```
pip install jupyterhub-dvtauthenticator
```

Alternately, you can clone this repository and run:

```
cd dvtauthenticator
pip install -e .
```

## Configuration

You should edit your :file:`jupyterhub_config.py` to set the authenticator class, the JSONWebTokenLocalAuthenticator provides features such as local user creation. If you already have local users then you may use the JSONWebTokenAuthenticator authenticator class:

##### For authentication of the token only

```
c.JupyterHub.authenticator_class = 'dvtauthenticator.dvtauthenticator.DataVaultTokenAuthenticator'
```

##### Required configuration

You'll also need to set some configuration options including the location of the signing certificate (in PEM format), field containing the userPrincipalName or sAMAccountName/username, and the expected audience of the JSONWebToken. This last part is optional, if you set audience to an empty string then the authenticator will skip the validation of that field.

```
c.DataVaultTokenAuthenticator.header_name = 'Authorization' # default value
c.DataVaultTokenAuthenticator.dvfiles_path = '/path/to/dvfiles'
c.DataVaultTokenAuthenticator.fabric = 'CORP'
```

You should be able to start jupyterhub. :)

## Issues

If you have any issues or bug reports, all are welcome in the issues section. I'll do my best to respond quickly.

## Contribution

If you want to fix the bugs yourself then raise a PR and I'll take a look :)
