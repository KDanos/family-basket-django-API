# DRF Custom Authentication – User Model, Validation, and Sign-Up Route

This README continues directly from your existing Books API and builds the foundation for **custom authentication**. You have already created your custom user model *before* the initial migration (as recommended), so now we extend it with new fields, validation, and a sign-up endpoint.

We will cover:
1. Updating the custom user model (unique email, extra fields)
2. Handling migrations for non-nullable fields
3. Creating a custom UserSerializer
4. Proper password + confirm_password handling
5. Adding password validation
6. Hashing the password
7. Creating a SignUpView and URL route
8. Verifying hashed passwords in Neon

---

# 1. Update the Custom User Model

Open your custom user model (in `users/models.py`). You now:
- Make **email required and unique**
- Optionally add custom fields such as `bio`, `profile_image`, etc.

Example:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # required + unique

    bio = models.TextField(max_length=255, blank=True, null=True)  # optional custom field
    profile_image = models.URLField(blank=True, null=True)  # another optional custom field
```

## 🔍 Notes
- `unique=True` ensures no two users share the same email.
- `blank=True` would allow an empty value to be skipped during validation, `null=True` allows you to add an empty value to the database.
- Remember: altering existing tables requires migrations.

📚 **Custom User Model Docs:** https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#substituting-a-custom-user-model

---

# 2. Migrating After Adding New Non-Nullable Fields

If you add a field that **cannot be null** (e.g., a `CharField` without `null=True`), Django will require a default.

You have two options when running migrations:

### ✔️ Option 1 — One-off default
Django asks:
```
Please enter the default value to use for existing rows
```
This adds a default *only for migration*, not for future rows.

### ✔️ Option 2 — Permanent default
Add `default=` to the model field:

```python
bio = models.TextField(default="Hello World")
```

**Important:** Choosing a permanent default changes your data model going forward.

📚 **Migrations Docs:** https://docs.djangoproject.com/en/5.0/topics/migrations/

---

# 3. Create a User Serializer

Create a file at:
```
users/serializers/common.py
```

Start with a `ModelSerializer`:

```python
from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'confirm_password',
            'bio',
            'profile_image',
            'is_staff',
        ]
```

## 🔍 Notes
- We explicitly list fields this time.
- `confirm_password` is **not** a model field—it's for validation.
- Any field you want users to provide **must** be listed here.

📚 **ModelSerializer Docs:** https://www.django-rest-framework.org/api-guide/serializers/#modelserializer

---

# 4. Mark Password Fields as Write-Only

Add write-only settings inside the serializer:

```python
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
```

### Why?
- These values should never be returned to the client.
- DRF automatically excludes them from responses.

📚 **Serializer Field Options:** https://www.django-rest-framework.org/api-guide/fields/#core-arguments

---

# 5. Add Validation: Matching Passwords

You now create a `validate()` method to check password vs. confirm_password.

```python
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None) # None will prevent an empty confirm_password field on the request not raising an exception

        if password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })
```

### Why use `pop()` for confirm_password?
- It removes the field so it is **never saved** to the model.

📚 **Validation Docs:** https://www.django-rest-framework.org/api-guide/serializers/#validation

---

# 6. Optional: Use Django’s Password Validators

Django allows enabling validators in your `settings.py` (e.g., min length, common passwords).

Import it like this:
```python
from django.contrib.auth import password_validation
```

Run them like this:

```python
        password_validation.validate_password(password)
```

This raises a ValidationError automatically if password rules are violated.

📚 **Password Validation Docs:** https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#password-validation

---

# 7. Hash the Password Before Saving

If you saved the validated data now, Django would store the password as **plain text**. Not good.

Import the `hashers` package like this:
```python
from django.contrib.auth import password_validation, hashers
```

Instead:

```python
        data['password'] = hashers.make_password(password)
```

This ensures the password stored in the database is hashed.

📚 **Password Hashing Docs:** https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#module-django.contrib.auth.hashers

---

# 8. Return the Validated Data

Finally:

```python
        return data
```

This completes the validation cycle.

---

# 9. Create the Sign Up View

Inside `users/views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers.common import UserSerializer

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User created successfully'})
```

### 🔍 Explanation
- The serializer handles **all validation + hashing**.
- `raise_exception=True` automatically returns 400 responses.

📚 **APIView Docs:** https://www.django-rest-framework.org/api-guide/views/

---

# 10. Add the URL Route

In `users/urls.py`:

```python
from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
]
```

And in your main `urls.py`:

```python
path('auth/', include('users.urls')),
```

---

# 11. Verify Password Hashing in Neon

1. Go to your project’s Neon dashboard
2. Open the **Tables** page
3. Look at `auth_user` (or your custom user table)
4. Verify that:
   - Passwords look something like: `pbkdf2_sha256$...`
   - Emails are saved correctly
   - Custom fields like `bio` and `profile_image` appear

If the password is stored in **plain text**, double-check your hashing step.

---

# ✔️ Summary

You now have:
- A custom user model with unique email + new fields
- A fully validated serializer with:
  - write-only password fields
  - matching password confirmation
  - optional password validation rules
  - hashed password storage
- A working SignUp endpoint
- Verified hashed password storage in Neon