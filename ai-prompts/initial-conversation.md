# ExcelDiff Tool - Complete Development Conversation

**Date**: October 16, 2025
**Project**: ExcelDiff - Excel Worksheet Comparison Tool
**Developer**: Claude (Sonnet 4.5)

---

## Initial Request

**User**: I want you to build a tool to make a diff between 2 excel worksheets (one sheet only per file). Specifications:
1. which language/framework to use is entirely up to you
2. it should be possible to specify the worksheet to use within the excel files. Defaults to the first sheet within the file
3. when a row is completely the same, don't color it
4. when a row differs, mark the cells with different values red
5. when a row is absent in the second file, mark it as yellow
6. when a row in the second file is not in the first file, mark it as orange
7. output to a new file
8. Only accept xlsx files
9. do it in a way which allows for extensibility so that other file formats can be added later on as well

---

## Technology Stack Decision

**Chosen Stack:**
- **Python 3.8+** - Widely used, excellent library support
- **openpyxl** - For reading/writing Excel files with formatting
- **Click** - For CLI interface

**Architecture Design:**
- Strategy pattern for file readers (extensibility for CSV, ODS, etc.)
- Separate concerns: Reader → Differ → Writer
- Clean interfaces for extensibility

**Project Structure:**
```
exceldiff/
├── reader.py         # Abstract FileReader interface
├── excel_reader.py   # Excel implementation of FileReader
├── differ.py         # Core diff engine (format-agnostic)
├── writer.py         # Excel output with formatting
└── cli.py            # Command-line interface
```

---

## Implementation Phase

### 1. Base Infrastructure
- Created virtual environment
- Set up `requirements.txt` and `setup.py`
- Implemented `FileReader` abstract base class with:
  - `read()` method
  - `get_sheet_names()` method
  - `supports()` method

### 2. Excel Reader Implementation
- Used openpyxl's `load_workbook()` with `data_only=True`
- Implemented sheet name validation
- Added default to first sheet

### 3. Diff Engine Implementation
Created `WorksheetDiffer` class with:
- Row normalization to handle different column counts
- Row-to-key hashing for comparison
- Modified row detection (50% match threshold)
- `RowDiff` class to store:
  - Row index
  - Diff type (IDENTICAL, MODIFIED, REMOVED, ADDED)
  - Row data
  - Modified cell indices

### 4. Excel Writer with Formatting
Initial implementation:
- IDENTICAL rows: No coloring
- MODIFIED rows: Red cells for changed values
- REMOVED rows: Yellow background
- ADDED rows: Orange background

---

## Feature Additions

### Feature 1: Diff-Only Mode

**User**: Add an option to only output rows if there's actually a difference

**Implementation:**
- Added `--diff-only` flag to CLI
- Updated writer to filter out identical rows
- Updated stats display to show row count

### Feature 2: Header Row Support

**User**: When using diff-only, also make it so that unless a command line argument is given, the header row from the first file is also added to the diff output

**Implementation:**
- Added `--no-header` flag to CLI
- By default with `--diff-only`, first row is included as header
- Header row written without coloring
- Row count adjusts for header inclusion

---

## Rich Text Formatting Enhancement

### Initial Attempt: Rich Text in Cells

**User**: When a cell value differs, i'd like to have the original value in the output cell: the original value should be darkish yellow stricken through, the new value should stay red. Add a space between the values

