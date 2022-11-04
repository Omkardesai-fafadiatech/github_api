from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import GitIssues, GitPullRequests
from collections import defaultdict
from .utils import get_iso_time, get_oldest_issues
from datetime import timedelta
from dateutil import relativedelta


class IssuesMetrics(APIView):
    git_issues = GitIssues()

    """
    This is issue metrics
    """

    def get_username_issues_status(self, username):
        results = defaultdict(int)
        for row in self.git_issues.find({'user': {'$regex': f"{username}", "$options": "i"}}):
            results[row['issue_status']] += 1
        return results

    def get_oldest_issues_with_name(self, name, status, metrics,):
        cycle_comp_git = ["7 days", "14 days", "30 days", "90 days"]
        all_data = {}
        for per_cyc_data in cycle_comp_git:
            issues = {"avg_cycle_of": [], 'title': [], 'dates': [], 'counts': []}
            sorted_data = self.git_issues.find(
                {'user': {'$regex': f"{name}", "$options": "i"},
                 'issue_status': status, 'created_at': {'$gte': get_iso_time(per_cyc_data), }})
            if len(sorted_data) != 0:
                sorted_data.sort(key=lambda p: p['created_at'],)
                for row in sorted_data:
                    issues['title'].append(row['issue_title'])
                    issues['dates'].append(row['created_at'])
                issues['counts'].append(len(issues['title']))

                all_data[per_cyc_data] = issues
            else:
                all_data[per_cyc_data] = "No records found."
        return all_data

    def burndown_repo(self, repo_name, time_duration):
        results = {"repo_name": f"{repo_name}", f"{time_duration}_based": [],
                   "total_issue_counts": "", f"total_per_{time_duration}": [], f"done_per_{time_duration}": []}
        total_issue_counts, counts_per_cycle, done = (0, 0, 0)
        per_month_cycle = 0
        curr_month_counts = 0
        curr_month = 0
        for row in sorted(
                self.git_issues.find({'repo_name': {"$regex": repo_name, "$options": "i"}}),
                key=lambda p: p["created_at"]):
            total_issue_counts += 1
        for row in sorted(
                self.git_issues.find({'repo_name': {"$regex": repo_name, "$options": "i"}}),
                key=lambda p: p["created_at"]):
            print(row)
            td = row['created_at'].strftime("%b-%y")
            if td not in results[f"{time_duration}_based"]:
                results[f"{time_duration}_based"].append(td)
            # if row["created_at"].month== row["closed_at"].month:
            #     per_month_cycle= total_issue_counts-1
            if row["closed_at"] != None:
                closed_same_month, closed_different_month = (0, 0)

                if row['closed_at'].month-row['created_at'].month == 0:
                    curr_month_counts += 1

                elif row['closed_at'].month-row['created_at'].month != 0:
                    print(results)
                    print(row['closed_at'].month, row['created_at'].month)
                    time_taken = row['closed_at'].month - row["created_at"].month
                    print(time_taken)
                    print(len(results[f"done_per_{time_duration}"]), time_taken)
                    print(len(results[f"done_per_{time_duration}"])+1 < time_taken)
                    if len(results[f"done_per_{time_duration}"]) < time_taken:
                        print("inner")
                        results[f"done_per_{time_duration}"].extend([0 for i in range(time_taken+1)])
                        print(results)
                    results[f"done_per_{time_duration}"][time_taken] += 1
                    print(results)
            if curr_month != td and curr_month != 0:
                results[f"done_per_{time_duration}"].append(total_issue_counts-curr_month_counts)
            curr_month = row['created_at'].strftime("%b-%y")
        results["total_issue_counts"] = total_issue_counts
        return results

    def get(self, request, format=None):
        username = request.GET.get('username', None)
        status = request.GET.get('status', None)
        metrics = request.GET.get('metrics', None)
        repo_name = request.GET.get('repo_name', None)
        td = request.GET.get('td', None)
        if metrics == "agg_issues_counts":
            return Response(self.get_username_issues_status(username))
        if metrics == 'oldest_issues':
            return Response(self.get_oldest_issues_with_name(username, status, metrics, ))
        if metrics == "burndown_analyzer":
            return Response(self.burndown_repo(repo_name, td))


