import click
import os
import platform
from thunder import api
from thunder import auth_helper
import requests

OAUTH_URL = "https://console.thundercompute.com/login"


def get_token_from_user():
    return click.prompt("Token", type=str, hide_input=False)


def login():
    credentials_file_path = auth_helper.get_credentials_file_path()

    # Check if a saved token exists
    if os.path.exists(credentials_file_path):
        with open(credentials_file_path, "r", encoding="utf-8") as f:
            token = f.read().strip()

        if token:
            click.echo(
                "Already logged in. Please log out using `tnr logout` and try again."
            )
            return token  # Return the valid token, skip the login process
    click.echo(
        f"Please click the following link and generate an API token in the Thunder Compute console: {OAUTH_URL}"
    )
    # Wait for user to input the token
    success = False
    num_attempts = 0
    while not success and num_attempts < 5:
        token = get_token_from_user()

        endpoint = f"https://api.thundercompute.com:8443/uid"
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {token}"})

        if response.status_code == 200:
            success = True
        elif response.status_code == 401:
            click.echo(
                click.style(
                    f"Invalid token, please update the TNR_API_TOKEN environment variable or login again",
                    fg="red",
                    bold=True,
                )
            )
            num_attempts += 1
        else:
            click.echo(
                click.style(
                    f"Failed to authenticate token, please use `tnr logout` and try again.",
                    fg="red",
                    bold=True,
                )
            )
            exit(1)

    if not success and num_attempts == 5:
        click.echo(
            click.style(
                f"Failed to login to thunder compute after 5 attempts. Please sign in with a valid API token",
                fg="red",
                bold=True,
            )
        )
        exit(1)

    credentials_file_path = auth_helper.get_credentials_file_path()
    with open(credentials_file_path, "w", encoding="utf-8") as f:
        f.write(token)

    click.echo(
        click.style(
            "Logged in successfully",
            fg="green",
        )
    )
    return token


def logout():
    auth_helper.delete_data()
    click.echo(
        click.style(
            "Logged out successfully",
            fg="green",
        )
    )


if __name__ == "__main__":
    login()
