from django.urls import path
from rooms import views as room_views

app_name = "core"
urlpatterns = [
    path("", room_views.HomeView.as_view(), name="home"),
    # path("", room_views.all_rooms, name="home"), pagination/수동
    # path는 오직 함수만 갖는다 = HomeView = 클래스 따라서 .as_view()를 붙여줘야 한다
]
