import os
import sys
import json
import time
import typing
import winreg
import requests

from loguru import logger
import types
import json
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)
if sys.path[0] != ROOT_PATH:
    sys.path.insert(0, ROOT_PATH)

def __load_json(json_name='General.json', default_path='config\\settings') -> dict:
    all_path = os.path.join(ROOT_PATH, default_path, json_name)
    return json.load(open(all_path, 'r', encoding='utf-8'))

def get_logger_format_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def get_logger_format_date():
    return time.strftime('%Y-%m-%d', time.localtime())

jpath = fr"{ROOT_PATH}/config/settings/General.json"
if os.path.exists(jpath):
    j = json.load(open(jpath, 'r', encoding='utf-8'))
    DEBUG_MODE = j["DEBUG"]
else:
    DEBUG_MODE = False
warned_dict={}
def warning_once(self, message):
    is_warned = warned_dict.setdefault(message, False)
    if not is_warned:
        self.warning(message)
        warned_dict[message]=True

def demo(self, message):
    self.info(f"DEMO: {message}")

def add_logger_to_GUI(cb_func):
    logger.add(cb_func, level="INFO", backtrace=True, colorize=True)

import datetime

def delete_files(path, days):
    now = datetime.datetime.now()
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if (now - modified_time).days > days:
                if DEBUG_MODE:
                    print(f"Log File Delete: Deleting file {file_path} Last modified {modified_time} Days since modified {(now - modified_time).days} Days to delete {days}")
                os.remove(file_path)

delete_files(f"{ROOT_PATH}/Logs", 15)


# configure loguru
logger.remove(handler_id=None)
logger.warning_once = types.MethodType(warning_once, logger)
logger.demo = types.MethodType(demo, logger)
logger.add(os.path.join(ROOT_PATH, os.path.join(ROOT_PATH, 'Logs', "{time:YYYY-MM-DD}/{time:YYYY-MM-DD}.log")), level="TRACE", backtrace=True)
STDOUT_HANDEL_ID = None
if DEBUG_MODE:
    STDOUT_HANDEL_ID = logger.add(sys.stdout, level="TRACE", backtrace=True)
else:
    STDOUT_HANDEL_ID = logger.add(sys.stdout, level="INFO", backtrace=True)

def hr(title, level=3):
    title = str(title).upper()
    if level == 1:
        logger.info('=' * 20 + ' ' + title + ' ' + '=' * 20)
    if level == 2:
        logger.info('-' * 20 + ' ' + title + ' ' + '-' * 20)
    if level == 3:
        logger.info('<' * 3 + ' ' + title + ' ' + '>' * 3)
    if level == 0:
        middle = '|' + ' ' * 20 + title + ' ' * 20 + '|'
        border = '+' + '-' * (len(middle) - 2) + '+'
        logger.info(border)
        logger.info(middle)
        logger.info(border)


def attr(name, text):
    logger.info('[%s] %s' % (str(name), str(text)))


def attr_align(name, text, front='', align=22):
    name = str(name).rjust(align)
    if front:
        name = front + name[len(front):]
    logger.info('%s: %s' % (name, str(text)))


logger.hr = hr
logger.attr = attr
logger.attr_align = attr_align

import locale
t2t = lambda x : x
import subprocess
import urllib.request
import ssl

PROGRAM_NAME = "Python-Git-Program-Launcher"
DEBUG_MODE = False
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE_PATH = os.path.join(ROOT_PATH, "..\\toolkit\\Miniconda\\python.exe")
LAUNCHER_PYTHON_PATH = PYTHON_EXE_PATH
PROGRAM_PYTHON_PATH = LAUNCHER_PYTHON_PATH
REPO_PATH = ""
os.chdir(ROOT_PATH)
CONFIG_TEMPLATE = {
    "RequirementsFile": "requirements.txt",
    "InstallDependencies": True,
    "PypiMirror": "AUTO",
    "PythonMirror": "AUTO",
    "Repository": "https://github.com/infstellar/python-git-program-launcher",
    "Main": "main.py",
    "Branch": "main",
    "GitProxy": False,
    "KeepLocalChanges": False,
    "AutoUpdate": True,
    "Tag": "",
    "PythonVersion": "3.10.10",
    "UAC": True
}


