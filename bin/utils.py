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

from configparser import ConfigParser


class config():
    """
    設定檔讀取類別
    """
    def __init__(self):
        pass

    def get_config(self, section, config_path):
        config = ConfigParser()
        config.read(config_path)
        return dict(config.items(section))


class File():
    """
    輸出檔案類別
    """
    def __init__(self):
        import datetime
        self.today = datetime.datetime.now().strftime("%Y%m%d")

    def save(self, data, path, file_name, file_type):
        import os
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            if file_type == 'json':
                try:
                    export = self.export(path, file_name, file_type, data)
                    return export
                except Exception as _:
                    return _
            elif file_type == 'csv':
                try:
                    data = data.replace('\t', ',')
                    export = self.export(path, file_name, file_type, data)
                    return export
                except Exception as _:
                    return _
            else:
                return False

        except Exception as _:
            return _

    def export(self, path, file_name, file_type, data):
        file = f"{path}/{file_name}{self.today}.{file_type}"
        with open(file, "w", encoding='utf-8') as f:
            f.write(data)
        return F"輸出{file_type}檔案至--->> {file}"


class Bot():
    """
    機器人推播類別
    """
    def __init__(self):
        pass

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    def send_message(self, webhook, key):
        import requests
        import json
        params = (
            ('key', str(key)),
        )
        headers = {
            'Content-Type': 'application/json',
            'charset': 'utf-8'
        }
        if self.content:
            data = {
                "msgtype": "text",
                "text": {"content": str(self.content)}
            }
            data = json.dumps(data)
            try:
                response = requests.post(
                    webhook, headers=headers,
                    params=params, data=data.encode('utf-8'),
                    verify=False
                )
                return True, True
            except Exception as _:
                return False, _
        else:
            return False, "清洗完的數據是空的,請檢查ETL清洗邏輯"
