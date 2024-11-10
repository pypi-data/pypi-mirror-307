# dj
from django.urls import path

# internal
from . import views


urlpatterns = [
    path("<int:report_pk>", views.RenderReportView.as_view(), name="render_report")
]
