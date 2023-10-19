# Generated by Django 4.0.1 on 2023-04-22 15:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('PrimaryKey', models.UUIDField(primary_key=True, serialize=False)),
                ('uniqueFacilityIdentificationNumber', models.CharField(blank=True, max_length=64, null=True)),
                ('facilityTypeCode', models.IntegerField(default=99, validators=[django.core.validators.MaxValueValidator(99)])),
                ('facilityServiceCode', models.CharField(blank=True, max_length=18, null=True)),
                ('departmentName', models.CharField(blank=True, max_length=99, null=True)),
                ('referralFacilityIdentificationNumber', models.CharField(blank=True, max_length=10, null=True)),
                ('referralFacilityTypeCode', models.IntegerField(default=99, validators=[django.core.validators.MaxValueValidator(99)])),
                ('referralFromFacilityIdentificationNumber', models.CharField(blank=True, max_length=10, null=True)),
                ('referralFromFacilityTypeCode', models.IntegerField(default=99, validators=[django.core.validators.MaxValueValidator(99)])),
                ('facilityGlobalUniqueIdentifier', models.BinaryField(blank=True, null=True)),
                ('facilitySpecialtyCode', models.IntegerField(default=999, validators=[django.core.validators.MaxValueValidator(999)])),
            ],
            options={
                'verbose_name_plural': 'Facility',
                'db_table': 'Facility',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('PrimaryKey', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('PatientName', models.CharField(blank=True, max_length=99, null=True)),
                ('PatientAge', models.CharField(default='999,99,99', max_length=9)),
                ('PatientGender', models.CharField(blank=True, max_length=12, null=True)),
                ('PatientDOB', models.DateTimeField(blank=True, null=True)),
                ('IdentityUnknownIndicator', models.IntegerField(default=0)),
                ('facilityId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_management.facility')),
            ],
            options={
                'verbose_name_plural': 'Patient',
                'db_table': 'Patient',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('PrimaryKey', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('UniqueHealthIdentificationNumber', models.CharField(blank=True, max_length=18, null=True)),
                ('UniqueHealthIdentificationID', models.CharField(blank=True, max_length=254, null=True)),
                ('AlternateUniqueIdentificationNumberType', models.IntegerField(default=0)),
                ('AlternateUniqueIdentificationNumber', models.CharField(blank=True, max_length=18, null=True)),
                ('NationalityCode', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Person',
                'db_table': 'Person',
            },
        ),
        migrations.CreateModel(
            name='patientAddressDetail',
            fields=[
                ('PrimaryKey', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('PatientAddress', models.CharField(blank=True, max_length=254, null=True)),
                ('PatientAddressType', models.CharField(blank=True, max_length=1, null=True)),
                ('patientLandlineNumber', models.CharField(blank=True, max_length=8, null=True)),
                ('patientMobileNumber', models.CharField(blank=True, max_length=10, null=True)),
                ('patientEmailAddressURL', models.CharField(blank=True, max_length=254, null=True)),
                ('patientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_management.patient')),
            ],
            options={
                'verbose_name_plural': 'patientAddressDetail',
                'db_table': 'patientAddressDetail',
            },
        ),
        migrations.AddField(
            model_name='patient',
            name='personId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_management.person'),
        ),
    ]
