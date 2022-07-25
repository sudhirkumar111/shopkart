# Generated by Django 4.0.4 on 2022-07-25 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0006_shippingdetail_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingdetail',
            name='contact',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shippingdetail',
            name='user',
            field=models.ForeignKey(default='SUDHIR', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
