# Generated by Django 3.0.4 on 2020-03-31 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200331_1154'),
        ('user', '0002_auto_20200331_1553'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuizUser',
            new_name='UserQuiz',
        ),
        migrations.AlterModelOptions(
            name='userquiz',
            options={'verbose_name': 'UserQuiz', 'verbose_name_plural': 'UserQuizs'},
        ),
    ]