def get_local_lang():
    lang = locale.getdefaultlocale()[0]
    print(lang)
    if lang in ["zh_CN", "zh_SG", "zh_MO", "zh_HK", "zh_TW"]:
        return "zh_CN"
    else:
        return "en_US"


GLOBAL_LANG = get_local_lang()
if locale.getdefaultlocale()[0] == 'zh_CN':
    PROXY_LANG = 'zh_CN'
else:
    PROXY_LANG = "en_US"

if sys.path[0] != ROOT_PATH:
    sys.path.insert(0, ROOT_PATH)


def load_config_json(json_name) -> dict:
    if '.json' not in json_name:
        json_name += '.json'
    f = open(os.path.join(ROOT_PATH, 'configs', json_name), 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a


def load_json(json_name) -> dict:
    if '.json' not in json_name:
        json_name += '.json'
    f = open(json_name, 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a


def download_url(url, dst):
    from tqdm import tqdm
    import requests
    first_byte = 0
    logger.info(t2t("downloading url:") + f"{url} -> {dst}")
    # tqdm 里可选 total= 参数，不传递这个参数则不显示文件总大小
    pbar = tqdm(initial=first_byte, unit='B', unit_scale=True, desc=dst)
    # 设置stream=True参数读取大文件
    req = requests.get(url, stream=True, verify=False)
    with open(dst, 'ab') as f:
        # 每次读取一个1024个字节
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()


def save_config_json(x, json_name):
    """保存json.

    Args:
        x (_type_): dict/list对象
        json_name (str, optional): 同load_json. Defaults to 'General.json'.
        default_path (str, optional): 同load_json. Defaults to 'config\\settings'.
        sort_keys (bool, optional): 是否自动格式化. Defaults to True.
        auto_create (bool, optional): _description_. Defaults to False.
    """
    if '.json' not in json_name:
        json_name += '.json'
    json.dump(x, open(os.path.join(ROOT_PATH, 'configs', json_name), 'w', encoding='utf-8'), sort_keys=True, indent=2,
              ensure_ascii=False)


def save_json(x, json_name):
    """保存json.

    Args:
        x (_type_): dict/list对象
        json_name (str, optional): 同load_json. Defaults to 'General.json'.
    """
    if '.json' not in json_name:
        json_name += '.json'
    json.dump(x, open(json_name, 'w', encoding='utf-8'), sort_keys=True, indent=2,
              ensure_ascii=False)


def load_json_from_folder(path, black_file: list = None):
    json_list = []
    if black_file is None:
        black_file = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f[f.index('.') + 1:] == "json":
                if f[:f.index('.')] not in black_file:
                    j = json.load(open(os.path.join(path, f), 'r', encoding='utf-8'))
                    json_list.append({"label": f, "json": j})
    return json_list


def verify_path(root):
    root = os.path.abspath(root)
    if not os.path.exists(root):
        verify_path(os.path.dirname(root))
        os.mkdir(root)
        logger.info(f"dir {root} has been created")


def read_file_flag(n: str) -> bool:
    p = os.path.join(ROOT_PATH, 'pgpl-cache')
    verify_path(p)
    with open(os.path.join(p, n), 'w+') as f:
        s = f.read()
        if s == '':
            f.write('False')
            return False
        else:
            return bool(s)


def write_file_flag(n: str, x: bool) -> None:
    p = os.path.join(ROOT_PATH, 'pgpl-cache')
    verify_path(p)
    with open(os.path.join(p, n), 'w') as f:
        f.write(str(x))


class ExecutionError(Exception):
    pass


class ProgressTracker():
    """
    给GUI用的进度追踪器
    """

    def __init__(self) -> None:
        self.percentage = 0
        self.info = ''
        self.end_flag = False
        self.cmd = ""
        self.console_output = ""
        self.err_info = ""
        self.err_code = 0
        self.err_slu = ""
        self.monitor_list = []

    def set_percentage(self, x):
        self.percentage = x

    def set_info(self, x, end='\n'):
        self.info = x + end

    def inp(self, info, percentage, end='\n'):
        self.info = info + end
        self.percentage = percentage

    def add_monitor(self, text: str):
        self.monitor_list.append({'text': text, 'count': 0})

    def monitor(self, t):
        for i in self.monitor_list:
            if t in i['text'] and t != '':
                i['count'] += 1

    def get_counts(self, t):
        for i in self.monitor_list:
            if t == i['text']:
                return i['count']

    def reset(self):
        self.monitor_list = []


def find_right_encoding(str):
    encodings = ['utf-8', 'gbk', 'gb2312', 'big5']
    for encoding in encodings:
        try:
            if DEBUG_MODE: logger.trace(f"encoding: {encoding}, decode: {str.decode(encoding)}")
            str.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            pass


def run_command(command, progress_tracker: ProgressTracker = None):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    i = 0
    pt = time.time()
    while True:
        output = process.stdout.readline()
        logger.info(f"output: {output}")
        right_encoding = find_right_encoding(output)
        if str(output, encoding=right_encoding) == '' and (process.poll() is not None):
            break
        if output:
            orimess = output.strip()
            mess = str(orimess, encoding=right_encoding)
            if progress_tracker is not None: progress_tracker.monitor(mess)
            if 'Requirement already satisfied: ' not in mess:
                logger.trace(mess)
                if progress_tracker is not None: progress_tracker.console_output = mess
                # print(mess)
            if 'Installing collected packages' in mess:
                logger.info(t2t('Please wait, pip is copying the file.'))
                # progress_tracker.set_info(t2t('Please wait, pip is copying the file.'))
                if progress_tracker is not None: progress_tracker.console_output = t2t(
                    'Please wait, pip is copying the file.') + '\n' + progress_tracker.console_output

        else:
            pass
            # if time.time()-pt>5:
            #     list = ["\\", "|", "/", "—"]
            #     index = i % 4
            #     sys.stdout.write("\r {}".format(list[index]))
            #     i+=1
    stdout, stderr = process.communicate()
    stdout_encoding = find_right_encoding(stdout)
    stderr_encoding = find_right_encoding(stderr)
    rc = process.poll()
    return rc, stdout.decode(stdout_encoding), stderr.decode(stderr_encoding)


class Command():

    def __init__(self, progress_tracker=None) -> None:
        if progress_tracker is None:
            logger.warning("progress_tracker is None")
            progress_tracker = ProgressTracker()
        self.progress_tracker = progress_tracker

    def error_checking(self, err_msg, err_code):
        def add_slu(msg: str):
            self.progress_tracker.err_slu += f"- {msg}\n"

        logger.info("Running automatic error checking...")
        if 'get-pip.py' in err_msg and "No such file or directory" in err_msg:
            add_slu(
                t2t("toolkit is not installed. Please check if you downloaded the correct file or if you cloned the submodule."))

    def show_error(self, command=None, error_code=None):
        logger.info("Update failed", 0)
        # self.show_config()
        logger.info("")
        logger.info(f"Last command: {command}\nerror_code: {error_code}")
        # logger.warning(t2t("Please check your NETWORK ENVIROUMENT and re-open Launcher.exe"))
        # logger.warning(t2t("Please check your NETWORK ENVIROUMENT and re-open Launcher.exe"))
        # logger.warning(t2t("Please check your NETWORK ENVIROUMENT and re-open Launcher.exe"))

    def logger_hr(self, message, hr_mode=0, progress=None):
        logger.hr(message, hr_mode)
        if progress is None:
            self.progress_tracker.set_info(message)
        else:
            self.progress_tracker.inp(message, progress)

    def info(self, x: str, mode='r', end='\n'):
        """output info to console and UI.

        Args:
            x (str): message.
        """
        logger.info(x)
        if mode == 'r':
            self.progress_tracker.set_info(x + end)
        elif mode == 'a':
            self.progress_tracker.set_info(self.progress_tracker.info + x)

    def execute(self, command, allow_failure=False, output=True,
                is_format=True):  # , systematic_retry=False, systematic_execute=False):
        """

        execute command in subprocess and synchronize command output to GUI and console.

        Args:
            command (str): command
            allow_failure (bool): whether to raise an exception on failure
            output(bool):

            # systematic_retry, systematic_execute: when subprocess fail but os.system succ, use it.

        Returns:
            bool: If success.
                Terminate installation if failed to execute and not allow_failure.
        """

        if is_format:
            command = command.replace(r"\\", "/").replace("\\", "/").replace('"', '"')
        # command = command.replace(r"/", "\\")
        if not output:
            command = command + ' >nul 2>nul'
        logger.info(command)
        self.progress_tracker.cmd = command
        self.progress_tracker.console_output = ""
        if False:  # systematic_execute:
            error_code = os.system(command)
            stdout = ""
            stderr = ""
        else:
            error_code, stdout, stderr = run_command(command, self.progress_tracker)
            # error_code = run_command(command, progress_tracker=self.progress_tracker) # os.system(command)
        if error_code:
            if allow_failure:
                logger.info(f"[ allowed failure ], error_code: {error_code} stdout: {stdout} stderr: {stderr}")
                return False
            elif False:  # systematic_retry:
                logger.info(f"[ failure - USE SYSTEM INSTEAD ], error_code: {error_code}")
                return self.execute(command, allow_failure, output, is_format, systematic_retry=False,
                                    systematic_execute=True)
            else:
                logger.info(f"[ failure ], error_code: {error_code} stdout: {stdout} stderr: {stderr}")
                self.show_error(command, error_code)
                self.progress_tracker.err_code = error_code
                self.progress_tracker.err_info = stderr
                self.progress_tracker.console_output = stdout
                self.error_checking(stderr, error_code)
                raise ExecutionError

        else:
            logger.info(f"[ success ]")
            return True


def url_file_exists(url):
    context = ssl._create_unverified_context()
    try:
        urllib.request.urlopen(url, context=context)
        return True
    except Exception as e:
        logger.error(e)
        return False


def isProtectedByGreatWall():
    try:
        r = requests.get("https://www.x.com", verify=False, proxies=None, timeout=5)
        logger.info(f'get x.com: code: {r.status_code}')
        return r.status_code > 210
    except Exception as e:
        logger.info(f'get x.com error: {e}')
        return True


def select_fastest_url(urls: typing.List[str], is_pypi=False, use_cache=True) -> str:
    input_str = str(urls)

    if not os.path.exists(f"{ROOT_PATH}\\cache\\url_speed_test.json"):
        verify_path(f"{ROOT_PATH}\\cache")
        with open(f"{ROOT_PATH}\\cache\\url_speed_test.json", 'w', encoding='utf-8') as f:
            f.write('{}')
    if use_cache:
        x = load_json(f"{ROOT_PATH}\\cache\\url_speed_test.json")
        if input_str in x.keys():
            logger.info(f'Fastest url: {x[input_str]} (use cache)')
            return x[input_str]
    fastest_time = 999
    fastest_url = urls[0]
    requests.packages.urllib3.disable_warnings()
    for url in urls:
        total_time = 0
        domain = url[:url.replace("http://", '').replace("https://", "").rfind('/') + url.find('://') + 3]
        for i in range(4):
            pt = time.time()
            try:
                r = requests.get(domain, verify=False, proxies=None, timeout=(3.05, 1))
                if r.status_code == 200:
                    if is_pypi:
                        pt = time.time()
                        try_download_url = f"{domain}/packages/00/00/0188b746eefaea75d665b450c9165451a66aae541e5f73db4456eebc0289/loginhelper-0.0.5-py3-none-any.whl"
                        r2 = requests.get(try_download_url, verify=False, proxies=None, timeout=(3.05, 1))
                        if r2.status_code == 200:
                            logger.info(f'get {domain} code: {r.status_code} time: {time.time() - pt}')
                        else:
                            total_time = 9999999999999.999999999
                            logger.info(
                                f'get {domain} error: 被风控/无法下载 code_1:{r.status_code} code_1:{r2.status_code} time: {total_time}')
                            break
                    use_time = time.time() - pt
                else:
                    use_time = time.time() - pt
                    logger.info(f'get {domain} code: {r.status_code} time: {use_time}')
                if r.status_code > 210:
                    total_time += 4
                else:
                    total_time += use_time
            except Exception as e:
                logger.info(f'get {domain} error: {e}')
                total_time += 4
        if total_time <= fastest_time:
            fastest_time = total_time
            fastest_url = url
    logger.info(f'Fastest url: {fastest_url}; average cost {fastest_time / 4}')

    output_result = fastest_url
    x = load_json(f"{ROOT_PATH}\\cache\\url_speed_test.json")
    x[input_str] = output_result
    save_json(x, json_name=f"{ROOT_PATH}\\cache\\url_speed_test.json")

    return fastest_url


def proxy_info():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Internet Settings")
    try:
        is_proxy_enabled = bool(winreg.QueryValueEx(key, "ProxyEnable")[0])
    except Exception as e:
        logger.exception(e)
        is_proxy_enabled = False
    try:
        proxy_server = str(winreg.QueryValueEx(key, "ProxyServer")[0])
    except Exception as e:
        logger.exception(e)
        proxy_server = "0.0.0.0"
    winreg.CloseKey(key)
    logger.debug(f'proxy: {proxy_server}; enabled:{is_proxy_enabled}')
    return is_proxy_enabled, proxy_server


requesting_administrative_privileges = "@echo off\n" + \
                                       "\n" + \
                                       ":: BatchGotAdmin\n" + \
                                       ":-------------------------------------\n" + \
                                       "REM  --> Check for permissions\n" + \
                                       "    IF \"%PROCESSOR_ARCHITECTURE%\" EQU \"amd64\" (\n" + \
                                       ">nul 2>&1 \"%SYSTEMROOT%\SysWOW64\cacls.exe\" \"%SYSTEMROOT%\SysWOW64\config\system\"\n" + \
                                       ") ELSE (\n" + \
                                       ">nul 2>&1 \"%SYSTEMROOT%\system32\cacls.exe\" \"%SYSTEMROOT%\system32\config\system\"\n" + \
                                       ")\n" + \
                                       "\n" + \
                                       "REM --> If error flag set, we do not have admin.\n" + \
                                       "if '%errorlevel%' NEQ '0' (\n" + \
                                       "    echo Requesting administrative privileges...\n" + \
                                       "    goto UACPrompt\n" + \
                                       ") else ( goto gotAdmin )\n" + \
                                       "\n" + \
                                       ":UACPrompt\n" + \
                                       "    echo Set UAC = CreateObject^(\"Shell.Application\"^) > \"%temp%\getadmin.vbs\"\n" + \
                                       "    set params= %*\n" + \
                                       "    echo UAC.ShellExecute \"cmd.exe\", \"/c \"\"%~s0\"\" %params:\"=\"\"%\", \"\", \"runas\", 1 >> \"%temp%\getadmin.vbs\"\n" + \
                                       "\n" + \
                                       "    \"%temp%\getadmin.vbs\"\n" + \
                                       "    del \"%temp%\getadmin.vbs\"\n" + \
                                       "    exit /B\n" + \
                                       "\n" + \
                                       ":gotAdmin\n" + \
                                       "    pushd \"%CD%\"\n" + \
                                       "    CD /D \"%~dp0\"\n" + \
                                       ":--------------------------------------    \n"



import os
import shutil
import re

def parse_gitignore(gitignore_path):
    patterns = []
    with open(gitignore_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns

def should_ignore(path, patterns):
    for pattern in patterns:
        if re.match(pattern, path):
            return True
    return False

def copy_directory(src, dst, gitignore_path):
    patterns = parse_gitignore(gitignore_path)
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path, gitignore_path)
        elif not should_ignore(src_path, patterns):
            shutil.copy2(src_path, dst_path)

