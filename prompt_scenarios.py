import streamlit as st

# Data from the image
business_problems = {
    "Profitability by Customer Segment": {"Visualization Type": "Bar chart (Profit by Segment, % of total)", "Complexity": "Easy"},
    "Top 10 Products by Sales Volume": {"Visualization Type": "Horizontal bar chart (Product Name vs Sales)", "Complexity": "Easy"},
    "Customer Profitability Analysis": {"Visualization Type": "Table or bar chart (Top 10 Customers by Total Profit)", "Complexity": "Easy"},
    "Sales Distribution Across Regions": {"Visualization Type": "Pie chart (Region-wise Sales %)", "Complexity": "Easy"},
    "Segment-wise Purchase Behavior": {"Visualization Type": "Bar chart (Avg Quantity Purchased per Segment)", "Complexity": "Easy"},
    "Top 5 Most Profitable Cities": {"Visualization Type": "Horizontal bar chart (City vs Total Profit)", "Complexity": "Easy"},
    "Profit Relationship Across Product Categories": {"Visualization Type": "Scatter plot (Sales vs Profit, point size = Quantity)", "Complexity": "Medium"},
    "Regional Profit Contribution": {"Visualization Type": "Stacked bar chart (Profit by Region and Category)", "Complexity": "Medium"},
    "Impact of Discounts on Profit Margins": {"Visualization Type": "Line chart (Avg Discount vs Avg Profit per Order)", "Complexity": "Medium"},
    "Sub-Category Performance (Profit vs. Discount)": {"Visualization Type": "Dual-axis line chart (Profit and Discount % by Sub-Category)", "Complexity": "Medium"},
    "Discount Effectiveness by Category": {"Visualization Type": "Grouped bar chart (Profit and Discount % per Category)", "Complexity": "Medium"},
    "State-Level Profitability Analysis": {"Visualization Type": "Treemap (States sized by Profit, color = Region)", "Complexity": "Medium"},
    "Customer Loyalty vs. Profitability": {"Visualization Type": "Scatter plot (Total Purchases per Customer vs Total Profit)", "Complexity": "Medium"},
    "Product Sales Distribution by Cities": {"Visualization Type": "Maps", "Complexity": "Medium"},
    "Product Profitability Efficiency (Profit/Sales Ratio)": {"Visualization Type": "Scatter plot (Profit/Sales Ratio vs Product Name, color = Category)", "Complexity": "Medium"},
    "Product Sub-Category Risk Assessment (High Discounts, Low Profit)": {"Visualization Type": "Heatmap (Sub-Category vs Discount vs Profit Margin)", "Complexity": "Complex"},
    "Market Basket Analysis - Frequently Purchased Items": {"Visualization Type": "Network graph", "Complexity": "Complex"},
    "Correlation Between Discount and Sales Volume": {"Visualization Type": "Pair plot or scatter plot with trendline", "Complexity": "Complex"}
}

# Dropdown for selecting business problem
# (This code should only be used in the main app, not here)
# selected_problem = st.selectbox("Choose a Business Problem:", list(business_problems.keys()))

# Display visualization type and complexity based on selection
# if selected_problem:
#     details = business_problems[selected_problem]
#     st.write(f"**Visualization Type:** {details['Visualization Type']}")
#     st.write(f"**Complexity:** {details['Complexity']}")