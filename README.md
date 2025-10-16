# ExcelDiff

A tool to compare two Excel worksheets and highlight differences with color-coded output.

## Features

- Compare Excel (.xlsx) files worksheet by worksheet
- Color-coded diff output:
  - **No color**: Identical rows
  - **Red cells**: Modified cells within a row
  - **Yellow rows**: Rows removed in the second file
  - **Orange rows**: Rows added in the second file
- Specify which worksheet to compare (defaults to first sheet)
- Extensible architecture for adding support for other file formats

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Usage

### Basic usage

Compare two Excel files and output to `diff_output.xlsx`:

```bash
exceldiff file1.xlsx file2.xlsx
```

### Specify output file

```bash
exceldiff file1.xlsx file2.xlsx --output result.xlsx
```

or using short form:

```bash
exceldiff file1.xlsx file2.xlsx -o result.xlsx
```

### Specify worksheets

Compare specific sheets within the files:

```bash
exceldiff file1.xlsx file2.xlsx --sheet1 "Sheet1" --sheet2 "Sheet1"
```

### Full example

```bash
exceldiff baseline.xlsx updated.xlsx \
  --output comparison.xlsx \
  --sheet1 "Q1 Data" \
  --sheet2 "Q1 Data"
```

## Understanding the Output

The tool generates an Excel file with the following color scheme:

| Color | Meaning |
|-------|---------|
| No color | Row is identical in both files |
| Red (individual cells) | Cells that have different values |
| Yellow (entire row) | Row exists in file1 but not in file2 (removed) |
| Orange (entire row) | Row exists in file2 but not in file1 (added) |

## Architecture

The tool is designed with extensibility in mind:

```
exceldiff/
├── reader.py         # Abstract FileReader interface
├── excel_reader.py   # Excel implementation of FileReader
├── differ.py         # Core diff engine (format-agnostic)
├── writer.py         # Excel output with formatting
└── cli.py            # Command-line interface
```

### Adding Support for Other Formats

To add support for CSV, ODS, or other formats:

1. Create a new reader class implementing the `FileReader` interface in `reader.py`
2. Implement the three required methods: `read()`, `get_sheet_names()`, and `supports()`
3. Update the CLI to use the appropriate reader based on file extension

Example:

```python
from exceldiff.reader import FileReader

class CSVReader(FileReader):
    def read(self, file_path: str, sheet_name: Optional[str] = None) -> List[List[Any]]:
        # Implementation here
        pass

    def get_sheet_names(self, file_path: str) -> List[str]:
        return ["Sheet1"]  # CSV has only one sheet

    def supports(self, file_path: str) -> bool:
        return file_path.endswith('.csv')
```

## Requirements

- Python 3.8+
- openpyxl >= 3.1.2
- click >= 8.1.7

## License

MIT
