"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# dotenv config
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_DIR = BASE_DIR.parent / 'dotenv_files' / '.env'

load_dotenv(ENV_DIR, override=True)

# django config
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()
