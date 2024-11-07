from datazone.core.connections.auth import AuthService
from rich import print


def login():
    AuthService.login()
    print("You logged in successfully :tada:")
