import base64
import datetime
import functools
import json
import os
import random
import shutil
import string
import time
import pytest
from decimal import Decimal, ROUND_HALF_UP

from PyPDF2 import PdfReader
from allure_commons._allure import step


def timeit(func):
    #  decorator for measuring method's elapsed time
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        arg_list = [repr(arg) for arg in args]
        arg_list.extend(f"{key}={value!r}" for key, value in kwargs.items())
        arg_str = ", ".join(arg_list)
        func_elapsed_time = f"{elapsed:0.2f}; {func.__name__}({arg_str})\n"
        # example of func_elapsed_time - 1.42; post('/api/data/user/options/get', {})
        pytest.elapsed_time += func_elapsed_time
        return result

    return clocked

# TODO move methods to separate class
def round_half_up(number, ndigits=0):
    # built-in round - 1.5 -> 2, 2.5 -> 2
    # round_half_up  - 1.5 -> 2, 2.5 -> 3
    rounding = Decimal("1." + "0" * ndigits)
    rounded_decimal = Decimal(str(number)).quantize(rounding, ROUND_HALF_UP)
    return float(rounded_decimal)


def truncate_float(n, places):
    return int(float(n) * (10 ** places)) / 10 ** places


def is_close(*args, tolerance=1):
    # compare two or more numbers to be almost equal
    print(args)
    print(max(*args))
    print(min(*args))
    return abs(max(*args) - min(*args)) <= tolerance


class DateTime:
    @staticmethod
    def now():
        return datetime.datetime.now(datetime.UTC)

    @staticmethod
    def get_datetime(to_format="%Y-%m-%d %H-%M-%S", *, days=0, hours=0, minutes=0, seconds=0):
        current_date_time = datetime.datetime.now(tz=datetime.timezone.utc)
        current_date_time = current_date_time.replace(second=0).replace(microsecond=0)
        date_time_with_delta = current_date_time + datetime.timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds)
        return DateTime.convert_date_time_obj_to_str(date_time_with_delta, to_format)

    @staticmethod
    def convert_datetime(text, from_format, to_format):
        date_time = DateTime.get_date_time_obj_from_str(text, from_format)
        return DateTime.convert_date_time_obj_to_str(date_time, to_format)

    @staticmethod
    def round_to_previous_full_hour(date_time):
        return date_time.replace(minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)

    @staticmethod
    def convert_seconds_to_hh_mm(seconds):
        timedelta = datetime.timedelta(seconds=seconds)
        date_time = DateTime.get_date_time_obj_from_str(str(timedelta), "%H:%M:%S")
        if divmod(date_time.second, 60)[1] >= 30:
            date_time = date_time + datetime.timedelta(minutes=1)
        return DateTime.convert_date_time_obj_to_str(date_time, "%H:%M")

    @staticmethod
    def sum_date_time_as_string(date_time_1_str, date_time_2_str, format_):
        date_time_1 = datetime.datetime.strptime(date_time_1_str, format_)
        date_time_2 = datetime.datetime.strptime(date_time_2_str, format_)
        summary = date_time_1 + datetime.timedelta(days=date_time_2.day, hours=date_time_2.hour,
                                                   minutes=date_time_2.minute, seconds=date_time_2.second)
        return summary.strftime(format_)

    @staticmethod
    def get_date_time_for_taf(taf_date_time_str):
        if taf_date_time_str.endswith("24"):
            taf_date_time_str = taf_date_time_str[0:2] + "23"
            minute = 59
        else:
            minute = 0

        taf_date_time = datetime.datetime.strptime(taf_date_time_str, "%d%H")
        return DateTime.now().replace(day=taf_date_time.day, hour=taf_date_time.hour, minute=minute)

    @staticmethod
    def convert_date_time_obj_to_str(date_time_obj, to_format):
        if to_format.lower() == "iso":
            return date_time_obj.isoformat()
        elif to_format.lower() == "timestamp":
            return date_time_obj.timestamp()
        else:
            return date_time_obj.strftime(to_format)

    @staticmethod
    def get_date_time_obj_from_str(text, from_format):
        if from_format.lower() == "iso":
            return datetime.datetime.fromisoformat(text)
        elif from_format.lower() == "timestamp":
            return datetime.datetime.fromtimestamp(text, tz=datetime.timezone.utc)
        else:
            return datetime.datetime.strptime(text, from_format).replace(tzinfo=datetime.timezone.utc)


class FileMethods:
    @staticmethod
    def get_path(*args):
        return os.path.join(*args)

    @staticmethod
    def create_directory_if_not_exists(*args):
        path = FileMethods.get_path(*args)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def create_empty_dir(dir_name):
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)
        return dir_name

    @staticmethod
    def create_empty_file(file_path, kb_size=1):
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "wb") as file:
            file.seek((kb_size * 1024) - 1)
            file.write(b'\0')

    @staticmethod
    def create_text_file(file_name, text):
        with open(file_name, 'w') as f:
            f.write(text)

    @staticmethod
    def get_json(link):
        with open(os.getcwd() + link, 'r') as file:
            dict_ = json.load(file)
        return dict_

    @staticmethod
    def read_file(link):
        with open(os.getcwd() + link, 'r', encoding='UTF-8') as f:
            file = f.read()
        return file

    @staticmethod
    def get_file_list(dir_name):
        return os.listdir(dir_name)

    @staticmethod
    def get_file_size(file_name):
        return os.path.getsize(file_name)


class Random:
    @staticmethod
    def text(length=6, lowercase=False):
        if lowercase:
            return "".join(random.choices(string.ascii_lowercase, k=length))
        else:
            return "".join(random.choices(string.ascii_uppercase, k=length))

    @staticmethod
    def number(length=6):
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def color(length=6):
        return "#" + "".join(random.choices(string.hexdigits.upper(), k=length))

    @staticmethod
    def int(start, stop=None):
        if not stop:
            start, stop = 0, start
        return random.choice(range(start, stop))

    @staticmethod
    def fl(min_fl, max_fl):
        return str(random.choice(range(min_fl, max_fl, 10)))

    @staticmethod
    def coordinates():
        latitude = f"{Random.int(900000):06}{random.choice('NS')}"
        longitude = f"{Random.int(1800000):07}{random.choice('EW')}"
        return f"{latitude}{longitude}"

