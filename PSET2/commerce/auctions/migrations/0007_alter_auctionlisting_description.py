# Generated by Django 4.2.11 on 2024-10-25 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='description',
            field=models.TextField(),
        ),
    ]
