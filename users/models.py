from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateField



class User(AbstractUser):
    """ Custom User Model"""

    GENDER_MALE= "male"
    GENDER_FEMALE= "female"
    GENDER_OTHER= "other"

    GENDER_CHOICES= {
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),

    }

    LANGUAGE_ENGLISH = "english"
    LANGUAGE_KOREAN = "korean"
    LANGUAGE_CHOICES= {
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    }

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_CHOICES= {
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    }

    avatar = models.ImageField(upload_to ="avatars", blank = True)
    gender = models.CharField(choices =GENDER_CHOICES, max_length=10, blank = True) #single line
    #choices같은 form의 변화는 migrate 불필요
    bio = models.TextField(blank = True)
    birthday = models.DateField(null=True,blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES,max_length=6,blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES,max_length=3,blank=True)
    superhost = models.BooleanField(default=False)

