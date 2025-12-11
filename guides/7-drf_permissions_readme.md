# DRF Permissions Guide

This short README explains how to secure your DRF API using **permissions**, with JWT authentication as the base.

---

# 1. Add SimpleJWT Middleware

Before adding permissions, ensure your project uses JWT authentication to manage user access.

### Installation
```bash
pipenv install djangorestframework-simplejwt
```

### Add to settings.py
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

### 🔍 Explanation
- SimpleJWT provides **JSON Web Token** authentication.
- JWT allows clients to authenticate with a token rather than sending credentials every time.
- DRF will automatically use this authentication when checking permission classes.

📚 **Getting Started with SimpleJWT:** https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html

---

# 2. Add Permission Classes

Permissions determine which users can access which endpoints.

### Example: Restricting access to authenticated users
Inside your views (e.g., `BooksView`):

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class BooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # your GET logic
        pass
```

### 🔍 Explanation
- `IsAuthenticated` ensures only logged-in users (with valid JWT) can access this view.
- Other common permission classes include:
  - `AllowAny` – default, no restriction
  - `IsAdminUser` – only admin users
  - `IsAuthenticatedOrReadOnly` – authenticated users can write, others can only read

📚 **DRF Permissions Docs:** https://www.django-rest-framework.org/api-guide/permissions/

---

# ✔️ Summary

By adding JWT authentication and permission classes, you now have:
- Secure authentication using tokens
- Fine-grained access control to your API endpoints
- Flexibility to use global or per-view permission settings