"""
ASGI config for sa_shop project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sa_shop.settings')

application = get_asgi_application()
