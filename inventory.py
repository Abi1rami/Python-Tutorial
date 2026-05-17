import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title = "Inventory & Billing Management",
    page_icon  = "🏪",
    layout     = "wide"
)

st.title("🏪 Inventory & Billing Management System")
st.markdown("---")

if 'inventory'  not in st.session_state:
    st.session_state.inventory  = []
if 'customers'  not in st.session_state:
    st.session_state.customers  = []
if 'bills'      not in st.session_state:
    st.session_state.bills      = []
if 'bill_items' not in st.session_state:
    st.session_state.bill_items = []

menu = st.sidebar.radio("📌 Navigation", [
    "📦 Inventory",
    "👥 Customers",
    "🧾 Billing",
    "📊 Dashboard"
])

# ============================================
# INVENTORY PAGE
# ============================================
if menu == "📦 Inventory":
    st.header("📦 Inventory Management")
    st.markdown("---")

    st.subheader("➕ Add New Product")

    # Row 1
    col1, col2, col3 = st.columns(3)
    with col1:
        product_name = st.text_input("📝 Product Name")
    with col2:
        category = st.selectbox("📂 Category", [
            "Electronics", "Clothing", "Food",
            "Medicine", "Stationery", "Other"
        ])
    with col3:
        supplier = st.text_input("🏭 Supplier Name")

    # Row 2
    col4, col5, col6 = st.columns(3)
    with col4:
        available_qty = st.number_input(
            "📦 Available Quantity",
            min_value = 0,
            step      = 1,
            format    = "%d"
        )
    with col5:
        damaged_qty = st.number_input(
            "⚠️ Damaged Quantity",
            min_value = 0,
            step      = 1,
            format    = "%d"
        )
    with col6:
        min_stock = st.number_input(
            "🔻 Minimum Stock Level",
            min_value = 0,
            step      = 1,
            format    = "%d"
        )

    # Row 3
    col7, col8, col9 = st.columns(3)
    with col7:
        price = st.number_input(
            "💰 Price (₹)",
            min_value = 0.0,
            step      = 10.0,
            format    = "%.2f"
        )
    with col8:
        expiry_date = st.date_input(
            "📅 Expiry Date",
            value = date.today()
        )
    with col9:
        added_date = st.date_input(
            "📅 Added Date",
            value = date.today()
        )

    st.markdown("---")

    # Add Button
    if st.button("➕ Add Product", use_container_width=True):
        if product_name and price > 0:
            if expiry_date < date.today():
                exp_status = "⚠️ Expired"
            elif (expiry_date - date.today()).days <= 30:
                exp_status = "⚠️ Expiring Soon"
            else:
                exp_status = "✅ Valid"

            st.session_state.inventory.append({
                "Product"       : product_name,
                "Category"      : category,
                "Supplier"      : supplier,
                "Available Qty" : available_qty,
                "Damaged Qty"   : damaged_qty,
                "Min Stock"     : min_stock,
                "Price (₹)"     : price,
                "Total Value"   : available_qty * price,
                "Expiry Date"   : str(expiry_date),
                "Added Date"    : str(added_date),
                "Expiry Status" : exp_status,
                "Stock Status"  : "Low Stock" if available_qty <= min_stock else "In Stock"
            })
            st.success(f"✅ {product_name} added successfully!")
        else:
            st.warning("⚠️ Please fill Product Name and Price!")

    st.markdown("---")

    # Inventory Table
    st.subheader("📋 Inventory List")

    if st.session_state.inventory:
        df = pd.DataFrame(st.session_state.inventory)

        # Filters
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_cat = st.selectbox("Filter Category", [
                "All", "Electronics", "Clothing",
                "Food", "Medicine", "Stationery", "Other"
            ])
        with col_f2:
            filter_stock = st.selectbox("Filter Stock", [
                "All", "In Stock", "Low Stock"
            ])
        with col_f3:
            filter_exp = st.selectbox("Filter Expiry", [
                "All", "✅ Valid",
                "⚠️ Expiring Soon", "⚠️ Expired"
            ])

        if filter_cat   != "All": df = df[df['Category']      == filter_cat]
        if filter_stock != "All": df = df[df['Stock Status']  == filter_stock]
        if filter_exp   != "All": df = df[df['Expiry Status'] == filter_exp]

        def highlight_rows(row):
            if row['Expiry Status'] == '⚠️ Expired':
                return ['background-color: #ffcccc'] * len(row)
            elif row['Stock Status'] == 'Low Stock':
                return ['background-color: #fff3cc'] * len(row)
            elif row['Expiry Status'] == '⚠️ Expiring Soon':
                return ['background-color: #ffe0cc'] * len(row)
            return [''] * len(row)

        st.dataframe(
            df.style.apply(highlight_rows, axis=1),
            use_container_width=True
        )

        # Alerts
        st.markdown("---")
        st.subheader("⚠️ Alerts")
        col_a1, col_a2 = st.columns(2)

        with col_a1:
            low_stock_items = [
                i for i in st.session_state.inventory
                if i['Stock Status'] == "Low Stock"
            ]
            if low_stock_items:
                st.error("🔴 Low Stock Alerts:")
                for item in low_stock_items:
                    st.warning(
                        f"**{item['Product']}** - "
                        f"Available: {item['Available Qty']} | "
                        f"Min Stock: {item['Min Stock']}"
                    )

        with col_a2:
            expired_items = [
                i for i in st.session_state.inventory
                if "Expired" in i['Expiry Status']
            ]
            if expired_items:
                st.error("🔴 Expiry Alerts:")
                for item in expired_items:
                    st.warning(
                        f"**{item['Product']}** - "
                        f"Expiry: {item['Expiry Date']} | "
                        f"Status: {item['Expiry Status']}"
                    )

        st.markdown("---")

        # Delete Product
        st.subheader("🗑️ Delete Product")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            delete_product = st.selectbox(
                "Select Product to Delete",
                [i['Product'] for i in st.session_state.inventory]
            )
        with col_d2:
            if st.button("🗑️ Delete Product"):
                st.session_state.inventory = [
                    i for i in st.session_state.inventory
                    if i['Product'] != delete_product
                ]
                st.success(f"✅ {delete_product} deleted!")
                st.rerun()

        # Download
        st.markdown("---")
        csv = df.to_csv(index=False)
        st.download_button(
            label     = "📥 Download Inventory CSV",
            data      = csv,
            file_name = "inventory.csv",
            mime      = "text/csv"
        )

    else:
        st.info("📭 No products added yet!")

