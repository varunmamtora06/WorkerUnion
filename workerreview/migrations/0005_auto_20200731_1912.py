# Generated by Django 3.0.4 on 2020-07-31 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workerreview', '0004_auto_20200728_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='body',
            field=models.TextField(),
        ),
    ]
