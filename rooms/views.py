from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from . import models
from django_countries import countries
from django.http import Http404

#  ------------------------------------------------------------------
# from typing import Generic


# from django.utils import timezone
# import rooms
# from math import ceil
# from django.core.paginator import EmptyPage, Paginator


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# ------------------------------------------------------------------------

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     now = timezone.now() - get_context 알기 위한 함수
#     context["now"] = now
#     return context


class RoomDetail(DetailView):  # Class 기반

    """RoomDetail Definition"""

    model = models.Room
    # pk_url_kwarg = "potato" urls.py의 path의 pk 이름을 바꾸면 여기서도 이렇게 바꿔줘야한다


def search(request):  # 수동으로 한 form 만들기
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", "0"))
    room_types = models.RoomType.objects.all()
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    selected_amenities = request.GET.getlist("amenities")
    selected_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "selected_room_type": room_type,
        "selected_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "selected_amenities": selected_amenities,
        "selected_facilities": selected_facilities,
        "instant": instant,
        "superhost": superhost,
    }
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type  # room_type  = foreign key

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    rooms = models.Room.objects.filter(**filter_args)

    if len(selected_amenities) > 0:
        for s_amenity in selected_amenities:
            rooms = rooms.filter(amenities__pk=int(s_amenity))

    if len(selected_facilities) > 0:
        for s_facility in selected_facilities:
            rooms = rooms.filter(facilities__pk=int(s_facility))

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms},
    )


# ------------------------------------------------------------------------


def room_detail(request, pk):  # Function 기반
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()


# --------------------------------------------------------------------------

# def all_rooms(request):               #paginator 이용
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:
#         return redirect("/")

# ------------------------------------------------------------------------

# page = request.GET.get("page", 1)  paginator 원리
#     page = int(page or 1)
#     page_size = 10
#     limit = page_size * page
#     offset = limit - page_size
#     all_rooms = models.Room.objects.all()[offset:limit]
#     page_count = ceil(models.Room.objects.count() / page_size)
#     return render(
#         request,
#         "rooms/home.html",
#         context={
#             "rooms": all_rooms,
#             "page": page,
#             "page_count": page_count,
#             "page_range": range(1, page_count + 1),
#         }
#     )
# 템플릿 이름(template폴더에 있는 html)/ extension 이름은 같아야 한다"""
# view 이름은 url.py의 이름이랑 같아야한다 """
# context와 템플릿 이름은 같아야한다."""
