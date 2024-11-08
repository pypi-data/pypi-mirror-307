import typer

from datazone.cli.auth.login import login

app = typer.Typer()
app.command()(login)
