# Generated by Django 5.1.4 on 2024-12-21 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osds_app', '0005_alter_documents_invoice_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='invoice_file',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]
