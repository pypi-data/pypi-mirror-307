import sys
import json
import uuid
import pytz
import urllib
import asyncio
import platform
import requests
import threading
import traceback
from os import mkdir
from pathlib import Path
import concurrent.futures
from os.path import exists
from urllib.error import HTTPError
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from datetime import datetime, timezone
from dateutil import parser as dt_parser
from dateutil.relativedelta import relativedelta


class GlobalValues:
    home_dir = ''
    log_dir = ''
    host_os = ''

    @classmethod
    def get_server_os(cls):
        if cls.host_os:
            return cls.host_os
        cls.host_os = platform.system().lower()
        return cls.host_os

    @classmethod
    def get_dir_home(cls):
        if cls.home_dir:
            return cls.home_dir
        cls.home_dir = Path.home()
        return cls.home_dir

    @classmethod
    def get_dir_logs(cls):
        if cls.log_dir:
            return cls.log_dir
        new_dir = str(cls.home_dir) + '/logs'
        if not exists(new_dir):
            mkdir(new_dir)
        cls.log_dir = new_dir


class CoreUtils:

    @classmethod
    def download_image(cls, file):
        img_temp = NamedTemporaryFile(delete=True)
        try:
            if file['source'] == 'Google':
                headers = {'Authorization': 'Bearer ' + file['access_token']}
                request = urllib.request.Request(file['url'], headers=headers)
                img_temp.write(urlopen(request).read())
            else:
                img_temp.write(urlopen(file['url']).read())
            img_temp.flush()
            return img_temp
        except HTTPError as e:
            return str(e.code) + e.reason

    @classmethod
    def decode_bytes(cls, my_bytes_value):
        res = my_bytes_value.decode('utf8').replace("'", '"')
        return res

    @classmethod
    def set_obj_attrs(cls, dict_key_values, py_obj):
        for prop in dict_key_values:
            py_obj.__setattr__(prop, dict_key_values[prop])

    @classmethod
    def unique_id(cls):
        res = str(uuid.uuid4())
        return res

    @classmethod
    def get_file_extension(cls, file_name):
        arr = file_name.split('.')
        extension = arr[len(arr) - 1]
        return extension

    @classmethod
    def stringify_fields(cls, dict_object):
        if dict_object.get('updated_at'):
            dict_object['updated_at'] = str(dict_object['updated_at'])
        if dict_object.get('created_at'):
            dict_object['created_at'] = str(dict_object['created_at'])
        if dict_object.get('updated_by'):
            dict_object['updated_by'] = str(dict_object['updated_by'])
        if dict_object.get('created_by'):
            dict_object['created_by'] = str(dict_object['created_by'])


class DateUtils:

    @classmethod
    def now_str(cls):
        now = str(datetime.now())
        now = now[:-7]
        return now

    @classmethod
    def add_interval(cls, interval_type, inc, dt=None):
        inc = int(inc)
        if not dt:
            dt = datetime.now()
        elif type(dt) == str:
            dt = dt_parser.parse(dt)
        if interval_type == 'y':
            dt = dt + relativedelta(years=inc)
        if interval_type == 'mm':
            dt = dt + relativedelta(months=inc)
        if interval_type == 'w':
            dt = dt + relativedelta(weeks=inc)
        if interval_type == 'd':
            dt = dt + relativedelta(days=inc)
        if interval_type == 'h':
            dt = dt + relativedelta(hours=inc)
        if interval_type == 'm':
            dt = dt + relativedelta(minutes=inc)
        if interval_type == 's':
            dt = dt + relativedelta(seconds=inc)
        return dt

    @classmethod
    def time_difference(cls, start_time, end_time=None):
        if not end_time:
            end_time = datetime.now()
        start_time = start_time.replace(tzinfo=pytz.utc)
        end_time = end_time.replace(tzinfo=pytz.utc)
        diff = relativedelta(end_time, start_time)
        return diff

    @classmethod
    def time_to_str(cls, dt=None, style=''):
        if not dt:
            dt = datetime.now()
        if not style:
            style = '%Y-%m-%d %I:%M:%S %p'
        if style == '14':
            style = '%Y%m%d%H%M%S'
        res = dt.strftime(style)
        return res

    @classmethod
    def time_to_utc(cls, dt):
        # dst_str = str(dt)
        # dst_str = '2021-09-21T09:29:21Z'
        dt_str = str(dt)
        dt_str = dt_str.replace(' ', 'T')
        if '.' in dt_str:
            dt_str = dt_str[:19] + 'Z'
        else:
            dt_str = dt_str.replace('+00:00', 'Z')
        return dt_str

    @classmethod
    def get_month_year(cls, dt):
        year = str(dt.year)
        month = dt.month
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        return year, month

    @classmethod
    def get_timestamp(cls, dt=None):
        if not dt:
            dt = datetime.now()
        elif type(dt) == str:
            dt = dt_parser.parse(dt)
        timestamp = round(dt.timestamp())
        return timestamp


