import click
from flask.cli import AppGroup

from App.utils import (
    requires_login,
    whoami,
    login_cli,
    clear_session
)

from App.database import get_migrate
from App.main import create_app
from App.models import Street, Driver
from App.controllers import (
    initialize,
    get_all_streets_json,
    get_all_streets,
    get_all_drivers_json,
    get_all_drivers,
    get_street_by_string,
    register_user
)

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')


'''
Driver Commands
'''

# e.g. flask driver <command>
driver_cli = AppGroup('driver', help="Driver object commands")

@driver_cli.command("list", help="List drivers in the database")
@click.option("--f", default="string")
@requires_login(['driver'])
def list_driver_command(f):
    if f == 'string':
        print(get_all_drivers())
    elif f == 'json':
        print(get_all_drivers_json())
    else:
        print("Invalid form argument. (json, string)")


@driver_cli.command("schedule", help="Schedule a stop for a street")
@click.argument("street")
@click.argument("scheduled_date")
@requires_login(['driver'])
def driver_schedule_stop(street: str, scheduled_date: str):
    """Use case 1: Schedule a stop for a street"""
    driver: Driver = whoami()
    street_obj: Street | None = get_street_by_string(street)

    if street_obj is None:
        print("Command failed: Could not get street")
        return

    if driver.schedule_stop(street_obj, scheduled_date):
        click.echo(f"Successfully scheduled a stop to {street_obj.name}.")
    else:
        click.echo(f"Failed to schedule a stop to {street_obj.name}.")

app.cli.add_command(driver_cli) # add group to the cli


'''
Street Commands
'''
# e.g. flask street <command>
street_cli = AppGroup('street', help="Street object commands")

@street_cli.command("list", help="List streets in the database")
@click.option("--f", default="string")
def list_driver_command(f: str):
    if f == 'string':
        print(get_all_streets())
    elif f == 'json':
        print(get_all_streets_json())
    else:
        print("Invalid form argument. (json, string)")

app.cli.add_command(street_cli) # add group to the cli


'''
Auth Commands
'''
# e.g. flask auth <command>
auth_cli = AppGroup("auth", help="Authentication commands")

@auth_cli.command("login", help="Log in and persist session")
@click.option("--username", required=True)
@click.option("--password", required=True, prompt=True, hide_input=True)
def auth_login(username, password):
    """Use case 2: Login"""
    if login_cli(username, password):
        u = whoami()
        click.secho(f"Logged in as {u.username} ({u.first_name} {u.last_name})", fg="green")
    else:
        raise click.ClickException("Invalid credentials.")

@auth_cli.command("register", help="Create an account")
@click.option("--username", required=True)
@click.option("--password", required=True)
@click.option("--firstname", required=True)
@click.option("--lastname", required=True)
@click.option("--role", default="resident")
@click.option("--street")
def auth_register(username: str, password: str, firstname: str, lastname: str, role: str, street: str):
    """User case 3: Register"""
    register_user(username, password, firstname, lastname, role, street)


@auth_cli.command("logout", help="Clear session")
def auth_logout():
    clear_session()
    click.secho("Logged out.", fg="yellow")

@auth_cli.command("profile", help="Show current session user")
def auth_whoami():
    u = whoami()
    if not u:
        click.secho("Not logged in.", fg="red")
        return
    click.echo(f"{u.username} ({u.first_name} {u.last_name})")

app.cli.add_command(auth_cli)