# Generated by Django 3.2.9 on 2022-02-04 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Dispatched', 'Dispatched'), ('Delivered', 'Delivered')], default='Pending', max_length=50),
        ),
    ]
