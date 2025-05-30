from django.urls import path
from . import views
from utils.constants import LIST_CREATE, REVIEW_UPDATE_DESTROY

urlpatterns = [
    path('', views.PostViewSet.as_view(LIST_CREATE)),
    path('<int:id>/', views.PostViewSet.as_view(REVIEW_UPDATE_DESTROY)),
    path('<int:id>/comments/', views.CommentAPIViewSet.as_view()),

]