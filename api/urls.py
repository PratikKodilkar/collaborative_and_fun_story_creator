from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from .views import (
    RegisterView, 
    StoryListCreateView, 
    StoryDetailView, 
    ContributionCreateView,
    GetUser
    )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get_user/', GetUser.as_view(), name='get_user'),

    path('stories/', StoryListCreateView.as_view(), name='story-list-create'),
    path('stories/<int:story_id>/', StoryDetailView.as_view(), name='story-detail'),
    path('stories/<int:story_id>/contribute/', ContributionCreateView.as_view(), name='contribution-create'),
]