from datetime import datetime
from dateutil.relativedelta import relativedelta


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
# total_issue_counts += 1
    # td = row['created_at'].strftime("%b-%y")
    # if td not in results[f"{time_duration}_based"]:
    #     results[f"{time_duration}_based"].append(td)
    # if row["closed_at"] != None:
    #     time_taken = row['closed_at'].month - row["created_at"].month
    #     if time_taken != 0:
    #         results[f"done_per_{time_duration}"].extend(0 for i in range(time_taken+1))
    #         results[f"done_per_{time_duration}"][time_taken] += 1
    #     elif row['created_at']
    #     else:
    #         done+=1
    # elif

    # print(row)
    # counts_per_cycle += 1
    # td = row['created_at'].strftime("%b-%y")
    # total_issue_counts += 1
    # if td not in results[f"{time_duration}_based"]:
    #     print("that")
    #     results[f"{time_duration}_based"].append(td)
    # if row["closed_at"] != None:
    #     print(row, "inner")
    #     time_taken = row['closed_at'].month - row["created_at"].month
    #     counts_per_cycle += 1
    #     if time_taken != 0:
    #         results[f"done_per_{time_duration}"].extend(0 for i in range(time_taken+1))
    #         results[f"done_per_{time_duration}"][time_taken] = +1
    #     # [f"total_per_{time_duration}"].append(counts_per_cycle)
    #     print(results)

    # elif results[len(f"{time_duration}_based")-2] != td:
    #     print("thsi")
    #     results[f"total_per_{time_duration}"].append(counts_per_cycle)
    #     results[f"done_per_{time_duration}"].append(done)
    #     if done < counts_per_cycle:
    #         counts_per_cycle = counts_per_cycle-done
    #         done = 0
    #     else:
    #         counts_per_cycle = 0
    #         done = 0
    # total_issue_counts += 1
    #     elif results[len(results[f"{time_duration}_based"])-1] == td and row["closed_at"] != None:
    #         counts_per_cycle += 1
    #         done += 1
    #     elif results[len(f"{time_duration}_based")-2] != td:
    #         results[f"total_per_{time_duration}"].append(counts_per_cycle)
    #         results[f"done_per_{time_duration}"].append(done)
    #         if done < counts_per_cycle:
    #             counts_per_cycle = counts_per_cycle-done
    #             done = 0
    #         else:
    #             counts_per_cycle = 0
    #             done = 0
    #     total_issue_counts += 1
    # results["total_issue_counts"].append(total_issue_counts)
    # return results
