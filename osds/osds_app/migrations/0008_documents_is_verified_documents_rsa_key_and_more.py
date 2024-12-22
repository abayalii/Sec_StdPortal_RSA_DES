# Generated by Django 5.1.4 on 2024-12-22 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osds_app', '0007_alter_documents_invoice_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='documents',
            name='rsa_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='osds_app.rsa'),
        ),
        migrations.AddField(
            model_name='documents',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='documents',
            name='verification_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rsa',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]