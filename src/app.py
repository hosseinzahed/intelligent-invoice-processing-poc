import streamlit as st
import os
import pandas as pd
from utils import load_invoices
from foundry_service import FoundryService
from doc_intel_service import DocumentIntelligenceService
from azure.ai.documentintelligence.models import AnalyzeResult
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize services
foundry_service = FoundryService()
document_intelligence_service = DocumentIntelligenceService()

# Get document paths for documents
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
docs_folder = os.path.join(workspace_root, "documents")


# Load invoice records from local folder
def load_invoice_records() -> None:
    invoice_records = load_invoices(docs_folder)
    df = pd.DataFrame(invoice_records)
    st.session_state["invoice_df"] = df


# Show preprocessing results
def show_preprocessing_results(pages: list) -> None:
    """ Display preprocessing results in a table with images.
    Args:
        pages (list): The list of pages with preprocessing results.
    Returns:
        None
    """

    # Create table data
    table_data = []
    for page in pages:
        table_data.append({
            "Page": page["page_num"],
            "Is Invoice": "Yes" if page["is_invoice"] else "No",
            "Image": page["image"],
            "Input Tokens": page["input_tokens"],
            "Output Tokens": page["output_tokens"],
            "Total Tokens": int(page["input_tokens"]) + int(page["output_tokens"]),
        })

    # Create DataFrame
    df_images = pd.DataFrame(table_data)

    # Display table with images
    st.subheader("Document Pages")

    # Use custom rendering to display images
    for idx, row in df_images.iterrows():
        col1, col2 = st.columns([3, 6])
        with col1:
            st.write(f"**Page {row['Page']}**")
            # Color the Is Invoice line based on value
            if row['Is Invoice'] == "Yes":
                st.markdown(
                    f"Is Invoice: <span style='color: green;'>{row['Is Invoice']}</span>", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"Is Invoice: <span style='color: red;'>{row['Is Invoice']}</span>", unsafe_allow_html=True)
            st.write(f"Input Tokens: {row['Input Tokens']}")
            st.write(f"Output Tokens: {row['Output Tokens']}")
            st.write(f"Total Tokens: {row['Total Tokens']}")
        with col2:
            st.image(
                f"data:image/png;base64,{row['Image']}", width=200)


