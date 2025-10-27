from django.urls import path
from .views import (
    PartListView,
    PartDetailView,
    PartCreateView,
    PartUpdateView,
    PartDeleteView,
    ImportCSVView,
    ImportTaskListView,
)

urlpatterns = [
    path("parts/", PartListView.as_view(), name="part-list"),
    path("parts/<int:pk>/", PartDetailView.as_view(), name="part-detail"),
    path("parts/create/", PartCreateView.as_view(), name="part-create"),
    path("parts/<int:pk>/update/", PartUpdateView.as_view(), name="part-update"),
    path("parts/<int:pk>/delete/", PartDeleteView.as_view(), name="part-delete"),
    path("import-csv/", ImportCSVView.as_view(), name="import-csv"),
    path("import-tasks/", ImportTaskListView.as_view(), name="import-task-list"),
]
