# Generated by Django 2.1.8 on 2019-07-03 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("contacts", "0102_contacturn_channel")]

    operations = [migrations.AlterField(model_name="contact", name="is_test", field=models.BooleanField(null=True))]
