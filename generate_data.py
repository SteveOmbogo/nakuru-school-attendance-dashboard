import csv
import random
from datetime import date, timedelta

# Make our sample data reproducible
random.seed(42)

# Define our five classes and their student populations
classes = {
    "Grade 1": 42,
    "Grade 2": 40,
    "Grade 3": 38,
    "Grade 4": 45,
    "Grade 5": 41
}

# Define the starting attendance rate for each class
base_rates = {
    "Grade 1": 0.96,
    "Grade 2": 0.94,
    "Grade 3": 0.92,
    "Grade 4": 0.90,
    "Grade 5": 0.88
}

# Start date for our eight-week dataset
start_date = date(2026, 9, 1)

# Store all attendance records here
attendance_records = []

# Generate 40 school days (Monday to Friday)
school_days = []
current_date = start_date

while len(school_days) < 40:

    # weekday() returns 0 for Monday and 6 for Sunday
    if current_date.weekday() < 5:
        school_days.append(current_date)

    current_date += timedelta(days=1)


# Generate attendance records for every class and school day
for day_number, school_date in enumerate(school_days):

    for class_name, students_total in classes.items():

        # Grade 4 experiences a gradual attendance decline
        decline = 0

        if class_name == "Grade 4":
            decline = day_number * 0.002

        # Introduce small random daily variations
        variation = random.uniform(-0.025, 0.025)

        attendance_rate = (
            base_rates[class_name] - decline + variation
        )

        # Keep attendance within realistic limits
        attendance_rate = max(0.70, min(0.99, attendance_rate))

        students_present = round(
            students_total * attendance_rate
        )

        attendance_records.append({
            "date": school_date,
            "class_name": class_name,
            "students_present": students_present,
            "students_total": students_total
        })


# Write the records into a CSV file
with open("attendance.csv", "w", newline="") as file:

    fieldnames = [
        "date",
        "class_name",
        "students_present",
        "students_total"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(attendance_records)


print("Attendance dataset generated successfully!")
print(f"Total attendance records: {len(attendance_records)}")
print(f"Number of school days: {len(school_days)}")
print(f"Number of classes: {len(classes)}")