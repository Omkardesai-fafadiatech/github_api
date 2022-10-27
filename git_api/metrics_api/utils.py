from datetime import datetime
from dateutil.relativedelta import relativedelta
import operator


def get_iso_time(avg_cycle='1 month'):
    now = datetime.now()
    if avg_cycle in 'month' or 'months':
        avg_cycle = avg_cycle.split(' ')[0]
        last_month_date = now + relativedelta(months=-int(avg_cycle))
    else:
        avg_cycle = avg_cycle.split(' ')[0]
        last_month_date = now + relativedelta(days=-int(avg_cycle))

    return last_month_date


def get_oldest_issues(results, top=3):
    # sorted_res = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    # sorted_list = dict(sorted(results, key=lambda t: t[0]))
    sorted_list = sorted(results.items())
    # sorted_res = results.sort(key=operator.itemgetter('date'))
    return sorted_list
