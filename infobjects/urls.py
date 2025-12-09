from django.urls import path
from . import views

app_name = "infobjects"

urlpatterns = [
    # More specific pattern for editing category first
    path(
        "categories/<int:category_pk>/edit/",
        views.CategoryUpdatePage().as_view(),
        name="category_edit",
    ),
    # Then, the pattern for viewing category details
    path(
        "categories/<int:category_pk>/",
        views.CategoryCRUDPage().as_view(),
        name="category_detail",
    ),
    path(
        "categories/<int:category_pk>/delete/",
        views.CategoryCRUDPage().as_view(),
        name="category_delete",
    ),
    # Generic pattern for category list
    path("categories/", views.CategoryCRUDPage().as_view(), name="category_list"),
    # notes
    path("notes/", views.NoteListView.as_view(), name="note_list"),
    path("notes/add/", views.NoteEditView.as_view(), name="note_add"),
    path("notes/<int:pk>/edit/", views.NoteEditView.as_view(), name="note_edit"),
    path("note/<int:pk>/delete/", views.NoteDeleteView.as_view(), name="note_delete"),
    path("notes/<int:pk>/", views.NoteDetailView.as_view(), name="note_detail"),
]
