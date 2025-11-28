from datetime import datetime

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def posted_time(value):
    """Display datetime in a human-friendly Japanese format."""
    if not value or not isinstance(value, datetime):
        return value or ""

    current_tz = timezone.get_current_timezone()
    dt = timezone.localtime(value, current_tz) if timezone.is_aware(value) else timezone.make_aware(value, current_tz)
    now = timezone.localtime(timezone.now(), current_tz)

    delta = now - dt
    seconds = int(delta.total_seconds())

    if seconds < 0:
        if now.year == dt.year:
            return dt.strftime("%m月%d日")
        return dt.strftime("%Y年%m月%d日")

    if seconds < 60:
        return "たった今"
    if seconds < 3600:
        return f"{seconds // 60}分前"
    if seconds < 86400:
        return f"{seconds // 3600}時間前"

    days = delta.days
    if days < 7:
        return f"{days}日前"

    if now.year == dt.year:
        return dt.strftime("%m月%d日")
    return dt.strftime("%Y年%m月%d日")
