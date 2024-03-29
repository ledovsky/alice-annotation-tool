# Generated by Django 4.1.5 on 2023-06-04 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0014_auto_20211106_0929'),
        ('main_app', '0002_icaimages_img_sources_plot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icalinks',
            name='next',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='link_from_prev_old', to='data_app.icacomponent'),
        ),
        migrations.AlterField(
            model_name='icalinks',
            name='prev',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='link_from_next_old', to='data_app.icacomponent'),
        ),
        migrations.CreateModel(
            name='ICExtended',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_ready', models.BooleanField(default=False)),
                ('ic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='x', to='data_app.icacomponent')),
                ('next', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='link_from_prev', to='data_app.icacomponent')),
                ('prev', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='link_from_next', to='data_app.icacomponent')),
            ],
        ),
    ]
