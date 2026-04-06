import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class GoldSalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامج بيع الذهب")
        self.root.geometry("1250x700")
        self.root.configure(bg="#f8fafc")

        self.inventory = [
            {
                "id": 1,
                "name": "خاتم",
                "karat": "21",
                "grams": 12,
                "buy_price": 7800,
                "sell_price": 8300,
                "quantity": 4,
            },
            {
                "id": 2,
                "name": "سلسلة",
                "karat": "24",
                "grams": 20,
                "buy_price": 9000,
                "sell_price": 9600,
                "quantity": 2,
            },
        ]
        self.sales = []
        self.next_id = 3

        self.build_ui()
        self.refresh_inventory_table()
        self.refresh_sales_table()
        self.update_stats()
        self.refresh_sale_items()

    def format_currency(self, value):
        return f"{value:,.2f} دج"

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="برنامج بيع الذهب",
            font=("Arial", 20, "bold"),
            bg="#f8fafc",
            fg="#0f172a",
        )
        title.pack(pady=10)

        stats_frame = tk.Frame(self.root, bg="#f8fafc")
        stats_frame.pack(fill="x", padx=10, pady=5)

        self.stock_value_var = tk.StringVar()
        self.expected_sales_var = tk.StringVar()
        self.total_revenue_var = tk.StringVar()
        self.total_profit_var = tk.StringVar()

        self.create_stat_box(stats_frame, "قيمة المخزون", self.stock_value_var, 0)
        self.create_stat_box(stats_frame, "قيمة البيع المتوقعة", self.expected_sales_var, 1)
        self.create_stat_box(stats_frame, "إجمالي المبيعات", self.total_revenue_var, 2)
        self.create_stat_box(stats_frame, "إجمالي الأرباح", self.total_profit_var, 3)

        forms_frame = tk.Frame(self.root, bg="#f8fafc")
        forms_frame.pack(fill="x", padx=10, pady=10)

        self.build_add_product_frame(forms_frame)
        self.build_sale_frame(forms_frame)

        tables_frame = tk.Frame(self.root, bg="#f8fafc")
        tables_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_inventory_table(tables_frame)
        self.build_sales_table(tables_frame)

    def create_stat_box(self, parent, title, variable, column):
        frame = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=20, pady=10)
        frame.grid(row=0, column=column, padx=5, sticky="nsew")
        parent.grid_columnconfigure(column, weight=1)

        tk.Label(frame, text=title, font=("Arial", 12, "bold"), bg="white").pack()
        tk.Label(frame, textvariable=variable, font=("Arial", 14), bg="white", fg="#1d4ed8").pack(pady=5)

    def build_add_product_frame(self, parent):
        frame = tk.LabelFrame(parent, text="إضافة قطعة ذهب", font=("Arial", 12, "bold"), bg="#f8fafc", padx=10, pady=10)
        frame.pack(side="right", fill="both", expand=True, padx=5)

        tk.Label(frame, text="اسم القطعة", bg="#f8fafc").grid(row=0, column=0, sticky="e", pady=5)
        tk.Label(frame, text="العيار", bg="#f8fafc").grid(row=1, column=0, sticky="e", pady=5)
        tk.Label(frame, text="الوزن بالغرام", bg="#f8fafc").grid(row=2, column=0, sticky="e", pady=5)
        tk.Label(frame, text="سعر الشراء/غ", bg="#f8fafc").grid(row=3, column=0, sticky="e", pady=5)
        tk.Label(frame, text="سعر البيع/غ", bg="#f8fafc").grid(row=4, column=0, sticky="e", pady=5)
        tk.Label(frame, text="الكمية", bg="#f8fafc").grid(row=5, column=0, sticky="e", pady=5)

        self.name_entry = tk.Entry(frame, justify="right")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.karat_combo = ttk.Combobox(frame, values=["24", "22", "21", "18"], state="readonly", justify="right")
        self.karat_combo.grid(row=1, column=1, padx=5, pady=5)
        self.karat_combo.set("21")

        self.grams_entry = tk.Entry(frame, justify="right")
        self.grams_entry.grid(row=2, column=1, padx=5, pady=5)

        self.buy_price_entry = tk.Entry(frame, justify="right")
        self.buy_price_entry.grid(row=3, column=1, padx=5, pady=5)

        self.sell_price_entry = tk.Entry(frame, justify="right")
        self.sell_price_entry.grid(row=4, column=1, padx=5, pady=5)

        self.quantity_entry = tk.Entry(frame, justify="right")
        self.quantity_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(frame, text="إضافة للمخزون", command=self.add_product, bg="#2563eb", fg="white").grid(
            row=6, column=0, columnspan=2, pady=10, sticky="ew"
        )

    def build_sale_frame(self, parent):
        frame = tk.LabelFrame(parent, text="تسجيل عملية بيع", font=("Arial", 12, "bold"), bg="#f8fafc", padx=10, pady=10)
        frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(frame, text="القطعة", bg="#f8fafc").grid(row=0, column=0, sticky="e", pady=5)
        tk.Label(frame, text="الكمية", bg="#f8fafc").grid(row=1, column=0, sticky="e", pady=5)
        tk.Label(frame, text="اسم الزبون", bg="#f8fafc").grid(row=2, column=0, sticky="e", pady=5)

        self.sale_item_combo = ttk.Combobox(frame, state="readonly", justify="right")
        self.sale_item_combo.grid(row=0, column=1, padx=5, pady=5)

        self.sale_quantity_entry = tk.Entry(frame, justify="right")
        self.sale_quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        self.sale_quantity_entry.insert(0, "1")

        self.customer_entry = tk.Entry(frame, justify="right")
        self.customer_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="تأكيد البيع", command=self.record_sale, bg="#16a34a", fg="white").grid(
            row=3, column=0, columnspan=2, pady=10, sticky="ew"
        )

    def build_inventory_table(self, parent):
        frame = tk.LabelFrame(parent, text="المخزون الحالي", font=("Arial", 12, "bold"), bg="#f8fafc")
        frame.pack(side="right", fill="both", expand=True, padx=5)

        columns = ("name", "karat", "grams", "buy_price", "sell_price", "quantity")
        self.inventory_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        headings = {
            "name": "القطعة",
            "karat": "العيار",
            "grams": "الوزن",
            "buy_price": "سعر الشراء",
            "sell_price": "سعر البيع",
            "quantity": "الكمية",
        }

        for col in columns:
            self.inventory_tree.heading(col, text=headings[col])
            self.inventory_tree.column(col, anchor="center", width=100)

        self.inventory_tree.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Button(frame, text="حذف القطعة المحددة", command=self.delete_selected_product, bg="#dc2626", fg="white").pack(
            fill="x", padx=5, pady=5
        )

    def build_sales_table(self, parent):
        frame = tk.LabelFrame(parent, text="سجل المبيعات", font=("Arial", 12, "bold"), bg="#f8fafc")
        frame.pack(side="left", fill="both", expand=True, padx=5)

        columns = ("date", "item", "customer", "quantity", "total", "profit")
        self.sales_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        headings = {
            "date": "التاريخ",
            "item": "القطعة",
            "customer": "الزبون",
            "quantity": "الكمية",
            "total": "الإجمالي",
            "profit": "الربح",
        }

        for col in columns:
            self.sales_tree.heading(col, text=headings[col])
            self.sales_tree.column(col, anchor="center", width=110)

        self.sales_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_product(self):
        try:
            name = self.name_entry.get().strip()
            karat = self.karat_combo.get()
            grams = float(self.grams_entry.get())
            buy_price = float(self.buy_price_entry.get())
            sell_price = float(self.sell_price_entry.get())
            quantity = int(self.quantity_entry.get())

            if not name:
                raise ValueError("اسم القطعة مطلوب")

            self.inventory.append(
                {
                    "id": self.next_id,
                    "name": name,
                    "karat": karat,
                    "grams": grams,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "quantity": quantity,
                }
            )
            self.next_id += 1

            self.name_entry.delete(0, tk.END)
            self.grams_entry.delete(0, tk.END)
            self.buy_price_entry.delete(0, tk.END)
            self.sell_price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)

            self.refresh_inventory_table()
            self.refresh_sale_items()
            self.update_stats()
            messagebox.showinfo("نجاح", "تمت إضافة القطعة بنجاح")
        except ValueError as e:
            messagebox.showerror("خطأ", f"تحقق من البيانات: {e}")

    def refresh_sale_items(self):
        items = [f"{item['id']} - {item['name']} - عيار {item['karat']} - الكمية {item['quantity']}" for item in self.inventory]
        self.sale_item_combo["values"] = items
        if items:
            self.sale_item_combo.current(0)
        else:
            self.sale_item_combo.set("")

    def record_sale(self):
        try:
            selected = self.sale_item_combo.get()
            if not selected:
                raise ValueError("لا توجد قطعة محددة")

            item_id = int(selected.split(" - ")[0])
            quantity = int(self.sale_quantity_entry.get())
            customer = self.customer_entry.get().strip() or "زبون مباشر"

            item = next((x for x in self.inventory if x["id"] == item_id), None)
            if item is None:
                raise ValueError("القطعة غير موجودة")
            if quantity <= 0 or quantity > item["quantity"]:
                raise ValueError("الكمية غير صالحة")

            total = quantity * item["grams"] * item["sell_price"]
            cost = quantity * item["grams"] * item["buy_price"]
            profit = total - cost

            self.sales.append(
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "item": f"{item['name']} / {item['karat']}",
                    "customer": customer,
                    "quantity": quantity,
                    "total": total,
                    "profit": profit,
                }
            )

            item["quantity"] -= quantity
            if item["quantity"] == 0:
                self.inventory = [x for x in self.inventory if x["id"] != item_id]

            self.sale_quantity_entry.delete(0, tk.END)
            self.sale_quantity_entry.insert(0, "1")
            self.customer_entry.delete(0, tk.END)

            self.refresh_inventory_table()
            self.refresh_sales_table()
            self.refresh_sale_items()
            self.update_stats()
            messagebox.showinfo("نجاح", "تم تسجيل عملية البيع")
        except ValueError as e:
            messagebox.showerror("خطأ", f"تعذر تسجيل البيع: {e}")

    def delete_selected_product(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "اختر قطعة أولاً")
            return

        values = self.inventory_tree.item(selected[0], "values")
        name = values[0]
        matching_item = next((item for item in self.inventory if item["name"] == name and str(item["karat"]) == str(values[1])), None)

        if matching_item:
            self.inventory.remove(matching_item)
            self.refresh_inventory_table()
            self.refresh_sale_items()
            self.update_stats()
            messagebox.showinfo("نجاح", "تم حذف القطعة")

    def refresh_inventory_table(self):
        for row in self.inventory_tree.get_children():
            self.inventory_tree.delete(row)

        for item in self.inventory:
            self.inventory_tree.insert(
                "",
                tk.END,
                values=(
                    item["name"],
                    item["karat"],
                    item["grams"],
                    self.format_currency(item["buy_price"]),
                    self.format_currency(item["sell_price"]),
                    item["quantity"],
                ),
            )

    def refresh_sales_table(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)

        for sale in self.sales:
            self.sales_tree.insert(
                "",
                tk.END,
                values=(
                    sale["date"],
                    sale["item"],
                    sale["customer"],
                    sale["quantity"],
                    self.format_currency(sale["total"]),
                    self.format_currency(sale["profit"]),
                ),
            )

    def update_stats(self):
        stock_value = sum(item["quantity"] * item["grams"] * item["buy_price"] for item in self.inventory)
        expected_sales = sum(item["quantity"] * item["grams"] * item["sell_price"] for item in self.inventory)
        total_revenue = sum(sale["total"] for sale in self.sales)
        total_profit = sum(sale["profit"] for sale in self.sales)

        self.stock_value_var.set(self.format_currency(stock_value))
        self.expected_sales_var.set(self.format_currency(expected_sales))
        self.total_revenue_var.set(self.format_currency(total_revenue))
        self.total_profit_var.set(self.format_currency(total_profit))


if __name__ == "__main__":
    root = tk.Tk()
    app = GoldSalesApp(root)
    root.mainloop()
