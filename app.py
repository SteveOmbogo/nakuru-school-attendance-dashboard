
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
# 3. LOAD ATTENDANCE DATA
# ==========================================

df = pd.read_csv(
    "attendance.csv",
    parse_dates=["date"]
)

# ==========================================
# 4. CREATE DATE-RANGE SLIDER
# ==========================================

min_date = df["date"].min().date()
max_date = df["date"].max().date()

# Default reporting period: last 30 calendar days
default_start = max(
    min_date,
    max_date - timedelta(days=29)
)

st.header("Select Reporting Period")

selected_dates = st.slider(
    "Choose the date range:",
    min_value=min_date,
    max_value=max_date,
    value=(default_start, max_date),
    format="DD MMM YYYY"
)

# ==========================================
# 5. FILTER ATTENDANCE DATA
# ==========================================

filtered_df = df[
    df["date"].between(
        pd.Timestamp(selected_dates[0]),
        pd.Timestamp(selected_dates[1])
    )
].copy()

# ==========================================
# 6. CALCULATE ATTENDANCE METRICS
# ==========================================

st.header("Attendance Performance Overview")

if not filtered_df.empty:

    # Calculate overall attendance rate
    overall_rate = (
        filtered_df["students_present"].sum()
        / filtered_df["students_total"].sum()
    ) * 100

    # Calculate attendance performance by class
    class_performance = (
        filtered_df.groupby("class_name")
        [["students_present", "students_total"]]
        .sum()
    )

    class_performance["attendance_rate"] = (
        class_performance["students_present"]
        / class_performance["students_total"]
    ) * 100

    # Identify best and worst attending classes
    best_class = class_performance["attendance_rate"].idxmax()
    worst_class = class_performance["attendance_rate"].idxmin()

    # Display three metrics
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
    # 7. ATTENDANCE BY CLASS
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
    # 8. DAILY ATTENDANCE TREND
    # ==========================================

    st.header("Daily Attendance Trends")

    # Group records by date and class
    daily_attendance = (
        filtered_df.groupby(["date", "class_name"])
        [["students_present", "students_total"]]
        .sum()
        .reset_index()
    )

    # Calculate daily attendance rate
    daily_attendance["attendance_rate"] = (
        daily_attendance["students_present"]
        / daily_attendance["students_total"]
    ) * 100

    # Reshape data: dates as rows, classes as columns
    attendance_chart = daily_attendance.pivot(
        index="date",
        columns="class_name",
        values="attendance_rate"
    )

    # Display line chart
    st.line_chart(
        attendance_chart,
        x_label="Date",
        y_label="Attendance Rate (%)"
    )

    # ==========================================
    # 9. DISPLAY ATTENDANCE RECORDS
    # ==========================================

    with st.expander("View Detailed Attendance Records"):

        st.dataframe(
            filtered_df,
            width="stretch"
        )

    # Display reporting information
    st.caption(
        f"Selected reporting period: "
        f"{selected_dates[0]} to {selected_dates[1]}"
    )

    st.caption(
        f"Attendance records displayed: {len(filtered_df)} "
        f"out of {len(df)} total records."
    )

else:
    st.warning("No attendance records found for the selected dates.")
