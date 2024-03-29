# Generated by Django 4.2.11 on 2024-03-15 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_remove_studentsubjectcourse_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectmeeting',
            name='platform',
            field=models.CharField(blank=True, choices=[('1', 'Google Meet'), ('2', 'Zoom'), ('3', 'Microsoft Teams')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='subjectmeeting',
            name='mode',
            field=models.CharField(blank=True, choices=[('1', 'Online'), ('2', 'Face to Face')], max_length=2, null=True),
        ),
    ]
