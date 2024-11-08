import typer
from rich import print

from datazone.core.common.settings import SettingsManager
from datazone.core.connections.auth import AuthService
from datazone.utils.helpers import check_host_https


def create(
    profile: str = typer.Option("default", prompt=True, help="Profile name"),
    host: str = typer.Option("app.datazone.co", prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., hide_input=True, confirmation_prompt=True, prompt=True),
):
    profile_exist = SettingsManager.check_profile_exists(profile)
    if profile_exist:
        replace = typer.confirm(
            f"There is a profile named {profile}, it will be replaced. Are you sure?",
        )
        if not replace:
            return

    host = check_host_https(host)

    SettingsManager.create_profile(
        profile_name=profile,
        email=email,
        password=password,
        server_endpoint=host,
    )

    AuthService.login()

    print("You logged in successfully :tada:")
