# Generated by Django 3.2.8 on 2021-10-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_userfollows'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfollows',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='userfollows',
            constraint=models.UniqueConstraint(
                fields=('user', 'followed_user'), name='unique_user'),
        ),
    ]
