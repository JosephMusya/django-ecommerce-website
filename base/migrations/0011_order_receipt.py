# Generated by Django 3.2.9 on 2022-02-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.FileField(null=True, upload_to='PDF/'),
        ),
    ]