# Add subtitle and bg_class to InvitationCategory for fully dynamic frontend

from django.db import migrations, models


def set_subtitle_and_bg(apps, schema_editor):
    InvitationCategory = apps.get_model('invitations', 'InvitationCategory')
    defaults = {
        'uzatu': ('Үйлену', 'bg-amber-50 group-hover:bg-amber-100'),
        'qyz_uzatu': ('Қыз шығару', 'bg-pink-50 group-hover:bg-pink-100'),
        'sunnet': ('Сүндет', 'bg-blue-50 group-hover:bg-blue-100'),
        'tusaukesar': ('Алғашқы қадам', 'bg-green-50 group-hover:bg-green-100'),
        'merey': ('Мерейтой', 'bg-purple-50 group-hover:bg-purple-100'),
        'besik': ('Нәресте', 'bg-yellow-50 group-hover:bg-yellow-100'),
        'betashar': ('Дәстүр', 'bg-rose-50 group-hover:bg-rose-100'),
        'other': ('Басқалары', 'bg-orange-50 group-hover:bg-orange-100'),
    }
    for cat in InvitationCategory.objects.all():
        sub, bg = defaults.get(cat.code, ('Той шақырулары', 'bg-emerald-50 group-hover:bg-emerald-100'))
        cat.subtitle = sub
        cat.bg_class = bg or 'bg-emerald-50 group-hover:bg-emerald-100'
        cat.save(update_fields=['subtitle', 'bg_class'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0002_add_invitation_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitationcategory',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Short subtitle shown under the category name (e.g. Үйлену)', max_length=128),
        ),
        migrations.AddField(
            model_name='invitationcategory',
            name='bg_class',
            field=models.CharField(
                blank=True,
                default='bg-emerald-50 group-hover:bg-emerald-100',
                help_text='Tailwind classes for the icon box, e.g. bg-amber-50 group-hover:bg-amber-100',
                max_length=128,
            ),
        ),
        migrations.RunPython(set_subtitle_and_bg, noop),
    ]
