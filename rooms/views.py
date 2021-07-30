from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from . import models, forms
from django.core.paginator import Paginator


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):  # Class 기반

    """RoomDetail Definition"""

    model = models.Room
    # pk_url_kwarg = "potato" urls.py의 path의 pk 이름을 바꾸면 여기서도 이렇게 바꿔줘야한다


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)  # unbounded form / #bounded form
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                faciliities = form.cleaned_data.get("faciliities")
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in faciliities:
                    filter_args["faciliities"] = facility
                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms},
                )
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


# -------------------------------------------------
# def search(request): # FBV
#     country = request.GET.get("country")

#     if country:
#         form = forms.SearchForm(request.GET)  # unbounded form / #bounded form
#         if form.is_valid():
#             city = form.cleaned_data.get("city")
#             country = form.cleaned_data.get("country")
#             room_type = form.cleaned_data.get("room_type")
#             price = form.cleaned_data.get("price")
#             guests = form.cleaned_data.get("guests")
#             bedrooms = form.cleaned_data.get("bedrooms")
#             beds = form.cleaned_data.get("beds")
#             baths = form.cleaned_data.get("baths")
#             instant_book = form.cleaned_data.get("instant_book")
#             superhost = form.cleaned_data.get("superhost")
#             amenities = form.cleaned_data.get("amenities")
#             faciliities = form.cleaned_data.get("faciliities")
#     else:
#         form = forms.SearchForm()

#     filter_args = {}

#     if city != "Anywhere":
#         filter_args["city__startswith"] = city

#     filter_args["country"] = country

#     if room_type is not None:
#         filter_args["room_type"] = room_type

#     if price is not None:
#         filter_args["price__lte"] = price

#     if guests is not None:
#         filter_args["guests__gte"] = guests

#     if bedrooms is not None:
#         filter_args["bedrooms__gte"] = bedrooms

#     if beds is not None:
#         filter_args["beds__gte"] = beds

#     if baths is not None:
#         filter_args["baths__gte"] = baths

#     if instant_book is True:
#         filter_args["instant_book"] = True

#     if superhost is True:
#         filter_args["host__superhost"] = True

#     rooms = models.Room.objects.filter(**filter_args)

#     for amenity in amenities:
#         filter_args["amenities"] = amenity

#     for facility in faciliities:
#         filter_args["faciliities"] = facility

#     return render(
#         request,
#         "rooms/search.html",
#         {"form": form, "rooms": rooms},
#     )