**Implementation:**
- Updated `RowDiff` to store `original_row_data`
- Used openpyxl's `CellRichText`, `TextBlock`, and `InlineFont`
- Created rich text with:
  - Old value: dark yellow (#999900) with strikethrough
  - New value: red (#FF0000)
  - Space separator

### Problem: Excel Corruption

**User**: Apparently there's something wrong with the output file as excel doesn't dig it. This is the recovery log:
```xml
<repairedRecord>Repaired Records: String properties from /xl/worksheets/sheet1.xml part</repairedRecord>
```

**Root Cause:** openpyxl's `CellRichText` implementation wasn't fully compatible with Excel's expectations.

### Solution: Simplified Approach

**Implementation:**
- Removed rich text formatting
- Used plain text with arrow separator: `old_value → new_value`
- Applied red font color to entire cell
- Added cell comments with detailed change info: "Changed from: [old]\nTo: [new]"

**Benefits:**
- Fully Excel-compatible
- Clear visual indication
- Hover-over comments provide context
- Simpler, more reliable implementation

---

## Standalone Executable Creation

**User**: So we have this venv now, but it would be nice if I'd have a redistributable (binary?) so that I don't need to create a venv everywhere I use it on or install the necessary dependencies. Can you make it happen?

**Implementation:**
1. Installed PyInstaller
2. Created `exceldiff.spec` configuration:
   - Single-file executable
   - Console application
   - Hidden imports for openpyxl and click
   - UPX compression enabled
3. Built 11MB standalone executable
4. Tested successfully - no dependencies needed!

**Result:** `dist/exceldiff` - fully portable, includes Python + all libraries

---

## GitHub Actions for Automated Releases

**User**: Can you create github actions to build binaries for macos and linux when a semver tag is pushed?

**Implementation:**

Created `.github/workflows/release.yml`:

**Workflow Features:**
- Triggers on semver tags (v*.*.*)
- Matrix build strategy for:
  - Ubuntu (Linux x86_64)
  - macOS (ARM64 - M1/M2/M3)
- Parallel builds for speed
- Automatic GitHub release creation
- Binary artifacts attached to release
- Professional release notes with usage instructions

**Usage:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

**Output:**
- `exceldiff-linux` - Linux x86_64 binary
- `exceldiff-macos` - macOS ARM64 binary
- GitHub Release at: https://github.com/mumasoft/exceldiff/releases

---

## Final Project Structure

```
exceldiff/
├── .github/
│   └── workflows/
│       └── release.yml           # Automated release builds
├── exceldiff/
│   ├── __init__.py
│   ├── cli.py                    # Click-based CLI
│   ├── differ.py                 # Diff engine with RowDiff class
│   ├── excel_reader.py           # Excel file reader
│   ├── reader.py                 # Abstract FileReader interface
│   └── writer.py                 # Excel writer with formatting
├── ai-prompts/
│   └── conversation-history.md   # This file
├── .gitignore
├── exceldiff.spec                # PyInstaller configuration
├── README.md                     # User documentation
├── requirements.txt              # Python dependencies
└── setup.py                      # Package setup
```

---

## Key Features Delivered

### Core Functionality
✅ Compare two Excel worksheets
✅ Color-coded diff output:
  - Modified cells: Red text with "old → new" format
  - Removed rows: Yellow background
  - Added rows: Orange background
✅ Cell comments showing change details
✅ Support for specifying sheets (defaults to first)
✅ Output to new Excel file
✅ Only accepts .xlsx files

### Enhanced Features
✅ `--diff-only` flag to show only changed rows
✅ `--no-header` flag to exclude header when using diff-only
✅ Automatic header row inclusion by default with diff-only
✅ Extensible architecture for adding new file formats

### Distribution
✅ Standalone executables (no Python/dependencies needed)
✅ Automated builds for Linux and macOS
✅ GitHub Actions for release automation
✅ Professional README with installation instructions

---

## CLI Usage Examples

### Basic comparison
```bash
exceldiff file1.xlsx file2.xlsx
```

### Specify output file
```bash
exceldiff file1.xlsx file2.xlsx -o result.xlsx
```

### Compare specific sheets
```bash
exceldiff file1.xlsx file2.xlsx --sheet1 "Sheet1" --sheet2 "Sheet1"
```

### Show only differences
```bash
exceldiff file1.xlsx file2.xlsx --diff-only
```

### Full example
```bash
exceldiff baseline.xlsx updated.xlsx \
  --output comparison.xlsx \
  --sheet1 "Q1 Data" \
  --sheet2 "Q1 Data" \
  --diff-only
```

---

## Technical Decisions & Rationale

### 1. Python + openpyxl
- **Why**: Mature library with excellent Excel support
- **Benefits**: Handles complex formatting, widely used, well-documented

### 2. Strategy Pattern for Readers
- **Why**: Easy to add new file formats (CSV, ODS, etc.)
- **Benefits**: Clean separation, testable, extensible

### 3. Plain Text vs Rich Text
- **Initial**: Rich text with strikethrough
- **Problem**: Excel compatibility issues
- **Solution**: Plain text with arrows + comments
- **Benefits**: Universal compatibility, cleaner code

### 4. PyInstaller for Distribution
- **Why**: Single-file executable, cross-platform
- **Benefits**: No installation, portable, user-friendly

### 5. GitHub Actions for CI/CD
- **Why**: Automated, consistent builds
- **Benefits**: Multi-platform support, versioned releases

---

## Lessons Learned

1. **Excel Compatibility**: openpyxl's advanced features (like CellRichText) may not be fully Excel-compatible. Always test with actual Excel.

2. **User Experience**: Standalone executables greatly improve user experience - no dependencies, no setup required.

3. **Extensibility**: Designing with interfaces/abstract classes from the start makes future enhancements easier.

4. **Automation**: GitHub Actions eliminate manual build processes and ensure consistent releases.

5. **Iterative Development**: Starting with core features and adding enhancements based on feedback led to a better end result.

---

## Future Enhancement Ideas

1. **Windows Support**: Add Windows executable to GitHub Actions
2. **CSV/TSV Support**: Implement CSV reader using the FileReader interface
3. **Configuration File**: Support for .exceldiffrc to set defaults
4. **Color Customization**: Allow users to configure colors
5. **Web UI**: Optional web interface for non-technical users
6. **Diff Statistics**: More detailed statistics about changes
7. **Side-by-side View**: Generate two-column comparison view
8. **Large File Support**: Streaming for very large files

---

## Dependencies

**Runtime:**
- openpyxl >= 3.1.2
- click >= 8.1.7

**Development:**
- pyinstaller (for building executables)

**Python Version:** 3.8+

---

## Project Outcome

Successfully created a professional, production-ready Excel diff tool with:
- Clean, extensible architecture
- User-friendly CLI
- Standalone executables for easy distribution
- Automated release process
- Professional documentation

The tool is ready for use and can be easily extended to support additional file formats or features.
