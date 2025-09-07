import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App import get_all_drivers, get_all_drivers_json
from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

driver_cli = AppGroup('driver', help="Driver object commands")

@driver_cli.command("list", help="List drivers in the database")
@click.argument("f", default="string")
def list_driver_command(f):
    if f == 'string':
        print(get_all_drivers())
    elif f == 'json':
        print(get_all_drivers_json())
    else:
        print("Invalid form argument. (json, string)")

app.cli.add_command(driver_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)