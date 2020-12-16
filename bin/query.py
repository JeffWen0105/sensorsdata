# =======================================================================
# Author: Jeff
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# If not, see <http://www.gnu.org/licenses/>.
# =======================================================================

import utils
import log
import os
import json

import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


class Api():
    """
    查詢API核心程序
    """

    def __init__(self):
        self.log = log.Log()
        config = utils.config()
        self.root_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)))
        config_file_path = os.path.join(
            self.root_path, "../conf/dataExport.conf")
        # config_file_path = os.path.join(self.root_path, "conf/dataExport.conf")
        self.sa_config = config.get_config(
            section="sa", config_path=config_file_path)
        self.api_config = config.get_config(
            section="api", config_path=config_file_path)

    def query(self):
        # 查詢API執行入口
        if self.conf_check():
            query = self.controller()
            return query
        else:
            return False

    def request(self, params, uri, data):
        # 送出請求
        headers = {'content-type': 'application/json'}
        try:
            response = requests.post(
                self.sa_config['sa_url'] + uri, params=params, data=json.dumps(data), headers=headers, verify=False)
        except Exception as _:
            self.log.write_log(f"WARN  {_}")
            self.log.write_log(f"WARN  請檢查伺服器是否正確，程式終止。。。")
            exit(1)

        if response.status_code == 200:
            self.log.write_log(
                f"INFO  取得數據成功")
            return response.text
        else:
            self.log.write_log(
                f"WARN  回傳狀態：{response.status_code}, {response.text}")
            self.log.write_log(
                f"WARN  請檢查設定檔或是SQL是否正確，程式終止。。。。。。")
            exit(1)

    def controller(self):
        # 不同登入條件控制器
        token = None
        if self.sa_config['super-token']:
            params, uri, data = self.get_query_data(token)
            if params and uri:
                self.log.write_log(f"INFO 嘗試使用super-token取得數據")
                rawdata = self.request(params, uri, data)
                return rawdata
            else:
                return False

        elif self.sa_config['sensorsdata-toke']:
            params, uri, data = self.get_query_data(token)
            if params and uri:
                self.log.write_log(f"INFO 嘗試使用sensorsdata-toke取得數據")
                rawdata = self.request(params, uri, data)
                return rawdata
            else:
                return False

        elif self.sa_config['user'] and self.sa_config['passwd']:
            params, uri, data = self.get_token()
            if params and uri and data:
                self.log.write_log(f"INFO 嘗試取得使用者Token")
                token = self.request(params, uri, data)
                params, uri, data = self.get_query_data(
                    json.loads(token)["session_id"])
                if params and uri:
                    self.log.write_log(f"INFO 嘗試使用sensorsdata-toke取得數據")
                    rawdata = self.request(params, uri, data)
                    return rawdata
            else:
                return False
        else:
            self.log.write_log(f"WARN  Token或是帳號密碼沒有設置，請檢查設定檔，程式終止。。。")
            exit(1)

    def conf_check(self):
        # 必填的項目設定檔檢查
        sa = ['sa_url', 'http', 'project']
        api = ['format', 'table', 'sql']
        sum = 0
        for _ in sa:
            try:
                if not self.sa_config[_]:
                    self.log.write_log(f"WARN  {_}參數設定有漏，請檢查設定檔")
                    return False
            except Exception as _:
                self.log.write_log(f"WARN  {_}參數設定有漏，請檢查設定檔")
                return False
        sum += 1
        for _ in api:
            try:
                if not self.api_config[_]:
                    self.log.write_log(f"WARN  {_}參數設定有漏，請檢查設定檔")
                    return False
            except Exception as _:
                self.log.write_log(f"WARN  {_}參數設定有漏，請檢查設定檔")
                return False
        sum += 1
        return True if sum == 2 else False

    def get_token(self):
        # 使用帳號密碼登入取得使用者Token
        uri = f'/api/v2/auth/login'
        data = {
            "account_name": self.sa_config['user'], "password": self.sa_config['passwd']}
        params = {'project': self.sa_config['project'], 'is_global': 'true'}
        return params, uri, data

    def get_query_data(self, token):
        # SQL設定檔內容檢查
        if self.api_config['sql']:
            SQL = self.api_config['sql']
            params = self.params_maker(token, SQL)
            return params
        elif self.api_config['table']:
            get_table = self.api_config['table']
            if get_table == 'events':
                pass
            elif get_table == 'users':
                pass
            elif get_table == 'items':
                pass
            else:
                self.log.write_log(f"WARN  導出的表設置錯誤，請指定events 、 users 、 items")
                return False
        else:
            self.log.write_log(f"WARN  自定義SQL表達式或是導出的表沒有設置，請檢查設定檔")
            return False

    def get_all_data(self):
        # 依天數去導出全部數據功能尚未完成。。。。
        pass

    def params_maker(self, token, SQL):
        # API參數控制器
        data = ""
        uri = '/api/sql/query'
        marager = [
            ('project', self.sa_config['project']),
            ('q', SQL),
            ('format', self.api_config['format'])
        ]
        if self.sa_config['super-token']:
            marager.append(('token', self.sa_config['super-token']))
            params = tuple(marager)
            return params, uri, data

        elif self.sa_config['sensorsdata-toke']:
            marager.append(
                ('sensorsdata-token', self.sa_config['sensorsdata-toke']))
            params = tuple(marager)
            return params, uri, data

        elif token:
            marager.append(('sensorsdata-token', token))
            params = tuple(marager)
            return params, uri, data

        else:
            self.log.write_log(f"WARN  神策管理者Token或是一般使用者Token沒有設置，請檢查設定檔")
            return False, False, False
