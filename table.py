import tkinter as tk
from tkinter import ttk
import pandas as pd


class DataTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Table Application")

        # Sample data (you can replace this with your own dataset)
        self.data = {
            "Name": ["John", "Jane", "Alice", "Bob", "Eve"],
            "Age": [25, 30, 28, 35, 27],
            "City": ["New York", "San Francisco", "Los Angeles", "Chicago", "Seattle"],
        }

        self.df = pd.DataFrame(self.data)
        self.sorted_by = None  # To keep track of currently sorted column
        self.ascending = True  # To track sorting order

        self.tree = ttk.Treeview(
            self.root, columns=list(self.df.columns), show="headings"
        )

        # Configure columns
        for col in self.df.columns:
            self.tree.heading(
                col, text=col, command=lambda c=col: self.sort_by_column(c)
            )
            self.tree.column(col, width=100, anchor=tk.CENTER)

        # Insert data into the table
        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.tree.pack(pady=20)

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
