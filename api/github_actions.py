import os
import argparse
from github import Github

def create_github_release(token, repo_name, tag_name, release_name, body):
    """
    Create a new release in the specified GitHub repository.
    """
    g = Github(token)
    repo = g.get_repo(repo_name)
    repo.create_git_release(tag=tag_name, name=release_name, message=body)
    print(f"Successfully created release '{release_name}' with tag '{tag_name}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a GitHub release.")
    parser.add_argument("--token", required=True, help="GitHub token")
    parser.add_argument("--repo-name", required=True, help="Repository name (e.g., 'user/repo')")
    parser.add_argument("--tag-name", required=True, help="Tag name for the release")
    parser.add_argument("--release-name", required=True, help="Name of the release")
    parser.add_argument("--body", required=True, help="Body of the release")

    args = parser.parse_args()

    create_github_release(
        token=args.token,
        repo_name=args.repo_name,
        tag_name=args.tag_name,
        release_name=args.release_name,
        body=args.body
    )
