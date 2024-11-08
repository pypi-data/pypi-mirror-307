import datetime

__all__ = [
    "get_current_datetime_extra_data",
]


weekdays = [
    ["星期一", "周一", "礼拜一"],
    ["星期二", "周二", "礼拜二"],
    ["星期三", "周三", "礼拜三"],
    ["星期四", "周四", "礼拜四"],
    ["星期五", "周五", "礼拜五"],
    ["星期六", "周六", "礼拜六"],
    ["星期日", "星期天", "周日", "礼拜天", "礼拜日"],
]


def get_weekday_info(nowtime: datetime.datetime, prefix: str = "今天是"):
    return "，".join([prefix + x for x in weekdays[nowtime.weekday()]]) + "。"


def get_day_info(nowtime: datetime.datetime, prefix: str = "今天是"):
    return prefix + nowtime.strftime("%Y-%m-%d") + "。"


def get_nowtime(nowtime: datetime.datetime, prefix: str = "现在时间是"):
    return prefix + nowtime.strftime("%Y-%m-%d %H:%M:%S") + "。"


def get_week_range_info(nowtime: datetime.datetime, prefix: str = "本周时间范围是"):
    today_weekday = nowtime.weekday()
    monday = nowtime - datetime.timedelta(days=today_weekday)
    sunday = monday + datetime.timedelta(days=6)
    return (
        prefix
        + "从"
        + monday.strftime("%Y-%m-%d 00:00:00")
        + "到"
        + sunday.strftime("%Y-%m-%d 23:59:59")
        + "。"
    )


def get_this_month_range_info(
    nowtime: datetime.datetime, prefix: str = "本月时间范围是"
):
    next_month_year = nowtime.year
    next_month_month = nowtime.month + 1
    if next_month_month > 12:
        next_month_month = 1
        next_month_year += 1
    day1 = datetime.datetime(nowtime.year, nowtime.month, 1, 0, 0, 0)
    day31 = datetime.datetime(
        next_month_year, next_month_month, 1, 0, 0, 0
    ) - datetime.timedelta(days=1)
    return (
        prefix
        + "从"
        + day1.strftime("%Y-%m-%d 00:00:00")
        + "到"
        + day31.strftime("%Y-%m-%d 23:59:59")
        + "。"
    )


def get_last_month_range_info(
    nowtime: datetime.datetime, prefix: str = "上月时间范围是"
):
    day31 = datetime.datetime(nowtime.year, nowtime.month, 1) - datetime.timedelta(
        days=1
    )
    day1 = datetime.datetime(day31.year, day31.month, 1, 0, 0, 0)
    return (
        prefix
        + "从"
        + day1.strftime("%Y-%m-%d 00:00:00")
        + "到"
        + day31.strftime("%Y-%m-%d 23:59:59")
        + "。"
    )


def get_next_month_range_info(
    nowtime: datetime.datetime, prefix: str = "下个月时间范围是"
):
    next_month_year = nowtime.year
    next_month_month = nowtime.month + 1
    if next_month_month > 12:
        next_month_month = 1
        next_month_year += 1
    day1 = datetime.datetime(next_month_year, next_month_month, 1, 0, 0, 0)

    next_month_year = day1.year
    next_month_month = day1.month + 1
    if next_month_month > 12:
        next_month_month = 1
        next_month_year += 1
    day31 = datetime.datetime(
        next_month_year, next_month_month, 1
    ) - datetime.timedelta(days=1)
    return (
        prefix
        + "从"
        + day1.strftime("%Y-%m-%d 00:00:00")
        + "到"
        + day31.strftime("%Y-%m-%d 23:59:59")
        + "。"
    )


def get_year_info(year: int, prefix: str = "今年是"):
    return f"{prefix}{year}年。"


def get_lastn_days_info(
    nowtime: datetime.datetime,
    n: int,
    prefix: str = "最近7天的范围是",
):
    start = nowtime - datetime.timedelta(days=n - 1)
    return (
        prefix
        + "从"
        + start.strftime("%Y-%m-%d 00:00:00")
        + "至"
        + nowtime.strftime("%Y-%m-%d 23:59:59")
        + "。"
    )


def get_day_time_range(nowtime: datetime.datetime, prefix="今天的时间范围是"):
    return (
        prefix
        + nowtime.strftime("%Y-%m-%d 00:00:00")
        + "至"
        + nowtime.strftime("%Y-%m-%d 23:59:59")
    )


quarter_start_months = {
    1: 1,
    2: 1,
    3: 1,
    4: 3,
    5: 3,
    6: 3,
    7: 6,
    8: 6,
    9: 6,
    10: 9,
    11: 9,
    12: 9,
}


def get_this_quarter_range_info(
    nowtime: datetime.datetime, prefix="这个季度的时间范围是"
):
    start_month = quarter_start_months[nowtime.month]
    start_day = datetime.datetime(nowtime.year, start_month, 1)
    end_day = datetime.datetime(
        start_day.year, start_day.month + 3, 1
    ) - datetime.timedelta(days=1)
    return (
        prefix
        + start_day.strftime("%Y-%m-%d 00:00:00")
        + "至"
        + end_day.strftime("%Y-%m-%d 23:59:59")
    )


