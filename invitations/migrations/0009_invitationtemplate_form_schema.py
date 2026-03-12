from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invitations", "0008_alter_invitation_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="invitationtemplate",
            name="form_schema",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="Dynamic form field definitions",
            ),
        ),
    ]
