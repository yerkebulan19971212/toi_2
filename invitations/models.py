from django.db import models


class Invitation(models.Model):
  slug = models.SlugField(unique=True)
  title = models.CharField(max_length=255, blank=True)
  couple_names = models.CharField(max_length=255)
  date = models.CharField(max_length=128)
  time = models.CharField(max_length=64)
  location = models.CharField(max_length=255)
  description = models.TextField(blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return self.title or self.couple_names


class Guest(models.Model):
  invitation = models.ForeignKey(
      Invitation, related_name="guests", on_delete=models.CASCADE
  )
  name = models.CharField(max_length=255)
  phone = models.CharField(max_length=32, blank=True)
  status = models.CharField(
      max_length=32,
      choices=[
          ("yes", "Қатысады"),
          ("no", "Қатыса алмайды"),
          ("maybe", "Әлі ойлануда"),
      ],
      default="maybe",
  )
  table_number = models.PositiveIntegerField(null=True, blank=True)
  notes = models.TextField(blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return f"{self.name} ({self.invitation.slug})"
