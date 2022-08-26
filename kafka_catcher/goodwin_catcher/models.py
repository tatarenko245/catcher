from django.db import models


class Message(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, serialize=True)
    ocid = models.CharField(max_length=55, blank=True)
    x_operation_id = models.CharField(max_length=55, blank=True)
    message = models.JSONField()
    date_of_creation = models.DateField(auto_now_add=True, auto_created=True)
