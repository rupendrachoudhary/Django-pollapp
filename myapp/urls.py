from django.urls import path
from . import views

app_name = 'myapp'  # this namespace will help to let django link view-app properly eg : {% url 'myapp:details' %}
urlpatterns = [
    # Home page

    # index page for poll questions
    path('', views.IndexView.as_view(), name="index"),
    # poll questions with detailed choices
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    # 6/results
    path('<int:pk>/results/', views.ResultsView.as_view(), name="results"),
    # 6/vote
    path('<int:question_id>/vote/', views.vote, name="vote"), ]
