# Generated by Django 4.0.4 on 2022-09-27 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_signup_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='Email',
            field=models.EmailField(max_length=35, unique=True),
        ),
    ]
