from multiprocessing.util import close_all_fds_except
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import GitIssues, GitPullRequests
from collections import defaultdict
from .utils import get_iso_time, get_oldest_issues#, meanTime
from datetime import datetime, timedelta


class IssuesMetrics(APIView):
    git_issues = GitIssues()
    

    """
    This is issue metrics
    """
    
    def get_username_issues_status(self, username):
        results = defaultdict(int)
        for row in self.git_issues.find({'user': {'$regex': f"{username}", "$options": "i"}}):
            print(row)
            results[row['issue_status']] += 1
        return results

    def get_oldest_issues_with_name(self, name, status, metrics, avg_cycle):
        issues = {'title': [], 'dates': [], 'counts': []}
        sorted_data = self.git_issues.find(
            {'user': {'$regex': f"{name}", "$options": "i"},
             'issue_status': status, 'created_at': {'$gte': get_iso_time(avg_cycle), }})
        sorted_data.sort(key=lambda p: p['created_at'], )
        for row in sorted_data:
            print(row)
            issues['title'].append(row['issue_title'])
            issues['dates'].append(row['created_at'])
        issues['counts'].append(len(issues['title']))
        # sorted_results = get_oldest_issues(issues)
        return issues

    def get(self, request, format=None):
        username = request.GET.get('username', None)
        status = request.GET.get('status', None)
        metrics = request.GET.get('metrics', None)
        avg_cycle = request.GET.get('avg_cycle', None)
        if metrics=="agg_issues_counts":
            return Response(self.get_username_issues_status(username))
        if metrics == 'oldest':
            print(username, status, metrics)
            return Response(self.get_oldest_issues_with_name(username, status, metrics, avg_cycle))

class PersonMetrics(APIView):
    """
    This is person metrics
    """
    """
    Alawyas convert time delta before storing in dictionary
    """
    git_issues = GitIssues()
    git_pr = GitPullRequests()


    def get_username_average_cycle(self, username, avg_cycle1, status):
        results = {'username': [], 'average_time': []}
        completion_time = {'issue_number': [], 'time_taken': [] }
        time_list = []

        sorted_data = self.git_issues.find({'user': {'$regex': f"{username}", "$options": "i"},
             'issue_status': status, 'created_at': {'$gte': get_iso_time(avg_cycle1), }})
        sorted_data.sort(key=lambda p: p['created_at'], )
        for row in sorted_data:
            created_at = row['created_at']
            closed_at = row['closed_at']
            time_taken = closed_at - created_at
            time_list.append(time_taken)
            completion_time['issue_number'].append(row['issue_number'])
            completion_time['time_taken'].append(str(time_taken))

        average_time = sum(time_list,timedelta())/len(time_list)
        results['username'].append(row['user'])
        results['average_time'].append(str(average_time))
        return results, completion_time

    def open_to_close_ratio(self, username):
        results = {'username': [], 'open_to_close_ratio': []}
        open_count= int()
        closed_count = int()

        for row in self.git_issues.find({'user': {'$regex': f"{username}", "$options": "i"}}):
            if row['issue_status'] == "open":
                open_count += 1
            elif row['issue_status'] == "closed":
                closed_count += 1
        total_count = open_count+closed_count
        open_to_close_ratio = (closed_count/total_count)*100
        results['username'].append(row['user'])
        results['open_to_close_ratio'] = f"{open_to_close_ratio}%"
        return results

    def pr_average_cycle_time(self, username, status='closed'):
        results = {'username': [], 'average_time': []}
        completion_time = {'pr_number': [], 'time_taken': [] }
        time_list = []

        for row in self.git_pr.find({'user': {'$regex': f"{username}", "$options": "i"},'pr_status': status, }):
            created_at = row['created_at']
            closed_at = row['closed_at']
            time_taken = closed_at - created_at
            time_list.append(time_taken)
            pr_number = row['pr_number']
            completion_time['pr_number'].append(row['pr_number'])
            completion_time['time_taken'].append(str(time_taken))

        average_time = sum(time_list,timedelta())/len(time_list)
        results['username'].append(row['user'])
        results['average_time'].append(str(average_time))
        return results, completion_time

    def get(self, request, format=None):
        username = request.GET.get('username', None)
        status = request.GET.get('status', "closed")
        metrics = request.GET.get('metrics', None)
        avg_cycle1 = request.GET.get('avg_cycle', None)

        if metrics=="average_cycle_time":
            return Response(self.get_username_average_cycle(username, avg_cycle1, status))
        if metrics == "open_to_close_ratio":
            return Response(self.open_to_close_ratio(username))
        if metrics == "pr_average_cycle_time":
            return Response(self.pr_average_cycle_time(username, status))

    