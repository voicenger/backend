# Env

```python
python3 -m venv env
source env/bin/activate
```

# Install all libs
```
pip install -r requirements.txt
```

# Run server and create migrates to db
```python
python manage.py runserver

python manage.py migrate
```

# Create SuperUser
```python
python manage.py createsuperuser

```

# Sync all libs to file requirements.txt
```python
pip freeze > requirements.txt
```
