"""
Migration: move html_template from DB TextField to file-based template_file CharField.

Steps:
1. Add template_file CharField
2. Populate template_file = slug for all templates that had html_template
3. Remove html_template field
"""

from django.db import migrations, models


def populate_template_file(apps, schema_editor):
    InvitationTemplate = apps.get_model('invitations', 'InvitationTemplate')
    for tmpl in InvitationTemplate.objects.exclude(html_template=''):
        tmpl.template_file = tmpl.slug
        tmpl.save(update_fields=['template_file'])


def reverse_populate(apps, schema_editor):
    """Cannot restore html_template content from files in reverse migration."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0011_fill_empty_templates'),
    ]

    operations = [
        # Step 1: Add template_file
        migrations.AddField(
            model_name='invitationtemplate',
            name='template_file',
            field=models.CharField(
                blank=True,
                help_text='Filename (without .html) in invitations/templates_html/',
                max_length=100,
            ),
        ),
        # Step 2: Copy slug -> template_file for rows that had html_template
        migrations.RunPython(populate_template_file, reverse_populate),
        # Step 3: Remove html_template
        migrations.RemoveField(
            model_name='invitationtemplate',
            name='html_template',
        ),
    ]
