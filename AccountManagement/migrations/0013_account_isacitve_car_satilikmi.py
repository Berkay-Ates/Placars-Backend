# Generated by Django 4.1.7 on 2023-05-06 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountManagement', '0012_alter_account_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='isAcitve',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='car',
            name='satilikMi',
            field=models.BooleanField(default=False),
        ),
    ]