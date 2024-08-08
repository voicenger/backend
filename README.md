# Backend
[![voicenger](https://github.com/voicenger/backend/actions/workflows/python-test.yml/badge.svg)](https://github.com/voicenger/backend/blob/main/.github/workflows/python-test.yml) [![Docker Build](https://github.com/voicenger/backend/actions/workflows/docker-build.yml/badge.svg)](https://github.com/voicenger/backend/actions/workflows/docker-build.yml) [![GitHub license](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/voicenger/backend/blob/main/LICENSE)

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
docker compose -f "docker-compose.dev.yml" up --build

docker compose -f "docker-compose.dev.yml" down
```
