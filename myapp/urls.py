from django.urls import path
from . import views

app_name = 'myapp'  # this namespace will help to let django link view-app properly
urlpatterns = [
    # /myapp/
    path('', views.IndexView.as_view(), name="index"),
    # /myapp/6
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    # /myapp/6/results
    path('<int:pk>/results/', views.ResultsView.as_view(), name="results"),
    # /myapp/6/vote
    path('<int:question_id>/vote/', views.vote, name="vote"), ]
