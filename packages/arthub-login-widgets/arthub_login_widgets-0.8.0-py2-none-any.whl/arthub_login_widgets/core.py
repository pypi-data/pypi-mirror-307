# -*- coding: utf-8 -*-
"""A Qt Widget for login ArtHub."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import logging
import webbrowser
import os
import re

from arthub_api import OpenAPI
from arthub_api import api_config_qq
from arthub_api import api_config_qq_test

# Import local modules
from arthub_login_widgets.constants import ARTHUB_RESET_PASSWORD_WEB_URL
from arthub_login_widgets.constants import ARTHUB_SET_ACCOUNT_INFO_WEB_URL
from arthub_login_widgets.constants import UI_TEXT_MAP
from arthub_login_widgets.filesystem import get_login_account
from arthub_login_widgets.filesystem import get_resource_file
from arthub_login_widgets.filesystem import get_client_exe_path
from arthub_login_widgets.filesystem import save_login_account
from arthub_login_widgets.filesystem import get_token_from_file
from arthub_login_widgets.filesystem import run_exe_sync
from arthub_login_widgets.filesystem import ProcessRunner
from arthub_login_widgets.exception import ErrorClientNotExists


def load_style_sheet(style_file):
    with open(style_file, "r") as css_file:
        css_string = css_file.read().strip("\n")
        data = os.path.expandvars(css_string)
        return data


class TaskPadWindow(ProcessRunner):
    def __init__(self,
                 login_backend,
                 port_id,
                 window_x=None,
                 window_y=None
                 ):
        self.login_backend = login_backend
        args = login_backend.get_args(window_x=window_x, window_y=window_y, ipc_port=port_id)
        args.append("--taskpad")
        super(TaskPadWindow, self).__init__(exe_path=login_backend.exe_path, args=args)

    def open(self):
        self.start_process()

    def close(self):
        self.stop_process()


class LoginBackend(object):
    def __init__(
            self,
            terminal_type="default",
            business_type="default",
            dev_mode=False,
            exe_path=None
    ):
        r"""
        The following characters cannot be used in the terminal_type and business_type strings:
            - Space
            - " # $ % & ' ( ) + , / : ; < = > ? @ [ \ ] ^ { | } ~
        """
        self.terminal_type = terminal_type
        self.business_type = business_type
        self.dev_mode = dev_mode
        self._last_token = None
        self._account_detail = None
        self._exe_path = get_client_exe_path()
        self._did_logged_out = False
        if exe_path:
            self._exe_path = exe_path
        default_api_config = api_config_qq_test if dev_mode else api_config_qq
        self.open_api = OpenAPI(config=default_api_config,
                                get_token_from_cache=False,
                                api_config_name=None,
                                apply_blade_env=False)
        self.check_exe()

    @property
    def exe_path(self):
        return self._exe_path

    @property
    def token(self):
        return self._last_token

    @property
    def account_detail(self):
        return self._account_detail

    @property
    def token_cache_file_path(self):
        appdata_path = os.getenv('APPDATA')
        return os.path.join(appdata_path, 'arthub-tools', self.business_type, self.terminal_type, "token_cache.yml")

    def base_url(self):
        return self.open_api.base_url()

    def check_exe(self):
        if not os.path.exists(self.exe_path):
            raise ErrorClientNotExists()

    def get_token_from_cache(self):
        return get_token_from_file(self.token_cache_file_path)

    def clear_token_cache(self):
        file_path = self.token_cache_file_path
        if os.path.exists(file_path):
            os.remove(file_path)

    def is_login(self):
        if self._check_local_token_cache():
            return True
        if self._check_blade_env():
            return True
        return False

    def popup_task_pad(self, port_id, window_x=None, window_y=None):
        w = TaskPadWindow(login_backend=self, port_id=port_id)
        w.open()
        return w

    def popup_login(self, window_x=None, window_y=None):
        args = self.get_args(window_x=window_x, window_y=window_y)
        r = self._call_exe(args)
        if not r[0]:
            return False
        return bool(r[1])

    def popup_admin(self, window_x=None, window_y=None):
        args = self.get_args(window_x=window_x, window_y=window_y)
        args.append("--admin")
        r = self._call_exe(args)
        return r[0]

    def popup_introduction(self, window_x=None, window_y=None):
        args = self.get_args(window_x=window_x, window_y=window_y)
        args.append("--introduction")
        r = self._call_exe(args)
        return r[0]

    def get_args(self, window_x=None, window_y=None, ipc_port=None):
        args = [
            "--terminal-type={}".format(self.terminal_type),
            "--business-type={}".format(self.business_type)
        ]
        if self.dev_mode:
            args.append("--dev-mode")
        if (window_x is not None) and (window_y is not None):
            args.append("--window-center-x={}".format(window_x))
            args.append("--window-center-y={}".format(window_y))
        if ipc_port is not None:
            args.append("--ipc-port={}".format(ipc_port))
        return args

    def _call_exe(self, args):
        exit_code, stdout = run_exe_sync(self._exe_path, args)
        match = re.search(r'\[GetArtHubToken\]\s*([^\n]+)', stdout)
        if not match:
            return True, None
        if not self._check_local_token_cache():
            return True, None
        return True, self.token

    def logout(self):
        self.clear_token_cache()
        self._on_logout()

    def _on_logout(self):
        self._last_token = None
        self._account_detail = None
        self.open_api.logout()
        self._did_logged_out = True

    def _check_blade_env(self):
        if self._did_logged_out:
            return False
        open_api = OpenAPI(config=None,
                           get_token_from_cache=False,
                           api_config_name=None,
                           apply_blade_env=True)
        return self._check_open_api(open_api)

    def _check_local_token_cache(self):
        token_data = self.get_token_from_cache()
        if not token_data:
            return False
        # token_data: {"api_token": "xx", "api_env": "qq" or "qq_test" or "public"}
        token = token_data.get("api_token")
        if not token:
            return False
        api_env = token_data.get("api_env") or "qq"
        open_api = OpenAPI(config=None,
                           get_token_from_cache=False,
                           api_config_name=api_env,
                           apply_blade_env=False
                           )
        open_api.set_token(token, False)
        return self._check_open_api(open_api)

    def _check_open_api(self, open_api):
        if not open_api.config or not open_api.token:
            return False
        account_detail = open_api.current_account_info
        if account_detail is None:
            return False

        self.open_api = open_api
        self._account_detail = account_detail
        self._last_token = open_api.token
        return True
