from github import Github
from django.core.management.base import BaseCommand
from core.models import GitIssues, GitPullRequests
from pathlib import Path


class Command(BaseCommand):
    help = "Ingest bootstrap git_data into MongoDB"

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).parent.resolve()
        issues = GitIssues()
        pull_requests = GitPullRequests()

        access_token = "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"

        login = Github(access_token)
        user = login.get_user()

        my_repos = user.get_repos()

        for repository in my_repos:
            repo_name = repository.name
            private = repository.private

            if private:
                print(f"get pull request for repo {repo_name}")
                pulls = repository.get_pulls(state="all")
                for pr in pulls:
                    pull_requests.add(
                        {   
                            "user": pr.user.login,
                            "pr_title": pr.title,
                            "pr_number": pr.number,
                            "assignees":[i.login for i in pr.assignees],
                            "pr_status": pr.state,
                            "repo_name": repo_name,
                            "created_at": pr.created_at,
                            "closed_at": pr.closed_at
                        }
                    )
                print(f"Ingested pull request")

                all_issues = repository.get_issues(state="all")
                for issue in all_issues:
                    issues.add({
                                "user": issue.user.login,
                                "issue_title": issue.title,
                                "assignees":[i.login for i in issue.assignees],
                                "issue_number": issue.number,
                                "issue_status": issue.state,
                                "repo_name": repo_name,
                                "created_at": issue.created_at,
                                "closed_at": issue.closed_at
                    })
                print(f"Ingested GitIssues")

