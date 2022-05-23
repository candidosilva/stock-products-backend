import click
import getpass
from ..extentions.database import mongo
from werkzeug.security import generate_password_hash
from flask import Blueprint

userCommands = Blueprint('user', __name__)

@userCommands.cli.command("getUser")
@click.argument("name")
def get_user(name):
    userCollection = mongo.db.users
    user = [u for u in userCollection.find({"name":name})]
    print(user)

@userCommands.cli.command("addUser")
@click.argument("name")
def create_user(name):
    userCollection = mongo.db.users
    password = getpass.getpass()
    user = {
        "name":name,
        "password":generate_password_hash(password)
    }

    userExists = userCollection.find_one({"name":name})
    if userExists:
        print(f'Usuário {name} já existe')
    else: 
        userCollection.insert_one(user)
        print('Usuário cadastrado com sucesso')

@userCommands.cli.command("dropUser")
@click.argument("name")
def delete_user(name):
    userCollection = mongo.db.users
    userExists = userCollection.find_one({"name": name})

    if userExists:
        question = input(f'Deseja realmente deletar o usuário {name} ? (S/N)')

        if question.upper() == 'S':
            userCollection.delete_one({"name":name})
            print("Usuário deletado com sucesso")
        else:
            exit()
        
    else:
        print("Usuário não encontrado ")