from setuptools import setup

setup(
    name='jupyterhub-dvtauthenticator',
    version='0.1',
    description='Data Vault Authenticator for JupyterHub',
    url='https://github.com/pranay/dvtauthenticator',
    author='mogthesprog',
    author_email='pranayhasan@gmail.com',
    license='Apache 2.0',
    tests_require = [
    'unittest2',
    ],
    test_suite = 'unittest2.collector',
    packages=['dvtauthenticator'],
    install_requires=[
        'jupyterhub',
        'python-jose'
    ]
)
