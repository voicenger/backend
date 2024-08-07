# Project Setup Guide (Backend)

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

## 5. Start the Development Server

```
python manage.py runserver
```
Your project should now be up and running on http://127.0.0.1:8000.

# Backend

All documentation is in the "docs" directory and online at [voicenger.docs](https://voicenger.github.io/backend/).

Docs folders, install mdbook

```
brew install mdbook
```


```dosc
.
├── SUMMARY.md
├── aws.md
├── chapter_1.md
├── django.md
└── docker.md

1 directory, 5 files
```

```
cd /docs 
```

Run *mdbook serve*
```
mdbook serve       
2024-08-06 15:03:08 [INFO] (mdbook::book): Book building has started
2024-08-06 15:03:08 [INFO] (mdbook::book): Running the html backend
2024-08-06 15:03:08 [INFO] (mdbook::cmd::serve): Serving on: http://localhost:3000
2024-08-06 15:03:08 [INFO] (mdbook::cmd::watch::poller): Watching for changes...
2024-08-06 15:03:08 [INFO] (warp::server): Server::run; addr=[::1]:3000
2024-08-06 15:03:08 [INFO] (warp::server): listening on http://[::1]:3000
```

Linux

1. Install Docker Linux all
```docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

1. docker-compose
```docker
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)"  -o /usr/local/bin/docker-compose
sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
docker compose version
```
Mac

1. Docker
```docker
brew install docker

brew install docker-compose
```


# Development
 
1. Create .env.dev
```shell
 cp .env.dev.example .env.dev
```

2. Docker-compose up/down
```docker
docker compose -f "docker-compose.dev.yaml" up --build

docker compose -f "docker-compose.dev.yaml" down
```

# Production
 
1. Create .env.prod
```shell
 cp .env.dev.example .env.prod
```

2. Docker-compose up/down
```docker
docker compose -f "docker-compose.yaml" up --build

docker compose -f "docker-compose.yaml" down
```

#   t e s t _ b a c k e n d 
 
 #   t e s t _ b a c k e n d 
 
 #   t e s t _ b a c k e n d 
 
 