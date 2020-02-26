# Generated by Django 3.0.3 on 2020-02-25 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postHandler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]