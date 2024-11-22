import streamlit as st
import pandas as pd
import numpy as np
from networkx import random_regular_graph, to_numpy_array
import io

st.title("Teacher Schedule Generator")

num_teachers = st.number_input("Enter the number of teachers (x):", min_value=1, step=1, value=38)
num_classes = st.number_input("Enter the number of classes per teacher (y):", min_value=1, step=1, value=5)

if st.button("Generate Schedule"):
    try:
        # Generate a y-regular graph with x nodes
        graph = random_regular_graph(num_classes, num_teachers)

        # Convert the graph adjacency matrix to a numpy array
        adj_matrix = to_numpy_array(graph, dtype=int)

        # Fill the table with the adjacency matrix (✓ for connections)
        table = np.array(adj_matrix, dtype=str)
        table[table == "1"] = "✓"
        table[table == "0"] = ""

        # Create a DataFrame for better visualization
        teachers = [f"Teacher_{i+1}" for i in range(num_teachers)]
        table_df = pd.DataFrame(table, columns=teachers, index=teachers)

        # Display and download the schedule
        st.write("Schedule Table:")
        st.dataframe(table_df)

        # Create downloadable Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            table_df.to_excel(writer, sheet_name="Schedule")
        output.seek(0)
        st.download_button(
            label="Download Schedule as Excel",
            data=output,
            file_name="teacher_schedule.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except:
        st.error("Unable to generate schedule. Ensure x * y is even and y ≤ x - 1.")
