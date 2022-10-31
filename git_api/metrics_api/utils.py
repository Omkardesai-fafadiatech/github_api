from datetime import datetime
from dateutil.relativedelta import relativedelta

from cmath import rect, phase
from math import radians, degrees


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

# mean time for average user cycle time
# def meanAngle(deg):
#     complexDegree = sum(rect(1, radians(d)) for d in deg) / len(deg)
#     argument = phase(complexDegree)
#     meanAngle = degrees(argument)
#     return meanAngle

# def meanTime(times):
#     t = (time.split(',') for time in times)
#     seconds = ((float(s) + int(m) * 60 + int(h) * 3600) 
#                for h, m, s in t)
#     day = 24 * 60 * 60
#     toAngles = [s * 360. / day for s in seconds]
#     meanAsAngle = meanAngle(toAngles)
#     meanSeconds = meanAsAngle * day / 360.
#     if meanSeconds < 0:
#         meanSeconds += day
#     h, m = divmod(meanSeconds, 3600)
#     m, s = divmod(m, 60)
#     return('%02i:%02i:%02i' % (h, m, s))