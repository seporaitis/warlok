import os
import re
from contextlib import contextmanager

import git

RepositoryNotFoundMessage = 'No git repository found in the path: {original}.'.format


class RepositoryNotFoundError(Exception):
    pass


def get_repository_dir(path):
    original = path
    while path.count('/') > 0:
        git_dir = os.path.join(path, '.git')
        if os.path.exists(git_dir):
            return path
        path = path[:path.rfind('/')]
    raise RepositoryNotFoundError(RepositoryNotFoundMessage(original=original))


@contextmanager
def stash(repo):
    dirty = repo.is_dirty()
    if dirty:
        repo.git.stash()

    yield

    if dirty:
        repo.git.stash('pop')


def get_repository():
    repo_path = get_repository_dir(os.getcwd())
    return git.Repo(repo_path)


def get_repository_full_name(url):
    rex = re.compile(r'git@github.com:(?P<username>[\w\d-]+)\/(?P<reponame>[\w\d-]+).git')
    match = rex.match(url)

    username = match.group('username')
    reponame = match.group('reponame')

    return f'{username}/{reponame}'
