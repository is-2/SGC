from django.db import models
from django.contrib.auth.models import User

# REAL MODELS
User.add_to_class('firstName', models.CharField(max_length=100, blank=True))
User.add_to_class('lastName', models.CharField(max_length=100, blank=True))
User.add_to_class('status', models.BooleanField(default=True))
User.add_to_class('phonenum', models.CharField(max_length=100, blank=True))
User.add_to_class('address', models.CharField(max_length=100, blank=True))
User.add_to_class('observation', models.CharField(max_length=100, blank=True))
