from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import ListView, DetailView, View, FormView
from . import models, forms
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView
from users import mixins as user_mixins
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 12
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


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.get(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = "Photo Updated"

    def get_success_url(self) -> str:
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = (
        "caption",
        "file",
    )
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))
