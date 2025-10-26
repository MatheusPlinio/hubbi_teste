from django.db import models
from django.conf import settings


class Part(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "parts"
        verbose_name = "part"
        verbose_name_plural = "part"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.quantity} unid.)"

    def is_below_minimum(self):
        return self.quantity < 10

    def replenish_stock(self, minimum: int = 10):
        if self.quantity < minimum:
            self.quantity = minimum
            self.save(update_fields=["quantity"])


class ImportTask(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "IN Progress"),
        ("done", "Done"),
        ("error", "Error"),
    ]

    file_path = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    total_imported = models.PositiveIntegerField(default=0)
    executed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="import_tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "import_tasks"
        verbose_name = "Import Task"
        verbose_name_plural = "Import Tasks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Import #{self.id} - {self.status}"
