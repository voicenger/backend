Follow these steps to set up and run the project on your local machine.

## 1. Set up a Virtual Environment

Create and activate a virtual environment:

```sh
python -m venv venv
venv\Scripts\activate
```
## 2.Create a .env File
Create a .env file in the root directory and add the following configurations:

Create key
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
```
SECRET_KEY=secret.key
ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_BASE_FRONTEND_URL=http://localhost:3000
GOOGLE_OAUTH2_CLIENT_ID=your_google_oauth2_client_id
GOOGLE_OAUTH2_CLIENT_SECRET=your_google_oauth2_client_secret
```

## 3. Install Dependencies
Install all required packages from the requirements.txt file:

```
pip install -r requirements.txt
```

## 4. Apply Database Migrations
Run the following command to apply database migrations:

```
python manage.py migrate
```

```
python manage.py runserver
```
Your project should now be up and running on http://127.0.0.1:8000.
