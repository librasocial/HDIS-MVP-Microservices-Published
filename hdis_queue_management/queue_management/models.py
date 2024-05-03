from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Token(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_id = models.CharField(max_length=64)
    date = models.DateField()
    last_token_number = models.SmallIntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['resource_id', 'date'], name='unique_resource_id_and_day')]
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        db_table = 'token'
    def __str__(self):
        return f"Resource ID: '{self.resource_id}', Date: '{self.date}', Current Token: '{self.last_token_number}'"


class Queue(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_id = models.CharField(max_length=64)
    date = models.DateField()
    token_number = models.SmallIntegerField(validators=[MinValueValidator(1)])
    encounter_id = models.UUIDField()

    class Meta:
        verbose_name = 'Queue'
        verbose_name_plural = 'Queues'
        db_table = 'queue'
    def __str__(self):
        return f"Resource ID: '{self.resource_id}', Date: '{self.date}', Current Token: '{self.token_number}'"
