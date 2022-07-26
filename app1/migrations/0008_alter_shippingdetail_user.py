# Generated by Django 4.0.4 on 2022-07-26 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0007_alter_shippingdetail_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingdetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
