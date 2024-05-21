# Generated by Django 4.2.8 on 2024-05-21 11:04

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult', models.BooleanField(null=True)),
                ('backdrop_path', models.TextField(null=True)),
                ('budget', models.BigIntegerField(null=True)),
                ('imdb_id', models.TextField(null=True)),
                ('origin_country', models.CharField(max_length=100, null=True)),
                ('original_language', models.CharField(max_length=100, null=True)),
                ('original_title', models.CharField(max_length=300, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('popularity', models.FloatField(null=True)),
                ('poster_path', models.TextField(null=True)),
                ('release_date', models.DateField(default=datetime.date.today, null=True)),
                ('revenue', models.BigIntegerField(null=True)),
                ('runtime', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('tagline', models.TextField(null=True)),
                ('title', models.CharField(max_length=300)),
                ('video', models.TextField(null=True)),
                ('vote_average', models.FloatField(null=True)),
                ('vote_count', models.IntegerField(null=True)),
                ('detail_count', models.IntegerField(null=True)),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.genre')),
                ('keyword', models.ManyToManyField(blank=True, related_name='movies', to='movies.keyword')),
                ('like_user', models.ManyToManyField(blank=True, related_name='like_movie', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult', models.BooleanField(null=True)),
                ('biography', models.TextField(null=True)),
                ('birthday', models.DateField(null=True)),
                ('deathday', models.DateField(null=True)),
                ('gender', models.CharField(max_length=20)),
                ('imdb_id', models.CharField(max_length=100, null=True)),
                ('known_for_department', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
                ('place_of_birth', models.TextField(null=True)),
                ('popularity', models.FloatField(null=True)),
                ('profile_path', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PeopleLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.people')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='people',
            field=models.ManyToManyField(related_name='filmography', to='movies.people'),
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(null=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
    ]
