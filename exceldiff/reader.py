"""File reader interface and implementations."""

from abc import ABC, abstractmethod
from typing import List, Any, Optional


class FileReader(ABC):
    """Abstract base class for file readers."""

    @abstractmethod
    def read(self, file_path: str, sheet_name: Optional[str] = None) -> List[List[Any]]:
        """
        Read a worksheet from a file.

        Args:
            file_path: Path to the file
            sheet_name: Name of the sheet to read (None for first sheet)

        Returns:
            List of rows, where each row is a list of cell values
        """
        pass

    @abstractmethod
    def get_sheet_names(self, file_path: str) -> List[str]:
        """
        Get list of sheet names in the file.

        Args:
            file_path: Path to the file

        Returns:
            List of sheet names
        """
        pass

    @abstractmethod
    def supports(self, file_path: str) -> bool:
        """
        Check if this reader supports the given file.

        Args:
            file_path: Path to the file

        Returns:
            True if the reader can handle this file
        """
        pass
