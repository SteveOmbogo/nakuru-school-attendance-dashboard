# Nakuru School Attendance Dashboard

## Project Overview

The Nakuru School Attendance Dashboard is an interactive data application developed using Python, Streamlit and Pandas.

It helps school administrators monitor student attendance, compare class performance and identify attendance trends over time without manually opening Excel spreadsheets.

## Key Features

- **Overall Attendance Rate:** Displays the overall percentage of students attending school.
- **Best-Attending Class:** Identifies the class with the highest attendance rate.
- **Worst-Attending Class:** Identifies the class with the lowest attendance rate.
- **Attendance by Class:** Displays attendance statistics for individual classes.
- **Interactive Date Filter:** Allows users to select a reporting period.
- **Attendance Trend Analysis:** Displays a line chart showing daily attendance rates across five classes.
- **Detailed Records:** Allows users to inspect attendance records for the selected period.

## Technologies Used

- Python
- Streamlit
- Pandas
- CSV for sample data storage

## Project Structure

```text
nakuru_school_attendance/
│
├── app.py
├── generate_data.py
├── attendance.csv
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate into the project directory

```bash
cd nakuru_school_attendance
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your default web browser.

## CSV Data Format

The application expects an attendance CSV file named `attendance.csv`.

The CSV must contain the following columns:

| Column | Description |
|---|---|
| date | Date of attendance |
| class_name | Name of the class |
| students_present | Number of students present |
| students_total | Total registered students |

Example:

```csv
date,class_name,students_present,students_total
2026-09-01,Grade 1,40,42
2026-09-01,Grade 2,38,40
2026-09-01,Grade 3,35,38
```

Each row represents one class's attendance on a particular school day.

The application calculates attendance rates using:

Attendance Rate = (Students Present / Students Total) × 100

## Sample Dataset

The project includes a sample dataset covering eight weeks of school attendance across five classes, with 200 attendance records.

To regenerate the sample dataset, run:

```bash
python generate_data.py
```

## Analytical Approach

Pandas is used to:

- Load and process attendance records.
- Filter records by date.
- Group attendance data by class.
- Calculate weighted attendance rates.
- Reshape data for time-series visualization.

Streamlit provides the interactive web interface through which users explore the results.

## Author

Developed as a practical Python data analytics and Streamlit application project.