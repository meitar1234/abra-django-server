from django.urls import path
from .views import signup, signout, send_message, signinapi,get_messages_for_logged_in_user, get_unread_messages_for_logged_in_user, message

urlpatterns = [
    path('signup/', signup),
    path('signout/', signout),
    path('token/', signinapi),
    path('api/receivers/<str:receiverId>/message/', send_message),
    path('api/messages/', get_messages_for_logged_in_user),
    path('api/messages/unread', get_unread_messages_for_logged_in_user),
    path('api/messages/<str:messageId>/', message)
]
