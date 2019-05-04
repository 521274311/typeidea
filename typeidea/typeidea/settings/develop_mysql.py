from .base import * # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME' : 'typeidea',
        'USER' : 'root',
        'PASSWORD' : '123456',
        'HOST' : '127.0.0.1',
        'PORT' : '3306',
    }
}