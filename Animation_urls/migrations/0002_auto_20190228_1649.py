# Generated by Django 2.1.5 on 2019-02-28 08:49

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Animation_urls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animation',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
