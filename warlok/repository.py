import os

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
