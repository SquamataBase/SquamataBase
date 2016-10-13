# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-09 16:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Glossary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Glossary.OntologyTerm'))
            ],
            options={
                'verbose_name_plural': 'Data sources',
                'verbose_name': 'Data source',
                'db_table': 'sb_ref',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'people',
                'db_table': 'sb_person',
            },
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Glossary.OntologyTerm')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Bibliography.Person')),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Bibliography.Ref')),
            ],
            options={
                'db_table': 'sb_contribution',
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal_name', models.CharField(max_length=255)),
                ('issn', models.CharField(blank=True, max_length=255, null=True)),
                ('prior_names', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sb_journal',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Bibliography.Ref')),
                ('title', models.CharField(max_length=255)),
                ('year_published', models.IntegerField()),
                ('publisher', models.CharField(blank=True, max_length=255, null=True)),
                ('pages', models.IntegerField(blank=True, null=True)),
                ('isbn', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'sb_book',
            },
        ),
        migrations.CreateModel(
            name='BookChapter',
            fields=[
                ('ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Bibliography.Ref')),
                ('title', models.CharField(max_length=255)),
                ('page_start', models.CharField(max_length=255)),
                ('page_end', models.CharField(max_length=255)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Bibliography.Book')),
            ],
            options={
                'db_table': 'sb_book_chapter',
            },
        ),
        migrations.CreateModel(
            name='JournalArticle',
            fields=[
                ('ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Bibliography.Ref')),
                ('title', models.CharField(max_length=255)),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Bibliography.Journal')),
                ('volume', models.CharField(max_length=255)),
                ('issue', models.CharField(blank=True, max_length=255, null=True)),
                ('year_published', models.IntegerField()),
                ('page_start', models.CharField(max_length=255)),
                ('page_end', models.CharField(max_length=255)),
                ('doi', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'sb_journal_article',
            },
        ),
    ]
