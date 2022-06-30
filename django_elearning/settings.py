import os
from pathlib import Path

from configurations import Configuration
from configurations import values
import dj_database_url


class Dev(Configuration):

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-to=f9f3l+bb2(lx982e-2-u!*2w$p&sobl)$o0pp)nf&vo*el8'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # my own app
        'homepage',
        'courses',
        'students',

        # third packageparty
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        
        
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'django_elearning.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, "/templates"),
                os.path.join(BASE_DIR, "templates"),
            ],
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

    WSGI_APPLICATION = 'django_elearning.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases

    DATABASES = {
        "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
        "alternative": dj_database_url.config(
            "ALTERNATIVE_DATABASE_URL",
            default=f"sqlite:///{BASE_DIR}/alternative_db.sqlite3",
        ),
    }


    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = values.Value("UTC")

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



    # allauth settings

    AUTH_USER_MODEL = 'students.CustomeUserModel'

    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

    from django.urls import reverse_lazy, reverse
    # LOGIN_REDIRECT_URL = reverse_lazy('student_course_list')


    ACCOUNT_FORMS = {
        'login': 'accounts.forms.CustomSignInForm',
        'signup': 'accounts.forms.CustomSignupForm',
        'add_email': 'allauth.account.forms.AddEmailForm',
        'change_password': 'accounts.forms.CustomChangePasswordForm',
        'set_password': 'allauth.account.forms.SetPasswordForm',
        'reset_password': 'allauth.account.forms.ResetPasswordForm',
        'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
        'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
    }


class Prod(Dev):
    DEBUG = False