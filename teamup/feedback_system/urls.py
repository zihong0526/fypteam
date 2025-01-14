from django.urls import path
from .views import leave_feedback, view_feedback

urlpatterns = [
    path('leave-feedback/<int:receiver_profile_id>/', leave_feedback, name='leave-feedback'),
    path('view-feedback/<int:receiver_profile_id>/', view_feedback, name='view-feedback'),
]
