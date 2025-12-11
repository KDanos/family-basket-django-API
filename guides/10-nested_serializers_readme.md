# DRF – Nested Serializers Guide (Using a Separate `populated.py` Serializer)

This README explains how to return **nested objects** in Django REST Framework without modifying your existing serializer. Instead, you will create a **new serializer** in `populated.py` that **extends** your base serializer and adds nested fields, including related `genres`.

Docs: https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects

---

# 1. Why Use Nested Serializers?

Nested serializers allow your API to return complete related objects instead of only the primary key.

### Without nested serializer:
```json
{
  "id": 1,
  "title": "Dune",
  "genres": [1, 2]
}
```

### With nested serializer:
```json
{
  "id": 1,
  "title": "Dune",
  "genres": [
    { "id": 1, "name": "Sci-Fi" },
    { "id": 2, "name": "Adventure" }
  ]
}
```

This makes GET responses clearer and more useful for frontend applications.

---

# 2. Ensure the Related Model Has Its Own Serializer

Before nesting, create a simple serializer for the `Genre` model.

**`genres/serializers/common.py`**:
```python
from rest_framework.serializers import ModelSerializer
from .models import Genre

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
```

This serializer defines how the nested `genres` objects will appear.

---

# 3. Your Existing Book Serializer Stays the Same

You *do not* modify the existing serializer.

**`books/serializers/common.py`**:
```python
from rest_framework.serializers import ModelSerializer
from ..models import Book

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

This continues to handle **POST**, **PUT**, and **PATCH** operations.

---

# 4. Create a Populated Serializer That Extends `BookSerializer`

To provide nested objects, create a new serializer:

**`books/serializers/populated.py`**:
```python
from .common import BookSerializer
from genres.serializers.common import GenreSerializer

class PopulatedBookSerializer(BookSerializer):
    genres = GenreSerializer(many=True)
```

### Explanation
* `PopulatedBookSerializer` **inherits** all fields from `BookSerializer`.
* You add a new nested `genres` field using `GenreSerializer()`.
* Don't forget `many=True` when working with many-to-many fields, though it's not needed when populating a ForeignKey field (one-to-many).

This allows GET requests to return nested objects without affecting write operations.

---

# 5. Use the Populated Serializer in Your GET Route

Update your show route to use the new serializer.

```python
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers.populated import PopulatedBookSerializer
from .models import Book

class BookDetailView(APIView):

    ...

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = PopulatedBookSerializer(book)
        return Response(serializer.data)
```

This now returns nested genres data when retrieving a single book.

---

# 6. Summary

You now support nested serializers using a clean, maintainable structure:

* Your **base serializer stays simple** (`BookSerializer`).
* You **extend it** in a new file (`PopulatedBookSerializer`).
* You display nested related objects (`genres`) only when needed.
* Your create/update logic remains unaffected.

This pattern is ideal for real-world APIs where you often need different serializers for different levels of detail.

