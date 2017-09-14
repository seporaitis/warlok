import os

import click
import git


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
        click.echo("Run the command in repository root.", color='red')
        return 1

    if base is None:
        base = "origin/master"

    repo = git.Repo(os.getcwd())

    click.echo("'feature' not implemented yet.", color='red')


@click.command()
def push():
    click.echo("'push' not implemented yet.")


@click.command()
def review():
    click.echo("'review' not implemented yet.")


@click.group()
def main():
    pass


main.add_command(feature)
main.add_command(push)
main.add_command(review)
