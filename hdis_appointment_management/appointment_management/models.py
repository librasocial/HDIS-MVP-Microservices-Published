import datetime
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

def compute_default_effective_to():
    return datetime.date.today() + datetime.timedelta(days=365)

class ResourceSchedule(models.Model):   #TODO: Limit access to Employee concerned and Facility Admin
    """Represents a published weekly schedule for a resource associated with a Facility, such as a Provider or Equipment."""
    
    @staticmethod
    def create_new_schedule(inputs):   #TODO: Wrap in transaction
        """Creates a new Schedule (including all child entities) based on the provided inputs."""

        new_resource_schedule = ResourceSchedule(resource_id=inputs['resource_id'], resource_type=inputs['resource_type'], 
                                                 effective_from=inputs['effective_from'], effective_to=inputs['effective_to'])
        new_resource_schedule.save()

        days_of_week = inputs.get('days_of_week')
        for day in ResourceScheduleDay.DayOfWeek.values:
            day_schedule = ResourceScheduleDay(resource_schedule=new_resource_schedule, day_of_the_week=day)

            # If days_of_week list is provided in input, days not included are considered non-working days
            current_day_inputs = days_of_week.get(day)
            if days_of_week and current_day_inputs:
                day_schedule.day_of_the_week_working_status = True
                overbooking_allowed = current_day_inputs.get('overbooking_allowed')
                overbooking_quantity = current_day_inputs.get('overbooking_quantity')
                if overbooking_allowed: day_schedule.overbooking_allowed = overbooking_allowed
                if overbooking_quantity: day_schedule.overbooking_quantity = overbooking_quantity
                day_schedule.save()

                # Generate relevant Appointment Session entries for each day of week
                # If session configuration parameters have been specified for the current day, apply them
                if appointment_sessions := current_day_inputs.get('appointment_sessions'):
                    for current_session in appointment_sessions:    #TODO: Validate session overlaps
                        day_sessions = ResourceScheduleSession(resource_schedule_day=day_schedule, start_time=current_session['start_time'])
                        end_time = current_session.get('end_time')
                        duration = current_session.get('duration')
                        if end_time: day_sessions.end_time = end_time
                        if duration: day_sessions.duration = datetime.timedelta(minutes=duration)
                        day_sessions.save()
                else:   #If session configuration parameters are unspecified for the current day, create sessions with default workday configuration
                    day_sessions = ResourceScheduleSession(resource_schedule_day=day_schedule)
                    day_sessions.save()
            else:
                day_schedule.day_of_the_week_working_status = False
            
        return new_resource_schedule
    
    class ResourceType(models.IntegerChoices):
        Provider = 1
        #TODO: Add other applicable Roles / Equipment

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_id = models.CharField(max_length=64)
    resource_type = models.IntegerField(choices=ResourceType.choices)
    effective_from = models.DateField(default=datetime.date.today, blank=False, null=False)    #TODO: Improve defaults and date overlap handling
    effective_to = models.DateField(default=compute_default_effective_to, blank=True, null=False)

    class Meta:
        verbose_name = 'Resource Schedule'
        verbose_name_plural = 'Resource Schedules'
        db_table = 'resource_schedule'

    def __str__(self):
        return str(self.primary_key)


class ResourceScheduleDay(models.Model):
    """Configurations of a published schedule for a resource specific to a day of week."""
    
    class DayOfWeek(models.TextChoices):
        MON = "Mon", "Monday"
        TUE = "Tue", "Tuesday"
        WED = "Wed", "Wednesday"
        THU = "Thu", "Thursday"
        FRI = "Fri", "Friday"
        SAT = "Sat", "Sunday"
        SUN = "Sun", "Sunday"
    
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_schedule = models.ForeignKey(ResourceSchedule, related_name="days_of_the_week", on_delete=models.CASCADE)
    day_of_the_week = models.CharField(max_length=3, choices=DayOfWeek.choices)
    day_of_the_week_working_status = models.BooleanField(default=True)
    overbooking_allowed = models.BooleanField(default=True)
    overbooking_quantity = models.IntegerField(default=4)

    class Meta:
        verbose_name = 'Resource Schedule Day'
        verbose_name_plural = 'Resource Schedule Days'
        db_table = 'resource_schedule_day'

    def __str__(self):
        return str(self.primary_key)


class ResourceScheduleSession(models.Model):
    """Defines one or more working sessions available for appointments on a given working day of the week as per a published Resource Schedule at a Facility."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_schedule_day = models.ForeignKey(ResourceScheduleDay, related_name="sessions", on_delete=models.CASCADE)
    start_time = models.TimeField(default=datetime.time(8, 00))
    end_time = models.TimeField(default=datetime.time(22,00))
    duration = models.DurationField(default=datetime.timedelta(minutes=15), 
                                    validators=[MinValueValidator(datetime.timedelta(minutes=1)), MaxValueValidator(datetime.timedelta(days=1))] )
    status = models.BooleanField(default=True)    #TODO: Determine if needed

    class Meta:
        verbose_name = 'Resource Schedule Session'
        verbose_name_plural = 'Resource Schedule Sessions'
        db_table = 'resource_schedule_session'

    def __str__(self):
        return str(self.primary_key)


class ResourceUnavailability(models.Model):     #TODO: Limit access to employee concerned, Facility Admin and Front Desk
    """Used to keep track of one-off unavailability of resources, such as Provider Leave or Equipment Breakdown."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_id = models.CharField(max_length=64)
    unavailability_date = models.DateField()
    resource_schedule_session = models.ForeignKey(ResourceScheduleSession, on_delete=models.CASCADE, blank=True, null=True)    #TODO: Retain?
    start_time = models.TimeField(blank=True, default=datetime.time(0, 00))
    end_time = models.TimeField(blank=True, default=datetime.time(23,59))

    class Meta:
        verbose_name = 'Resource Unavailability'
        db_table = 'resource_unavailability'

    def __str__(self):
        return str(self.primary_key)


class Appointment(models.Model):
    """An appointment made by a Paitent for a Resource (Provider, Equipment, etc.) at a Facility."""

    class Status(models.IntegerChoices):
        Active = 1
        Cancelled = 2

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.CharField(max_length=18)
    resource_id = models.CharField(max_length=64)
    facility_id = models.UUIDField()
    resource_schedule_session = models.ForeignKey(ResourceScheduleSession, on_delete=models.CASCADE, null=True) #Dev Note: Nullable for potential standalone use without Resource Schedule
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    booking_datetime = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(default=Status.Active, choices=Status.choices)
    appointment_channel = models.CharField(max_length=50, default='Walkin')

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        db_table = 'appointment'

    def __str__(self):
        return str(self.primary_key)
