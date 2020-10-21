from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework import serializers


class UserData(model.Models):
    user_id = models.CharField(primary_key=True)
    partner_id = models.CharField(max_length=200, default=None)
    data = JSONField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['user_id', 'partner_id', 'data']
    