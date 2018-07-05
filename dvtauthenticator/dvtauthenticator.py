from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode

import subprocess

class DataVaultTokenLoginHandler(BaseHandler):

    def get(self):
        header_name = self.authenticator.header_name
        param_name = self.authenticator.param_name
        # dv_token = self.authenticator.dv_token_param

        auth_header_content = self.request.headers.get(header_name, "")
        auth_cookie_content = self.get_cookie("XSRF-TOKEN", "")
        tokenParam = self.get_argument(param_name, default=False)

        if auth_header_content and tokenParam:
            raise web.HTTPError(400)
        elif auth_header_content:
            # we should not see "token" as first word in the AUTHORIZATION header, if we do it could mean someone coming in with a stale API token
            if auth_header_content.split()[0] != "DVToken":
                raise web.HTTPError(403)
            token = auth_header_content.split()[1]
            username = get_username_from_dvtoken(self.authenticator.dvfiles_path, self.authenticator.fabric, token)
            if username is "":
                raise web.HTTPError(403)
            user = self.user_from_username(username)
            self.set_login_cookie(user)
        elif auth_cookie_content:
            token = auth_cookie_content
        elif tokenParam:
            token = tokenParam
        else:
           raise web.HTTPError(401)

        # Set token to be passed to Spawner as an environmental variable
        # self.set_cookie('datavault_access_token', resp_json['access_token'])

        _url = url_path_join(self.hub.server.base_url, 'home')
        next_url = self.get_argument('next', default=False)
        if next_url:
            _url = next_url

        self.redirect(_url, permanent=False)

def _stream(cmd):
    """
    Method helps execute a command via subprocess
    :param cmd: The command to execute
    :return:
    """
    # color_print(getuser() + '$ ' + cmd, COLOR.BLUE)
    output = []  # used to collect o/p from both stdout and stderr

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, shell=True)
    except subprocess.CalledProcessError as ex:
        print("Status : FAIL", ex.returncode, ex.output)
    else:
        with proc.stdout:
            for line in iter(proc.stdout.readline, b''):
                # print(line)
                output.append(line)

                # Note: output is streamed to the user as and when it occurs.
        with proc.stderr:
            for line in iter(proc.stderr.readline, b''):
                # print(line)
                output.append(line)

        return output

def get_username_from_dvtoken(path, fabric, token):
    if path[-1] == '/':
        path = path[:-1]
    output = _stream(path + '/jupyterhub.pex ' + path + '/dvtoken -t ' + token + ' -f ' + fabric)
    user = str(output[0][:-1], 'utf-8')
    return user

class DataVaultTokenAuthenticator(Authenticator):
    """
    Accept the authenticated Data Valut Token from header.
    """
    header_name = Unicode(
        config=True,
        default_value='Authorization',
        help="""HTTP header to inspect for the authenticated Data Vault Token.""")

    param_name = Unicode(
        config=True,
        default_value='access_token',
        help="""The name of the query parameter used to specify the DVT token""")

    dvfiles_path = Unicode(
        config=True,
        help="""The path to the pex and the python bin for DVToken authorization"""
    )

    fabric = Unicode(
        config=True,
        default_value='EI',
        help="""Fabric for which the DVToken is being validated for"""
    )

    def get_handlers(self, app):
        return [
            (r'/login', DataVaultTokenLoginHandler),
        ]

    # @gen.coroutine
    # def authenticate(self, handler, data=None):
    #     # username = yield identity_user(handler, data)
    #     self.set_cookie('other_access_token', resp_json['access_token'])
