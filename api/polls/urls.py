from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path('votes/create/', views.VoteCreateView.as_view(), name='vote-create'),
    path('channel/list/<int:pk>/', views.PollOwnerChatsView.as_view(), name='channel-list'),
    path('<int:pk>/', views.PollDetailView.as_view(), name='poll-detail'),
    path('poll/send/<int:pk>/', views.poll_send, name='poll-send'),
]
