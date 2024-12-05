from django.urls import path
from report import views
app_name = "report"

urlpatterns = [
    path("users/",views.UserReportView.as_view(),name="users"),
    # path("posts/",views.PostPdfFileView.as_view(),name="post-pdf-view"),
]

#127.0.0.1:8080/api/v1/posts/ => post-list => {% url 'report:post-list' %}
#127.0.0.1:8080/posts/ => post-list => {% url 'post-list' %}