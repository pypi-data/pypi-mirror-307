from chinese_calendar import is_workday
import datetime


def to_str(date, sep=''):
    """
    :param date: a datetime
    :param sep: '' or '-'
    :return: date string of format '%Y%m%d' ('%Y-%m-%d' if sep='-')
    """
    return datetime.datetime.strftime(date, sep.join(['%Y', '%m', '%d']))


def to_date(date_str):
    """
    :param date_str: date string of format '%Y%m%d'
    :return: a datetime
    """
    if '-' in date_str:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return datetime.datetime.strptime(date_str, '%Y%m%d')


def date_plus(date_str, days):
    """
    :param date_str: date string of format '%Y%m%d'
    :param days: a positive or negative integer
    :return: date + days, string of format '%Y%m%d'
    """
    date = to_date(date_str)
    res_date = date + datetime.timedelta(days)
    if '-' in date_str:
        return to_str(res_date, '-')
    return to_str(res_date)


def today(sep=''):
    return to_str(datetime.datetime.today(), sep)


def is_trade_day(date):
    # 检查日期是否是工作日且不是周末
    if is_workday(date) and date.weekday() < 5:  # 周一到周五
        return True
    return False


