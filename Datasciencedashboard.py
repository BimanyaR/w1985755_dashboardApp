import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

# Loading the dataset
df = pd.read_excel('cleaned_data.xlsx')

# Streamlit app title
st.title("Minger Sales Analysis")

# Creating columns to display total revenue and profit 
col1, col2 = st.columns(2)
total_sales = f"${df['Sales'].sum():,.0f}"
total_profit = f"${df['Profit'].sum():,.0f}"

with col1: 
    st.metric("Total Sales", total_sales)

with col2:
    st.metric("Total Profit", total_profit)

with st.sidebar:
    st.sidebar.header("Select Analysis")
    Analysis = st.radio("", ["Sales Analysis", "Key Insights"])

if Analysis == "Sales Analysis":

    # Filter options for sales analysis
    sales_over_time = df.groupby('Order Date')['Sales'].sum().reset_index()
    fig1 = px.line(sales_over_time, x='Order Date', y='Sales', title='Total Sales Over Time')
    fig1.update_xaxes(title='Order Date')
    fig1.update_yaxes(title='Total Sales')
    st.plotly_chart(fig1)

    country_data = df.groupby('Country').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig2 = px.choropleth(
        country_data,
        locations="Country",
        locationmode='country names',  # Set to match the names in your 'Country' column
        color="Sales",
        hover_name="Country",
        hover_data={"Sales": True, "Profit": True},
        color_continuous_scale=px.colors.sequential.Plasma)
    st.subheader("Sales by Country")
    st.plotly_chart(fig2)

    col1,col2 =st.columns(2)
    with col1:
        sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
        fig3 = px.pie(sales_by_category, values='Sales', names='Category', title='Sales by Category')
        st.plotly_chart(fig3,use_container_width=True)

    with col2:
        sales_by_segment = df.groupby('Segment')['Sales'].sum().reset_index()
        fig4 = px.pie(sales_by_segment, values='Sales', names='Segment', 
              title='Sales by Segment')
        st.plotly_chart(fig4,use_container_width=True)
    
    sales_by_subcategory = df.groupby('Sub-Category')['Sales'].sum().reset_index()
    color_palette = px.colors.qualitative.Set2
    fig5 = px.bar(sales_by_subcategory, x='Sub-Category', y='Sales', 
              title='Sales by Subcategory', 
              labels={'Sub-Category': 'Subcategory', 'Sales': 'Total Sales'},
              color='Sub-Category', color_discrete_sequence=color_palette)
    fig5.update_xaxes(tickangle=45)
    st.plotly_chart(fig5)

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    profit_over_the_years = df.groupby('Year')['Profit'].sum().reset_index()
    fig6 = px.line(profit_over_the_years, x='Year', y='Profit', 
               title='Profit over the years',
               labels={'Year': 'Year', 'Profit': 'Total Profit'})
    fig6.update_traces(line=dict(color='#FF6961', width=2), marker=dict(color='#FF6961', size=8))
    fig6.update_layout(title_font_size=16, title_font_color='white', title_font_family='Arial', title_font_weight='bold',
                   xaxis=dict(title='Year', tickmode='linear', tickfont=dict(size=12), tickangle=45),
                   yaxis=dict(title='Total Profit'))
    st.plotly_chart(fig6) 
    
    sales_by_ship_mode = df.groupby('Ship Mode')['Sales'].sum().reset_index()
    fig7 = px.pie(sales_by_ship_mode, values='Sales', names='Ship Mode', 
             title='Total Sales by Ship Mode')
    st.plotly_chart(fig7)

    product_categories = df['Category'].unique()
    selected_category = st.selectbox('Select Product Category', product_categories)
    filtered_data = df[df['Category'] == selected_category]
    fig8 = px.scatter(filtered_data, x='Discount', y='Sales', title=f'Sales vs. Discount for {selected_category}', labels={'Discount': 'Discount (%)', 'Sales': 'Sales ($)'}, hover_data=['Product Name'], color='Discount', template='simple_white') 
    st.plotly_chart(fig8)



elif Analysis== "Key Insights":
    col1,col2= st.columns(2)
    with col1:
        subcategory_sales = df.groupby('Sub-Category')['Sales'].sum().reset_index()
        top_subcategories = subcategory_sales.sort_values(by='Sales', ascending=False).head(5)
        fig9 = px.bar(top_subcategories, x='Sub-Category', y='Sales', color='Sub-Category', title='Top 5 Subcategories with Highest Sales')
        st.plotly_chart(fig9,use_container_width=True)
    
    with col2:
        profit_by_subcategory = df.groupby('Sub-Category')['Profit'].sum().reset_index()
        top_5_subcategories = profit_by_subcategory.sort_values(by='Profit',ascending=False).head(5)
        fig10 = px.bar(top_5_subcategories, x='Sub-Category', y='Profit', color='Sub-Category',title='Top 5 Subcategories with Highest Profit')
        st.plotly_chart(fig10,use_container_width=True)

    
    avg_discount_by_subcategory = df.groupby('Sub-Category')['Discount'].mean().reset_index()
    fig11 = px.bar(avg_discount_by_subcategory, x='Sub-Category', y='Discount', 
               title='Average Discount by Subcategory',
               labels={'Sub-Category': 'Subcategory', 'Discount': 'Average Discount'},
               color='Sub-Category', color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig11)
    fig12 = px.scatter(df, x='Sales', y='Profit', color='Category', 
                  title='Profit vs. Sales', 
                  labels={'Sales': 'Sales', 'Profit': 'Profit',})
    st.plotly_chart(fig12)