class PersonMetrics(APIView):
    """
    This is person metrics
    """
    """
    Alawyas convert time delta before storing in dictionary
    """
    git_issues = GitIssues()
    git_pr = GitPullRequests()

    def get_username_average_cycle(self, username, avg_cycle, status='closed'):
        results = {'username': [], 'average_time': []}
        completion_time = {'issue_number': [], 'time_taken': []}
        time_list = []
        sorted_data = self.git_issues.find(
            {'user': {'$regex': f"{username}", "$options": "i"},
             'issue_status': status, 'created_at': {'$gte': get_iso_time(avg_cycle), }})

        if len(sorted_data) != 0:
            sorted_data.sort(key=lambda p: p['created_at'], )
            for row in sorted_data:
                created_at = row['created_at']
                closed_at = row['closed_at']
                time_taken = closed_at - created_at
                time_list.append(time_taken)
                completion_time['issue_number'].append(row['issue_number'])
                completion_time['time_taken'].append(str(time_taken))
            average_time = sum(time_list, timedelta())/len(time_list)
            results['username'].append(row['user'])
            results['average_time'].append(str(average_time))
            return results, completion_time
        return "No records found", results, completion_time

    def open_to_close_ratio(self, username, avg_cycle):
        results = {'username': [], 'open_to_close_ratio': []}
        open_count = int()
        closed_count = int()
        sorted_data = self.git_issues.find({'user': {'$regex': f"{username}", "$options": "i"},
                                            'created_at': {'$gte': get_iso_time(avg_cycle), }})
        print(sorted_data)
        if len(sorted_data) != 0:
            sorted_data.sort(key=lambda p: p['created_at'], )
            for row in sorted_data:
                if row['issue_status'] == "open":
                    open_count += 1
                elif row['issue_status'] == "closed":
                    closed_count += 1
            total_count = open_count+closed_count
            open_to_close_ratio = (closed_count/total_count)*100
            results['username'].append(row['user'])
            results['open_to_close_ratio'] = f"{open_to_close_ratio}%"
            return results
        return results

    def pr_average_cycle_time(self, username, avg_cycle, status='closed'):
        results = {'username': [], 'average_time': []}
        completion_time = {'pr_number': [], 'time_taken': []}
        time_list = []

        sorted_data = self.git_pr.find({'user': {'$regex': f"{username}", "$options": "i"}, 'pr_status': status,
                                        'created_at': {'$gte': get_iso_time(avg_cycle), }})
        if len(sorted_data) != 0:
            for row in sorted_data:
                created_at = row['created_at']
                closed_at = row['closed_at']
                time_taken = closed_at - created_at
                time_list.append(time_taken)
                completion_time['pr_number'].append(row['pr_number'])
                completion_time['time_taken'].append(str(time_taken))

            average_time = sum(time_list, timedelta())/len(time_list)
            results['username'].append(row['user'])
            results['average_time'].append(str(average_time))
            return results, completion_time
        return results, completion_time

    def get(self, request, format=None):
        username = request.GET.get('username', None)
        status = request.GET.get('status', "closed")
        metrics = request.GET.get('metrics', None)
        avg_cycle = request.GET.get('avg_cycle', None)

        if metrics == "average_cycle_time":
            return Response(self.get_username_average_cycle(username, avg_cycle, status))
        if metrics == "open_to_close_ratio":
            return Response(self.open_to_close_ratio(username, avg_cycle))
        if metrics == "pr_average_cycle_time":
            return Response(self.pr_average_cycle_time(username, avg_cycle, status))
