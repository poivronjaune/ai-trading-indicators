# src/ind/cli.py
import os
import sys
import click
from tabulate import tabulate

from . import io, processor


@click.command()
@click.option(
    "--data-folder",
    prompt="Enter the data folder path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Folder containing ticker data files (CSV).",
)
@click.option(
    "--filename",
    prompt="Enter the ticker filename",
    type=str,
    help="CSV file name containing OHLCV data.",
)
def main(data_folder: str, filename: str) -> None:
    """CLI entry point for AI Trading Indicators."""

    filepath = os.path.join(data_folder, filename)

    if not os.path.isfile(filepath):
        click.echo(f"❌ File not found: {filepath}", err=True)
        sys.exit(1)

    # Step 1: Load data
    df = io.load_csv(filepath)

    # Step 2: Run default indicators
    results = processor.run_default_indicators(df)

    # Step 3: Display results
    click.echo("\n📊 Indicator Results:\n")
    click.echo(tabulate(results.items(), headers=["Indicator", "Value"]))


if __name__ == "__main__":
    main()
