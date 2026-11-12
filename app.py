

import streamlit as st
import pandas as pd
from datetime import timedelta

# ==========================================
# 1. CONFIGURE THE WEB APPLICATION
# ==========================================

st.set_page_config(
    page_title="Nakuru School Attendance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. APPLICATION TITLE
# ==========================================

st.title("Nakuru School Attendance Dashboard")

st.write(
    "Monitor student attendance across different classes "
    "and track attendance trends over time."
)

# ==========================================
# 3. UPLOAD AND LOAD ATTENDANCE DATA
# ==========================================

st.header("Upload Attendance Sheet")

uploaded_file = st.file_uploader(
    "Upload your attendance CSV file",
    type=["csv"]
)

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("attendance.csv")

except FileNotFoundError:
    st.error("The default attendance.csv file could not be found.")
    st.stop()

except pd.errors.EmptyDataError:
    st.error("The uploaded CSV file is empty.")
    st.stop()

except Exception as e:
    st.error(f"Unable to read the CSV file: {e}")
    st.stop()

# Required columns
required_columns = [
    "date",
    "class_name",
    "students_present",
    "students_total"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Missing required columns: {', '.join(missing_columns)}"
    )
    st.stop()

if df.empty:
    st.warning("The attendance file contains no records.")
    st.stop()

# Convert columns into appropriate data types
df["date"] = pd.to_datetime(df["date"], errors="coerce")

df["students_present"] = pd.to_numeric(
    df["students_present"], errors="coerce"
)

df["students_total"] = pd.to_numeric(
    df["students_total"], errors="coerce"
)

# Remove invalid records
df = df.dropna(subset=required_columns)

df = df[
    (df["students_total"] > 0)
    & (df["students_present"] >= 0)
    & (df["students_present"] <= df["students_total"])
].copy()

if df.empty:
    st.error("No valid attendance records were found in this file.")
    st.stop()

# ==========================================
# 4. FILTER ATTENDANCE BY CLASS
# ==========================================

st.header("Filter Attendance by Class")

class_options = ["All Classes"] + sorted(
    df["class_name"].astype(str).unique().tolist()
)

selected_class = st.selectbox(
    "Select Class:",
    class_options
)

# ==========================================
# 5. SELECT REPORTING PERIOD
# ==========================================

min_date = df["date"].min().date()
max_date = df["date"].max().date()

default_start = max(
    min_date,
    max_date - timedelta(days=29)
)

st.header("Select Reporting Period")

selected_dates = st.date_input(
    "Choose the reporting period:",
    value=(default_start, max_date),
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY"
)

# ==========================================
# 6. FILTER ATTENDANCE DATA
# ==========================================

if len(selected_dates) != 2:
    st.info("Please select both a start date and an end date.")
    st.stop()

filtered_df = df[
    df["date"].between(
        pd.Timestamp(selected_dates[0]),
        pd.Timestamp(selected_dates[1])
    )
].copy()

if selected_class != "All Classes":
    filtered_df = filtered_df[
        filtered_df["class_name"].astype(str) == selected_class
    ].copy()

# ==========================================
# 7. CALCULATE ATTENDANCE METRICS
# ==========================================

st.header("Attendance Performance Overview")

if not filtered_df.empty:

    overall_rate = (
        filtered_df["students_present"].sum()
        / filtered_df["students_total"].sum()
    ) * 100

    class_performance = (
        filtered_df.groupby("class_name")
        [["students_present", "students_total"]]
        .sum()
    )

    class_performance["attendance_rate"] = (
        class_performance["students_present"]
        / class_performance["students_total"]
    ) * 100

    best_class = class_performance["attendance_rate"].idxmax()
    worst_class = class_performance["attendance_rate"].idxmin()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Overall Attendance",
            value=f"{overall_rate:.2f}%"
        )

    with col2:
        st.metric(
            label="Best Attending Class",
            value=best_class,
            delta=f"{class_performance.loc[best_class, 'attendance_rate']:.2f}% attendance"
        )

    with col3:
        st.metric(
            label="Worst Attending Class",
            value=worst_class,
            delta=f"{class_performance.loc[worst_class, 'attendance_rate']:.2f}% attendance"
        )

    # ==========================================
    # 8. ATTENDANCE BY CLASS
    # ==========================================

    st.header("Attendance by Class")

    class_display = class_performance[
        ["students_present", "students_total", "attendance_rate"]
    ].copy()

    class_display["attendance_rate"] = (
        class_display["attendance_rate"].round(2)
    )

    st.dataframe(
        class_display,
        width="stretch"
    )

    # ==========================================
    # 9. DAILY ATTENDANCE TRENDS
    # ==========================================

    st.header("Daily Attendance Trends")

    daily_attendance = (
        filtered_df.groupby(["date", "class_name"])
        [["students_present", "students_total"]]
        .sum()
        .reset_index()
    )

    daily_attendance["attendance_rate"] = (
        daily_attendance["students_present"]
        / daily_attendance["students_total"]
    ) * 100

    attendance_chart = daily_attendance.pivot(
        index="date",
        columns="class_name",
        values="attendance_rate"
    )

    st.line_chart(
        attendance_chart,
        x_label="Date",
        y_label="Attendance Rate (%)"
    )

    # ==========================================
    # 10. DISPLAY ATTENDANCE RECORDS
    # ==========================================

    with st.expander("View Detailed Attendance Records"):

        st.dataframe(
            filtered_df,
            width="stretch"
        )

    st.caption(
        f"Selected reporting period: "
        f"{selected_dates[0]} to {selected_dates[1]}"
    )

    st.caption(
        f"Attendance records displayed: {len(filtered_df)} "
        f"out of {len(df)} valid records."
    )

    # ==========================================
    # 11. DOWNLOAD FILTERED ATTENDANCE REPORT
    # ==========================================

    st.header("Download Attendance Report")

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Attendance CSV",
        data=csv_data,
        file_name="filtered_attendance_report.csv",
        mime="text/csv"
    )

else:
    st.warning(
        "No attendance records found for the selected class and dates."
    )
