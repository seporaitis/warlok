import os
from contextlib import contextmanager

import click
import git


@contextmanager
def stash(repo):
    dirty = repo.is_dirty()
    if dirty:
        repo.git.stash()

    yield

    if dirty:
        repo.git.stash('pop')


def get_repo_dir():
    repo_path = os.path.join(os.getcwd(), ".git")
    if not os.path.exists(repo_path):
        click.secho("Run the command in repository root.", fg='red')
        return None
    return os.getcwd()


def get_repo():
    repo_path = get_repo_dir()
    if repo_path:
        return git.Repo(repo_path)
    return None


@click.command()
@click.argument('name')
@click.argument('base', required=False)
def feature(name, base):
    """Start off a new feature.

    Creates a new feature branch NAME, branching off BASE.

    If BASE is not provided, defaults to the current branch.

    """
    repo = get_repo()

    if base is None:
        base = "master"

    origin = repo.remotes.origin
    origin.fetch()

    if base not in origin.refs:
        click.secho("'{}' not found in remote 'origin'. Did you forget to push it?".format(base), fg='red')
        return 1

    with stash(repo):
        branch = repo.create_head(name, origin.refs[base].commit)
        branch.checkout()

    return 0


@click.command()
def push():
    click.secho("TODO: launch $EDITOR with a warlok pull-request template.", fg='yellow')
    click.secho("TODO: process the message.", fg='yellow')
    click.secho("TODO: create pull-request.", fg='yellow')
    click.secho("TODO: set pull-request attributes based on the message.", fg='yellow')
    click.secho("TODO: OR update an existing pull-request.", fg='green')
    click.secho("'push' not implemented yet.", fg='red')


@click.command()
@click.argument('number')
def pull(number):
    repo = get_repo()
    origin = repo.remotes.origin
    fetch_info = origin.fetch('pull/{}/head'.format(number))
    branch = repo.create_head("PR{}".format(number), fetch_info[0].commit)
    branch.checkout()

    return 0

@click.command()
def review():
    click.secho("TODO: print pull-requests waiting on user.", fg='yellow')
    click.secho("TODO: print user pull-requests waiting on others.", fg='yellow')
    click.secho("'review' not implemented yet.", fg='red')


@click.group()
def main():
    pass


main.add_command(feature)
main.add_command(push)
main.add_command(pull)
main.add_command(review)