def extract_content_from_invoices(file_name: str, pages: list) -> None:
    """ Extract and display content from the invoices.
    Args:
        file_name (str): The name of the selected invoice file.
        pages (list): The list of pages with preprocessing results.
    Returns:
        None
    """

    # Extract content from invoices
    invoice_pages = [page for page in pages if page["is_invoice"]]
    for page in invoice_pages:
        st.subheader(f"Extracting Content from Page {page['page_num']}...")
        # Call Document Intelligence Service to extract content
        pdf_path = os.path.join(docs_folder, file_name)

        # Read PDF file as bytes
        with open(pdf_path, "rb") as f:
            document_bytes = f.read()

        # Analyze document for the specific page
        invoices: AnalyzeResult = document_intelligence_service.analyze_document(
            document_bytes, pages=[page["page_num"]])

        # Display extracted content
        if invoices.documents:
            for idx, invoice in enumerate(invoices.documents):
                st.markdown(f"### 📄 Invoice #{idx + 1}")

                # Create 2x2 grid layout with equal height and width
                # First row
                col1, col2 = st.columns(2)

                with col1:
                    with st.container(border=True):
                        st.markdown("#### 🏢 Vendor Information")
                        vendor_name = invoice.fields.get("VendorName")
                        if vendor_name:
                            st.markdown(
                                f"**Vendor Name:** {vendor_name.get('content')}")

                        vendor_address = invoice.fields.get("VendorAddress")
                        if vendor_address:
                            st.markdown(
                                f"**Address:** {vendor_address.get('content')}")

                        vendor_address_recipient = invoice.fields.get(
                            "VendorAddressRecipient")
                        if vendor_address_recipient:
                            st.markdown(
                                f"**Address Recipient:** {vendor_address_recipient.get('content')}")

                with col2:
                    with st.container(border=True):
                        st.markdown("#### 👤 Customer Information")
                        customer_name = invoice.fields.get("CustomerName")
                        if customer_name:
                            st.markdown(
                                f"**Customer Name:** {customer_name.get('content')}")

                        customer_id = invoice.fields.get("CustomerId")
                        if customer_id:
                            st.markdown(
                                f"**Customer ID:** {customer_id.get('content')}")

                        customer_address = invoice.fields.get(
                            "CustomerAddress")
                        if customer_address:
                            st.markdown(
                                f"**Address:** {customer_address.get('content')}")

                        customer_address_recipient = invoice.fields.get(
                            "CustomerAddressRecipient")
                        if customer_address_recipient:
                            st.markdown(
                                f"**Address Recipient:** {customer_address_recipient.get('content')}")

                # Second row
                col3, col4 = st.columns(2)

                with col3:
                    with st.container(border=True):
                        st.markdown("#### 📍 Billing & Shipping")
                        billing_address = invoice.fields.get("BillingAddress")
                        if billing_address:
                            st.markdown(
                                f"**Billing Address:** {billing_address.get('content')}")

                        billing_address_recipient = invoice.fields.get(
                            "BillingAddressRecipient")
                        if billing_address_recipient:
                            st.markdown(
                                f"**Billing Recipient:** {billing_address_recipient.get('content')}")

                        shipping_address = invoice.fields.get(
                            "ShippingAddress")
                        if shipping_address:
                            st.markdown(
                                f"**Shipping Address:** {shipping_address.get('content')}")

                        shipping_address_recipient = invoice.fields.get(
                            "ShippingAddressRecipient")
                        if shipping_address_recipient:
                            st.markdown(
                                f"**Shipping Recipient:** {shipping_address_recipient.get('content')}")

                with col4:
                    with st.container(border=True):
                        st.markdown("#### 📋 Invoice Details")
                        invoice_id = invoice.fields.get("InvoiceId")
                        if invoice_id:
                            st.markdown(
                                f"**Invoice ID:** {invoice_id.get('content')}")

                        invoice_date = invoice.fields.get("InvoiceDate")
                        if invoice_date:
                            st.markdown(
                                f"**Invoice Date:** {invoice_date.get('content')}")

                        due_date = invoice.fields.get("DueDate")
                        if due_date:
                            st.markdown(
                                f"**Due Date:** {due_date.get('content')}")

                        purchase_order = invoice.fields.get("PurchaseOrder")
                        if purchase_order:
                            st.markdown(
                                f"**Purchase Order:** {purchase_order.get('content')}")

                        invoice_total = invoice.fields.get("InvoiceTotal")
                        if invoice_total:
                            st.markdown(
                                f"**💰 Invoice Total:** `{invoice_total.get('content')}`")

                st.divider()
                st.markdown("#### 🛒 Invoice Items")

                # Create items table
                items_data = []
                for idx, item in enumerate(invoice.fields.get("Items").get("valueArray")):
                    item_dict = {"Item #": idx + 1}

                    item_description = item.get(
                        "valueObject").get("Description")
                    if item_description:
                        item_dict["Description"] = item_description.get(
                            'content')

                    item_quantity = item.get("valueObject").get("Quantity")
                    if item_quantity:
                        item_dict["Quantity"] = item_quantity.get('content')

                    unit = item.get("valueObject").get("Unit")
                    if unit:
                        item_dict["Unit"] = unit.get('content')

                    unit_price = item.get("valueObject").get("UnitPrice")
                    if unit_price:
                        unit_price_code = (
                            unit_price.get("valueCurrency").get("currencyCode")
                            if unit_price.get("valueCurrency").get("currencyCode")
                            else ""
                        )
                        item_dict["Unit Price"] = f"{unit_price.get('content')}{unit_price_code}"

                    product_code = item.get("valueObject").get("ProductCode")
                    if product_code:
                        item_dict["Product Code"] = product_code.get('content')

                    item_date = item.get("valueObject").get("Date")
                    if item_date:
                        item_dict["Date"] = item_date.get('content')

                    tax = item.get("valueObject").get("Tax")
                    if tax:
                        item_dict["Tax"] = tax.get('content')

                    amount = item.get("valueObject").get("Amount")
                    if amount:
                        item_dict["Amount"] = amount.get('content')

                    items_data.append(item_dict)

                # Display items as dataframe
                if items_data:
                    items_df = pd.DataFrame(items_data)
                    st.dataframe(items_df)

                st.divider()

                # Financial Summary
                st.markdown("#### 💵 Financial Summary")
                col1, col2, col3 = st.columns(3)

                with col1:
                    subtotal = invoice.fields.get("SubTotal")
                    if subtotal:
                        st.metric("Subtotal", subtotal.get('content'))

                    total_tax = invoice.fields.get("TotalTax")
                    if total_tax:
                        st.metric("Total Tax", total_tax.get('content'))

                with col2:
                    previous_unpaid_balance = invoice.fields.get(
                        "PreviousUnpaidBalance")
                    if previous_unpaid_balance:
                        st.metric("Previous Unpaid Balance",
                                  previous_unpaid_balance.get('content'))

                    amount_due = invoice.fields.get("AmountDue")
                    if amount_due:
                        st.metric("Amount Due", amount_due.get('content'))

                with col3:
                    service_start_date = invoice.fields.get("ServiceStartDate")
                    if service_start_date:
                        st.markdown(
                            f"**Service Start:** {service_start_date.get('content')}")

                    service_end_date = invoice.fields.get("ServiceEndDate")
                    if service_end_date:
                        st.markdown(
                            f"**Service End:** {service_end_date.get('content')}")

                # Additional Addresses
                service_address = invoice.fields.get("ServiceAddress")
                service_address_recipient = invoice.fields.get(
                    "ServiceAddressRecipient")
                remittance_address = invoice.fields.get("RemittanceAddress")
                remittance_address_recipient = invoice.fields.get(
                    "RemittanceAddressRecipient")

                if service_address or service_address_recipient or remittance_address or remittance_address_recipient:
                    st.divider()
                    st.markdown("#### 📮 Additional Addresses")
                    col1, col2 = st.columns(2)

                    with col1:
                        if service_address:
                            st.markdown(
                                f"**Service Address:** {service_address.get('content')}")
                        if service_address_recipient:
                            st.markdown(
                                f"**Service Recipient:** {service_address_recipient.get('content')}")

                    with col2:
                        if remittance_address:
                            st.markdown(
                                f"**Remittance Address:** {remittance_address.get('content')}")
                        if remittance_address_recipient:
                            st.markdown(
                                f"**Remittance Recipient:** {remittance_address_recipient.get('content')}")

            st.divider()


