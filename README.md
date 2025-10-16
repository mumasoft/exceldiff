# ExcelDiff

A tool to compare two Excel worksheets and highlight differences with color-coded output.

## Features

- Compare Excel (.xlsx) files worksheet by worksheet
- Modified cells show both old and new values with red text and comments
- Color-coded diff output:
  - **Modified cells**: Red text showing "old → new" with explanatory comment
  - **Yellow rows**: Rows removed in the second file
  - **Orange rows**: Rows added in the second file
- Specify which worksheet to compare (defaults to first sheet)
- Option to output only rows with differences (exclude identical rows)
- Extensible architecture for adding support for other file formats

## Installation

### Option 1: Standalone Executable (Recommended)

Download the pre-built executable from the [latest release](https://github.com/mumasoft/exceldiff/releases/latest):

**Available platforms:**
- **Linux (x86_64)**: `exceldiff-linux`
- **macOS (ARM64/M1/M2/M3)**: `exceldiff-macos`

**Usage:**
```bash
# Download from releases page, then:

# Make it executable (macOS/Linux)
chmod +x exceldiff-linux  # or exceldiff-macos

# Move to a directory in your PATH (optional)
sudo mv exceldiff-linux /usr/local/bin/exceldiff

# Or use directly
./exceldiff-linux file1.xlsx file2.xlsx -o output.xlsx
```

**No Python or dependencies required!** The executable includes everything needed to run.

### Option 2: Install from Source

If you want to modify the code or build it yourself:

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

### Building a Standalone Executable

To build your own standalone executable:

```bash
# Activate virtual environment
source venv/bin/activate

# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller exceldiff.spec

# Executable will be in dist/exceldiff
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

### Show only differences

Output only rows with differences (exclude identical rows):

```bash
exceldiff file1.xlsx file2.xlsx --diff-only
```

This is useful when comparing large files where you only want to see what changed.

By default, when using `--diff-only`, the first row from the first file is included as a header row. To exclude the header:

```bash
exceldiff file1.xlsx file2.xlsx --diff-only --no-header
```

### Full example

```bash
exceldiff baseline.xlsx updated.xlsx \
  --output comparison.xlsx \
  --sheet1 "Q1 Data" \
  --sheet2 "Q1 Data" \
  --diff-only
```

## Understanding the Output

The tool generates an Excel file with the following formatting:

### Modified Cells
For cells with different values, the output shows:
- Cell displays both values: `old_value → new_value` (separated by an arrow)
- **Red text color** to indicate the cell has changed
- **Cell comment** showing details: "Changed from: [old] To: [new]"

Example: If a cell changed from "25" to "26", it will display as "25 → 26" in red text, with a comment showing the change details

### Row Colors

| Color | Meaning |
|-------|---------|
| No color | Row is identical in both files |
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

- Python 3.13+
- openpyxl >= 3.1.2
- click >= 8.1.7

## Releases

Pre-built binaries are automatically created when a version tag is pushed:

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

This triggers a GitHub Actions workflow that:
1. Builds executables for Linux (x86_64) and macOS (ARM64)
2. Creates a GitHub release with the binaries attached
3. Makes them available at: `https://github.com/mumasoft/exceldiff/releases`

## License

MIT
