from github import Github
from django.core.management.base import BaseCommand
from core.models import GitIssues,GitPullRequests
from pathlib import Path

class Command(BaseCommand):
    help = "Ingest bootstrap git_data into MongoDB"

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).parent.resolve()
        issues = GitIssues()
        pull_requests = GitPullRequests()
        
        access_token ="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"

        login  = Github(access_token)
        user  = login.get_user()

        my_repos = user.get_repos()
        
        for repository  in my_repos:
            repo_name =  repository.name
            private = repository.private

            if private:
                print(f"get pull request for repo {repo_name}")
                pulls = repository.get_pulls(state="all") 
                for pr in pulls:
                    issue_number, pr_title,state,name, created_at, closed_at = pr.number, pr.title,pr.state,pr.user.login, pr.created_at, pr.closed_at
                    pull_requests.add(
                        {
                            'user':name,
                            "issue_number": issue_number,
                            "pr_title": pr_title,
                            "state": state,
                            "repo_name": repo_name,
                            "created_at": created_at,
                            "closed_at": closed_at
                        }
                    )
                print(f"Ingested pull request")

                all_issues = repository.get_issues(state='all')
                for issue in all_issues:
                    issues.add({
                                'title': issue.title,
                                'number': issue.number,
                                'name': issue.user.login,
                                'state': issue.state,
                                "repo_name": repo_name,
                                "created_at": issue.created_at,
                                "closed_at": issue.closed_at
                                })
                print(f"Ingested GitIssues")
