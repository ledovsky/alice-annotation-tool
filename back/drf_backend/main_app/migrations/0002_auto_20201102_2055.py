# Generated by Django 3.1.2 on 2020-11-02 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='icacomponent',
            name='images_calculated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='icacomponent',
            unique_together={('name', 'subject', 'dataset')},
        ),
        migrations.CreateModel(
            name='ICAImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_topomap', models.ImageField(upload_to='images/')),
                ('ic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main_app.icacomponent')),
            ],
        ),
        migrations.CreateModel(
            name='DatasetStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_components', models.IntegerField(default=0)),
                ('agreement', models.FloatField(default=0)),
                ('dataset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='main_app.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_brain', models.BooleanField(default=False)),
                ('flag_eyes', models.BooleanField(default=False)),
                ('flag_muscles', models.BooleanField(default=False)),
                ('flag_hearth', models.BooleanField(default=False)),
                ('flag_line_noise', models.BooleanField(default=False)),
                ('flag_ch_noise', models.BooleanField(default=False)),
                ('comment', models.TextField(default='')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.icacomponent')),
            ],
        ),
    ]