import click


def get_credentials():
    username = click.prompt(text="Username")
    # TODO: use click.prompt(text="Password (never stored):", hide_input=True)
    # and use that to automatically generate token.
    token = click.prompt(text="Token (generated online)", hide_input=True)

    return {
        'github.com': {
            'username': username,
            'token': token,
        }
    }
