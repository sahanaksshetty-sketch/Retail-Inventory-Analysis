import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Retail Inventory Profit Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Inventory Profit Analysis Dashboard")
st.write("Upload your Retail Inventory Excel file.")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    # Remove spaces from column names
    df.columns = df.columns.str.strip()

    st.success("✅ File Uploaded Successfully!")

    # ---------------- SIDEBAR FILTERS ----------------

    st.sidebar.title("Filters")

    if "Category" in df.columns:
        category = st.sidebar.selectbox(
            "Category",
            ["All"] + sorted(df["Category"].dropna().unique())
        )

        if category != "All":
            df = df[df["Category"] == category]

    if "Supplier_Name" in df.columns:
        supplier = st.sidebar.selectbox(
            "Supplier",
            ["All"] + sorted(df["Supplier_Name"].dropna().unique())
        )

        if supplier != "All":
            df = df[df["Supplier_Name"] == supplier]

    if "Month" in df.columns:
        month = st.sidebar.selectbox(
            "Month",
            ["All"] + sorted(df["Month"].dropna().unique())
        )

        if month != "All":
            df = df[df["Month"] == month]

    # ---------------- DATASET ----------------

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # ---------------- KPI ----------------

    st.header("📈 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    if "Sales" in df.columns:
        total_sales = df["Sales"].sum()
        col1.metric("Total Sales", f"₹ {total_sales:,.0f}")

    if "Cost" in df.columns:
        total_cost = df["Cost"].sum()
        col2.metric("Total Cost", f"₹ {total_cost:,.0f}")

    if "Profit" in df.columns:
        total_profit = df["Profit"].sum()
        col3.metric("Total Profit", f"₹ {total_profit:,.0f}")

    # ---------------- PRODUCT SALES ----------------

    if "Product_Name" in df.columns and "Sales" in df.columns:

        st.header("📊 Product Sales")

        product_sales = (
            df.groupby("Product_Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(10,5))

        product_sales.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Product Sales Analysis")
        ax.set_xlabel("Product")
        ax.set_ylabel("Sales")

        plt.xticks(rotation=45)

        plt.tight_layout()

        st.pyplot(fig)

    # ---------------- SUPPLIER PROFIT ----------------

    if "Supplier_Name" in df.columns and "Profit" in df.columns:

        st.header("📈 Supplier Profit")

        supplier_profit = (
            df.groupby("Supplier_Name")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(10,5))

        supplier_profit.plot(
            kind="bar",
            color="green",
            ax=ax
        )

        ax.set_title("Supplier Profit Analysis")
        ax.set_xlabel("Supplier")
        ax.set_ylabel("Profit")

        plt.xticks(rotation=45)

        plt.tight_layout()

        st.pyplot(fig)

    # ---------------- MONTHLY SALES ----------------

    if "Month" in df.columns and "Sales" in df.columns:

        st.header("📉 Monthly Sales")

        monthly_sales = (
            df.groupby("Month")["Sales"]
            .sum()
        )

        fig, ax = plt.subplots(figsize=(10,5))

        monthly_sales.plot(
            kind="line",
            marker="o",
            ax=ax
        )

        ax.set_title("Monthly Sales")
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales")

        ax.grid(True)

        plt.tight_layout()

        st.pyplot(fig)

    # ---------------- CATEGORY SALES ----------------

    if "Category" in df.columns and "Sales" in df.columns:

        st.header("🥧 Category Sales")

        category_sales = (
            df.groupby("Category")["Sales"]
            .sum()
        )

        fig, ax = plt.subplots(figsize=(3,3))

        category_sales.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )

        ax.set_ylabel("")

        plt.tight_layout()

        st.pyplot(fig)

    # ---------------- TOP 5 PRODUCTS ----------------

    if "Product_Name" in df.columns and "Profit" in df.columns:

        st.header("🏆 Top 5 Products")

        top_products = (
            df.groupby("Product_Name")["Profit"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        st.table(top_products)

    # ---------------- TOP 5 SUPPLIERS ----------------

    if "Supplier_Name" in df.columns and "Profit" in df.columns:

        st.header("🏆 Top 5 Suppliers")

        top_suppliers = (
            df.groupby("Supplier_Name")["Profit"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        st.table(top_suppliers)
# ---------------- DOWNLOAD DATA ----------------

    st.header("📥 Download Report")

    excel_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download Filtered Data (CSV)",
        data=excel_data,
        file_name="Retail_Inventory_Report.csv",
        mime="text/csv"
    )

else:

    st.info("Please upload your Retail Inventory Excel file.")