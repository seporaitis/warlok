import os
from contextlib import contextmanager
from subprocess import call

import click
import git

from warlok.repository import (
    get_repository_dir,
    RepositoryNotFoundError,
)


@contextmanager
def stash(repo):
    dirty = repo.is_dirty()
    if dirty:
        repo.git.stash()

    yield

    if dirty:
        repo.git.stash('pop')


def get_repo():
    repo_path = get_repository_dir(os.getcwd())
    return git.Repo(repo_path)


@click.command()
@click.argument('name')
@click.argument('base', required=False)
def feature(name, base):
    """Start off a new feature.

    Creates a new feature branch NAME, branching off BASE.

    If BASE is not provided, defaults to the current branch.

    """
    try:
        repo = get_repo()
    except RepositoryNotFoundError as err:
        click.secho(str(err))
        return 1

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
@click.argument('base', required=False)
def push(base):
    """Updates remote branch and creates pull-request if necessary.

    """
    try:
        repo = get_repo()
    except RepositoryNotFoundError as err:
        click.secho(str(err))
        return 1
    
    if base is None:
        base = "master"

    branch = repo.head.ref.name
    origin = repo.remotes.origin
    base_exists = base in origin.refs

    if not base_exists:
        click.secho("Could not find 'origin/{}. Did you forget to push the base branch?".format(base))
        return 1

    push_info = origin.push(branch)[0]
    if not ((push_info.flags & push_info.UP_TO_DATE)
            or (push_info.flags & push_info.NEW_HEAD)
            or (push_info.flags & push_info.FAST_FORWARD)):
        click.secho("Failed pushing to 'origin/{}'.".format(branch), fg='red')
        click.echo(push_info.summary)
        return 1

    click.secho("Pushed changes successfuly...", fg='green')

    if push_info.flags & push_info.NEW_HEAD:
        call(['hub', 'pull-request', '-h', branch, '-b', base])

    return 0

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
    """An evil cousin to Arcanist. Command-line interface to GitHub."""
    pass


main.add_command(feature)
main.add_command(push)
main.add_command(pull)
main.add_command(review)
