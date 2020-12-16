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


import datetime
import os
import sys



class Log:
    """
    輸出log功能的類別
    """
    def __init__(self):

        # today = datetime.date.today().strftime("%Y%m%d")
        logDir = os.path.join("log")
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        self.log_file = open(
            os.path.join(logDir, "api.log"), "a+")


    def write_log(self, log_str):

        date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        format_log_str = f"{date_now} ---> {log_str} \n "
        print(format_log_str)
        self.log_file.write(format_log_str)

