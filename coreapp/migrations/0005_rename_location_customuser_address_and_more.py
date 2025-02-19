# Generated by Django 5.0.7 on 2024-10-12 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0004_alter_customuser_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='location',
            new_name='address',
        ),
        migrations.AddField(
            model_name='customuser',
            name='addcity',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='addstate',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='addzipcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
