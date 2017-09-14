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


@click.command()
@click.argument('name')
@click.argument('base', required=False)
def feature(name, base):
    """Start off a new feature.

    Creates a new feature branch NAME, branching off BASE.

    If BASE is not provided, defaults to the current branch.

    """
    repo_path = os.path.join(os.getcwd(), ".git")
    if not os.path.exists(repo_path):
        click.secho("Run the command in repository root.", fg='red')
        return 1

    repo = git.Repo(os.getcwd())

    if base is None:
        base = repo.head.commit

    click.secho("TODO: check that '{}' exists on remote.".format(base))

    with stash(repo):
        # do something here
        click.secho("TODO: checkout '{}'".format(base), fg='yellow')
        click.secho("TODO: branch off '{}'".format(name), fg='yellow')

    click.secho("'feature' not implemented yet.", fg='red')


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
    click.secho("TODO: pull pull-request '{}' locally.".format(number), fg='yellow')
    click.secho("TODO: checkout pull-request '{}' locally.".format(number), fg='yellow')
    click.secho("'pull' not implemented yet.", fg='red')


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
