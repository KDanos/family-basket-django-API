# Django REST Framework Class Guide

This guide will walk you through setting up a Django project using Django REST Framework (DRF), creating a custom user model, connecting a database, and creating your first API endpoint.

---

## 1. Create a Project Folder and Open in VSCode

Create a folder for your project and open it in VSCode:

```bash
mkdir ~/code/ga/labs/my_django_project
code ~/code/ga/labs/my_django_project
```

---

## 2. Install Django and Other Packages Using Pipenv

Open the integrated terminal in VSCode and run:

```bash
pipenv install django djangorestframework psycopg2-binary pylint django-environ
```

**Explanation:**  
- `django` – The main Django framework.  
- `djangorestframework` – Adds REST API functionality.  
- `psycopg2-binary` – PostgreSQL database adapter.  
- `pylint` – Code linter.  
- `django-environ` – Manage environment variables.  

[Pipenv Documentation](https://pipenv.pypa.io/en/latest/)  
[Django REST Framework Docs](https://www.django-rest-framework.org/)

---

## 3. Enter the Pipenv Shell

```bash
pipenv shell
```

**Explanation:**  
Activates the virtual environment created by Pipenv so that installed packages are available.

---

## 4. Start the Django Project

```bash
django-admin startproject project .
```

**Explanation:**  
- `startproject project` creates a new project named `project`.  
- The `.` ensures files are created in the current folder.  

[Django Startproject Docs](https://docs.djangoproject.com/en/stable/intro/tutorial01/#creating-a-project)

---

## 5. Create a User App and Custom User Model

1. Create a user app:

```bash
python manage.py startapp users
```

2. Add `users` to `INSTALLED_APPS` in `project/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'users',
    'rest_framework',
]
```

3. Create a custom user model in `users/models.py`:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
```

4. Update `settings.py`:

```python
AUTH_USER_MODEL = 'users.User'
```

**Explanation:**  
We must define a custom user model **before running migrations** to avoid conflicts with the default user model.  

[Django Custom User Docs](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model)

---

## 6. Create a New Database on Neon.com

1. Go to [Neon.com](https://neon.com/).  
2. Dashboard → Connect → Create new database.  
3. Only select **parameters**, then copy details into a `.env` file inside the project folder:

```
PGHOST='hgvfdrtyhnmkjhgf.eu-west-2.aws.neon.tech'
PGDATABASE='hiking-app'
PGUSER='neondb_owner'
PGPASSWORD='jvcdrtyhjiytf'
```

---

## 7. Update Database Settings

Use `django-environ` to read the `.env` file in `settings.py`:

```python
import environ

env = environ.Env()
environ.Env.read_env()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('PGDATABASE'),
        'USER': env('PGUSER'),
        'PASSWORD': env('PGPASSWORD'),
        'HOST': env('PGHOST')
    }
}
```

[Guide to Environment Variables](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f)

---

## 8. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

**Explanation:**  
This sets up your database tables according to your models.

---

## 9. Create a Superuser

```bash
python manage.py createsuperuser
```

**Explanation:**  
This creates an admin user you can use to log into Django's admin interface.  

[Django Createsuperuser Docs](https://docs.djangoproject.com/en/stable/ref/django-admin/#createsuperuser)

## 10. Create Another Django App (Resource App)

You can choose a resource like `books`, `posts`, or `products`:

```bash
python manage.py startapp books
```

Add the app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'books',
]
```

---

## 11. Define a Model in Your App

In `books/models.py`:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title
```

**Explanation:**  
- `CharField` – Short text.  
- `TextField` – Long text.  
- `DateField` – Stores dates.  

[Django Model Field Reference](https://docs.djangoproject.com/en/stable/ref/models/fields/)

---

## 12. Make Migrations and Migrate

```bash
python manage.py makemigrations
python manage.py migrate
```

**Explanation:**  
- `makemigrations` generates migration files.  
- `migrate` applies them to the database.

---

## 13. Register the Model in Admin

In `books/admin.py`:

```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

---

## 14. Add Records via Admin

1. Run the server:

```bash
python manage.py runserver
```

2. Visit `http://127.0.0.1:8000/admin/`.  
3. Log in and add a few `Book` records.

---

## 15. Optional: Use `__str__` Method

The `__str__` method defines how the object appears in admin:

```python
def __str__(self):
    return self.title
```

**Explanation:**  
Dunder methods (methods surrounded by `__`) allow Python objects to implement special behavior.  

[Python Dunder Methods](https://rszalski.github.io/magicmethods/)

---

## 16. Create First DRF View

In `books/views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})
```

[DRF - View Documentation](https://www.django-rest-framework.org/api-guide/views/)

---

## 17. Define URL Paths

[Django - URL Dispatcher](https://docs.djangoproject.com/en/5.2/topics/http/urls/)

**In `project/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
]
```

**Create `books/urls.py`:**

```python
from django.urls import path
from .views import HelloWorldView

urlpatterns = [
    path('hello/', HelloWorldView.as_view()),
]
```

---

## 18. Test with Postman

1. Open Postman.  
2. Send a GET request to:

```
http://127.0.0.1:8000/api/books/hello/
```

3. You should receive:

```json
{"message": "Hello, world!"}
```

---

✅ You now have a basic Django REST Framework project with a custom user model, a PostgreSQL database, and your first API endpoint!

