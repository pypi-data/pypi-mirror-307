"""The is before applicator applies the is before operator to the data."""

from datetime import datetime
from operator import le
from typing import Any, Optional
from zoneinfo import ZoneInfo

from mui.v6.integrations.sqlalchemy.utils import apply_timezone_to_datetime


def apply_on_or_before_operator(
    column: Any, value: Any, timezone: Optional[ZoneInfo]
) -> Any:
    """Handles applying the on or before x-data-grid operator to a column.

    Args:
        column (Any): The column the operator is being applied to, or equivalent
            property, expression, subquery, etc.
        value (Any): The value being filtered.

    Returns:
        Any: The column after applying the on or before filter using the provided value.
    """
    if value is None:
        return column
    # if the column is on or before the received date, it will be less than or equal to
    # the received date.
    parsed = datetime.fromisoformat(value)
    parsed = apply_timezone_to_datetime(dt=parsed, timezone=timezone)
    return le(column, parsed)
