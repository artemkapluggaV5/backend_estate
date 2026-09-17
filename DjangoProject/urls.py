"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet
from properties.views import CategoryViewSet, AmenityViewSet, PropertyViewSet, PropertyImageViewSet, FavoriteViewSet
from property_requests.views import ViewingRequestViewSet, CallRequestViewSet, ContactRequestViewSet
from communications.views import ChatMessageViewSet, ReviewViewSet, NotificationViewSet, GuestChatViewSet, GuestMessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'amenities', AmenityViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'photos', PropertyImageViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'requests', ViewingRequestViewSet, basename='viewingrequest')
router.register(r'call-requests', CallRequestViewSet, basename='callrequest')
router.register(r'contact-requests', ContactRequestViewSet, basename='contactrequest')
router.register(r'chats', ChatMessageViewSet, basename='chatmessage')
router.register(r'reviews', ReviewViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'guest-chats', GuestChatViewSet, basename='guestchat')
router.register(r'guest-messages', GuestMessageViewSet, basename='guestmessage')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
