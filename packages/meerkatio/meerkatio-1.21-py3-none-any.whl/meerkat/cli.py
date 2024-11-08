import click
import os

from meerkat import (
    email as send_email, 
    ping as send_ping, 
    sms as send_sms, 
    slack as send_slack, 
    system as send_system, 
    teams as send_teams, 
    google_chat as send_google_chat
)
from meerkat.api import get_user_token, register_user

@click.group()
def meerkat():
    pass

@meerkat.command()
def ping():
    """Trigger ping sound to play from your local machine"""
    send_ping()

@meerkat.command()
@click.argument('message', type=str)
def system(message):
    """Send a message to the System Tray with MESSAGE content"""
    send_system(message=message)

@meerkat.command()
@click.argument('message', type=str)
def email(message):
    """Send an email to your MeerkatIO email address with MESSAGE content"""
    send_email(message=message)

@meerkat.command()
@click.argument('message', type=str)
def sms(message):
    """Send an SMS to your MeerkatIO email address with MESSAGE content"""
    send_sms(message=message)

@meerkat.command()
@click.argument('message', type=str)
def slack(message):
    """Send a Slack direct message to yourself with MESSAGE content"""
    send_slack(message=message)

@meerkat.command()
@click.argument('message', type=str)
def teams(message):
    """Send a teams direct message to yourself with MESSAGE content"""
    send_teams(message=message)

@meerkat.command()
@click.argument('message', type=str)
def google_chat(message):
    """Send a google_chat direct message to yourself with MESSAGE content"""
    send_google_chat(message=message)

@meerkat.command()
def login():
    """Login to MeerkatIO Platform and setup local environment"""
    email = click.prompt("Enter Email")
    password = click.prompt("Enter Password", hide_input=True)
    token = get_user_token(email, password)

    if not token:
        click.echo("Invalid email or password.")
        return

    #save token to user HOME and set OS env
    with open(os.path.expanduser("~") + "/.meerkat", "w") as file:
        file.write(token)
    os.environ["MEERKAT_TOKEN"] = token

    click.echo(f"\nMeerkatIO initialized successfully!")

@meerkat.command()
def register():
    """Register on the MeerkatIO Platform and setup local environment"""
    email = click.prompt("Enter Email")
    password = click.prompt("Enter Password", hide_input=True)
    token = register_user(email, password)

    if not token:
        click.echo("Registration error, please check email and password.")
        return

    #save token to user HOME and set OS env
    with open(os.path.expanduser("~") + "/.meerkat", "w") as file:
        file.write(token)
    os.environ["MEERKAT_TOKEN"] = token

    click.echo(f"\nMeerkatIO account created successfully! Your 30 day free trial starts now. Go to https://meerkatio.com/account to configure additional communication channels.")

if __name__ == "__main__":
    meerkat()