# ============================================
# CUSTOMERS PAGE
# ============================================
elif menu == "👥 Customers":
    st.header("👥 Customer Management")
    st.markdown("---")

    st.subheader("➕ Add New Customer")

    col1, col2, col3 = st.columns(3)
    with col1:
        customer_name  = st.text_input("👤 Customer Name")
        customer_email = st.text_input("📧 Email")
        customer_phone = st.text_input("📞 Phone Number")
    with col2:
        customer_addr  = st.text_area("🏠 Address")
        customer_city  = st.text_input("🏙️ City")
        customer_state = st.text_input("🗺️ State")
    with col3:
        customer_type  = st.selectbox("👥 Customer Type", [
            "Regular", "VIP", "Wholesale", "Retail"
        ])
        customer_dob   = st.date_input("🎂 Date of Birth", value=date.today())
        joined_date    = st.date_input("📅 Joined Date",   value=date.today())

    if st.button("➕ Add Customer", use_container_width=True):
        if customer_name and customer_phone:
            st.session_state.customers.append({
                "Customer ID"  : f"CUST{len(st.session_state.customers)+1:04d}",
                "Name"         : customer_name,
                "Email"        : customer_email,
                "Phone"        : customer_phone,
                "Address"      : customer_addr,
                "City"         : customer_city,
                "State"        : customer_state,
                "Type"         : customer_type,
                "Date of Birth": str(customer_dob),
                "Joined Date"  : str(joined_date)
            })
            st.success(f"✅ {customer_name} added!")
        else:
            st.warning("⚠️ Please fill Name and Phone!")

    st.markdown("---")

    st.subheader("📋 Customer List")
    if st.session_state.customers:
        df_cust     = pd.DataFrame(st.session_state.customers)
        filter_type = st.selectbox("Filter by Type", [
            "All", "Regular", "VIP", "Wholesale", "Retail"
        ])
        if filter_type != "All":
            df_cust = df_cust[df_cust['Type'] == filter_type]
        st.dataframe(df_cust, use_container_width=True)

        csv = df_cust.to_csv(index=False)
        st.download_button(
            label     = "📥 Download Customer CSV",
            data      = csv,
            file_name = "customers.csv",
            mime      = "text/csv"
        )
    else:
        st.info("📭 No customers added yet!")

