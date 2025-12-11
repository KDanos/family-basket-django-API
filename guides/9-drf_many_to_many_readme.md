# DRF – Adding a Many-to-Many Relationship

This README introduces **Many-to-Many (M2M)** relationships in Django and how to use them inside a Django REST Framework project.

---

# 1. Choose a Realistic Many-to-Many Relationship
Many-to-Many means:
> **One item can have many of another item, and vice versa.**

Possible examples in a Books API:

### ✔️ Books ↔ Genres
- A book can belong to many genres
- A genre can have many books

### ✔️ Books ↔ Tags
- A book can have multiple tags
- A tag can apply to many books

### ✔️ Books ↔ Authors (if modelling authors separately)
- A book may have multiple authors
- An author may write multiple books

For this guide, we'll choose: **Books ↔ Genres**.

---

# 2. Create a New App (for Genres)

```bash
python manage.py startapp genres
```

Add it to `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'genres',
]
```

Docs: https://docs.djangoproject.com/en/5.0/ref/applications/#configuring-applications

---

# 3. Define the Genre Model & Migrate
Inside `genres/models.py`:

```python
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
```

Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 4. Add Genre to the Admin (Optional)

In `genres/admin.py`:
```python
from django.contrib import admin
from .models import Genre

admin.site.register(Genre)
```

You can now manage genres through Django admin.

---

# 5. Add a Route or Create via Admin
You have two choices:

### Option A — Create genres via Django Admin
This is the simplest way for testing.

### Option B — Add an API route
Add in `genres/views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Genre
from .serializers import GenreSerializer

class GenreListCreateView(APIView):
    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
```

Then wire it up in `genres/urls.py` and the main `urls.py`.

---

# 6. Add a Many-to-Many Field to the Book Model
Open `books/models.py` and import your Genre model:

```python
from genres.models import Genre
```

Add a new field to the Book model:

```python
genres = models.ManyToManyField(Genre, related_name="books")
```

Your model now looks like:

```python
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
```

### 🔍 Explanation
- ManyToManyField creates a **join table** automatically.
- `related_name='books'` lets you do:

```python
genre.books.all()
```

Docs: https://docs.djangoproject.com/en/5.0/topics/db/models/#many-to-many-relationships

---

# 7. Migrate the New M2M Field
Run:
```bash
python manage.py makemigrations
python manage.py migrate
```

Django will create a join table like:
```
books_book_genres
```

---

# 8. Create a Book with Genres Using Postman
Using your existing POST `/books/` route, you can now include genres.

In Postman:
- Add your JWT token in the **Authorization** header
- Send JSON like this:

```json
{
  "title": "Dune",
  "author": "Frank Herbert",
  "genres": [1, 2, 5]
}
```

### 🔍 Explanation
- The array contains **genre primary keys**.
- Django/DRF automatically maps these IDs to Genre instances.

If the serializer includes the `genres` field, DRF will:
- Validate each PK
- Create the book
- Add genre relationships in the join table

Docs: https://www.django-rest-framework.org/api-guide/relations/#manytomanyfields

---

# ✔️ Summary
You have now:
- Created a new app (`genres`)
- Defined a new model
- Added a Many-to-Many relationship to Book
- Migrated the database changes
- Added genres via admin or API
- Successfully created a book with multiple genre relationships using Postman

Your API now supports rich, scalable relationships between resources!

