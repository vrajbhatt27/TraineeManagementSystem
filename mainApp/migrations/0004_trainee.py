# Generated by Django 4.0.1 on 2022-02-01 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_alter_form_fid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.CharField(max_length=50, null=True)),
                ('trainee_name', models.CharField(max_length=50, null=True)),
                ('trainee_email', models.CharField(max_length=50, null=True)),
                ('trainee_age', models.IntegerField(null=True)),
                ('trainee_college', models.CharField(max_length=50, null=True)),
                ('trainee_cgpa', models.FloatField(null=True)),
                ('trainee_hsc', models.FloatField(null=True)),
                ('trainee_ssc', models.FloatField(null=True)),
                ('trainee_domain', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
