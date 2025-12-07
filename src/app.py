import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv(override=True)


def main():
    st.title("Intelligent Invoice Processing")

    # Sidebar
    st.sidebar.header("Actions")
    if st.sidebar.button("🔃 Load Invoices"):
        # Load files from local documents/raw folder
        # Get workspace root (parent of src)
        workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        raw_folder = os.path.join(workspace_root, "documents", "raw")
        invoice_records = []
        if os.path.exists(raw_folder):
            for filename in os.listdir(raw_folder):
                file_path = os.path.join(raw_folder, filename)
                if os.path.isfile(file_path):
                    size_kb = round(os.path.getsize(file_path) / 1024, 2)
                    invoice_records.append({
                        "Name": filename,
                        "Size (KB)": size_kb,
                        "Status": "Unprocessed"
                    })
        df = pd.DataFrame(invoice_records)
        st.session_state["invoice_df"] = df
        st.success(f"Loaded {len(invoice_records)} invoices from local folder.")

    # Show table if loaded
    if "invoice_df" in st.session_state:
        st.subheader("Invoices Table")
        st.dataframe(st.session_state["invoice_df"])

    # ...existing code...

if __name__ == "__main__":
    main()


