# Generated by Django 3.1.3 on 2020-11-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='icaimages',
            name='img_sources_plot',
            field=models.JSONField(null=True),
        ),
    ]