# ============================================
# BILLING PAGE
# ============================================
elif menu == "🧾 Billing":
    st.header("🧾 Billing Management")
    st.markdown("---")

    if not st.session_state.customers:
        st.warning("⚠️ Please add customers first!")
    elif not st.session_state.inventory:
        st.warning("⚠️ Please add products first!")
    else:
        st.subheader("👥 Select Customer")
        selected_cust = st.selectbox(
            "Select Customer",
            [c['Name'] for c in st.session_state.customers]
        )
        cust_details = next(
            (c for c in st.session_state.customers
             if c['Name'] == selected_cust), None
        )
        if cust_details:
            col_c1, col_c2, col_c3 = st.columns(3)
            col_c1.info(f"📞 {cust_details['Phone']}")
            col_c2.info(f"📧 {cust_details['Email']}")
            col_c3.info(f"🏙️ {cust_details['City']}")

        st.markdown("---")
        st.subheader("🛒 Add Items to Bill")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            selected_prod = st.selectbox(
                "Select Product",
                [i['Product'] for i in st.session_state.inventory]
            )
        with col_b2:
            bill_qty = st.number_input(
                "Quantity",
                min_value = 1,
                step      = 1
            )

        prod_details = next(
            (i for i in st.session_state.inventory
             if i['Product'] == selected_prod), None
        )
        if prod_details:
            col_p1, col_p2 = st.columns(2)
            col_p1.info(f"💰 Price: ₹{prod_details['Price (₹)']}")
            col_p2.info(f"📦 Available: {prod_details['Available Qty']}")

        if st.button("➕ Add to Bill", use_container_width=True):
            if prod_details and bill_qty <= prod_details['Available Qty']:
                st.session_state.bill_items.append({
                    "Product"   : selected_prod,
                    "Quantity"  : bill_qty,
                    "Price (₹)" : prod_details['Price (₹)'],
                    "Total (₹)" : bill_qty * prod_details['Price (₹)']
                })
                st.success(f"✅ {selected_prod} added to bill!")
            else:
                st.error("❌ Insufficient stock!")

        st.markdown("---")
        st.subheader("🧾 Bill Preview")

        if st.session_state.bill_items:
            df_bill  = pd.DataFrame(st.session_state.bill_items)
            subtotal = sum(i['Total (₹)'] for i in st.session_state.bill_items)

            st.dataframe(df_bill, use_container_width=True)

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                tax_rate = st.slider("Tax (%)", 0, 28, 18)
            with col_t2:
                discount = st.number_input("Discount (₹)", min_value=0.0, step=10.0)

            tax_amount = (subtotal - discount) * tax_rate / 100
            total      = subtotal - discount + tax_amount

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("🛒 Subtotal", f"₹{subtotal:.2f}")
            col_m2.metric("🏷️ Discount", f"₹{discount:.2f}")
            col_m3.metric("📊 Tax",      f"₹{tax_amount:.2f}")
            col_m4.metric("💰 Total",    f"₹{total:.2f}")

            payment = st.selectbox("💳 Payment Method", [
                "Cash", "Credit Card",
                "Debit Card", "UPI", "Net Banking"
            ])

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("✅ Generate Bill", use_container_width=True):
                    bill_id = f"BILL{len(st.session_state.bills)+1:04d}"
                    for item in st.session_state.bill_items:
                        for inv in st.session_state.inventory:
                            if inv['Product'] == item['Product']:
                                inv['Available Qty'] -= item['Quantity']
                                inv['Total Value']    = (
                                    inv['Available Qty'] * inv['Price (₹)']
                                )
                    st.session_state.bills.append({
                        "Bill ID"       : bill_id,
                        "Date"          : str(date.today()),
                        "Customer"      : selected_cust,
                        "Items"         : len(st.session_state.bill_items),
                        "Subtotal (₹)"  : subtotal,
                        "Discount (₹)"  : discount,
                        "Tax (₹)"       : tax_amount,
                        "Total (₹)"     : total,
                        "Payment Method": payment,
                        "Status"        : "Paid"
                    })
                    st.session_state.bill_items = []
                    st.success(f"✅ Bill {bill_id} generated!")
                    st.rerun()

            with col_btn2:
                if st.button("🗑️ Clear Bill", use_container_width=True):
                    st.session_state.bill_items = []
                    st.rerun()

        else:
            st.info("📭 No items added to bill yet!")

        st.markdown("---")
        st.subheader("📋 Bills History")
        if st.session_state.bills:
            df_bills = pd.DataFrame(st.session_state.bills)
            st.dataframe(df_bills, use_container_width=True)
            csv = df_bills.to_csv(index=False)
            st.download_button(
                label     = "📥 Download Bills CSV",
                data      = csv,
                file_name = "bills.csv",
                mime      = "text/csv"
            )
        else:
            st.info("📭 No bills generated yet!")

