# Generated by Django 4.0.1 on 2023-05-07 03:57

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
            name='Facilitytype',
            fields=[
                ('facility_type_code', models.IntegerField(primary_key=True, serialize=False)),
                ('facility_type_description', models.CharField(max_length=64)),
                ('facility_short_type_name', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'FacilityType',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('PrimaryKey', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('uniqueFacilityIdentificationNumber', models.UUIDField(default=uuid.uuid4)),
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
            name='FacilityApplication',
            fields=[
                ('PrimaryKey', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('facilityApplicantName', models.CharField(max_length=64)),
                ('facilityApplicantEmail', models.CharField(max_length=128)),
                ('facilityApplicantMobile', models.CharField(max_length=15)),
                ('facilityApplicantCountry', models.CharField(max_length=64)),
                ('facilityApplicantCity', models.CharField(max_length=64)),
                ('facilityName', models.CharField(max_length=128)),
                ('facilityTypeCode', models.IntegerField()),
                ('facilityInternalClass', models.IntegerField()),
                ('facilityApplicantRemarks', models.CharField(blank=True, max_length=128)),
            ],
            options={
                'verbose_name_plural': 'FacilityApplication',
                'db_table': 'FacilityApplication',
            },
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('PrimaryKey', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('userRole', models.CharField(max_length=64)),
                ('memberName', models.CharField(max_length=64)),
                ('memberEmail', models.CharField(blank=True, max_length=128)),
                ('memberMobile', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Members',
                'db_table': 'Members',
            },
        ),
        migrations.CreateModel(
            name='FacilityMembers',
            fields=[
                ('PrimaryKey', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('facilityId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility_management.facility')),
                ('memberId', models.ManyToManyField(related_name='members', to='facility_management.Members')),
            ],
            options={
                'verbose_name_plural': 'FacilityMembers',
                'db_table': 'FacilityMembers',
            },
        ),
    ]
