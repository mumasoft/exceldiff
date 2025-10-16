"""Diff engine for comparing worksheets."""

from typing import List, Any, Dict, Tuple
from enum import Enum


class DiffType(Enum):
    """Types of differences between rows."""
    IDENTICAL = "identical"
    MODIFIED = "modified"
    REMOVED = "removed"
    ADDED = "added"


class RowDiff:
    """Represents the diff information for a single row."""

    def __init__(self, row_index: int, diff_type: DiffType, row_data: List[Any],
                 modified_cells: List[int] = None, original_row_data: List[Any] = None):
        """
        Initialize a RowDiff.

        Args:
            row_index: Index of the row in the result
            diff_type: Type of difference
            row_data: The actual row data (new values)
            modified_cells: List of column indices that were modified (for MODIFIED type)
            original_row_data: The original row data (old values, for MODIFIED type)
        """
        self.row_index = row_index
        self.diff_type = diff_type
        self.row_data = row_data
        self.modified_cells = modified_cells or []
        self.original_row_data = original_row_data


class WorksheetDiffer:
    """Engine for comparing two worksheets."""

    def compare(self, sheet1: List[List[Any]], sheet2: List[List[Any]]) -> List[RowDiff]:
        """
        Compare two worksheets and generate diff information.

        Args:
            sheet1: First worksheet (baseline)
            sheet2: Second worksheet (comparison)

        Returns:
            List of RowDiff objects describing the differences
        """
        result = []

        # Normalize rows to handle different column counts
        max_cols = max(
            max((len(row) for row in sheet1), default=0),
            max((len(row) for row in sheet2), default=0)
        )

        sheet1_normalized = [self._normalize_row(row, max_cols) for row in sheet1]
        sheet2_normalized = [self._normalize_row(row, max_cols) for row in sheet2]

        # Create mapping of rows for comparison
        sheet1_map = {self._row_to_key(row): idx for idx, row in enumerate(sheet1_normalized)}
        sheet2_map = {self._row_to_key(row): idx for idx, row in enumerate(sheet2_normalized)}

        processed_sheet1 = set()
        processed_sheet2 = set()

        # First pass: find identical and modified rows
        for idx1, row1 in enumerate(sheet1_normalized):
            key1 = self._row_to_key(row1)

            if key1 in sheet2_map:
                # Row exists in both sheets (identical)
                idx2 = sheet2_map[key1]
                result.append(RowDiff(idx1, DiffType.IDENTICAL, row1))
                processed_sheet1.add(idx1)
                processed_sheet2.add(idx2)
            else:
                # Check if this row has a modified version in sheet2
                match_idx, modified_cells = self._find_modified_row(row1, sheet2_normalized, processed_sheet2)

                if match_idx is not None:
                    # Found a modified version
                    result.append(RowDiff(idx1, DiffType.MODIFIED, sheet2_normalized[match_idx], modified_cells, row1))
                    processed_sheet1.add(idx1)
                    processed_sheet2.add(match_idx)
                else:
                    # Row removed in sheet2
                    result.append(RowDiff(idx1, DiffType.REMOVED, row1))
                    processed_sheet1.add(idx1)

        # Second pass: find added rows (in sheet2 but not in sheet1)
        for idx2, row2 in enumerate(sheet2_normalized):
            if idx2 not in processed_sheet2:
                result.append(RowDiff(len(result), DiffType.ADDED, row2))

        return result

    def _normalize_row(self, row: List[Any], target_length: int) -> List[Any]:
        """
        Normalize a row to a target length by padding with None.

        Args:
            row: The row to normalize
            target_length: Desired length

        Returns:
            Normalized row
        """
        if len(row) >= target_length:
            return row[:target_length]
        return row + [None] * (target_length - len(row))

    def _row_to_key(self, row: List[Any]) -> Tuple:
        """
        Convert a row to a hashable key for comparison.

        Args:
            row: The row to convert

        Returns:
            Tuple representation of the row
        """
        return tuple(self._normalize_value(v) for v in row)

    def _normalize_value(self, value: Any) -> Any:
        """
        Normalize a cell value for comparison.

        Args:
            value: The value to normalize

        Returns:
            Normalized value
        """
        if value is None:
            return None
        if isinstance(value, float):
            # Handle floating point comparison
            return round(value, 10)
        return value

    def _find_modified_row(self, target_row: List[Any], sheet: List[List[Any]],
                          processed: set) -> Tuple[int, List[int]]:
        """
        Find a row that matches the target row with some modifications.

        Args:
            target_row: Row to find a match for
            sheet: Sheet to search in
            processed: Set of already processed row indices

        Returns:
            Tuple of (row_index, list of modified cell indices) or (None, None)
        """
        # Simple heuristic: if more than 50% of cells match, consider it a modified row
        best_match = None
        best_score = 0
        best_modified = []

        for idx, row in enumerate(sheet):
            if idx in processed:
                continue

            matches = 0
            modified = []

            for col_idx, (v1, v2) in enumerate(zip(target_row, row)):
                if self._normalize_value(v1) == self._normalize_value(v2):
                    matches += 1
                else:
                    modified.append(col_idx)

            score = matches / len(target_row) if target_row else 0

            # Require at least 50% match to consider it a modification
            if score > best_score and score >= 0.5:
                best_score = score
                best_match = idx
                best_modified = modified

        if best_match is not None:
            return best_match, best_modified

        return None, None
