from django.urls import path

from . import views


app_name = "hostels"

urlpatterns = [
    path("", views.home, name="home"),
    path("hostels/<slug:hostel_slug>/", views.hostel_detail, name="hostel_detail"),
    path(
        "hostels/<slug:hostel_slug>/rooms/<slug:room_slug>/",
        views.room_detail,
        name="room_detail",
    ),
]
