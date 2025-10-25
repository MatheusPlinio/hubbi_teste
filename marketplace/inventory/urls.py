from django.urls import path
from . import views

urlpatterns = [
    path('pecas/', views.PeçaList.as_view(), name='peca_list'),
    path('pecas/<int:pk>/', views.PeçaDetail.as_view(), name='peca_detail'),
    path('pecas/', views.PeçaCreate.as_view(), name='peca_create'),
    path('pecas/<int:pk>/', views.PeçaUpdate.as_view(), name='peca_update'),
    path('pecas/<int:pk>/', views.PeçaDelete.as_view(), name='peca_delete'),
]