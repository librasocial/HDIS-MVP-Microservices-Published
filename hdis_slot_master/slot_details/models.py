from django.db import models
import uuid
# Create your models here.
class ProviderSchedule(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #ResourceScheduleId = models.AutoField(primary_key=True)
    LocalHealthCareProviderNumber = models.CharField(max_length=64, blank=True, null=True)
    UniqueIndividualHealthCareProviderNumber = models.CharField(max_length=64, blank=True, null=True)
    UniqueFacilityIdentificationNumber = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'ProviderSchedule'
        db_table = 'ProviderSchedule'

    def __str__(self):
        return str(self.PrimaryKey)

class ProviderWeekDayDetails(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    providerWeekDayId = models.ForeignKey(ProviderSchedule, on_delete=models.CASCADE)
    dayOfTheWeek = models.CharField(max_length=10)
    dayOfTheWeekWorkingStatus = models.BooleanField(default=True)
    overBookingAllowed = models.BooleanField(default=True)
    overBookQuantity = models.IntegerField(default=4)
    class Meta:
        verbose_name_plural = 'ProviderWeekDayDetails'
        db_table = 'ProviderWeekDayDetails'

    def __str__(self):
        return str(self.PrimaryKey)

class AppointmentSessionSlots(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slotId = models.ForeignKey(ProviderWeekDayDetails, on_delete=models.CASCADE)
    dayOfTheWeekSlotStartTime = models.CharField(max_length=5, default="08:00")
    dayOfTheWeekSlotEndTime = models.CharField(max_length=5, default="22:00")
    dayOfTheWeekSlotDuration = models.CharField(max_length=5, default="15")
    dayOfTheWeekSlotStatus = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = 'AppointmentSessionSlots'
        db_table = 'AppointmentSessionSlots'

    def __str__(self):
        return str(self.PrimaryKey)

class ProviderLeaveMaster(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leaveId = models.ForeignKey(ProviderSchedule, on_delete=models.CASCADE)
    leaveDate = models.DateTimeField()
    leaveSlotId = models.ForeignKey(AppointmentSessionSlots, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'ProviderLeaveMaster'
        db_table = 'ProviderLeaveMaster'

    def __str__(self):
        return str(self.PrimaryKey)


#doctor_id
#start time
#end time
#duration of slot
#non working days

#leave management
#doctor_id
#start time
#end time
#leave date
#ResourceScheduleId
#ResourceScheduleStartDate
#ResourceScheduleEndDate
#ResourceScheduleStartTime
#ResourceScheduleEndTime
#Array of NonWorkingDates //Schedule creation will exclude non working days and leaves
#ResourceType(default=’CareProvider’)
#UniqueIndividualHealthCareProviderNumber
#UniqueFacilityIdentificationNumber
#Set(Collection) of AppointmentSessionSlotsVO Objects