from django.urls import path
from matzip import views

app_name = "Matzip"

urlpatterns = [
    path("", views.index, name='home'),
    path("matzip/list/", views.MatzipList.as_view(), name="list"),
    path("matzip/create/", views.MatzipCreate.as_view(), name="create"),
    path("matzip/detail/<int:pk>/", views.MatzipDetail.as_view(), name="detail"),
    path("matzip/update/<int:pk>/", views.MatzipUpdate.as_view(), name="update"),
    path("matzip/delete/<int:pk>/", views.MatzipDelete.as_view(), name="delete"),
    path("matzip/near/<str:address>/", views.MatzipNear.as_view(), name='near'),
]
