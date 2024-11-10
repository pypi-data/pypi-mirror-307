import django

from django.db import models
from django.conf import settings
from django.apps import apps
from django.db import connection
from django.core.management import call_command

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'djangoapprove',  # Your module
        'djangoapprove.tests',  # Include the tests app
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',  # In-memory database for testing
        }
    },
    SECRET_KEY="dummy-secret-key",
)

django.setup()
call_command('migrate')

class DummyModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    class Meta:
        app_label = "djangoapprove"


from djangoapprove.models import Approval

# Create the table for DummyModel
with connection.schema_editor() as schema_editor:
    schema_editor.create_model(DummyModel)
    schema_editor.create_model(Approval)
