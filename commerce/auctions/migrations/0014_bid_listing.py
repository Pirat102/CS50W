# Generated by Django 4.2.11 on 2024-10-26 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_rename_current_bid_bid_bid_remove_bid_listing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]