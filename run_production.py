import os
import sys
import logging
from django.core.wsgi import get_wsgi_application
from waitress import serve

# 1. FORCE LOGGING TO STDOUT
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    stream=sys.stdout  # Explicitly print to terminal
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vadrida.settings")
application = get_wsgi_application()

print("--- Starting High-Concurrency Server ---")
print("--- Serving PDFs requires MANY threads ---")

serve(
    application,
    host='127.0.0.1',
    port=8000,
    # CRITICAL CHANGE: Increase threads significantly
    # Because you are serving files, threads get blocked easily.
    # Increasing this allows other users to access the site while PDFs download.
    threads=100,           
    connection_limit=200,   # Allow more simultaneous connections
    channel_timeout=300,    # 5 minute timeout for slow networks
    _quiet=False
)