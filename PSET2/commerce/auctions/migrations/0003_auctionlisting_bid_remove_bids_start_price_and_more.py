# Generated by Django 4.2.11 on 2024-10-24 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlistings_bids'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('photo', models.URLField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_bid', models.DecimalField(blank=True, decimal_places=2, default=1, max_digits=6)),
                ('initial_price', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='initial_price', to='auctions.auctionlisting')),
            ],
        ),
        migrations.RemoveField(
            model_name='bids',
            name='start_price',
        ),
        migrations.DeleteModel(
            name='AuctionListings',
        ),
        migrations.DeleteModel(
            name='Bids',
        ),
    ]