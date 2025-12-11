# DRF Books API – Adding Ownership & Protecting Update/Delete

This README walks through implementing **per‑user book ownership** and protecting update/delete routes so that only the owner of a book can modify or remove it.

---

# 1. Add a User ForeignKey to the Book Model

Open `books/models.py` and add an `owner` field:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='books_owned'
    )

    def __str__(self):
        return self.title
```

### 🔍 Explanation
- `ForeignKey` creates a **many‑to‑one relation**, meaning one user can own many books.
- `on_delete=models.CASCADE` deletes all the user's books if the user is deleted.
- `related_name="books"` allows reverse lookup: `user.books.all()`.

You must now run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

If this new field is **non-nullable**, Django requires a default. You should:
- Provide a one‑off default during migration, ideally your Admin user, but it's not too important as this is test data.

Docs: https://docs.djangoproject.com/en/5.0/topics/migrations/#workflow

---

# 2. Update the POST Handler to Assign the Owner

Inside your `BooksView` POST route:

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BooksView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        # inject the owner into request data
        request.data['owner'] = request.user.id
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
```

### 🔍 Why we need permissions here
`request.user` only exists for authenticated users.

By adding:
```python
permission_classes = [IsAuthenticatedOrReadOnly]
```
We ensure:
- The user is logged in for POST, PUT, PATCH, DELETE routes
- We have access to `request.user`

Docs: https://www.django-rest-framework.org/api-guide/permissions/

---

# 3. Test POST in Postman with Authorization Header

In Postman:
1. Open your POST `/books/` request
2. Go to the **Headers** tab
3. Add:

```
Authorization: Bearer <your-jwt-token>
```

4. Send JSON body like:
```json
{
  "title": "Hyperion",
  "author": "Dan Simmons"
}
```

The new book should have its `owner` set to the user from the token.

---

# 4. Authorise Update/Delete Using Simple Ownership Check

Inside `BookDetailView`, import the `PermissionDenied` exception from Rest Framework:
```python
from rest_framework.exceptions import PermissionDenied
```

Then update your PUT handler:

```python
class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        book = self.get_object(pk)

        # basic ownership check
        if book.owner != request.user:
            raise PermissionDenied('You do not own this book.')

        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

### 🔍 Explanation
- This prevents other users from modifying someone else’s book.
- `403 Forbidden` is the correct HTTP status. This will automatically be sent when we raise a `PermissionDenied`

---

# 5. Create a Reusable Permission Class (IsOwnerOrReadOnly)

Instead of duplicating the `if book.owner != request.user` logic, create a permission to reuse.

Create a file: `utils/permissions.py` - it's outside of the app so it can be reused on other models that have an owner field.

```python
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Allow read-only requests for anyone
        if request.method in SAFE_METHODS:
            return True

        # Write access only for the owner
        return obj.owner == request.user
```

### 🔍 Explanation
- `SAFE_METHODS` = GET, HEAD, OPTIONS
- Useful for public read / private write APIs

Docs: https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

Now apply it to your detail view:

```python
from utils.permissions import IsOwnerOrReadOnly

class BookDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
```

DRF will:
- Run authentication → assign `request.user`
- Fetch the object (via `get_object()`)

We can remove the old authorization line:
```python
if book.owner != request.user:
    raise PermissionDenied('You do not own this book.')
```

And replace it with the below line which checks object permissions based on the method we defined in our `IsOwnerOrReadOnly` class

```python
def put(self, request, pk):
    book = self.get_object(pk)
    self.check_object_permissions(request, book) # This line will be added to check object permissions on the book.
    serializer = BookSerializer(book, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
```

If the owner of the book is not the same as the request.user, a PermissionDenied will automatically be raised when using `self.check_object_permissions(request, book)`.

[Documentation Entry](https://www.django-rest-framework.org/api-guide/permissions/#examples)

---

# 6. Apply the Permission to PATCH and DELETE

Repeat the same pattern:

### PATCH
```python
def patch(self, request, pk):
    book = self.get_object(pk)
    self.check_object_permissions(request, book) # New line for object permissions
    serializer = BookSerializer(book, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
```

### DELETE
```python
def delete(self, request, pk):
    book = self.get_object(pk)
    self.check_object_permissions(request, book) # New line for object permissions
    book.delete()
    return Response(status=204)
```

---

# ✔️ Summary
You now have:
- A `owner` field linking books to users
- POST routes that automatically assign owners
- JWT‑protected endpoints using `request.user`
- Ownership checks preventing unauthorised edits
- A reusable permission class (`IsOwnerOrReadOnly`)
- Protected PUT/PATCH/DELETE routes that only owners can modify

Your API is now multi‑user safe and ready for production‑grade behaviour.

