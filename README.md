# backend

```python
python3 -m venv env
source env/bin/activate
```

# Start python

```python
python manage.py runserver

python manage.py migrate
```

```python
python manage.py createsuperuser

pip install Django
```

```python
pip freeze > requirements.txt
```

```update
...
```
# Start Django
```
curl https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8
or
Create a project directory, in this case I use “django-postgres”

mkdir django-postgres

Point to django-postgres directory

cd django-postgres

django-admin startproject Voicenger

Start Django app
In VisualStudio Code terminal, you’ve to point to the project directory using “cd” command

cd Voicenger
Run the following command to start your first app
python manage.py startapp testdb

Run the server to make sure that everything is okay
python manage.py runserver

pip install django-environ

In the base or root directory, add .gitignore to not push .env file into our Git repo, also the files or directories following:

db.sqlite3 (SQLite database file)
/env (virtual environment folder)
*.env (all of .env files inside our project)
.gitignore

pip install psycopg2

```

# Install DBeaver
```
curl https://dbeaver.io/download/
or
Snap (sudo snap install dbeaver-ce)
Flatpak (flatpak install flathub io.dbeaver.DBeaverCommunity)
```
# Install PostgreSQL
```
curl https://www.postgresql.org/download/
or
Using apt:

Bash
sudo apt update
sudo apt install postgresql postgresql-contrib
Використовуйте цей код обачно.

Starting PostgreSQL:

Bash
sudo systemctl start postgresql
Використовуйте цей код обачно.

Accessing PostgreSQL:

Bash
sudo -i -u postgres
psql
Використовуйте цей код обачно.

Installing PostgreSQL on Linux (CentOS/RHEL)
Using yum:

Bash
sudo yum install postgresql14-server
Використовуйте цей код обачно.

Initializing PostgreSQL:

Bash
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb
Використовуйте цей код обачно.

Starting PostgreSQL:

Bash
sudo systemctl start postgresql-14
sudo systemctl enable postgresql-14
Використовуйте цей код обачно.

Accessing PostgreSQL:

Bash
sudo -i -u postgres
psql
Використовуйте цей код обачно.

Installing PostgreSQL on macOS (using Homebrew)
Bash
brew install postgresql
```
# DockerHub
```
register account 
curl https://hub.docker.com/
```
# AWS
```
register account 
curl https://aws.amazon.com/free/?nc1=h_ls&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all
