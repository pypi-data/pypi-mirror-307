from typing import List, Dict, Optional

class CustomDBQuery:
    def __init__(
        self,
        name: str,
        schedule: str,
        value: str,
        value_columns: Optional[str] = None,
        dimension_columns: Optional[str] = None,
        extra_dimensions: Optional[str] = None
    ) -> None:
        self.name = f"{name}"
        self.schedule = schedule if schedule else "* * * * *"
        self.value = value.replace("\n", " ")
        self.value_columns = value_columns.split(",") if value_columns else []
        self.dimension_columns = dimension_columns.split(",") if dimension_columns else []
        self.extra_dimensions = extra_dimensions.split(",") if extra_dimensions else []
