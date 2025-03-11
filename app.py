import streamlit as st
import pandas as pd

# Set page title and configuration
st.set_page_config(page_title="CSV Viewer and Filter", layout="wide")

# App title and description
st.title("CSV Viewer and Filter")
st.write("Upload a CSV file to view its content and filter by column values.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Main application logic
if uploaded_file is not None:
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display basic information
        st.subheader("Data Preview")
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        
        # Create two columns for layout
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Filter section
            st.subheader("Filter Data")
            
            # Column selection for filtering
            selected_column = st.selectbox(
                "Select column to filter by:",
                options=df.columns.tolist()
            )
            
            # Get unique values from the selected column for reference
            unique_values = df[selected_column].unique()
            st.write(f"This column has {len(unique_values)} unique values")
            
            # Value input for filtering
            filter_value = st.text_input("Enter value to match:")
            
            # Apply filter button
            filter_pressed = st.button("Apply Filter")
        
        with col2:
            # Display section
            st.subheader("Data Table")
            
            # Apply filter if requested
            if filter_pressed and filter_value:
                filtered_df = df[df[selected_column].astype(str) == filter_value]
                
                if not filtered_df.empty:
                    st.write(f"Showing {filtered_df.shape[0]} rows that match filter criteria")
                    st.dataframe(filtered_df)
                else:
                    st.warning(f"No matching rows found for '{filter_value}' in column '{selected_column}'")
                    st.dataframe(df)
            else:
                # Show the full dataset
                st.dataframe(df)
        
        # Show column information
        st.subheader("Column Information")
        column_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes,
            'Non-Null Count': df.count(),
            'Null Count': df.isna().sum()
        })
        st.dataframe(column_info)
                
    except Exception as e:
        st.error(f"Error loading or processing the CSV file: {e}")
else:
    # Instructions when no file is uploaded
    st.info("Please upload a CSV file to get started.")
    
    # Example info
    st.subheader("How to use this app:")
    st.markdown("""
    1. Click the 'Browse files' button to upload your CSV file
    2. Once uploaded, you'll see the data displayed as a table
    3. Select a column to filter by from the dropdown
    4. Enter a value to match in the text input
    5. Click 'Apply Filter' to show only the matching rows
    """)