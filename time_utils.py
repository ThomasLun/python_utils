# coding:utf-8
import calendar
from functools import wraps

import time
from datetime import datetime




def get_month_se(year, month):
    """
    获取传入月的开始时间和结束时间的时间戳
    :param year:2020
    :param month:5
    :return: 1588262400, 1590940800
    """

    def get_mouth(month):
        return "0%s" % month if month < 10 else month

    start = datetime_timestamp('%s-%s-01 00:00:00' % (year, get_mouth(month)))
    end = datetime_timestamp('%s-%s-01 00:00:00' % (year, get_mouth(month + 1)))
    return start, end


def get_day_se(year, month=None, day=None, string=False):
    """
    获取传入年、月、日的开始时间和结束时间的时间戳
    :param year: 2020
    :param month: 5
    :param day: 20
    :param string: 需要的是否是字符串格式化时间，默认是返回时间戳
    :return: 1588262400, 1590940800
    """

    def get_mouth(month):
        return "0%s" % month if month < 10 else month

    def get_day(day):
        return "0%s" % day if day < 10 else day

    if all([year, month, day]):
        start_str = '%s-%s-%s 00:00:00' % (year, get_mouth(month), get_day(day))
        end_str = '%s-%s-%s 23:59:59' % (year, get_mouth(month), get_day(day))
    elif all([year, month]) and not day:
        start_str = '%s-%s-01 00:00:00' % (year, get_mouth(month))
        if month == "12":
            end_str = '%s-01-01 00:00:00' % (year + 1)
        else:
            end_str = '%s-%s-01 00:00:00' % (year, get_mouth(month + 1))
    else:
        start_str = '%s-01-01 00:00:00' % (year)
        end_str = '%s-01-01 00:00:00' % (year + 1)
    if string:
        return start_str, end_str
    else:
        start = datetime_timestamp(start_str)
        end = datetime_timestamp(end_str)
        return start, end


def datetime_timestamp(date_time):
    """
    格式化字符串时间转时间戳
    :param date_time: 2020-5-20 10:10:10"
    :return: 1589940610
    """
    if isinstance(date_time, str):
        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    else:
        date_time = date_time
    try:
        return int(time.mktime(date_time.timetuple()))
    except:
        return 0


def date_format_day(t):
    """
    时间戳变成格式化时间
    :param t: 时间戳
    :return: 格式化时间
    """
    d = time.localtime(t)
    return time.strftime("%Y-%m-%d %H:%M:%S", d)


def get_years_all_days(years):
    """
    获取一年的所有天
    :param years: [2019,2018]
    :return: [[2020, 1, 24],[2020, 1, 25]]
    """
    days = []
    for year in years:
        for month in range(1, 13):
            _, last_day = calendar.monthrange(2016, 9)
            for day in range(1, last_day):
                days.append([year, month, day])
    return days


def years_days(years):
    """
    输入年份的每一天都传入执行一次
    :param years:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper():
            for year in years:
                for month in range(1, 13):
                    _, last_day = calendar.monthrange(year, month)
                    for day in range(1, last_day):
                        func(year, month, day)
            return

        return wrapper

    return decorator


def is_before_today(year, month, day):
    """
    判断传入的日期是否在今天之前
    :param year: 2020
    :param month: 5
    :param day: 20
    :return: True 是 False 不是
    """
    now_year = datetime.now().year
    now_month = datetime.now().month
    now_day = datetime.now().day
    if year > now_year:
        return False
    elif year < now_year:
        return True
    elif month > now_month:
        return False
    elif month < now_month:
        return True
    elif day > now_day:
        return False
    else:
        return True


def get_date_name(year=None, month=None, day=None, today=None):
    """
    获取日期命名
    :param year:
    :param month:
    :param day:
    :return:
    """
    if today:
        name = "%s年%s月%s日" % (datetime.now().year, datetime.now().month, datetime.now().day)
    else:
        name = "%s年" % year
        if month:
            name = name + "%s月" % month
        if day:
            name = name + "%s日" % day
    return name


def cost_time(function):
    '''
    函数计时
    :param function: 需要计时的函数
    :return: None
    '''

    @wraps(function)
    def function_timer(*args, **kwargs):
        doc = "%s(%s)" % (function.__name__, str(function.__doc__).split("\n")[1].strip())
        print '\033[31m[方法: {name} 开始...]'.format(name=doc)
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        ct = t1 - t0
        if ct > 1:
            print '\033[32m[方法: {name} 结束, 耗时: {time:.2f}秒]'.format(name=doc, time=t1 - t0)
        return result

    return function_timer


def get_age_detail(year, month, day):
    """
    通过生日获得详细年龄
    """
    today = datetime.today()
    age_year, age_month, age_day = today.year - year, today.month - month, today.day - day
    if age_day < 0:
        from calendar import monthrange
        age_day = age_day + monthrange(year, month)[1]
        age_month = age_month - 1
        if age_month < 0:
            age_month = age_month + 12
            age_year = age_year - 1
    if age_month < 0:
        age_month = age_month + 12
        age_year = age_year - 1
    return age_year, age_month, age_day


def get_age(bt):
    """
    获取粗年龄
    :param bt:出生日期
    :return: 年龄
    """
    if isinstance(bt, int):
        return (int(time.time()) - bt) / (3600 * 24 * 365)
    elif type(bt) in [str, datetime]:
        return (int(time.time()) - datetime_timestamp(bt)) / (3600 * 24 * 365)
    else:
        return bt


def stime_ymd(stime):
    """
    通过时间戳获取年月日
    :param stime: 时间戳
    :return: datetime时间
    """
    dtime = time.localtime(stime)
    return dtime
