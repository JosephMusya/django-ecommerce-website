# Generated by Django 3.2.9 on 2022-02-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_order_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='receipt',
            field=models.FileField(null=True, upload_to='static'),
        ),
    ]
