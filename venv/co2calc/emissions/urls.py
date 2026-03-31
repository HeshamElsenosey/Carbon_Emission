from django.urls import path
from . import views
from .views import EmissionListCreateView,EmissionDashboardView

urlpatterns = [
    path('calculate/', EmissionListCreateView.as_view(), name='calculate-emissions'),
    path('dashboard/', EmissionDashboardView.as_view(), name='emission-dashboard'),
    path('report-data/', views.EmissionReportDataView.as_view(), name='report-data'),
]