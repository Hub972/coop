# Generated by Django 2.2.5 on 2019-09-27 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20190927_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='idSeller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
