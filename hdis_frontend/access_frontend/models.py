from django.db import models

class Facilitytype(models.Model):
    facility_type_code = models.IntegerField(primary_key=True)
    facility_type_description = models.CharField(max_length=64)
    facility_short_type_name = models.CharField(max_length=4)
    facility_type_internal=models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'FacilityType'
    def __str__(self):
        return str(self.facility_type_code)
    


class SpecialityType(models.Model):
    Medical_Specialty_Type_Code = models.IntegerField(primary_key=True)
    Medical_Specialty_Type_Name = models.CharField(max_length=64)


    class Meta:
        managed = False
        db_table = 'SpecialityType'
    def __str__(self):
        return str(self.Medical_Specialty_Type_Code)
