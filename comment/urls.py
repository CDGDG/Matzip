from django.urls import path
from comment import views

app_name = "Comment"

urlpatterns = [
    path("comment/list/<int:pk>/<int:page>/", views.commentlist, name='list'),
    path("comment/create/<int:pk>/", views.CommentCreate.as_view(), name='create'),
    path("comment/update/<int:pk>/", views.CommentUpdate.as_view(), name="update"),
    path("comment/delete/<int:pk>/", views.CommentDelete.as_view(), name="delete"),
]
