# Generated by Django 3.0.4 on 2020-08-10 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workerreview', '0005_auto_20200731_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]