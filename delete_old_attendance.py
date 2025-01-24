import os
import django

# Initialize Django settings
if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aps.settings")
django.setup()

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import transaction
from emp.models import Attendance


def delete_old_attendance():
    try:
        # Calculate the threshold date (4 months ago)
        threshold_date = datetime.now() - relativedelta(months=5)
        # print(threshold_date)
        # Sanity check for threshold_date
        if threshold_date > datetime.now():
            raise ValueError("Threshold date is in the future. Aborting delete operation.")

        # Fetch attendance records older than the threshold
        old_records = Attendance.objects.filter(date__lt=threshold_date)
        total_records = old_records.count()

        if total_records == 0:
            print("No old attendance records found.")
            return

        # Delete in batches to avoid database lock issues
        batch_size = 500
        while old_records.exists():
            with transaction.atomic():
                old_records[:batch_size].delete()
            print(f"Deleted a batch of up to {batch_size} records.")

        print(f"Successfully deleted {total_records} attendance records older than {threshold_date.date()}.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    delete_old_attendance()

