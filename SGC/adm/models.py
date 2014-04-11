from django.db import models
from django.contrib.auth.models import User

# REAL MODELS
User.add_to_class('status', models.BooleanField(default=True))
User.add_to_class('email', models.CharField(max_length=50))
User.add_to_class('phonenum', models.CharField(max_length=100, blank=True))
User.add_to_class('direction', models.CharField(max_length=100, blank=True))
User.add_to_class('observation', models.CharField(max_length=100, blank=True))