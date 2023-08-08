# newsapp/apps.py

from django.apps import AppConfig

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'

    def ready(self):
        # Import and include the API URLs from the myapi app
        from myapi import urls as api_urls
        self.urlpatterns = api_urls.urlpatterns
