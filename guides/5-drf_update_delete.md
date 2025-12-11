# DRF Books API – Update & Delete Routes Guide

This README continues the API build you've started, where you already support:
- **GET /books/** — list all books
- **POST /books/** — create a new book
- **GET /books/<:pk>/** — retrieve a single book

You will now add support for:
- **PUT /books/<:pk>/** — update
- **DELETE /books/<:pk>/** — remove a book

These complete the CRUD functionality for the Books API.

---

# 1. Updating a Book (PUT)

Updating a book is similar to creating one, except you:
- Fetch the existing instance
- Pass both the **instance** and **new data** into the serializer
- Validate and save

Open `books/views.py` and modify your `BookDetailView` to include `put`.

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Book
from .serializers.common import BookSerializer

class BookDetailView(APIView):

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found.")

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)  # update
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

---

## 🔍 Explanation

### `get_object()` helper
To avoid repeating the `.get()` and error handling, the logic is moved into `get_object()`.

### Why pass the instance?

```python
serializer = BookSerializer(book, data=request.data)
```

Passing an instance tells DRF:
- "Update this object" (instead of creating a new one)

### Partial updates

Better served by a `PATCH` request, if needed.

```python
partial=True
```

Allows updating only a subset of fields.

📚 **PUT Docs**: https://www.django-rest-framework.org/api-guide/serializers/#partial-updates

📚 **Validation Docs**: https://www.django-rest-framework.org/api-guide/serializers/#validation

---

# 2. Deleting a Book (DELETE)

Now add a `delete` method to the same view.

```python
    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=204)
```

## 🔍 Explanation

- `.delete()` removes the instance from the database
- DRF convention for successful deletion is:
  - **204 No Content** (empty response body)

📚 **Status Codes Reference**: https://www.django-rest-framework.org/api-guide/status-codes/

---

# 4. Testing Update & Delete

You can test using Postman.

---

## ✔️ Testing PUT

Endpoint to use:
```bash
PUT http://localhost:8000/books/1/
```

Request body:
```json
{
    "title": "Dune Messiah", 
    "author": "Frank Herbert"
}
```

Expected response: status **200*, updated object as the body.

---

## ✔️ Testing DELETE
Endpoint to use:
```bash
DELETE http://localhost:8000/books/1/
```

Expected response: status **204**, empty body.

---

# ✔️ Summary

Your Books API now supports full CRUD:

| Method | Route | Action |
|--------|--------|---------|
| GET | /books/ | List all books |
| POST | /books/ | Create a new book |
| GET | /books/<id>/ | Retrieve a single book |
| PUT | /books/<id>/ | Full update |
| DELETE | /books/<id>/ | Remove the book |