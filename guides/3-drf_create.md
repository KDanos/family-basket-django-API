# DRF Books API – Create Route & Testing Guide

This README continues from your previous setup, where you created something similar to:
- A `Book` model
- A `BookSerializer`
- A `BooksView` class for handling GET requests
- A `/books` route

In this guide, you will:
1. Add a **POST (Create)** route to your APIView
2. Validate request data using your serializer
3. Save a new `Book` instance to the database
4. Return appropriate HTTP responses
5. Test your route using Postman

---

# 1. Adding a POST (Create) Route

To allow clients to create new `Book` records, you need to implement a `post()` method inside your existing `BooksView`.

Open `books/views.py` and add:

```python
class BooksView(APIView):

    def post(self, request):
      serializer = BookSerializer(data=request.data) # provide the incoming data on the data key
      serializer.is_valid(raise_exception=True) # validate the data based on our schema - raise exception if not
      serializer.save()  # create a new Book instance
      return Response(serializer.data, status=201) # return the persisted data and set the status to 201
```

## 🔍 Explanation

### `serializer = BookSerializer(data=request.data)`
- Passing `data=request.data` tells DRF to validate **incoming** JSON against the `Book` model fields.
- This uses the same serializer you used for GET.

### `serializer.is_valid()`
- Runs built‑in validation rules based on field types in your model.
- If validation fails, `serializer.errors` describes what was wrong.
- We can have APIView send automatic error responses by using `raise_exception=True` as an argument.

### `serializer.save()`
- Creates a new `Book` object in the database.
- Uses the `.create()` method under the hood (provided automatically by `ModelSerializer`).

### Status Codes
- `201 Created` — successful creation

📚 **DRF Serializers – Saving Instances**: https://www.django-rest-framework.org/api-guide/serializers/#saving-instances

📚 **APIView – Request Data**: https://www.django-rest-framework.org/api-guide/requests/#request-parsing

---

# 2. Validating Input Data Automatically

Your `BookSerializer` already knows the fields from your model because you used:

```python
class Meta:
    model = Book
    fields = '__all__'
```

This means DRF will handle:
- Missing required fields
- Wrong data types
- Fields that don’t exist on the model

You don't need to write extra validation unless you want custom rules.

📚 **Validation Docs**: https://www.django-rest-framework.org/api-guide/serializers/#validation

---

# 3. Sending a Proper JSON Response

When the object is valid and saved, this line runs:

```python
return Response(serializer.data, status=201)
```

Why this works:
- `.data` returns a **Python dict** containing the new object’s fields
- DRF automatically converts this into JSON for the response

📚 **Response Docs**: https://www.django-rest-framework.org/api-guide/responses/

---

# 4. Testing Your Create Route

Testing is essential to confirm that your POST route works as expected.

## Using Postman
1. Create a new POST request to:
   ```
   http://localhost:8000/books
   ```
2. Set **Body → JSON**.
3. Enter your fields, e.g.:

```json
{
  "title": "Dune",
  "author": "Frank Herbert"
}
```

4. Send the request.

You should get `201 Created` and the created object.

---

# 5. Testing Validation Errors

Try sending invalid JSON such as:

```json
{
  "title": 12345
}
```

You should receive:

```json
{
  "title": ["Not a valid string."]
}
```

This confirms your serializer is correctly validating input.

---

# ✔️ Summary

You now have:
- A fully functional **Create (POST)** endpoint at `/books`
- Automatic validation using your existing serializer
- JSON responses for success and failure
- Multiple testing methods available to verify behaviour

Your API now supports both **GET** (list) and **POST** (create) operations — forming the start of a complete CRUD API.

