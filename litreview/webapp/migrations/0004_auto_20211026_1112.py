# Generated by Django 3.2.8 on 2021-10-26 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20211026_1107'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userfollows',
            name='unique_user',
        ),
        migrations.AddConstraint(
            model_name='userfollows',
            constraint=models.UniqueConstraint(
                fields=('user', 'followed_user'), name='unique_user_follower'),
        ),
    ]
