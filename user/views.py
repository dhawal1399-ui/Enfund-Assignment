import os
import io
import tempfile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from .drive import upload_file  # Assuming this is your upload logic.
from .models import *
from allauth.socialaccount.models import SocialAccount
import os
from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from django.shortcuts import render, redirect
from google_auth_oauthlib.flow import InstalledAppFlow

import logging
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialApp
from django.http import JsonResponse

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.http import JsonResponse


logger = logging.getLogger(__name__)


def debug_google_redirect_uri(request):
    try:
        google_app = SocialApp.objects.get(provider="google")
        redirect_uris = google_app.redirect_uris
        logger.debug(f"Google Redirect URIs: {redirect_uris}")
        return redirect("account_login")
    except SocialApp.DoesNotExist:
        logger.error("Google SocialApp not found in the database.")
        return redirect("account_login")


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def loginSuccessfull(request):
    return render(request, 'loginSuccesfull.html')

def callback(request):
    return render(request, 'callback.html')

def authcallback(request):
    return render(request, 'auth_callback.html')

def welcome(request):
    google_data = {}

    if request.user.is_authenticated:
        try:
            # Try to retrieve the SocialAccount for the authenticated user
            print("Request User:", request.user)  # Debugging
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            
            # Retrieve Google data (email, name, profile picture)
            google_data = {
                'email': social_account.extra_data.get('email'),
                'name': social_account.extra_data.get('name'),
                'profile_picture': social_account.extra_data.get('picture'),
            }
        except SocialAccount.DoesNotExist:
            # Handle case where user doesn't have a linked Google account
            google_data = {'error': 'No Google account linked'}

    return render(request, 'welcome.html', context={'google_data': google_data})

def login(request):
    return render(request, 'login.html')

def upload(request):
    return render(request, "upload.html")

def files(request):
    pass

def download(request):
    pass

def chatingPage(request):
    recipient = ""
    user_a = User.objects.get(username="dhawal")
    user_db = User.objects.get(username="rahul")

    if request.user == user_a:
        recipient = "rahul"
    elif request.user == user_db:
        recipient = "dhawal"
    
    messages = ChatMessage.objects.filter(
        sender__username__in=[request.user.username, recipient],
        recipient__username__in=[request.user.username, recipient]
    ).order_by('timestamp')

    return render(request, "chat.html", {
        "user_a": user_a,
        "user_db": user_db,
        "recipient": recipient,
        "messages": messages,
    })

def logoutPage(request):
    logout(request)
    return redirect("welcome")

def upload_to_drive(request):
    print('auth:', request.user.is_authenticated)
    if request.method == "POST" and 'file' in request.FILES:
        file = request.FILES['file']
        
        temp_dir = tempfile.mkdtemp()  
        file_path = os.path.join(temp_dir, file.name)

        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        mime_type = file.content_type

        try:
            folder_id = '15mSKfKaH7gcIAjWxMBw_DSfvG_1M78C0'  
            file_id = upload_file(file_path, mime_type, folder_id)
            os.remove(file_path)  

            return redirect("files_from_drive")
        except Exception as e:
            return HttpResponse(f"Error during upload: {str(e)}", status=500)

    return render(request, 'upload.html')

# from allauth.socialaccount.models import SocialAccount
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
# from django.shortcuts import render, redirect

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from django.shortcuts import render, redirect
import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'user/config', 'google_credentials.json')

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google():
    """ Authenticate using a Service Account """
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    return creds

def fetch_from_google_drive(request):
    """ Fetch files from Google Drive using Service Account """
    creds = authenticate_google()
    service = build('drive', 'v3', credentials=creds)

    # Fetch files from Google Drive
    results = service.files().list(
        pageSize=10, fields="files(id, name)"
    ).execute()
    items = results.get('files', [])

    # If no files found
    if not items:
        return render(request, 'fetch_from_drive.html', {"message": "No files found."}, status=404)

    # Prepare response data
    file_list = [{"id": item["id"], "name": item["name"]} for item in items]

    return render(request,'fetch_from_drive.html',{"files": file_list})

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from django.http import HttpResponse, JsonResponse

def download_file_from_google_drive(request, file_id):
    """Download a file from Google Drive and return it as an HTTP response."""
    try:
        # Authenticate and build the Drive service
        creds = authenticate_google()
        drive_service = build('drive', 'v3', credentials=creds)

        # Fetch file metadata
        file = drive_service.files().get(fileId=file_id).execute()
        file_name = file.get('name', 'downloaded_file')

        # Download the file content
        request_file = drive_service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request_file)
        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Prepare the response
        file_stream.seek(0)
        response = HttpResponse(file_stream.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        return response

    except Exception as error:
        return JsonResponse({"error": str(error)}, status=500)
       