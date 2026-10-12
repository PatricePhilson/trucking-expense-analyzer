import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Trucking Expense Analyzer",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Trucking Expense Analyzer")
st.write("Track loads, expenses, miles, and profitability.")

EXPENSE_CATEGORIES = [
    "Fuel",
    "Maintenance",
    "Insurance",
    "Truck Payment",
    "Trailer Rental",
    "Tolls",
    "Food",
    "Permits",
    "Other",
]

if "loads" not in st.session_state:
    st.session_state.loads = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.sidebar.header("Add a Load")

with st.sidebar.form("load_form"):
    load_date = st.date_input("Load date")
    load_name = st.text_input("Load or customer reference")
    revenue = st.number_input(
        "Revenue ($)", min_value=0.0, step=50.0
    )
    miles = st.number_input(
        "Miles driven", min_value=0.0, step=10.0
    )
    load_submitted = st.form_submit_button("Save Load")

    if load_submitted:
        st.session_state.loads.append({
            "Date": str(load_date),
            "Load": load_name,
            "Revenue": revenue,
            "Miles": miles,
        })
        st.success("Load saved!")

st.sidebar.header("Add an Expense")

with st.sidebar.form("expense_form"):
    expense_date = st.date_input(
        "Expense date", key="expense_date"
    )
    category = st.selectbox(
        "Category", EXPENSE_CATEGORIES
    )
    amount = st.number_input(
        "Amount ($)", min_value=0.0, step=10.0
    )
    description = st.text_input("Description")
    expense_submitted = st.form_submit_button(
        "Save Expense"
    )

    if expense_submitted:
        st.session_state.expenses.append({
            "Date": str(expense_date),
            "Category": category,
            "Amount": amount,
            "Description": description,
        })
        st.success("Expense saved!")

loads = pd.DataFrame(
    st.session_state.loads,
    columns=["Date", "Load", "Revenue", "Miles"]
)

expenses = pd.DataFrame(
    st.session_state.expenses,
    columns=["Date", "Category", "Amount", "Description"]
)

total_revenue = loads["Revenue"].sum()
total_expenses = expenses["Amount"].sum()
total_miles = loads["Miles"].sum()
net_profit = total_revenue - total_expenses

profit_margin = (
    net_profit / total_revenue * 100
    if total_revenue else 0
)

cost_per_mile = (
    total_expenses / total_miles
    if total_miles else 0
)

profit_per_mile = (
    net_profit / total_miles
    if total_miles else 0
)

st.subheader("Business Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"${total_revenue:,.2f}")
c2.metric("Expenses", f"${total_expenses:,.2f}")
c3.metric("Net Profit", f"${net_profit:,.2f}")
c4.metric("Profit Margin", f"{profit_margin:.1f}%")

c5, c6, c7 = st.columns(3)
c5.metric("Total Miles", f"{total_miles:,.0f}")
c6.metric("Cost per Mile", f"${cost_per_mile:.2f}")
c7.metric("Profit per Mile", f"${profit_per_mile:.2f}")

st.subheader("Expense Breakdown")

if not expenses.empty:
    category_totals = (
        expenses.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(category_totals)
    st.dataframe(expenses, use_container_width=True)
else:
    st.info("Add an expense to see your expense breakdown.")

st.subheader("Load History")

if not loads.empty:
    st.dataframe(loads, use_container_width=True)
else:
    st.info("Add a load to start tracking revenue.")

st.subheader("Export Your Records")

if not loads.empty:
    st.download_button(
        "Download Loads CSV",
        loads.to_csv(index=False).encode("utf-8"),
        file_name="trucking_loads.csv",
        mime="text/csv",
    )

if not expenses.empty:
    st.download_button(
        "Download Expenses CSV",
        expenses.to_csv(index=False).encode("utf-8"),
        file_name="trucking_expenses.csv",
        mime="text/csv",
    )