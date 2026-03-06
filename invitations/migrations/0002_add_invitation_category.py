# Generated manually for InvitationCategory and category FK

import django.db.models.deletion
from django.db import migrations, models


def create_categories_and_migrate(apps, schema_editor):
    InvitationCategory = apps.get_model('invitations', 'InvitationCategory')
    InvitationTemplate = apps.get_model('invitations', 'InvitationTemplate')

    categories_data = [
        ('uzatu', 'Ұзату той', 0),
        ('qyz_uzatu', 'Қыз ұзату', 1),
        ('sunnet', 'Сүндет той', 2),
        ('tusaukesar', 'Тұсаукесер', 3),
        ('merey', 'Мерей той', 4),
        ('besik', 'Бесік той', 5),
        ('betashar', 'Беташар', 6),
        ('other', 'Асау тойлар', 7),
    ]
    created = {}
    for code, name_kz, order in categories_data:
        cat = InvitationCategory.objects.create(
            code=code,
            name_kz=name_kz,
            order=order,
            is_active=True,
        )
        created[code] = cat

    for t in InvitationTemplate.objects.all():
        if getattr(t, 'category_old', None) and t.category_old in created:
            t.category = created[t.category_old]
            t.save(update_fields=['category'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name_kz', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('name_ru', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('code', models.SlugField(max_length=32, unique=True)),
                ('icon', models.CharField(blank=True, help_text='Icon class or emoji', max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order', 'name_kz'],
                'verbose_name': 'Invitation category',
                'verbose_name_plural': 'Invitation categories',
            },
        ),
        migrations.RenameField(
            model_name='invitationtemplate',
            old_name='category',
            new_name='category_old',
        ),
        migrations.AddField(
            model_name='invitationtemplate',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='templates',
                to='invitations.invitationcategory',
            ),
        ),
        migrations.RunPython(create_categories_and_migrate, noop),
        migrations.RemoveField(
            model_name='invitationtemplate',
            name='category_old',
        ),
    ]
