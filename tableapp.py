import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests


class DataTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Table Application")

        # Initialize an empty DataFrame
        self.df = pd.DataFrame()

        self.sorted_by = None  # To keep track of currently sorted column
        self.ascending = True  # To track sorting order

        self.tree = ttk.Treeview(self.root, show="headings")

        # Fetch data from API
        self.fetch_data_from_api()

        # Configure columns (after fetching data)
        if not self.df.empty:
            for col in self.df.columns:
                self.tree.heading(
                    col, text=col, command=lambda c=col: self.sort_by_column(c)
                )
                self.tree.column(col, width=100, anchor=tk.CENTER)

            # Insert data into the table
            for index, row in self.df.iterrows():
                self.tree.insert("", "end", values=list(row))

            self.tree.pack(pady=20)
        else:
            tk.Label(self.root, text="Failed to fetch data from API").pack(pady=20)

    def fetch_data_from_api(self):
        # Replace with your API endpoint URL
        api_url = "https://api.example.com/data"

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            # Load JSON data from response
            self.data = response.json()

            # Convert data to DataFrame
            self.df = pd.DataFrame(self.data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            # Optionally handle the error, e.g., show an error message to the user

    def sort_by_column(self, column):
        # Determine if we are sorting in ascending or descending order
        if self.sorted_by == column:
            self.ascending = not self.ascending
        else:
            self.sorted_by = column
            self.ascending = True

        # Sort the dataframe
        self.df = self.df.sort_values(by=column, ascending=self.ascending)

        # Refresh the table
        self.refresh_table()

    def refresh_table(self):
        # Clear current table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Re-insert updated data
        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))


if __name__ == "__main__":
    root = tk.Tk()
    app = DataTableApp(root)
    root.mainloop()
