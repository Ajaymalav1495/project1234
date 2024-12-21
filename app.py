import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Print a welcome message
print("Hello Learners")

# Reading the data from an Excel file
df = pd.read_excel("Adidas.xlsx")

# Setting the page configuration
st.set_page_config(layout="wide")

# Adding custom CSS to modify the padding
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Loading the Adidas logo image
image = Image.open('adidas-logo.jpg')

# Creating two columns for layout
col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image, width=100)

# Custom HTML for the title
html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

# Creating three columns for the layout
col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")

# Displaying a bar chart for Total Sales by Retailer
with col4:
    fig = px.bar(df, x="Retailer", y="TotalSales", labels={"TotalSales": "Total Sales {$}"},
                 title="Total Sales by Retailer", hover_data=["TotalSales"],
                 template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

# Creating layout for viewing and downloading data
_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

# Processing data for the monthly sales line chart
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by=df["Month_Year"])["TotalSales"].sum().reset_index()

# Displaying a line chart for Total Sales Over Time
with col5:
    fig1 = px.line(result, x="Month_Year", y="TotalSales", title="Total Sales Over Time",
                   template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

# Expander for Monthly Sales data
with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Get Data", data=result.to_csv().encode("utf-8"),
                       file_name="MonthlySales.csv", mime="text/csv")

st.divider()

# Processing data for the bar and line chart by State
result1 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

# Adding a bar and line chart for Total Sales and Units Sold by State
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name="Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["UnitsSold"], mode="lines",
                          name="Units Sold", yaxis="y2"))
fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales", showgrid=False),
    yaxis2=dict(title="Units Sold", overlaying="y", side="right"),
    template="gridon",
    legend=dict(x=1, y=1.1)
)
_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width=True)

# Creating layout for viewing and downloading data by units sold
_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("Get Data", data=result1.to_csv().encode("utf-8"),
                       file_name="Sales_by_UnitsSold.csv", mime="text/csv")

st.divider()

# Processing data for the treemap chart
_, col7 = st.columns([0.1, 1])
treemap = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_00_000)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(treemap, path=["Region", "City"], values="TotalSales",
                  hover_name="TotalSales (Formatted)",
                  hover_data=["TotalSales (Formatted)"],
                  color="City", height=700, width=600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4, use_container_width=True)

# Creating layout for viewing and downloading data by region and city
_, view4, dwn4 = st.columns([0.5, 0.45, 0.45])
with view4:
    result2 = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum()
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button("Get Data", data=result2.to_csv().encode("utf-8"),
                       file_name="Sales_by_Region.csv", mime="text/csv")

# Expander for viewing and downloading raw data
_, view5, dwn5 = st.columns([0.5, 0.45, 0.45])
with view5:
    expander = st.expander("View Sales Raw Data")
    expander.write(df)
with dwn5:
    st.download_button("Get Raw Data", data=df.to_csv().encode("utf-8"),
                       file_name="SalesRawData.csv", mime="text/csv")

st.divider()
