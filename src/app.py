import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from utils import load_raw_invoices
# Load environment variables from .env file
load_dotenv(override=True)

# Get document paths for raw and processed documents
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
raw_folder = os.path.join(workspace_root, "documents", "raw")
processed_folder = os.path.join(workspace_root, "documents", "processed")


# Load invoice records from local folder
def load_invoice_records():
    invoice_records = load_raw_invoices(raw_folder)
    df = pd.DataFrame(invoice_records)
    st.session_state["invoice_df"] = df    


# Process selected invoice
def process_invoice(selected_item_name):
    st.write(f"Processing invoice: {selected_item_name}")


def main():
    st.title("Intelligent Invoice Processing")

    # Sidebar
    st.sidebar.header("Actions")
    if st.sidebar.button("🔃 Load Invoices"):
        load_invoice_records()
    
    # Show table if loaded
    if "invoice_df" in st.session_state:        
        st.subheader("Invoices Table")
        st.success(f"Loaded {len(st.session_state['invoice_df'])} invoices from local folder.")        
        st.dataframe(st.session_state["invoice_df"])
        
        # Get unique item names from the dataframe
        df = st.session_state["invoice_df"]
        if "Name" in df.columns and len(df) > 0:
            item_names = df["Name"].unique().tolist()
            
            # Create selectbox with a key to maintain state
            selected_item = st.selectbox(
                "Select an item:",
                options=item_names,
                key="selected_item_name"
            )
            
            # Add Process button
            if st.button("Process"):
                process_invoice(selected_item)


if __name__ == "__main__":
    main()
