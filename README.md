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

## Features

- Upload attendance records using CSV files.
- Filter attendance by class.
- Select a custom reporting date range.
- View overall attendance performance.
- Compare attendance across classes.
- Monitor daily attendance trends.
- View detailed attendance records.
- Download filtered attendance reports as CSV files.

## How to Use

1. Open the dashboard.
2. Upload an attendance CSV file.
3. Select a class or choose All Classes.
4. Select the reporting date range.
5. Review the attendance metrics and charts.
6. Download the filtered attendance report.

### Required CSV Columns

The attendance file must contain:

- `date`
- `class_name`
- `students_present`
- `students_total`

## Project Pricing

### Proposed Development Fee

My proposed introductory price for building and deploying this attendance dashboard is:

**KSh 20,000 per school.**

This covers:
- Dashboard development.
- CSV upload functionality.
- Attendance filtering and reporting.
- Data visualizations.
- Deployment and initial setup.
- Basic user guidance.

Hosting, ongoing maintenance, advanced security, authentication and additional features would be quoted separately.

### Pricing Model

I would charge per school rather than per teacher.

A school is the main client and benefits from a shared attendance reporting system. Charging per teacher could discourage adoption as more teachers join.

### Future Improvements

- Teacher login and authentication.
- Role-based access to individual class records.
- Secure storage of attendance data.
- Automated weekly and monthly reports.
- School-wide attendance summaries.

**Security note:** The current dashboard uses uploaded CSV files and filtering controls. It does not yet provide secure teacher-specific access. Authentication and server-side authorization would be required before using it for confidential multi-teacher access.
