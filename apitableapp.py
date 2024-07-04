import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import requests


class DataTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Table Application")

        # Initialize variables
        self.selected_api = tk.StringVar()
        self.selected_api.set("API 1")  # Default selection

        self.access_token = tk.StringVar()
        self.access_token_entry = tk.Entry(
            self.root, textvariable=self.access_token, show="*"
        )
        self.access_token_entry.pack(pady=10)
        self.access_token_entry.focus()

        # Dropdown menu to select API
        api_menu = ttk.Combobox(
            self.root,
            textvariable=self.selected_api,
            values=["API 1", "API 2", "API 3", "API 4"],
        )
        api_menu.pack(pady=10)

        # Fetch button
        fetch_button = tk.Button(
            self.root, text="Fetch Data", command=self.fetch_data_from_api
        )
        fetch_button.pack()

        # Initialize an empty DataFrame
        self.df = pd.DataFrame()

        self.sorted_by = None  # To keep track of currently sorted column
        self.ascending = True  # To track sorting order

        self.tree = ttk.Treeview(self.root, show="headings")

        self.tree.pack(pady=20)

    def fetch_data_from_api(self):
        selected_api = self.selected_api.get()
        access_token = self.access_token.get()

        if not access_token:
            tk.messagebox.showerror("Error", "Access token is required")
            return

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            # Add more headers if needed
        }

        api_options = {
            "API 1": {"url": "https://api.example.com/api1", "headers": headers},
            "API 2": {"url": "https://api.example.com/api2", "headers": headers},
            "API 3": {"url": "https://api.example.com/api3", "headers": headers},
            "API 4": {"url": "https://api.example.com/api4", "headers": headers},
        }

        selected_api_data = api_options[selected_api]

        try:
            response = requests.get(
                selected_api_data["url"], headers=selected_api_data["headers"]
            )
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            # Load JSON data from response
            self.data = response.json()

            # Convert data to DataFrame
            self.df = pd.DataFrame(self.data)

            # Clear current table and re-populate with new data
            self.refresh_table()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            tk.messagebox.showerror("Error", f"Error fetching data from API: {e}")

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
