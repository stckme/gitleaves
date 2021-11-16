import gitleaves.reports as reportslib

from typer import Typer, echo

app = Typer()


@app.command()
def genreports():
    echo("Begin reports generation...")
    outdir = reportslib.gen_ghwiki_reports()
    echo(f"Reports saved at `{outdir}`")


@app.command()
def uploadreports():
    echo("Uploading reports...")
    reportslib.upload_ghwiki_reports()


if __name__ == "__main__":
    app()
