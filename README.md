# MyAssignment Project

This project is a Django-based web application that allows users to log in using Google, connect with Google Drive to upload and download files, and chat with other users.

## Features

- Google Login
- Upload files to Google Drive
- Download files from Google Drive
- Chat functionality

## Prerequisites

- Python 3.x
- Django
- Google API credentials

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/myAssignment.git
    cd myAssignment
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up Google API credentials:**

    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project or select an existing one.
    - Enable the Google Drive API.
    - Create OAuth 2.0 credentials and download the JSON file.
    - Save the JSON file in the `myAssignment/config` directory as `google_credentials.json`.

5. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following:

    ```env
    GOOGLE_CLIENT_ID=your-google-client-id
    GOOGLE_CLIENT_SECRET=your-google-client-secret
    ```

6. **Run database migrations:**

    ```sh
    python manage.py migrate
    ```

7. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

8. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## Google Login

1. Go to the login page: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
2. Click on the "Login with Google" button.
3. Authorize the application to access your Google account.

## Connect with Google Drive

1. After logging in, go to the upload page: [http://127.0.0.1:8000/upload_to_drive/](http://127.0.0.1:8000/upload_to_drive/)
2. Select a file to upload and click the "Upload" button.
3. The file will be uploaded to your Google Drive.

## Download Files from Google Drive

1. Go to the files page: [http://127.0.0.1:8000/files_from_drive/](http://127.0.0.1:8000/files_from_drive/)
2. You will see a list of files from your Google Drive.
3. Click on the file you want to download.

## Chat Functionality

1. Go to the chat page: [http://127.0.0.1:8000/chatingPage/](http://127.0.0.1:8000/chatingPage/)
2. You can chat with other users in real-time.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.