# Generated by Django 3.0.7 on 2020-07-25 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200725_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='calldetailrecord',
            name='timebucket',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]