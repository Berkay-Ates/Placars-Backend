# Generated by Django 4.1.7 on 2023-05-09 12:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('AccountManagement', '0023_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('createDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('content', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_authored', to='AccountManagement.account')),
                ('targetCar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_targetCar', to='AccountManagement.car')),
            ],
        ),
    ]
