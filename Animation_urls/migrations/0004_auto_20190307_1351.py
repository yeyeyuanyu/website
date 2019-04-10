# Generated by Django 2.1.5 on 2019-03-07 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Animation_urls', '0003_animation_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='Read',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='animation',
            name='read',
        ),
        migrations.AddField(
            model_name='read',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='Animation_urls.Animation'),
        ),
    ]
