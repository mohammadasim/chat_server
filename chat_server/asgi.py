"""
ASGI config for chat_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
A channels routing configuration is an ASGI application that is
similar to a Django URLconf, in that it tells Channels what code
to run when an HTTP request is received by the Channels server.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_server.settings.dev')

application = get_asgi_application()