def get_last_quarter_range_info(
    nowtime: datetime.datetime, prefix="上个季度的时间范围是"
):
    if nowtime.month > 3:
        start_year = nowtime.year
        start_month = quarter_start_months[nowtime.month]
    else:
        start_year = nowtime.year - 1
        start_month = 9

    if start_month >= 9:
        end_year_nextday = start_year + 1
        end_month_nextday = 4
    else:
        end_year_nextday = start_year
        end_month_nextday = start_month + 3

    start_day = datetime.datetime(start_year, start_month, 1)
    end_day = datetime.datetime(
        end_year_nextday, end_month_nextday, 1
    ) - datetime.timedelta(days=1)
    return (
        prefix
        + start_day.strftime("%Y-%m-%d 00:00:00")
        + "至"
        + end_day.strftime("%Y-%m-%d 23:59:59")
    )


def get_pastn_days_info(nowtime: datetime.datetime, n=7, prefix="过去一周的时间范围是"):
    end_day = nowtime - datetime.timedelta(days=1)
    start_day = end_day - datetime.timedelta(days=n - 1)
    return (
        prefix
        + start_day.strftime("%Y-%m-%d 00:00:00")
        + "至"
        + end_day.strftime("%Y-%m-%d 23:59:59")
        + "。"
    )


def get_current_datetime_extra_data(nowtime=None):
    nowtime = nowtime or datetime.datetime.now()
    return [
        get_nowtime(nowtime=nowtime),
        get_day_info(nowtime=nowtime, prefix="今天是"),
        get_day_info(nowtime=nowtime + datetime.timedelta(days=1), prefix="明天是"),
        get_day_info(nowtime=nowtime - datetime.timedelta(days=1), prefix="昨天是"),
        get_weekday_info(nowtime=nowtime, prefix="今天是"),
        get_weekday_info(nowtime=nowtime + datetime.timedelta(days=1), prefix="明天是"),
        get_weekday_info(nowtime=nowtime - datetime.timedelta(days=1), prefix="昨天是"),
        get_year_info(year=nowtime.year, prefix="今年是"),
        get_year_info(year=nowtime.year - 1, prefix="去年是"),
        get_year_info(year=nowtime.year + 1, prefix="明年是"),
        get_pastn_days_info(nowtime=nowtime, n=7, prefix="过去一周的时间范围是"),
        get_pastn_days_info(nowtime=nowtime, n=1, prefix="过去一天的时间范围是"),
        get_pastn_days_info(nowtime=nowtime, n=3, prefix="过去三天的时间范围是"),
        get_pastn_days_info(nowtime=nowtime, n=7, prefix="过去七天的时间范围是"),
        get_lastn_days_info(nowtime=nowtime, n=7, prefix="最近一周的时间范围是"),
        get_lastn_days_info(nowtime=nowtime, n=7, prefix="最近7天的时间范围是"),
        get_lastn_days_info(nowtime=nowtime, n=14, prefix="最近14天的时间范围是"),
        get_lastn_days_info(nowtime=nowtime, n=21, prefix="最近21天的时间范围是"),
        get_lastn_days_info(nowtime=nowtime, n=30, prefix="最近30天的时间范围是"),
        get_day_time_range(nowtime=nowtime, prefix="今天的时间范围是"),
        get_day_time_range(
            nowtime=nowtime - datetime.timedelta(days=1), prefix="昨天的时间范围是"
        ),
        get_day_time_range(
            nowtime=nowtime + datetime.timedelta(days=1), prefix="明天的时间范围是"
        ),
        get_week_range_info(nowtime=nowtime, prefix="本周的时间范围是"),
        get_week_range_info(nowtime=nowtime, prefix="当前周的时间范围是"),
        get_week_range_info(nowtime=nowtime, prefix="这周的时间范围是"),
        get_week_range_info(nowtime=nowtime, prefix="这一周的时间范围是"),
        get_week_range_info(
            nowtime=nowtime - datetime.timedelta(days=7), prefix="上周的时间范围是"
        ),
        get_week_range_info(
            nowtime=nowtime - datetime.timedelta(days=7), prefix="上一周的时间范围是"
        ),
        get_week_range_info(
            nowtime=nowtime + datetime.timedelta(days=7), prefix="下周的时间范围是"
        ),
        get_week_range_info(
            nowtime=nowtime + datetime.timedelta(days=7), prefix="下一周的时间范围是"
        ),
        get_this_month_range_info(nowtime=nowtime, prefix="本月的时间范围是"),
        get_this_month_range_info(nowtime=nowtime, prefix="这月的时间范围是"),
        get_this_month_range_info(nowtime=nowtime, prefix="这个月的时间范围是"),
        get_last_month_range_info(nowtime=nowtime, prefix="上月的时间范围是"),
        get_last_month_range_info(nowtime=nowtime, prefix="上个月的时间范围是"),
        get_next_month_range_info(nowtime=nowtime, prefix="下月的时间范围是"),
        get_next_month_range_info(nowtime=nowtime, prefix="下个月的时间范围是"),
        get_this_quarter_range_info(nowtime=nowtime, prefix="这个季度的时间范围是"),
        get_this_quarter_range_info(nowtime=nowtime, prefix="本季度的时间范围是"),
        get_this_quarter_range_info(nowtime=nowtime, prefix="当前季度的时间范围是"),
        get_last_quarter_range_info(nowtime=nowtime, prefix="上个季度的时间范围是"),
        "重要：表示年份必须使用4位数字。禁止使用2位数字表示年份。",
        "重要：每天的时间范围总是从这一天的00:00:00到这一天的23:59:59。",
        "重要：最近(n)天，是指过去(n-1)天至今天。",
        "重要：过去(n)天，是指过去(n)天至昨天。",
        "重要：总是把星期一当成是一周的开始，把星期天当成是一周的结束。",
    ]
