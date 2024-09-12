from django.urls import path

from newspaper import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("post-list/",views.PostListView.as_view(),name="post-list"),
]
