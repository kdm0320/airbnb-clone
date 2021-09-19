from calendar import month
from django import template
from reservations import models as reservation_models

register = template.Library()
import datetime


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation_models.BookedDay.objects.get(
            day=date, reservation__room=room
        )  # __ = foreign key 이용하는 방식
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False
