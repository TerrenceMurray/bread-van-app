from functools import wraps

import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App import get_street_by_string
from App.database import db, get_migrate
from App.main import create_app, save_session, load_session, clear_session
from App.models import User
from App.controllers import (
    get_all_users_json,
    get_all_users,
    initialize,
    get_all_streets_json,
    get_all_streets,
    get_all_drivers_json,
    get_all_drivers,
    create_stop
)

app = create_app()
migrate = get_migrate(app)

def login_cli(username: str, password: str) -> bool:
    user = db.session.execute(
        db.select(User).where(User.username == username)
    ).scalar_one_or_none()
    if not user or not user.check_password(password):
        return False
    save_session(user.id)
    return True

def whoami() -> User | None:
    uid = load_session()
    if uid is None:
        return None
    return db.session.get(User, uid)

def requires_login(fn):
    """Decorator for commands that require a logged-in user."""
    @wraps(fn)
    @with_appcontext
    def wrapper(*args, **kwargs):
        if not whoami():
            raise click.ClickException("Not logged in. Use: flask auth login.")
        return fn(*args, **kwargs)
    return wrapper

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

'''
User Commands
'''

user_cli = AppGroup('user', help='User object commands')

@user_cli.command("list", help="Lists users in the database")
@click.option("--f", default="string")
def list_user_command(f):
    if f == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Driver Commands
'''

# e.g. flask driver <command>
driver_cli = AppGroup('driver', help="Driver object commands")

@driver_cli.command("list", help="List drivers in the database")
@click.option("--f", default="string")
@requires_login
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
@requires_login
def driver_schedule_stop(street: str, scheduled_date: str):
    """Use case 1: Schedule a stop for a street"""
    street_obj = get_street_by_string(street)

    if street_obj is None:
        print("Command failed: Could not get street")
        return

    new_stop = create_stop()


app.cli.add_command(driver_cli) # add group to the cli

'''
Street Commands
'''

street_cli = AppGroup('street', help="Street object commands")

@street_cli.command("list", help="List streets in the database")
@click.option("--f", default="string")
@requires_login
def list_driver_command(f: str):
    if f == 'string':
        print(get_all_streets())
    elif f == 'json':
        print(get_all_streets_json())
    else:
        print("Invalid form argument. (json, string)")

app.cli.add_command(street_cli) # add group to the cli


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
@requires_login
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)


'''
Auth Commands
'''
auth_cli = AppGroup("auth", help="Authentication commands")

@auth_cli.command("login", help="Log in and persist session")
@click.option("--username", required=True)
@click.option("--password", required=True, prompt=True, hide_input=True)
def auth_login(username, password):
    if login_cli(username, password):
        u = whoami()
        click.secho(f"Logged in as {u.username} ({u.first_name} {u.last_name})", fg="green")
    else:
        raise click.ClickException("Invalid credentials.")

@auth_cli.command("logout", help="Clear session")
def auth_logout():
    clear_session()
    click.secho("Logged out.", fg="yellow")

@auth_cli.command("whoami", help="Show current session user")
def auth_whoami():
    u = whoami()
    if not u:
        click.secho("Not logged in.", fg="red")
        return
    click.echo(f"{u.username} ({u.first_name} {u.last_name})")

app.cli.add_command(auth_cli)