from django import template
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

register = template.Library()

@register.filter
def is_past_date(date):
    print("is_past_date", date.date(), 'now: ', datetime.now().date())
    return date.date() < timezone.now().date()

@register.filter
def is_future_date(date):
    print("is_future_date", date.date(), 'now: ', datetime.now().date())
    return date.date() > timezone.now().date()

@register.filter
def is_today(date):
    print("is_today_date", date.date(), 'now: ', datetime.now().date())
    return date.date() == timezone.now().date()

@register.filter
def add_minutes(start_time, duration):
    """Adds duration (in minutes) to the start_time. Handles 24-hour format."""
    try:
        now = timezone.now()
        start_datetime = datetime.combine(now.date(), start_time, tzinfo=pytz.utc)
        end_datetime = start_datetime + timedelta(minutes=duration)
        return end_datetime.time()
    except ValueError:
        return None

@register.filter
def is_future_time(date, time):
    """Checks if the given date and time are in the future."""
    try:
        # Combine the date and time with the Asia/Kolkata timezone
        kolkata_timezone = pytz.timezone('Asia/Kolkata')
        exam_datetime = datetime.combine(date, time)
        exam_datetime = kolkata_timezone.localize(exam_datetime)

        # Convert the time to UTC
        utc_time = exam_datetime.astimezone(pytz.utc)

        # Get the current time in UTC
        now = datetime.now(pytz.utc)

        print(f"FUTURE: date: {date}; time: {time}; examdatetime: {utc_time}; current_datetime: {now}; >> {utc_time > now}")
        return utc_time > now
    except Exception as e:
        print('FUTURE_TIME', e)
        return False

@register.filter
def is_past_time(date, time):
    """Checks if the given date and time are in the past."""
    try:
        # Combine the date and time with the Asia/Kolkata timezone
        kolkata_timezone = pytz.timezone('Asia/Kolkata')
        exam_datetime = datetime.combine(date, time)
        exam_datetime = kolkata_timezone.localize(exam_datetime)

        # Convert the time to UTC
        utc_time = exam_datetime.astimezone(pytz.utc)

        # Get the current time in UTC
        now = datetime.now(pytz.utc)

        print(f"PAST: date: {date}; time: {time}; examdatetime: {utc_time}; current_datetime: {now}; >> {utc_time < now}")
        return utc_time.time() < now.time()
    except Exception as e:
        print('PAST_TIME', e)
        return False
