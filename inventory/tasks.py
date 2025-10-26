import csv
from celery import shared_task
from django.utils import timezone
from .models import Part, ImportTask


@shared_task
def import_csv_task(task_id):
    try:
        task = ImportTask.objects.get(id=task_id)
        task.status = "in_progress"
        task.save(update_fields=["status"])

        total_imported = 0
        with open(task.file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                part, created = Part.objects.update_or_create(
                    name=row["name"],
                    defaults={
                        "description": row.get("description", ""),
                        "price": float(row.get("price", 0)),
                        "quantity": int(row.get("quantity", 0)),
                        "category": row.get("category", ""),
                    }
                )
                total_imported += 1

        task.total_imported = total_imported
        task.status = "done"
        task.finished_at = timezone.now()
        task.save(update_fields=["total_imported", "status", "finished_at"])

    except Exception as e:
        task.status = "error"
        task.finished_at = timezone.now()
        task.save(update_fields=["status", "finished_at"])
        raise e

@shared_task
def daily_stock_replenish(minimum_stock=10):
    parts_low_stock = Part.objects.filter(quantity__lt=minimum_stock)
    for part in parts_low_stock:
        part.quantity = minimum_stock
        part.save(update_fields=["quantity"])
