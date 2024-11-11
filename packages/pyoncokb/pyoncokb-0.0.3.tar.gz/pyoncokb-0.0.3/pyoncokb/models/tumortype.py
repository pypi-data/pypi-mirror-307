"""	TumorType model.

See TumorType model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class MainType:
    """Main tumor type."""

    id: Optional[int]
    name: str
    tumor_form: str

    def __post_init__(self):
        if self.id is not None and not isinstance(self.id, int):
            raise ValueError(f"id {self.id} must be an int")
        if not isinstance(self.name, str):
            raise ValueError(f"name {self.name} must be a str")
        if not isinstance(self.tumor_form, str):
            raise ValueError(f"tumor_form {self.tumor_form} must be a str")


@dataclass
class TumorType:
    """Tumor type."""

    id: int
    code: str
    name: str
    main_type: MainType
    tissue: Optional[str]
    children: Any
    parent: Optional[str]
    level: int
    tumor_form: str

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise ValueError(f"id {self.id} must be an int")
        if not isinstance(self.code, str):
            raise ValueError(f"code {self.code} must be a str")
        if not isinstance(self.name, str):
            raise ValueError(f"name {self.name} must be a str")
        if not isinstance(self.main_type, MainType):
            raise ValueError(f"main_type {self.main_type} must be a MainType instance")
        if self.tissue is not None and not isinstance(self.tissue, str):
            raise ValueError(f"tissue {self.tissue} must be a str")
        if self.parent is not None and not isinstance(self.parent, str):
            raise ValueError(f"parent {self.parent} must be a str")
        if not isinstance(self.level, int):
            raise ValueError(f"level {self.level} must be an int")
        if not isinstance(self.tumor_form, str):
            raise ValueError(f"tumor_form {self.tumor_form} must be a str")

    def format(self) -> str:
        """Format as string.
        
        First try specific name in the name field. If it is empty, try name 
        field of main_type field.

        Raises:
            ValueError: if neither name nor main_type.name is not empty.

        Returns:
            str: tumor type name.
        """
        if self.name:
            return self.name
        elif self.main_type.name:
            return self.main_type.name
        raise ValueError("neither name nor main_type.name is valid")
