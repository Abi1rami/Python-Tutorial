import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Expenses Management", page_icon="💰", layout="wide")

st.title("💰 Expenses Management App")
st.markdown("---")

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# ============================================
# Sidebar - Add Expense
# ============================================
st.sidebar.title("➕ Add Expense")

category    = st.sidebar.selectbox("Category", [
    "Food", "Transport", "Shopping",
    "Entertainment", "Health",
    "Education", "Bills", "Other"])

description = st.sidebar.text_input("Description")
amount      = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=10.0)
exp_date    = st.sidebar.date_input("Date", value=date.today())
pay_method  = st.sidebar.selectbox("Payment Method", [
    "Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"])

if st.sidebar.button("➕ Add Expense"):
    if description and amount > 0:
        st.session_state.expenses.append({
            "Date"          : str(exp_date),
            "Category"      : category,
            "Description"   : description,
            "Amount"        : amount,
            "Payment Method": pay_method
        })
        st.sidebar.success("✅ Expense added!")
    else:
        st.sidebar.warning("⚠️ Please fill all fields!")

# ============================================
# Summary
# ============================================
col1, col2, col3 = st.columns(3)
total = sum(e['Amount'] for e in st.session_state.expenses)
col1.metric("💸 Total Expenses",    f"₹{total:.2f}")
col2.metric("📊 Total Transactions", len(st.session_state.expenses))

if st.session_state.expenses:
    highest = max(st.session_state.expenses, key=lambda x: x['Amount'])
    col3.metric("🔺 Highest Expense", f"₹{highest['Amount']:.2f}")
else:
    col3.metric("🔺 Highest Expense", "₹0.00")

st.markdown("---")

# ============================================
# Expenses Table
# ============================================
st.subheader("📋 All Expenses")

if st.session_state.expenses:
    df         = pd.DataFrame(st.session_state.expenses)
    filter_cat = st.selectbox("Filter by Category",
                              ["All", "Food", "Transport", "Shopping",
                               "Entertainment", "Health",
                               "Education", "Bills", "Other"])
    if filter_cat != "All":
        df = df[df['Category'] == filter_cat]

    st.dataframe(df, use_container_width=True)
    st.markdown("---")

    # ============================================
    # Charts
    # ============================================
    st.subheader("📊 Expense Charts")
    col4, col5 = st.columns(2)

    with col4:
        st.write("**Category Wise Expenses**")
        category_data = pd.DataFrame(
            st.session_state.expenses
        ).groupby('Category')['Amount'].sum()
        st.bar_chart(category_data)

    with col5:
        st.write("**Payment Method Wise Expenses**")
        payment_data = pd.DataFrame(
            st.session_state.expenses
        ).groupby('Payment Method')['Amount'].sum()
        st.bar_chart(payment_data)

    st.markdown("---")

    # ============================================
    # Delete & Clear
    # ============================================
    st.subheader("🗑️ Manage Expenses")
    col6, col7 = st.columns(2)

    with col6:
        delete_index = st.number_input(
            "Enter expense number to delete",
            min_value=1,
            max_value=len(st.session_state.expenses),
            step=1)
        if st.button("🗑️ Delete Expense"):
            st.session_state.expenses.pop(int(delete_index) - 1)
            st.success("✅ Expense deleted!")
            st.rerun()

    with col7:
        if st.button("❌ Clear All Expenses"):
            st.session_state.expenses = []
            st.success("✅ All expenses cleared!")
            st.rerun()

    st.markdown("---")

    # ============================================
    # Download CSV
    # ============================================
    st.subheader("📥 Download Expenses")
    csv = pd.DataFrame(st.session_state.expenses).to_csv(index=False)
    st.download_button(
        label    = "📥 Download CSV",
        data     = csv,
        file_name= "expenses.csv",
        mime     = "text/csv")

else:
    st.info("📭 No expenses added yet! Add expenses from the sidebar.")

st.markdown("---")
st.markdown("**💰 Expenses Management App** | Built with Streamlit")