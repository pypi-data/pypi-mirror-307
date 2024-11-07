from datetime import datetime


def get_current_datetime(**kwargs) -> str:
    """
        What does this function do: Tell current date and time in a formatted string.

        When to use this function: Use this function when you need to know current date and time.

        Args:
            None

        Returns:
            str: A string representing the current date and time in the format "Month abbreviation/day of month/year hour:minute:second AM/PM".
    """
    now = datetime.now()
    month_abbr = now.strftime("%b")
    current_datetime_abbr = f"{month_abbr}/{now.day:02d}/{now.year:04d} {now.hour:02d}:{now.minute:02d}:{now.second:02d} {now.strftime('%p')}"
    return current_datetime_abbr
