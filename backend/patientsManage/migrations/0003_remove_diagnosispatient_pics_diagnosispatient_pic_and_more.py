# Generated by Django 4.2.7 on 2023-11-24 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patientsManage", "0002_diagnosispatient_pics_patient_patientpic"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="diagnosispatient",
            name="Pics",
        ),
        migrations.AddField(
            model_name="diagnosispatient",
            name="Pic",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="patientPic",
            field=models.TextField(null=True),
        ),
    ]
