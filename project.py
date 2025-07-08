import streamlit as st
import pandas as pd
import plotly.express as px
earth_colors = px.colors.qualitative.Pastel

@st.cache_data
def load_data():
    df = pd.read_excel("Dataset_Hotel_Sales.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df.rename(columns={'(child)': 'child'}, inplace=True)
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    df['arrival_month'] = df['arrival_date'].dt.strftime('%B')
    df['arrival_month_num'] = df['arrival_date'].dt.month
    return df

def tampilkan_dashboard():
    st.subheader("📊 Hotel Sales Dashboard")

    df = load_data()

    hotels = sorted(df['hotel_name'].dropna().unique())
    months = sorted(df['arrival_month'].dropna().unique(), key=lambda m: pd.to_datetime(m, format='%B').month)

    # Sidebar state
    selected_hotel = st.selectbox("🏨 Pilih Hotel:", hotels)
    selected_month = st.selectbox("🗓️ Pilih Bulan:", months)

    # Filter data sesuai input
    filtered_df = df[
        (df['hotel_name'] == selected_hotel) &
        (df['arrival_month'] == selected_month)
    ]

    prev_month_num = pd.to_datetime(selected_month, format='%B').month - 1 or 12

    st.success(f"Menampilkan data untuk: **{selected_hotel} - {selected_month}**")

    # Grafik 1 & 2: Sales per hotel dan per segmen
    col1, col2 = st.columns(2)

    with col1:
        sales_per_hotel = filtered_df.groupby("hotel_name")["sales"].sum().reset_index()
        fig1 = px.bar(sales_per_hotel, x="hotel_name", y="sales", color="hotel_name", color_discrete_sequence=earth_colors,
                      title="Total Net Sales per Hotel", text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        sales_by_seg = filtered_df.groupby(['cus_seg'])['sales'].sum().reset_index()
        fig2 = px.bar(sales_by_seg, x='cus_seg', y='sales', color='cus_seg', color_discrete_sequence=earth_colors,
                      title='Total Sales by Customer Segment', text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)

    # Grafik 3: Jumlah customer per bulan (untuk hotel terpilih saja)
    monthly_customer = df[df['hotel_name'] == selected_hotel] \
    .groupby('arrival_month')['cus_name'].nunique().reset_index()

    monthly_customer.columns = ['Month', 'Customer Count']
    bulan_urut = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    monthly_customer['Month'] = pd.Categorical(monthly_customer['Month'], categories=bulan_urut, ordered=True)
    monthly_customer = monthly_customer.sort_values('Month')

    fig3 = px.line(monthly_customer, x='Month', y='Customer Count',
                   title=f'Customer Count per Month ({selected_hotel})', color_discrete_sequence=earth_colors,
                   markers=True, text='Customer Count')
    fig3.update_traces(textposition="top center")
    st.plotly_chart(fig3, use_container_width=True)


    # Grafik 4: Pie charts
    col3, col4 = st.columns(2)
    with col3:
        customer_per_hotel = df[df['arrival_month'] == selected_month].groupby("hotel_name")["cus_name"].nunique().reset_index()
        fig4 = px.pie(customer_per_hotel, names="hotel_name", values="cus_name", color_discrete_sequence=earth_colors,
                     title="Customer Distribution (All Hotels)", hole=0.4)
        fig4.update_traces(textinfo='percent+label')
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        customer_per_membership = filtered_df.groupby("membership")["cus_name"].nunique().reset_index()
        fig5 = px.pie(customer_per_membership, names="membership", values="cus_name", color_discrete_sequence=earth_colors,
                      title="Customer by Membership", hole=0.4)
        fig5.update_traces(textinfo='percent+label')
        st.plotly_chart(fig5, use_container_width=True)

    # Salesperson performance
    st.header(f"📈 Salesperson Performance - {selected_hotel}, {selected_month}")
    this_month = filtered_df
    last_month = df[
        (df['hotel_name'] == selected_hotel) &
        (df['arrival_month_num'] == prev_month_num)
    ]

    this_sales = this_month.groupby('sales_person')['sales'].sum().reset_index()
    last_sales = last_month.groupby('sales_person')['sales'].sum().reset_index()

    summary = pd.merge(this_sales, last_sales, on='sales_person', how='outer', suffixes=('_this', '_last')).fillna(0)

    cols = st.columns(len(summary)) if len(summary) > 0 else [st]
    for i, row in enumerate(summary.itertuples()):
        current = row.sales_this
        previous = row.sales_last
        delta = current - previous
        cols[i].metric(
            label=row.sales_person,
            value=f"Rp {current:,.0f}",
            delta=f"{delta:,.0f}",
            delta_color="normal"
        )