class HttpUtils:

    @classmethod
    def get_location_from_ip(cls, server_url, ip, query_string):
        req_url = server_url + ip + query_string
        print(req_url)
        res = cls.get_json(req_url)
        return res

    @classmethod
    def get_client_ip(cls, req_meta):
        x_forwarded_for = req_meta.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = req_meta.get('REMOTE_ADDR')
        return ip

    @classmethod
    def get_str_from_post(cls, req_url, args=None):
        res = cls.post_data(req_url, args)
        res = res._content.decode("utf-8")
        return res

    @classmethod
    def get(cls, req_url, args):
        headers = args.get('headers')
        timeout = args.get('timeout') or 6
        res = requests.get(req_url, headers=headers, timeout=timeout)
        return res

    @classmethod
    def post(cls, req_url, args):
        headers = args.get('headers')
        json_data = args.get('json')
        timeout = args.get('timeout') or 6
        res = requests.post(req_url, timeout=timeout, data=json_data, headers=headers)
        return res

    @classmethod
    def get_str(cls, req_url, args):
        res = requests.get(req_url, args)
        res = res._content.decode("utf-8")
        return res

    @classmethod
    def get_json(cls, req_url, args):
        res = requests.get(req_url, args)
        res = res.json()
        return res

    @classmethod
    def post_json(cls, req_url, args=None):
        res = cls.post(req_url, args)
        return res.json()

    @classmethod
    def post_str(cls, req_url, args):
        res = cls.post(req_url, args)
        res = res._content.decode("utf-8")
        return res


class JsonToObj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)


class JsonUtils:

    @classmethod
    def dict2obj(cls, dict_obj):
        res = json.loads(json.dumps(dict_obj), object_hook=JsonToObj)
        return res

    @classmethod
    def json_input(cls, kw, byte_data):
        if kw and len(kw.keys()):
            return kw
        if byte_data:
            data = byte_data.decode()
            if data:
                kw = json.loads(data)
        return kw


class LogUtils:

    @classmethod
    def get_error_message(cls, framework_path=''):
        eg = traceback.format_exception(*sys.exc_info())
        error_message = ''
        cnt = 0
        for er in eg:
            cnt += 1
            if not framework_path:
                framework_path = '/addons/'
            packages_path = '/lib/python'
            if GlobalValues.get_server_os() == 'windows':
                framework_path = framework_path.replace('/', '\\')
                packages_path = packages_path.replace('/', '\\')
            if packages_path not in er and framework_path not in er:
                error_message += " " + er
        if not error_message:
            error_message = 'empty error'
        return error_message

    @classmethod
    def get_error_json(cls):
        eg = traceback.format_exception(*sys.exc_info())
        user_message = eg[len(eg) - 1]
        detailed_message = cls.get_error_message()
        return {'error': { 'details': detailed_message, 'message': user_message}}


    @classmethod
    def log_error(cls, log_path='', prefix=''):
        if not log_path:
            log_path = GlobalValues.get_dir_logs()
        content = prefix + cls.get_error_message()
        cls.append_file(log_path, content, 'errors.log')

    @classmethod
    def append_file(cls, log_path='', content='Nothing', file_name='pyfile.txt'):
        if not log_path:
            log_path = GlobalValues.get_dir_logs()
        file_path = log_path + file_name
        f = open(file_path, "a")
        time_now = str(datetime.now())
        content = str(content)
        content = '\n' + content + '\n' + time_now + '\n'
        f.write(content)
        f.close()


    @classmethod
    def log_limited(cls, file_path, txt, take_lines=20):
        dt_now = str(datetime.now(tz=timezone.utc))[:19]
        fle = Path(file_path)
        fle.touch(exist_ok=True)
        with open(file_path, 'r') as my_file:
            ii = 0
            prev_content = ''
            while ii < take_lines:
                line = next(my_file)
                if line:
                    prev_content += '\n' + line.strip()
                ii += 1
        with open(file_path, 'w') as my_file:
            new_content = dt_now + '\t' + txt + prev_content
            my_file.write(new_content)


class StreamUtils:
    pass


class AsyncUtils:

    @classmethod
    async def _do_with_asynch_io(cls, task_list):
        tasks = [item[0](*item[1]) for item in task_list]
        results = await asyncio.gather(*tasks)
        print('All tasks completed')
        return results

    @classmethod
    def execute_asynchronous_tasks(cls, task_list):
        asyncio.run(cls._do_with_asynch_io(task_list))

    @classmethod
    def _do_with_threadpool(cls, task_list):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(item[0], *item[1]) for item in task_list]
            for item in futures:
                print(item.result())
            print(f'Tasks completed {DateUtils.now_str()}')

    @classmethod
    def execute_tasks_with_no_wait(cls, task_list):
        arguments = [task_list]
        obj = threading.Thread(target=cls._do_with_threadpool, args=arguments)
        obj.start()

