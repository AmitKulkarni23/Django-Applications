"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2nn(skr)y-h86+r0s2v(j2#64*oky3gc$v12ewmxe6#86r7o79'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Any subdomain on herokuapp.com is an allowed host
ALLOWED_HOSTS = [".herokuapp.com"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our own apps
    'products',
    'search',
    'tags',
    'carts',
    'orders',
    'accounts',
    'billing',
    'adresses',
    'analytics',
    'marketing',
]

# Chnages the built-in user model to ours
AUTH_USER_MODEL = 'accounts.User'

FORCE_USER_SESSION_END = False
FORCE_INACTIVE_USER_ENDSESSION = False

STRIPE_SECRET_KEY = "sk_test_DjVHt74y3ojZJJKuXM85Q3Aq00JNC0FkIO"
STRIPE_PUB_KEY = 'pk_test_y0LrxcrefvyUkATasoRO1jbZ00nhh2JLMV'

MAILCHIMP_API_KEY = "49caa8fa86f14fc041240143faa868a0-us20"
MAILCHIMP_DATA_CENTER = "us20"
MAILCHIMP_EMAIL_LIST_ID = "766a89e99f"  # Audience -> Settings -> Audience Name and Defaults

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGOUT_REDIRECT_URL = "/login/"
ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db2.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Media files are whatever we upload ourselves
MEDIA_URL = '/media/'

# If we are handling our own CSS / JS where would they be stored?
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "../../static_my_proj")
]

# All the static files from the CDN server will be put in here
STATIC_ROOT = os.path.join(BASE_DIR, "../../static_cdn", "static_root")
MEDIA_ROOT = os.path.join(BASE_DIR, "../../static_cdn", "media_root")

CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True
