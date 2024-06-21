import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from datetime import datetime
from models import ObservableFeatures, AnimalSaleEntry
from image_analysis import analyze_image
from database_operations import search_sales, get_all_clients
import traceback

class AnimalSalesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Animal Sales Application")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Customer selection
        self.customer_frame = ttk.Frame(self)
        self.customer_frame.pack(pady=10)
        ttk.Label(self.customer_frame, text="Select Customer:").pack(side=tk.LEFT)
        self.customer_var = tk.StringVar(self)
        self.customer_dropdown = ttk.Combobox(self.customer_frame, textvariable=self.customer_var, state="readonly")
        self.customer_dropdown.pack(side=tk.LEFT)
        self.load_customers()
        self.customer_dropdown.bind("<<ComboboxSelected>>", self.on_customer_selected)

        # Image selection
        ttk.Button(self, text="Select Image", command=self.select_image).pack(pady=10)

        # Search results frame
        self.results_frame = ttk.Frame(self)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.results_tree = ttk.Treeview(self.results_frame, columns=("ID", "Date", "Species", "Breed", "Size", "Price", "Client"), show="headings")
        self.results_tree.heading("ID", text="ID")
        self.results_tree.heading("Date", text="Date")
        self.results_tree.heading("Species", text="Species")
        self.results_tree.heading("Breed", text="Breed")
        self.results_tree.heading("Size", text="Size")
        self.results_tree.heading("Price", text="Price")
        self.results_tree.heading("Client", text="Client")
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        self.results_tree.bind("<Double-1>", self.on_result_double_click)

        # Order form
        self.order_frame = ttk.LabelFrame(self, text="Order Form")
        self.order_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        fields = [("Date", "date"), ("Species", "species"), ("Breed", "breed"), ("Size", "size"),
                  ("Weight", "weight"), ("Coat Length", "coat_length"), ("Coat Color", "coat_color"),
                  ("Price", "price"), ("Client Name", "client_name"), ("Client Email", "client_email")]

        self.order_vars = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(self.order_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            var = tk.StringVar()
            ttk.Entry(self.order_frame, textvariable=var).grid(row=i, column=1, sticky=tk.EW, padx=5, pady=2)
            self.order_vars[field] = var

        ttk.Button(self.order_frame, text="Save Order", command=self.save_order).grid(row=len(fields), column=1, sticky=tk.E, padx=5, pady=10)

    def load_customers(self):
        conn = sqlite3.connect('animal_sales.db')
        clients = ["Any"] + get_all_clients(conn)
        conn.close()
        self.customer_dropdown['values'] = clients
        self.customer_var.set(clients[0])

    def on_customer_selected(self, event):
        print(f"Selected customer: {self.customer_var.get()}")

    def select_image(self):
        print("Select image button clicked")
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        print(f"Selected image path: {image_path}")
        if image_path:
            self.analyze_and_search(image_path)
        else:
            print("No image selected")

    def analyze_and_search(self, image_path):
        print(f"Analyzing image: {image_path}")
        try:
            features = analyze_image(image_path)
            print(f"Extracted features: {features}")
            if features:
                conn = sqlite3.connect('animal_sales.db')
                selected_customer = self.customer_var.get()
                print(f"Selected customer: {selected_customer}")
                matches = search_sales(conn, features, selected_customer if selected_customer != "Any" else None)
                conn.close()
                if matches:
                    print(f"Matches found: {len(matches)}")
                    self.display_results(matches)
                    messagebox.showinfo("Matches Found", f"{len(matches)} matches found based on breed or coat characteristics.")
                else:
                    print("No matches found")
                    messagebox.showinfo("No Matches", "No matching sales found in the database. You can use the extracted features to create a new order.")
                self.populate_order_form_from_features(features)
            else:
                print("No features extracted from the image")
                messagebox.showerror("Analysis Failed", "Failed to extract features from the image. Please try another image.")
        except Exception as e:
            print(f"An error occurred during image analysis: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_results(self, matches):
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)
        for match in matches:
            self.results_tree.insert("", "end", values=(match.id, match.date.strftime("%Y-%m-%d"), 
                                                        match.species, match.breed, match.size, 
                                                        f"${match.price:.2f}", match.client_name))

    def on_result_double_click(self, event):
        item = self.results_tree.selection()[0]
        values = self.results_tree.item(item, "values")
        self.populate_order_form(values)

    def populate_order_form(self, values):
        fields = ["date", "species", "breed", "size", "price", "client_name"]
        for field, value in zip(fields, values[1:]):  # Skip ID
            self.order_vars[field].set(value)

    def populate_order_form_from_features(self, features):
        self.order_vars["date"].set(datetime.now().strftime("%Y-%m-%d"))
        self.order_vars["species"].set(features.species or "")
        self.order_vars["breed"].set(features.breed or "")
        self.order_vars["size"].set(features.size or "")
        self.order_vars["coat_length"].set(features.coat_length or "")
        self.order_vars["coat_color"].set(features.coat_color or "")

    def save_order(self):
        # Mock save functionality
        order_data = {field: var.get() for field, var in self.order_vars.items()}
        print("Order saved (mock):")
        for field, value in order_data.items():
            print(f"{field}: {value}")
        messagebox.showinfo("Order Saved", "The order has been saved (mock).")

if __name__ == "__main__":
    app = AnimalSalesApp()
    app.mainloop()