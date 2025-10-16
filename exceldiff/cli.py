"""Command-line interface for exceldiff."""

import sys
import click
from exceldiff.excel_reader import ExcelReader
from exceldiff.differ import WorksheetDiffer
from exceldiff.writer import ExcelDiffWriter


@click.command()
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
@click.option(
    '--output', '-o',
    type=click.Path(),
    default='diff_output.xlsx',
    help='Output file path (default: diff_output.xlsx)'
)
@click.option(
    '--sheet1',
    type=str,
    default=None,
    help='Sheet name in first file (default: first sheet)'
)
@click.option(
    '--sheet2',
    type=str,
    default=None,
    help='Sheet name in second file (default: first sheet)'
)
def main(file1: str, file2: str, output: str, sheet1: str, sheet2: str):
    """
    Compare two Excel worksheets and output differences to a new file.

    FILE1: Path to the first Excel file (baseline)
    FILE2: Path to the second Excel file (comparison)

    Color coding:
      - No color: Identical rows
      - Red cells: Modified cells in a row
      - Yellow row: Row removed in FILE2
      - Orange row: Row added in FILE2
    """
    try:
        reader = ExcelReader()

        # Validate file formats
        if not reader.supports(file1):
            click.echo(f"Error: {file1} is not a .xlsx file", err=True)
            sys.exit(1)

        if not reader.supports(file2):
            click.echo(f"Error: {file2} is not a .xlsx file", err=True)
            sys.exit(1)

        # Show available sheets if needed
        if sheet1 is None:
            sheets = reader.get_sheet_names(file1)
            click.echo(f"Reading first sheet from {file1}: '{sheets[0]}'")

        if sheet2 is None:
            sheets = reader.get_sheet_names(file2)
            click.echo(f"Reading first sheet from {file2}: '{sheets[0]}'")

        # Read worksheets
        click.echo(f"\nReading {file1}...")
        data1 = reader.read(file1, sheet1)
        click.echo(f"  Loaded {len(data1)} rows")

        click.echo(f"Reading {file2}...")
        data2 = reader.read(file2, sheet2)
        click.echo(f"  Loaded {len(data2)} rows")

        # Perform diff
        click.echo("\nComparing worksheets...")
        differ = WorksheetDiffer()
        diffs = differ.compare(data1, data2)

        # Count diff types
        stats = {
            'identical': 0,
            'modified': 0,
            'removed': 0,
            'added': 0
        }

        for diff in diffs:
            stats[diff.diff_type.value] += 1

        click.echo(f"\nDiff Summary:")
        click.echo(f"  Identical rows: {stats['identical']}")
        click.echo(f"  Modified rows:  {stats['modified']}")
        click.echo(f"  Removed rows:   {stats['removed']}")
        click.echo(f"  Added rows:     {stats['added']}")

        # Write output
        click.echo(f"\nWriting diff to {output}...")
        writer = ExcelDiffWriter()
        writer.write(diffs, output)

        click.echo(f"\nDone! Diff written to {output}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