# ============================================
# DASHBOARD PAGE
# ============================================
elif menu == "📊 Dashboard":
    st.header("📊 Dashboard")
    st.markdown("---")

    total_products  = len(st.session_state.inventory)
    total_value     = sum(i['Total Value'] for i in st.session_state.inventory)
    total_customers = len(st.session_state.customers)
    total_bills     = len(st.session_state.bills)
    total_revenue   = sum(b['Total (₹)'] for b in st.session_state.bills)
    low_stock       = sum(1 for i in st.session_state.inventory if i['Stock Status'] == "Low Stock")
    expired         = sum(1 for i in st.session_state.inventory if "Expired" in i['Expiry Status'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Products",  total_products)
    col2.metric("👥 Total Customers", total_customers)
    col3.metric("🧾 Total Bills",     total_bills)
    col4.metric("💰 Total Revenue",   f"₹{total_revenue:.2f}")

    st.markdown("---")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("💰 Inventory Value", f"₹{total_value:.2f}")
    col6.metric("⚠️ Low Stock",       low_stock)
    col7.metric("⚠️ Expired Items",   expired)
    col8.metric("📊 Avg Bill",
                f"₹{total_revenue/total_bills:.2f}"
                if total_bills > 0 else "₹0.00")

    if st.session_state.inventory:
        st.markdown("---")
        st.subheader("📊 Inventory Charts")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.write("**Category Wise Stock**")
            cat_data = pd.DataFrame(
                st.session_state.inventory
            ).groupby('Category')['Available Qty'].sum()
            st.bar_chart(cat_data)
        with col_c2:
            st.write("**Category Wise Value**")
            val_data = pd.DataFrame(
                st.session_state.inventory
            ).groupby('Category')['Total Value'].sum()
            st.bar_chart(val_data)

    if st.session_state.bills:
        st.markdown("---")
        st.subheader("📊 Sales Charts")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.write("**Daily Revenue**")
            rev_data = pd.DataFrame(
                st.session_state.bills
            ).groupby('Date')['Total (₹)'].sum()
            st.line_chart(rev_data)
        with col_s2:
            st.write("**Payment Method Wise**")
            pay_data = pd.DataFrame(
                st.session_state.bills
            ).groupby('Payment Method')['Total (₹)'].sum()
            st.bar_chart(pay_data)

st.markdown("---")
st.markdown("**🏪 Inventory & Billing Management** | Built with Streamlit")