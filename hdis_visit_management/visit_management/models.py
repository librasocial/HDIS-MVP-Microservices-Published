from django.db import models
from django.core.validators import MaxValueValidator
import uuid

class Episode(models.Model):
    """ Represents a series of Visits by a Patient to multiple Providers, potentially at different Facilities on different dates, in relation to a single health issue.
        Used to track the history of a specific ailment for a Patient across multiple Provider consultations.
    """
    
    class Type(models.IntegerChoices):
        Default = 0

    class Status(models.IntegerChoices):
        Open = 1
        Closed = 2
    
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    episode_type = models.IntegerField(choices=Type.choices, default=Type.Default)    #TODO: Standardized code master to be created.
    #person_id = models.UUIDField() #TODO: Implement link to Person
    status = models.IntegerField(choices=Status.choices, default=Status.Open)

    class Meta:
        verbose_name = 'Episode'
        verbose_name_plural = 'Episodes'
        db_table = 'episode'
    def __str__(self):
        return str(self.primary_key)
    

class Encounter(models.Model): 
    """Represents a particular Visit by a Patient to a Provider at a Facility on a specific date and time."""
    
    class Type(models.IntegerChoices):
        Outpatient = 1

    class Status(models.IntegerChoices):
        Planned = 1

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.IntegerField(choices=Type.choices, default=Type.Outpatient)    #TODO: Standardized codes that require master tables
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=18)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(choices=Status.choices, default=Status.Planned)    #TODO: Change to standardized code with master table
    appointment_id = models.UUIDField(blank=True, null=True, default=None)    #Appointment based on which the Visit (Encounter) was created. Not required for walk-ins.
    # Dev Note: The association of an Encounterwith Provider(s) is maintained within the microservice for the respective Service
    
    class Meta:
        verbose_name = 'Encounter'
        verbose_name_plural = 'Encounters'
        db_table = 'encounter'
    def __str__(self):
        return str(self.primary_key)
