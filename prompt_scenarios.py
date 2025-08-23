import streamlit as st


# Data from the image
BUSINESS_PROBLEMS = {
    "Profitability by Customer Segment": {
        "ProblemID": 1,
        "Visualization Type": "Bar chart (Profit by Segment, % of total)",
        "Complexity": "Easy"
    },
    "Top 10 Products by Sales Volume": {
        "ProblemID": 2,
        "Visualization Type": "Horizontal bar chart (Product Name vs Sales)",
        "Complexity": "Easy"
    },
    "Customer Profitability Analysis": {
        "ProblemID": 3,
        "Visualization Type": "Table or bar chart (Top 10 Customers by Total Profit)",
        "Complexity": "Easy"
    },
    "Sales Distribution Across Regions": {
        "ProblemID": 4,
        "Visualization Type": "Pie chart (Region-wise Sales %)",
        "Complexity": "Easy"
    },
    "Segment-wise Purchase Behavior": {
        "ProblemID": 5,
        "Visualization Type": "Bar chart (Avg Quantity Purchased per Segment)",
        "Complexity": "Easy"
    },
    "Top 5 Most Profitable Cities": {
        "ProblemID": 6,
        "Visualization Type": "Horizontal bar chart (City vs Total Profit)",
        "Complexity": "Easy"
    },
    "Profit Relationship Across Product Categories": {
        "ProblemID": 7,
        "Visualization Type": "Scatter plot (Sales vs Profit, point size = Quantity)",
        "Complexity": "Medium"
    },
    "Regional Profit Contribution": {
        "ProblemID": 8,
        "Visualization Type": "Stacked bar chart (Profit by Region and Category)",
        "Complexity": "Medium"
    },
    "Impact of Discounts on Profit Margins": {
        "ProblemID": 9,
        "Visualization Type": "Line chart (Avg Discount vs Avg Profit per Order)",
        "Complexity": "Medium"
    },
    "Sub-Category Performance (Profit vs. Discount)": {
        "ProblemID": 10,
        "Visualization Type": "Dual-axis line chart (Profit and Discount % by Sub-Category)",
        "Complexity": "Medium"
    },
    "Discount Effectiveness by Category": {
        "ProblemID": 11,
        "Visualization Type": "Grouped bar chart (Profit and Discount % per Category)",
        "Complexity": "Medium"
    },
    "State-Level Profitability Analysis": {
        "ProblemID": 12,
        "Visualization Type": "Treemap (States sized by Profit, color = Region)",
        "Complexity": "Medium"
    },
    "Customer Loyalty vs. Profitability": {
        "ProblemID": 13,
        "Visualization Type": "Scatter plot (Total Purchases per Customer vs Total Profit)",
        "Complexity": "Medium"
    },
    "Product Sales Distribution by Cities": {
        "ProblemID": 14,
        "Visualization Type": "Maps",
        "Complexity": "Medium"
    },
    "Product Profitability Efficiency (Profit/Sales Ratio)": {
        "ProblemID": 15,
        "Visualization Type": "Scatter plot (Profit/Sales Ratio vs Product Name, color = Category)",
        "Complexity": "Medium"
    },
    "Product Sub-Category Risk Assessment (High Discounts, Low Profit)": {
        "ProblemID": 16,
        "Visualization Type": "Heatmap (Sub-Category vs Discount vs Profit Margin)",
        "Complexity": "Complex"
    },
    "Market Basket Analysis - Frequently Purchased Items": {
        "ProblemID": 17,
        "Visualization Type": "Network graph",
        "Complexity": "Complex"
    },
    "Correlation Between Discount and Sales Volume": {
        "ProblemID": 18,
        "Visualization Type": "Pair plot or scatter plot with trendline",
        "Complexity": "Complex"
    }
}


# Legacy variable name for backward compatibility
business_problems = BUSINESS_PROBLEMS


# Dropdown for selecting business problem
# (This code should only be used in the main app, not here)
# selected_problem = st.selectbox("Choose a Business Problem:", list(business_problems.keys()))

# Display visualization type and complexity based on selection
# if selected_problem:
#     details = business_problems[selected_problem]
#     st.write(f"**Visualization Type:** {details['Visualization Type']}")
#     st.write(f"**Complexity:** {details['Complexity']}")