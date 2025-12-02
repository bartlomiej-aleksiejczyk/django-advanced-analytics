from django.db import models


class Note(models.Model):
    class NoteType(models.TextChoices):
        TEXT = "TEXT", "Text"
        TODO = "TODO", "Todo"
        JSON = "JSON", "JSON"

    type = models.CharField(
        max_length=10,
        choices=NoteType.choices,
        default=NoteType.TEXT,
    )
    content = models.TextField(
        help_text="Text body or JSON string, depending on the type."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()} note #{self.pk}"


class NoteAttachment(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file = models.FileField(upload_to="notes/attachments/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_name = models.CharField(max_length=255, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.original_name or self.file.name
