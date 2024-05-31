# Generated by Django 5.0.3 on 2024-05-31 01:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_uuid',
            field=models.CharField(default=uuid.uuid4, max_length=36, unique=True),
        ),
    ]