# Generated by Django 2.0.5 on 2019-07-09 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_addr'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='salt',
            field=models.CharField(default='', max_length=512),
        ),
    ]
