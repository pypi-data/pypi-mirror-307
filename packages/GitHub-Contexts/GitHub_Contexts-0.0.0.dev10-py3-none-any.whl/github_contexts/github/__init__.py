from github_contexts.github.context import GitHubContext
from github_contexts.github import enum, payload


def create(context: dict) -> GitHubContext:
    """Create a GitHub context object from the given dictionary."""
    return GitHubContext(context)
