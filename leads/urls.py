from django.urls import path
from .views import (
    LeadListCreateView,
    LeadDetailView,
    LeadStatsView,
    LeadAISummaryView,
    LeadWebhookView,
)

urlpatterns = [
    path('', LeadListCreateView.as_view(), name='lead-list-create'),
    path('stats/', LeadStatsView.as_view(), name='lead-stats'),
    path('ai/summary/', LeadAISummaryView.as_view(), name='lead-ai-summary'),
    path('webhook/', LeadWebhookView.as_view(), name='lead-webhook'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
]