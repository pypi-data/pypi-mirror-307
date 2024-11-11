# ✨ django-no-hot-reload-mod ✨

Effortlessly modify Django endpoint functionality without restarting the server.

[django-no-hot-reload-mod on PyPI](https://pypi.org/project/django-no-hot-reload-mod/)

---

## Installation

Run the following command to install the package:

```bash
pip install django-no-hot-reload-mod
```

# Overview
django-no-hot-reload-mod enables real-time modifications to Django endpoints without needing to restart the development server. This is perfect for rapid development and testing, allowing you to make frequent changes on the fly.

---

# Setup Instructions
## 1️⃣ Add to Installed Apps
In your settings.py file, add django_no_hot_reload_mod.code_modifier to the INSTALLED_APPS list:

```python
INSTALLED_APPS = [
    # Other apps...
    'django_no_hot_reload_mod.src.code_modifier',
]
```

## 2️⃣ Update URL Configuration
In your urls.py file, include code_modifier in your project’s URL configuration:

```python
from django.urls import path, include

urlpatterns = [
    # Other URL patterns...
    path("code_modifier/", include("django_no_hot_reload_mod.src.code_modifier.urls")),
]

```

##  ️3️⃣ Create Dummy Apps and Views
To test the setup, create some dummy apps and views in your project.

## 4️⃣ Access the Feature

Once the above steps are complete, you can visit the following URL to access the functionality:

[http://127.0.0.1:8000/code_modifier/code_mod/](http://127.0.0.1:8000/code_modifier/code_mod/)




