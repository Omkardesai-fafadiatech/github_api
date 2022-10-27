from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import GitIssues
from collections import defaultdict
from .utils import get_iso_time, get_oldest_issues
import operator


class IssuesMetrics(APIView):
    git_issues = GitIssues()
    results = defaultdict(int)

    """
    This is issue metrics
    """
    
    def get_username_issues_status(self, username):
        for row in self.git_issues.find({'name': {'$regex': f"{username}", "$options": "i"}}):
            self.results[row['state']] += 1
        return self.results

    def get_oldest_issues_with_name(self, name, status, metrics, avg_cycle):
        issues = {'title': [], 'dates': [], 'counts': []}
        sorted_data = self.git_issues.find(
            {'name': {'$regex': f"{name}", "$options": "i"},
             'state': status, 'created_at': {'$gte': get_iso_time(avg_cycle), }})
        sorted_data.sort(key=lambda p: p['created_at'], )
        for row in sorted_data:
            print(row)
            issues['title'].append(row['title'])
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

