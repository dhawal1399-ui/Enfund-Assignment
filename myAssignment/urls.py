"""myAssignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from user.views import *
from django.urls import re_path
from user import consumers

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", welcome, name="welcome"),
    path("login/", login, name="login"),
    path("accounts/google/login/callback/", callback, name="callback"),
    path("authcallback", authcallback, name="authcallback"),
    path('upload_to_drive/', upload_to_drive, name='upload_to_drive'),
    path('chatingPage/', chatingPage, name='chatingPage'),
    path('debug_google_redirect_uri/', debug_google_redirect_uri, name='debug_google_redirect_uri'),
    
    path('logout/', logoutPage, name='logout'),
    path('files_from_drive/', fetch_from_google_drive, name='files_from_drive'),
    path('download_from_drive/<str:file_id>/', download_file_from_google_drive, name='download_from_drive'),
    # path("upload/", upload, name="upload"),
    path("files/", files, name="files"),
    path("loginSuccessfull/", loginSuccessfull, name="loginSuccessfull"),
    path("download/", download, name="download"),
    path("chat/", include("user.routing")),



]

# websocket_urlpatterns = [
#     re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
# ]
