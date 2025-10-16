"""Excel writer with color formatting for diffs."""

from typing import List
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from exceldiff.differ import RowDiff, DiffType


class ExcelDiffWriter:
    """Writer for creating Excel files with diff highlighting."""

    # Color codes for different diff types
    COLOR_MODIFIED = "FF0000"  # Red for modified cells
    COLOR_REMOVED = "FFFF00"   # Yellow for removed rows
    COLOR_ADDED = "FFA500"     # Orange for added rows

    def write(self, diffs: List[RowDiff], output_path: str) -> None:
        """
        Write diff results to an Excel file with color highlighting.

        Args:
            diffs: List of RowDiff objects
            output_path: Path to write the output file

        Color scheme:
        - Identical rows: No coloring
        - Modified rows: Red cells for changed values
        - Removed rows: Yellow background for entire row
        - Added rows: Orange background for entire row
        """
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Diff"

        # Write all rows with appropriate formatting
        for diff in diffs:
            row_num = diff.row_index + 1  # Excel rows are 1-indexed

            # Write row data
            for col_idx, value in enumerate(diff.row_data, start=1):
                cell = worksheet.cell(row=row_num, column=col_idx, value=value)

                # Apply formatting based on diff type
                if diff.diff_type == DiffType.IDENTICAL:
                    # No coloring for identical rows
                    pass

                elif diff.diff_type == DiffType.MODIFIED:
                    # Color only the modified cells red
                    if col_idx - 1 in diff.modified_cells:
                        cell.fill = PatternFill(
                            start_color=self.COLOR_MODIFIED,
                            end_color=self.COLOR_MODIFIED,
                            fill_type="solid"
                        )

                elif diff.diff_type == DiffType.REMOVED:
                    # Color entire row yellow
                    cell.fill = PatternFill(
                        start_color=self.COLOR_REMOVED,
                        end_color=self.COLOR_REMOVED,
                        fill_type="solid"
                    )

                elif diff.diff_type == DiffType.ADDED:
                    # Color entire row orange
                    cell.fill = PatternFill(
                        start_color=self.COLOR_ADDED,
                        end_color=self.COLOR_ADDED,
                        fill_type="solid"
                    )

        # Auto-adjust column widths for better readability
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

        # Save the workbook
        workbook.save(output_path)
