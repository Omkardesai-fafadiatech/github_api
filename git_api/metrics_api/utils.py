from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from collections import OrderedDict

def get_iso_time(avg_cycle='1 month'):
    now = datetime.now()
    if avg_cycle.find("month" or "months") != -1:
        print("month", avg_cycle)
        avg_cycle = avg_cycle.split(' ')[0]
        last_month_date = now + relativedelta(months=-int(avg_cycle))
    else:
        print("days", avg_cycle)
        avg_cycle = avg_cycle.split(' ')[0]
        last_month_date = now + relativedelta(days=-int(avg_cycle))

    return last_month_date


def get_oldest_issues(results, top=3):
    # sorted_res = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    # sorted_list = dict(sorted(results, key=lambda t: t[0]))
    sorted_list = sorted(results.items())
    # sorted_res = results.sort(key=operator.itemgetter('date'))
    return sorted_list

def fill_months(start_month,end_month):
    dt=[start_month,end_month]
    start, end = [datetime.strptime(_, "%b-%y" ) for _ in dt]
    print(end)
    end=end+relativedelta(months=1)
    ordered_months=OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in range((end-start).days)).keys()
    return {i:0 for i in list(ordered_months)}
def fetch_first_end_month(data):
    start_month=data[0]["created_at"].strftime(r"%b-%y")
    end_month=data[-1]["created_at"].strftime(r"%b-%y")
    return start_month,end_month