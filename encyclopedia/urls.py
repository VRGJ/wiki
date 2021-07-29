from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.show_entry, name="entry"),
    path("error", views.show_entry, name="error"),
    path("search/", views.search, name="search"),
    path("new/", views.new_entry, name="new"),
    path("edit/<title>", views.edit_entry, name="edit"),
    path("random", views.randomize, name="random"),
]
