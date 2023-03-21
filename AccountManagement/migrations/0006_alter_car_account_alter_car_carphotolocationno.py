# Generated by Django 4.1.7 on 2023-03-10 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AccountManagement', '0005_car_account_comment_targetcar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AccountManagement.account'),
        ),
        migrations.AlterField(
            model_name='car',
            name='carPhotoLocationNo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
