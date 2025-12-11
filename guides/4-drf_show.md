# DRF Books API – Show Route (Retrieve by ID) Guide

This README explains how to add a **Show** route (a Retrieve endpoint) to your DRF Books API. This allows clients to request a **single Book** by its ID using a URL like:

```
/books/<pk>/
```

You will learn:
1. How to create a dedicated view for retrieving one book
2. How to update your URL patterns to accept a dynamic ID
3. How to fetch a single model instance using `.get()`
4. How to handle errors such as missing objects
5. How to return JSON using your existing serializer
6. How to test the Show route

---

# 1. Create a Show (Retrieve) View

Inside `books/views.py`, create a new view class or extend your existing view structure. For clarity, you will create a separate view class dedicated to retrieving a single book.

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Book
from .serializers.common import BookSerializer

class BookDetailView(APIView):

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)  # fetch single book
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found.")

        serializer = BookSerializer(book)
        return Response(serializer.data)
```

## 🔍 Explanation

### Accepting `pk`
- DRF passes the URL parameter into your view method.
- `pk` (primary key) is the Django convention for identifying a single record.

### `.get(pk=pk)`
- Unlike `.all()`, `.get()` retrieves **one specific object**.
- If the object doesn’t exist, Django raises a `DoesNotExist` exception.

### Handling Missing Objects
By catching `Book.DoesNotExist` and raising DRF's `NotFound` exception, you automatically return:

- HTTP `404 Not Found`
- A JSON error message

📚 Docs — Handling Exceptions: https://www.django-rest-framework.org/api-guide/exceptions/

### Serializing a Single Object
```python
serializer = BookSerializer(book)
```
- No `many=True` because you are serializing **one** object.

📚 ModelSerializer Docs: https://www.django-rest-framework.org/api-guide/serializers/#modelserializer

---

# 2. Add a Route for the Show View

Update your `books/urls.py` to include a dynamic path parameter.

```python
from django.urls import path
from .views import BooksView, BookDetailView

urlpatterns = [
    path('/', BooksView.as_view()),               # /books
    path('<int:pk>/',, BookDetailView.as_view()),  # /books/1
]
```

## 🔍 How This Works
- `<int:pk>` captures part of the URL and passes it to your view.
- Django ensures it is an integer before calling the view.
- If the parameter doesn't match (e.g. a string), Django returns a 404.

📚 Django Path Converters: https://docs.djangoproject.com/en/5.0/topics/http/urls/#path-converters

---

# 3. Serializing & Returning JSON

After fetching the instance, you serialize it:

```python
serializer = BookSerializer(book)
return Response(serializer.data)
```

- `.data` contains the Python-native structure
- DRF automatically turns it into JSON

📚 Response Docs: https://www.django-rest-framework.org/api-guide/responses/

---

# 4. Testing the Show Route in Postman

1. Create a new **GET** request.
2. Enter the URL:

```
http://localhost:8000/books/1/
```

3. Send the request.

You should receive the JSON for the requested book.

---

# ✔️ Summary

You have now added a **Show (Retrieve)** route using:
- A new `BookDetailView` class
- URL routing for `/books/<id>`
- Safe model retrieval using `.get()` with error handling
- JSON serialization of a single model instance

Your API now supports:
- **GET /books** — list all books
- **POST /books** — create a new book
- **GET /books/:pk/** — show a single book

