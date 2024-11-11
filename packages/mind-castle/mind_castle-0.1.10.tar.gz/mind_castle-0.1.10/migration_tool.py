import iterfzf
import typer
import json
from sqlalchemy import create_engine, select, table, inspect, func, and_
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from rich import print
from rich.prompt import Prompt
from rich.table import Table as RichTable
from rich.panel import Panel
from rich.progress import track

from mind_castle.stores import put_secret


def main(
    target_table: str = None,
    column: str = None,
    dry_run: bool = True,
    secret_type: str = "json",
):
    print("Creating DB engine..")
    engine = create_engine(
        "REDACTED"
    )

    # reflect the tables
    Base = automap_base()
    Base.prepare(autoload_with=engine)

    with Session(engine) as session:
        # None of the changes below will be committed to the DB unless we run session.commit()

        # Get the user's selection of table and column
        insp = inspect(engine)
        tables = insp.get_table_names()
        target_table = iterfzf.iterfzf(tables, prompt="Target table > ")

        # Create a auto-mapped class for the target table
        TargetTable = getattr(Base.classes, target_table)

        columns = TargetTable.__table__.columns.keys()
        target_column = iterfzf.iterfzf(columns, prompt="Target column > ")

        # Analyse and plan what to do. See how many rows we'll have to edit
        # We're not going to change any rows that have an empty value in the target column so don't count them
        filter_exclusions = and_(
            getattr(TargetTable, target_column) != "{}",
            getattr(TargetTable, target_column) != "",
        )
        stmt = select(func.count()).select_from(TargetTable).where(filter_exclusions)
        rows_to_edit = session.execute(stmt).scalar_one()

        # Warn the user of what's about to happen
        print(
            Panel(
                "[bold underline red]YOU'RE ABOUT TO MODIFY YOUR DATABASE[/bold underline red]\n\nIf you continue and don't have a backup of your DB, you should feel bad.",
                expand=False,
            )
        )

        print(
            f"- There are {rows_to_edit} rows about to be altered in the '{target_table}' table."
        )
        print(f"- We will be modifying the '{target_column}' column.")
        print("- Only JSON columns are supported for now")
        print("- This could take a while.")
        print(
            "- If any error occurs at any point, we will bail out and make no changes."
        )
        print("- You will get another chance to bail out before changes are committed.")

        cont = typer.confirm("Continue?")
        if not cont:
            raise typer.Abort()

        rows = session.query(TargetTable).filter(filter_exclusions).all()
        secrets_stored = 0
        for row in track(rows):
            data_str = getattr(row, target_column)
            data = json.loads(data_str)  # Check the data is valid JSON
            if not dry_run:
                secret_def = put_secret(data_str, secret_type)
                setattr(row, target_column, json.dumps(secret_def))
            secrets_stored += 1

        if secrets_stored != rows_to_edit:
            print(
                f"ERROR: Number of modified rows ({secrets_stored}) does not match expected ({rows_to_edit}). Is the database being written to?"
            )
            raise typer.Abort()

        if dry_run:
            print("Dry run completed successfully.")
            raise typer.Exit()

        cont = typer.confirm("Changes have been queued successfully. Commit them?")
        if not cont:
            raise typer.Abort()

        session.commit()


if __name__ == "__main__":
    typer.run(main)
