# Generated by Django 3.0.4 on 2020-03-16 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_questionuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionuser',
            options={'verbose_name': 'QuestionUser', 'verbose_name_plural': 'QuestionUsers'},
        ),
        migrations.AlterModelOptions(
            name='quizuser',
            options={'verbose_name': 'QuizUser', 'verbose_name_plural': 'QuizUsers'},
        ),
        migrations.AlterField(
            model_name='quizuser',
            name='date_finished',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
