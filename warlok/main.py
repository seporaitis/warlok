import os.path

import click
import github

from warlok.config import get_hub_config, get_or_create_config
from warlok.parser import get_message_template, parse_message_into_fields
from warlok.patches import patch_pull_request
from warlok.repository import (
    RepositoryNotFoundError,
    get_repository,
    get_repository_full_name,
    stash,
)


@click.command()
@click.argument('name')
@click.argument('base', required=False)
def feature(name, base):
    """Start off a new feature.

    Creates a new feature branch NAME, branching off BASE.

    If BASE is not provided, defaults to the current branch.

    """
    try:
        repo = get_repository()
    except RepositoryNotFoundError as err:
        click.secho(str(err))
        return 1

    if base is None:
        base = 'master'

    origin = repo.remotes.origin
    origin.fetch()

    if base not in origin.refs:
        click.secho(f'"{base}" not found in remote "origin". Did you forget to push it?', fg='red')
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
        repo = get_repository()
    except RepositoryNotFoundError as err:
        click.secho(str(err))
        return 1

    if base is None:
        base = 'master'

    branch = repo.head.ref.name
    origin = repo.remotes.origin

    if base not in origin.refs:
        click.secho(f'Could not find "origin/{base}". Did you forget to push the base branch?')
        return 1

    push_info = origin.push(branch)[0]
    if not ((push_info.flags & push_info.UP_TO_DATE)
            or (push_info.flags & push_info.NEW_HEAD)
            or (push_info.flags & push_info.FAST_FORWARD)):
        click.secho(f'Failed pushing to "origin/{branch}"', fg='red')
        click.echo(push_info.summary)
        return 1

    click.secho('Pushed changes successfuly...', fg='green')

    if push_info.flags & push_info.NEW_HEAD:
        dir_name = os.path.join(os.path.expanduser('~'), '.config')
        config = get_or_create_config(dir_name, 'warlok', get_hub_config)
        hub = github.Github(config['github.com'].get('oauth_token'))
        hub_repo = hub.get_repo(get_repository_full_name(origin.url))

        message = click.edit(get_message_template({
            'title': '',
            'summary': '',
            'reviewers': '',
        }))

        fields = parse_message_into_fields(
            message,
            ('title', 'summary', 'reviewers'),
        )

        pull_request = hub_repo.create_pull(
            title=fields['title'],
            body=fields['summary'],
            base=base,
            head=branch,
        )

        patch_pull_request(pull_request)

        reviewers = [x.strip() for x in fields['reviewers'].split(",")]
        headers, data = pull_request.create_review_request(reviewers=reviewers)
        print(headers)
        print(data)

    return 0


@click.command()
@click.argument('number')
def pull(number):
    repo = get_repository()
    origin = repo.remotes.origin
    fetch_info = origin.fetch(f'pull/{number}/head')
    branch = repo.create_head(f'PR{number}', fetch_info[0].commit)
    branch.checkout()

    return 0


@click.command()
def review():
    click.secho('TODO: print pull-requests waiting on user.', fg='yellow')
    click.secho('TODO: print user pull-requests waiting on others.', fg='yellow')
    click.secho('"review" not implemented yet.', fg='red')


@click.group()
def main():
    """An evil cousin to Arcanist. Command-line interface to GitHub."""
    pass


main.add_command(feature)
main.add_command(push)
main.add_command(pull)
main.add_command(review)
