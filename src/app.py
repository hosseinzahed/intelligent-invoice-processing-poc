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
    st.success(f"Loaded {len(df)} invoices from local folder.")
    # Show table if loaded
    if "invoice_df" in st.session_state:
        st.subheader("Invoices Table")
        st.dataframe(st.session_state["invoice_df"])


def main():
    st.title("Intelligent Invoice Processing")

    # Sidebar
    st.sidebar.header("Actions")
    if st.sidebar.button("🔃 Load Invoices"):
        load_invoice_records()


if __name__ == "__main__":
    main()