# Process selected invoice
def process_invoice(file_name: str):
    """ Process the selected invoice: preprocess and extract content. 
    Args:
        file_name (str): The name of the selected invoice file.
    Returns:
        None
    """

    # Start processing
    st.info(f"Processing document **{file_name}** started...")

    # Convert PDF to images
    pdf_path = os.path.join(docs_folder, file_name)
    pages = foundry_service.pre_process_pdf(pdf_path)

    # Show preprocessing results
    show_preprocessing_results(pages)

    # Extract and display content from the invoices
    extract_content_from_invoices(file_name, pages)

    # Processing completed
    st.success(f"Processing document **{file_name}** completed.")


def main():
    # Streamlit App Title
    st.title("✨ Intelligent Invoice Processing")

    # Sidebar
    st.sidebar.header("Actions")

    # Load Invoices button
    if st.sidebar.button("🔃 Load Invoices"):
        load_invoice_records()

    # Show table if loaded
    if "invoice_df" in st.session_state:
        st.subheader("Invoices Table")
        st.success(
            f"Loaded {len(st.session_state['invoice_df'])} invoices from local folder.")
        st.dataframe(st.session_state["invoice_df"])

        # Get unique item names from the dataframe
        df = st.session_state["invoice_df"]
        if "Name" in df.columns and len(df) > 0:
            item_names = df["Name"].unique().tolist()

            # Create selectbox with a key to maintain state
            selected_item = st.selectbox(
                "Select an invoice:",
                options=item_names,
                key="selected_item_name"
            )

            # Add Process button
            if st.button("⚙️ Process"):
                process_invoice(selected_item)


if __name__ == "__main__":
    main()
