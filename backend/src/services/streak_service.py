from datetime import date, timedelta
from typing import List
from src.models.habit import Completion

def calculate_streak(completions: List[Completion]) -> int:
    """
    Calculate current streak from a list of completions.
    Assumes completions are for a single habit and sorted by date descending.
    """
    if not completions:
        return 0

    sorted_completions = sorted(completions, key=lambda x: x.date, reverse=True)

    # Filter only successful completions
    completed_dates = {c.date for c in sorted_completions if c.status}
    if not completed_dates:
        return 0

    streak = 0
    today = date.today()
    check_date = today

    # If not completed today, check if completed yesterday to continue streak
    if today not in completed_dates:
        check_date = today - timedelta(days=1)
        if check_date not in completed_dates:
            return 0

    while check_date in completed_dates:
        streak += 1
        check_date -= timedelta(days=1)

    return streak

def calculate_longest_streak(completions: List[Completion]) -> int:
    if not completions:
        return 0

    completed_dates = sorted({c.date for c in completions if c.status})
    if not completed_dates:
        return 0

    max_streak = 0
    current_streak = 0
    prev_date = None

    for d in completed_dates:
        if prev_date is None or d == prev_date + timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1

        max_streak = max(max_streak, current_streak)
        prev_date = d

    return max_streak
