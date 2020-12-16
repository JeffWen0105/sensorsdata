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


import os

import log
import ETL
import utils


class Handler():
    """
    流程控制器
    """

    def __init__(self):
        self.log = log.Log()
        config = utils.config()
        self.root_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)))
        config_file_path = os.path.join(
            self.root_path, "../conf/dataExport.conf")
        self.file_config = config.get_config(
            section="file", config_path=config_file_path)
        self.api_config = config.get_config(
            section="api", config_path=config_file_path)
        self.ETL_config = config.get_config(
            section="ETL", config_path=config_file_path)
        self.wecom_config = config.get_config(
            section="wecom_push", config_path=config_file_path)

    def check_results(self, data):
        # 檢查查詢數據是否為空值，回傳的Json與Csv結果不同很坑
        if self.api_config['format'] == 'json':
            if data == "":
                return False
            else:
                return True
        elif self.api_config['format'] == 'csv':
            if data.split('\n')[1] == "":
                return False
            else:
                return True

    def pipeline(self, data):
        # 實現進階功能流水線
        if self.check_results(data):
            if self.file_config['export'] == 'True':
                # 依設定輸出檔案入口
                save = self.save(data)
                if save:
                    self.log.write_log(f"INFO  {save}")
                else:
                    self.log.write_log(f"WARN  檔案輸出失敗，只能接受json或是csv格式輸出。。")
            parser = ''
            if self.ETL_config['etl'] == 'True':
                if self.api_config['format'] == 'csv':
                    # ETL執行入口
                    self.log.write_log(f"INFO  ETL清洗功能")
                    self.etl = ETL.ETL()
                    parser = self.etl.parser(data)
                else:
                    self.log.write_log(f"WARN  執行ETL清洗請指定csv格式")

            if self.wecom_config['push'] == 'True':
                if self.ETL_config['etl'] == 'True' and str(parser):
                    # 機器人推播入口
                    self.log.write_log(f"INFO  開啟機器人推播功能")
                    self.wecom(parser)
                else:
                    self.log.write_log(
                        f"WARN  使用微信機器人訊息推播訊息，請開啟ETL功能，先清洗完資料再送出唷")

            else:
                self.log.write_log(f"INFO  查詢API功能驗證正常，可以於設定檔開啟進階功能")
        else:
            self.log.write_log(f"WARN  查無資料，請重新設定SQL條件。。。")

    def save(self, data):
        # 輸出檔案取得必要參數
        file_name = self.file_config['name']
        path = os.path.join(self.root_path, "../export")
        file_type = self.api_config['format']
        file = utils.File().save(data=data, path=path,
                                 file_name=file_name, file_type=file_type)
        return file

    def wecom(self, format_data):
        # 機器人推播取得必要參數
        try:
            if self.wecom_config['webhook'] and self.wecom_config['key']:
                webhook = self.wecom_config['webhook']
                key = self.wecom_config['key']
                bot = utils.Bot()
                bot.content = str(format_data)
                response, data = bot.send_message(webhook, key)
                if response:
                    self.log.write_log(f"INFO  已經發送數據至機器人")
                else:
                    self.log.write_log(f"WARN  發送失敗，錯誤訊息：{data}")
            else:
                self.log.write_log(f"WARN  發送失敗，請檢查機器人設定是否正確")

        except Exception as _:
            self.log.write_log(f"WARN  請檢查機器人{_}設定")
