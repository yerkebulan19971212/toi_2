"""
Add dynamic invitation system:
- InvitationTemplate: html_template, css_styles, slug, description, supported_vars, supported_image_layouts
- Invitation: event_title, description, extra_data, image_layout, rendered_html, is_published
  + make bride_name/groom_name/time/location optional
- New models: InvitationImage, GuestComment, RSVPResponse
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0003_invitationcategory_subtitle_bg_class'),
    ]

    operations = [
        # ------------------------------------------------------------------
        # InvitationTemplate — new fields
        # ------------------------------------------------------------------
        migrations.AddField(
            model_name='invitationtemplate',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='invitationtemplate',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='invitationtemplate',
            name='html_template',
            field=models.TextField(
                blank=True,
                help_text='Jinja2 HTML. Variables: {{ event_title }}, {{ event_date }}, {{ images }}, etc.',
            ),
        ),
        migrations.AddField(
            model_name='invitationtemplate',
            name='css_styles',
            field=models.TextField(blank=True, help_text='Scoped CSS injected into the template'),
        ),
        migrations.AddField(
            model_name='invitationtemplate',
            name='supported_vars',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='invitationtemplate',
            name='supported_image_layouts',
            field=models.JSONField(blank=True, default=list),
        ),

        # ------------------------------------------------------------------
        # Invitation — make existing fields optional + add new ones
        # ------------------------------------------------------------------
        migrations.AlterField(
            model_name='invitation',
            name='bride_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='groom_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='invitation',
            name='event_title',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='invitation',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='extra_data',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='invitation',
            name='image_layout',
            field=models.CharField(
                blank=True,
                choices=[
                    ('gallery_top', 'Gallery — Top'),
                    ('gallery_bottom', 'Gallery — Bottom'),
                    ('gallery_grid', '2×N Grid'),
                    ('single_hero', 'Single Hero Image'),
                ],
                default='gallery_top',
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='invitation',
            name='rendered_html',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='is_published',
            field=models.BooleanField(default=False),
        ),

        # ------------------------------------------------------------------
        # InvitationImage
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name='InvitationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=1000)),
                ('placement', models.CharField(
                    choices=[
                        ('gallery_top', 'Gallery Top'),
                        ('gallery_bottom', 'Gallery Bottom'),
                        ('gallery_grid', 'Gallery Grid'),
                        ('single_hero', 'Single Hero'),
                    ],
                    default='gallery_top',
                    max_length=50,
                )),
                ('caption', models.CharField(blank=True, max_length=300)),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invitation', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='images',
                    to='invitations.invitation',
                )),
            ],
            options={'ordering': ['sort_order']},
        ),

        # ------------------------------------------------------------------
        # GuestComment
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name='GuestComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_name', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('is_approved', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invitation', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments',
                    to='invitations.invitation',
                )),
            ],
            options={'ordering': ['-created_at']},
        ),

        # ------------------------------------------------------------------
        # RSVPResponse
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name='RSVPResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('response', models.CharField(
                    choices=[
                        ('solo', 'Иә, жалғыз өзім барамын!'),
                        ('with_partner', 'Жұбайыммен бірге барамын'),
                        ('declined', 'Өкінішке орай, келе алмаймын'),
                    ],
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invitation', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='rsvp_responses',
                    to='invitations.invitation',
                )),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.AddConstraint(
            model_name='rsvpresponse',
            constraint=models.UniqueConstraint(
                fields=['invitation', 'phone'],
                name='unique_rsvp_per_phone',
                condition=models.Q(phone__gt=''),  # only enforce when phone is not blank
            ),
        ),
    ]
