import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_excel("Dataset_Hotel_Sales.xlsx")
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    return df

def tampilkan_segmentasi():
    st.title("Customer Segmentation using RFM Analysis")

    df = load_data()

    # RFM Preparation
    df = df.sort_values(by='arrival_date')
    latest_hotel = df.groupby('cus_name').last().reset_index()

    rfm = df.groupby("cus_name").agg({
        "arrival_date": "max",
        "hotel_name": pd.Series.nunique,
        "sales": "sum"
    }).reset_index()

    rfm.columns = ["cus_name", "Last_Transaction", "Frequency", "Total_Transaction"]
    rfm = rfm.merge(latest_hotel[['cus_name', 'hotel_name']], on='cus_name', how='left')

    today = pd.Timestamp.today()
    rfm["Recency"] = (today - rfm["Last_Transaction"]).dt.days

    # RFM Scoring
    r_cut1 = rfm["Recency"].quantile(1/3)
    r_cut2 = rfm["Recency"].quantile(2/3)
    rfm["R_Score"] = rfm["Recency"].apply(lambda x: 3 if x <= r_cut1 else (2 if x <= r_cut2 else 1))
    rfm["F_Score"] = rfm["Frequency"]

    m_cut1 = rfm["Total_Transaction"].quantile(1/3)
    m_cut2 = rfm["Total_Transaction"].quantile(2/3)
    rfm["M_Score"] = rfm["Total_Transaction"].apply(lambda x: 3 if x >= m_cut2 else (2 if x >= m_cut1 else 1))

    rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

    # Segment Assignment
    def segment(row):
        score = int(row["R_Score"]) + int(row["F_Score"]) + int(row["M_Score"])
        if score >= 9:
            return "Champion"
        elif score >= 8:
            return "Loyal"
        elif score >= 7:
            return "Potential Loyalist"
        elif score >= 6 and row["R_Score"] == 3:
            return "Recent Customer"
        elif score >= 6 and row["R_Score"] == 1:
            return "Cannot Loose Them"
        elif score >= 6:
            return "Average"
        elif 4 <= score <= 5:
            return "About To Sleep"
        else:
            return "Lost Customer"

    rfm["Segment"] = rfm.apply(segment, axis=1)

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Data")
    selected_segment = st.sidebar.multiselect("Pilih Segmentasi Customer", options=rfm["Segment"].unique(), default=rfm["Segment"].unique())
    selected_hotel = st.sidebar.multiselect("Pilih Nama Hotel", options=rfm["hotel_name"].unique(), default=rfm["hotel_name"].unique())

    filtered_rfm = rfm[(rfm["Segment"].isin(selected_segment)) & (rfm["hotel_name"].isin(selected_hotel))]

    # ⬜ Checkbox Tabel RFM
    if st.checkbox("Tampilkan Tabel RFM"):
        st.subheader("📄 Tabel RFM Customer")
        st.dataframe(filtered_rfm)

    # 🎯 PIE CHART: % RFM Score by Hotel
    rfm_hotel_total = filtered_rfm.groupby("hotel_name")["Total_Transaction"].sum().reset_index()
    rfm_hotel_total.columns = ["Hotel", "Total_RFM_Score"]
    fig_pie = px.pie(
        rfm_hotel_total,
        names="Hotel",
        values="Total_RFM_Score",
        title="% RFM Score by Hotel Name",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # 📈 REVIEW CHART: Customer & Total Sales
    review_stats = df[df["cus_name"].isin(filtered_rfm["cus_name"])].groupby("customer_review").agg({
        "cus_name": pd.Series.nunique,
        "sales": "sum"
    }).reset_index()
    review_stats.columns = ["Customer Review", "Customer Count", "Total Sales"]

    pastel_colors = px.colors.qualitative.Pastel

    def short_number(n):
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        elif n >= 1_000:
            return f"{n/1_000:.0f}K"
        else:
            return str(n)

    bar = go.Bar(
        x=review_stats["Customer Review"],
        y=review_stats["Customer Count"],
        name="Jumlah Customer",
        marker_color=pastel_colors[0],
        yaxis='y1',
        text=[short_number(x) for x in review_stats["Customer Count"]],
        textposition='inside',
        textfont=dict(color='white', size=14)
    )

    line = go.Scatter(
        x=review_stats["Customer Review"],
        y=review_stats["Total Sales"],
        name="Total Sales",
        mode='lines+markers+text',
        text=[short_number(x) for x in review_stats["Total Sales"]],
        textposition='top center',
        marker=dict(color=pastel_colors[1]),
        line=dict(color=pastel_colors[1]),
        textfont=dict(color='green', size=14),
        yaxis='y2'
    )

    fig_review = go.Figure(data=[bar, line])
    fig_review.update_layout(
        title="Jumlah Customer dan Total Sales berdasarkan Customer Review",
        xaxis_title="Customer Review",
        yaxis=dict(
            title=dict(text="Jumlah Customer", font=dict(color=pastel_colors[0])),
            tickfont=dict(color=pastel_colors[0])
        ),
        yaxis2=dict(
            title=dict(text="Total Sales", font=dict(color=pastel_colors[1])),
            tickfont=dict(color=pastel_colors[1]),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        # ✅ Legend di bawah judul
        legend=dict(
            x=0.5,
            y=1.02,  # dari 1.15 → ke 1.02 agar tidak bertabrakan dengan judul
            xanchor="center",
            orientation="h"
        ),
        margin=dict(t=100, b=40)  # Tambah top margin agar judul punya ruang
    )
    # 🧱 Layout: Kanan-Kiri
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏨 % RFM Score by Hotel Name")
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.subheader("📊 Jumlah Customer dan Total Sales berdasarkan Customer Review")
        st.plotly_chart(fig_review, use_container_width=True)

    # 📊 Bar Chart Segmentasi
    st.subheader("📦 Customer Count by Segment")
    seg_count = filtered_rfm["Segment"].value_counts().reset_index()
    seg_count.columns = ["Segment", "Count"]
    fig_bar = px.bar(
        seg_count, x="Segment", y="Count", color="Segment",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Customer Count by Segment"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 📌 Rekomendasi Bisnis
    with st.expander("📌 Business Recommendations Based on Segmentation"):
        st.markdown("""
        ### 1. 🔁 Strengthen Engagement with At-Risk Customers
        - Launch reactivation campaigns with personalized emails and special offers.
        - Offer incentives for return visits, such as discounts or free upgrades.

        ### 2. 🌱 Convert Potential Loyalists and Average Customers
        - Promote loyalty programs and exclusive benefits.
        - Use targeted promotions to encourage more frequent stays and larger bookings.

        ### 3. 📉 Optimize Off-Peak Months
        - Run seasonal promotions or host special events to boost occupancy.
        - Offer bundle deals (e.g., spa + room, dining + stay) to increase average spend.

        ### 4. 💎 Enhance Value for Gold and Platinum Members
        - Offer exclusive perks to Gold members to retain and upgrade them.
        - Reassess Platinum member benefits to encourage higher spend.

        ### 5. 🏆 Empower Top-Performing Sales Staff
        - Incentivize top performers with bonuses or recognition.
        - Use their methods as best practices for training new staff.

        ### 6. 👨‍💼👨‍👩‍👧 Focus on Corporate and Family Segments
        - Offer corporate packages (meeting rooms, long-stay discounts).
        - Develop family-friendly amenities (kids’ activities, adjoining rooms).
        """)
