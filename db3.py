import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display title and Description
st.title('Vendor Management Portal')
st.markdown('Enter new details of the new vendor below')

# Establishing a google sheet connection
conn = st.connection('gsheets', type=GSheetsConnection)

# Fetch existing vendor data
existing_data = conn.read(worksheet="Vendors", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Bussiness Types and Products
BUSSINESS_TYPES = [
    "Manufacturer",
    "Distributor",
    "Wholesaler",
    "Retailer",
    "Service Provider"
]
PRODUCTS = [
    "Electronic",
    "Apparel",
    "Groceries",
    "Software",
    "Other"
]

# OnBoarding New Vendor Form
with st.form(key="vendor_form"):
    company_name = st.text_input(label="Company Name*")
    bussiness_type = st.selectbox("Bussiness Type*", options = BUSSINESS_TYPES, index = None)
    products = st.multiselect("Product Offered", options = PRODUCTS)
    years_in_bussiness = st.slider("Years in Bussiness", 0, 50, 5)
    onboarding_date = st.date_input(label = "Onboarding Date")
    additional_info = st.text_area(label = "Additional Notes")

    # Mark Mandatory Fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label = "Submit Vendor Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not company_name or not bussiness_type:
            st.warning("Ensure All Mandatory Fields are Filled.")
            st.stop()
        elif existing_data["CompanyName"].str.contains(company_name).any():
            st.warning("A Vendor with this company name already exists.")
            st.stop()
        else :
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "CompanyName" : company_name,
                        "BussinessType" : bussiness_type,
                        "Products" : ", ".join(products),
                        "YearsInBussiness" : years_in_bussiness,
                        "OnBoardingDate" : onboarding_date.strftime("%Y-%m-%d"),
                        "AdditionalInfo" : additional_info
                    }
                ]
            )

            # Add the new Vendor data to existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheet with the new vendor data
            conn.update(worksheet='Vendors', data=updated_df)

            st.success("Vendor details successfully submitted!!")