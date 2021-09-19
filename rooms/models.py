from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from django.urls import reverse
from cal import Calendar
from django.utils import timezone


class AbstarctItem(core_models.TimeStampedModel):
    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstarctItem):
    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstarctItem):
    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstarctItem):
    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstarctItem):
    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(null=True, blank=True, max_length=140)
    description = models.TextField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=80)
    price = models.IntegerField(null=True, blank=True)
    address = models.CharField(null=True, blank=True, max_length=140)
    guests = models.IntegerField(
        null=True, blank=True, help_text="How many people will be staying?"
    )
    beds = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    baths = models.IntegerField(null=True, blank=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User",
        related_name="rooms",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = (
            self.city.title()
        )  # (<- 도시 이름이 두 단어가 있을 수 있으으로) #str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        next_year = this_year + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(
            this_year if this_month != 12 else next_year, next_month
        )
        return [this_month_cal, next_month_cal]
