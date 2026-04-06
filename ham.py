import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class GoldSilverSalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامج بيع الذهب والفضة والتصليح")
        self.root.geometry("1450x820")
        self.root.configure(bg="#f8fafc")

        self.inventory = [
            {
                "id": 1,
                "category": "ذهب",
                "name": "خاتم",
                "karat": "21",
                "grams": 12,
                "buy_price": 7800,
                "sell_price": 8300,
                "quantity": 4,
            },
            {
                "id": 2,
                "category": "فضة",
                "name": "سلسلة",
                "karat": "925",
                "grams": 18,
                "buy_price": 120,
                "sell_price": 180,
                "quantity": 7,
            },
        ]
        self.sales = []
        self.repairs = []
        self.next_id = 3
        self.invoice_counter = 1001

        self.build_ui()
        self.refresh_inventory_table()
        self.refresh_sales_table()
        self.refresh_repairs_table()
        self.refresh_sale_items()
        self.update_stats()

    def format_currency(self, value):
        return f"{value:,.2f} دج"

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="برنامج بيع الذهب والفضة والتصليح والطباعة",
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
        self.total_repairs_var = tk.StringVar()

        self.create_stat_box(stats_frame, "قيمة المخزون", self.stock_value_var, 0)
        self.create_stat_box(stats_frame, "قيمة البيع المتوقعة", self.expected_sales_var, 1)
        self.create_stat_box(stats_frame, "إجمالي المبيعات", self.total_revenue_var, 2)
        self.create_stat_box(stats_frame, "إجمالي الأرباح", self.total_profit_var, 3)
        self.create_stat_box(stats_frame, "إيرادات التصليح", self.total_repairs_var, 4)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        sales_tab = tk.Frame(notebook, bg="#f8fafc")
        repair_tab = tk.Frame(notebook, bg="#f8fafc")
        notebook.add(sales_tab, text="المبيعات والمخزون")
        notebook.add(repair_tab, text="التصليح")

        self.build_sales_tab(sales_tab)
        self.build_repair_tab(repair_tab)

    def create_stat_box(self, parent, title, variable, column):
        frame = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=15, pady=10)
        frame.grid(row=0, column=column, padx=5, sticky="nsew")
        parent.grid_columnconfigure(column, weight=1)
        tk.Label(frame, text=title, font=("Arial", 11, "bold"), bg="white").pack()
        tk.Label(frame, textvariable=variable, font=("Arial", 13), bg="white", fg="#1d4ed8").pack(pady=5)

    def build_sales_tab(self, parent):
        forms_frame = tk.Frame(parent, bg="#f8fafc")
        forms_frame.pack(fill="x", padx=10, pady=10)

        self.build_add_product_frame(forms_frame)
        self.build_sale_frame(forms_frame)

        tables_frame = tk.Frame(parent, bg="#f8fafc")
        tables_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_inventory_table(tables_frame)
        self.build_sales_table(tables_frame)

    def build_repair_tab(self, parent):
        form = tk.LabelFrame(parent, text="تسجيل عملية تصليح", font=("Arial", 12, "bold"), bg="#f8fafc", padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        labels = ["اسم الزبون", "نوع القطعة", "الوصف", "تكلفة التصليح", "العربون", "الحالة"]
        for idx, label in enumerate(labels):
            tk.Label(form, text=label, bg="#f8fafc").grid(row=idx, column=0, sticky="e", pady=5, padx=5)

        self.repair_customer_entry = tk.Entry(form, justify="right")
        self.repair_customer_entry.grid(row=0, column=1, padx=5, pady=5)

        self.repair_item_entry = tk.Entry(form, justify="right")
        self.repair_item_entry.grid(row=1, column=1, padx=5, pady=5)

        self.repair_desc_entry = tk.Entry(form, justify="right", width=50)
        self.repair_desc_entry.grid(row=2, column=1, padx=5, pady=5)

        self.repair_cost_entry = tk.Entry(form, justify="right")
        self.repair_cost_entry.grid(row=3, column=1, padx=5, pady=5)

        self.repair_paid_entry = tk.Entry(form, justify="right")
        self.repair_paid_entry.grid(row=4, column=1, padx=5, pady=5)
        self.repair_paid_entry.insert(0, "0")

        self.repair_status_combo = ttk.Combobox(form, values=["قيد التصليح", "جاهز", "تم التسليم"], state="readonly", justify="right")
        self.repair_status_combo.grid(row=5, column=1, padx=5, pady=5)
        self.repair_status_combo.set("قيد التصليح")

        tk.Button(form, text="حفظ طلب التصليح", command=self.add_repair, bg="#7c3aed", fg="white").grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
        tk.Button(form, text="تحديث إلى جاهز/تم التسليم", command=self.update_selected_repair_status, bg="#ea580c", fg="white").grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)
        tk.Button(form, text="طباعة وصل التصليح", command=self.print_selected_repair_receipt, bg="#2563eb", fg="white").grid(row=8, column=0, columnspan=2, sticky="ew", pady=5)

        table_frame = tk.LabelFrame(parent, text="سجل التصليحات", font=("Arial", 12, "bold"), bg="#f8fafc")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("date", "customer", "item", "description", "cost", "paid", "remaining", "status")
        self.repairs_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=16)
        headings = {
            "date": "التاريخ",
            "customer": "الزبون",
            "item": "القطعة",
            "description": "الوصف",
            "cost": "التكلفة",
            "paid": "المدفوع",
            "remaining": "المتبقي",
            "status": "الحالة",
        }
        widths = {"date": 130, "customer": 120, "item": 110, "description": 220, "cost": 100, "paid": 100, "remaining": 100, "status": 100}
        for col in columns:
            self.repairs_tree.heading(col, text=headings[col])
            self.repairs_tree.column(col, anchor="center", width=widths[col])
        self.repairs_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def build_add_product_frame(self, parent):
        frame = tk.LabelFrame(parent, text="إضافة قطعة", font=("Arial", 12, "bold"), bg="#f8fafc", padx=10, pady=10)
        frame.pack(side="right", fill="both", expand=True, padx=5)

        fields = ["الصنف", "اسم القطعة", "العيار", "الوزن بالغرام", "سعر الشراء/غ", "سعر البيع/غ", "الكمية"]
        for idx, label in enumerate(fields):
            tk.Label(frame, text=label, bg="#f8fafc").grid(row=idx, column=0, sticky="e", pady=5)

        self.category_combo = ttk.Combobox(frame, values=["ذهب", "فضة"], state="readonly", justify="right")
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)
        self.category_combo.set("ذهب")

        self.name_entry = tk.Entry(frame, justify="right")
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.karat_combo = ttk.Combobox(frame, values=["24", "22", "21", "18", "925", "999"], state="readonly", justify="right")
        self.karat_combo.grid(row=2, column=1, padx=5, pady=5)
        self.karat_combo.set("21")

        self.grams_entry = tk.Entry(frame, justify="right")
        self.grams_entry.grid(row=3, column=1, padx=5, pady=5)

        self.buy_price_entry = tk.Entry(frame, justify="right")
        self.buy_price_entry.grid(row=4, column=1, padx=5, pady=5)

        self.sell_price_entry = tk.Entry(frame, justify="right")
        self.sell_price_entry.grid(row=5, column=1, padx=5, pady=5)

        self.quantity_entry = tk.Entry(frame, justify="right")
        self.quantity_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(frame, text="إضافة للمخزون", command=self.add_product, bg="#2563eb", fg="white").grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

    def build_sale_frame(self, parent):
        frame = tk.LabelFrame(parent, text="تسجيل عملية بيع", font=("Arial", 12, "bold"), bg="#f8fafc", padx=10, pady=10)
        frame.pack(side="left", fill="both", expand=True, padx=5)

        labels = ["القطعة", "الكمية", "اسم الزبون"]
        for idx, label in enumerate(labels):
            tk.Label(frame, text=label, bg="#f8fafc").grid(row=idx, column=0, sticky="e", pady=5)

        self.sale_item_combo = ttk.Combobox(frame, state="readonly", justify="right", width=38)
        self.sale_item_combo.grid(row=0, column=1, padx=5, pady=5)

        self.sale_quantity_entry = tk.Entry(frame, justify="right")
        self.sale_quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        self.sale_quantity_entry.insert(0, "1")

        self.customer_entry = tk.Entry(frame, justify="right")
        self.customer_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="تأكيد البيع", command=self.record_sale, bg="#16a34a", fg="white").grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        tk.Button(frame, text="طباعة فاتورة البيع", command=self.print_last_sale_invoice, bg="#0f766e", fg="white").grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

    def build_inventory_table(self, parent):
        frame = tk.LabelFrame(parent, text="المخزون الحالي", font=("Arial", 12, "bold"), bg="#f8fafc")
        frame.pack(side="right", fill="both", expand=True, padx=5)

        columns = ("category", "name", "karat", "grams", "buy_price", "sell_price", "quantity")
        self.inventory_tree = ttk.Treeview(frame, columns=columns, show="headings", height=16)
        headings = {
            "category": "الصنف",
            "name": "القطعة",
            "karat": "العيار",
            "grams": "الوزن",
            "buy_price": "سعر الشراء",
            "sell_price": "سعر البيع",
            "quantity": "الكمية",
        }
        for col in columns:
            self.inventory_tree.heading(col, text=headings[col])
            self.inventory_tree.column(col, anchor="center", width=95)
        self.inventory_tree.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Button(frame, text="حذف القطعة المحددة", command=self.delete_selected_product, bg="#dc2626", fg="white").pack(fill="x", padx=5, pady=5)

    def build_sales_table(self, parent):
        frame = tk.LabelFrame(parent, text="سجل المبيعات", font=("Arial", 12, "bold"), bg="#f8fafc")
        frame.pack(side="left", fill="both", expand=True, padx=5)

        columns = ("invoice", "date", "item", "customer", "quantity", "total", "profit")
        self.sales_tree = ttk.Treeview(frame, columns=columns, show="headings", height=16)
        headings = {
            "invoice": "رقم الفاتورة",
            "date": "التاريخ",
            "item": "القطعة",
            "customer": "الزبون",
            "quantity": "الكمية",
            "total": "الإجمالي",
            "profit": "الربح",
        }
        widths = {"invoice": 90, "date": 130, "item": 130, "customer": 120, "quantity": 80, "total": 100, "profit": 100}
        for col in columns:
            self.sales_tree.heading(col, text=headings[col])
            self.sales_tree.column(col, anchor="center", width=widths[col])
        self.sales_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_product(self):
        try:
            category = self.category_combo.get()
            name = self.name_entry.get().strip()
            karat = self.karat_combo.get()
            grams = float(self.grams_entry.get())
            buy_price = float(self.buy_price_entry.get())
            sell_price = float(self.sell_price_entry.get())
            quantity = int(self.quantity_entry.get())
            if not name:
                raise ValueError("اسم القطعة مطلوب")

            self.inventory.append({
                "id": self.next_id,
                "category": category,
                "name": name,
                "karat": karat,
                "grams": grams,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "quantity": quantity,
            })
            self.next_id += 1

            for entry in [self.name_entry, self.grams_entry, self.buy_price_entry, self.sell_price_entry, self.quantity_entry]:
                entry.delete(0, tk.END)

            self.refresh_inventory_table()
            self.refresh_sale_items()
            self.update_stats()
            messagebox.showinfo("نجاح", "تمت إضافة القطعة بنجاح")
        except ValueError as e:
            messagebox.showerror("خطأ", f"تحقق من البيانات: {e}")

    def refresh_sale_items(self):
        items = [f"{item['id']} - {item['category']} - {item['name']} - عيار {item['karat']} - الكمية {item['quantity']}" for item in self.inventory]
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

            sale = {
                "invoice": self.invoice_counter,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "item": f"{item['category']} / {item['name']} / {item['karat']}",
                "customer": customer,
                "quantity": quantity,
                "grams": item["grams"],
                "unit_price": item["sell_price"],
                "total": total,
                "profit": profit,
            }
            self.invoice_counter += 1
            self.sales.append(sale)

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
            messagebox.showinfo("نجاح", f"تم تسجيل عملية البيع. رقم الفاتورة: {sale['invoice']}")
        except ValueError as e:
            messagebox.showerror("خطأ", f"تعذر تسجيل البيع: {e}")

    def add_repair(self):
        try:
            customer = self.repair_customer_entry.get().strip()
            item = self.repair_item_entry.get().strip()
            description = self.repair_desc_entry.get().strip()
            cost = float(self.repair_cost_entry.get())
            paid = float(self.repair_paid_entry.get())
            status = self.repair_status_combo.get()
            if not customer or not item or not description:
                raise ValueError("جميع حقول التصليح مطلوبة")
            if paid > cost:
                raise ValueError("العربون لا يمكن أن يكون أكبر من التكلفة")

            self.repairs.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "customer": customer,
                "item": item,
                "description": description,
                "cost": cost,
                "paid": paid,
                "remaining": cost - paid,
                "status": status,
            })

            for entry in [self.repair_customer_entry, self.repair_item_entry, self.repair_desc_entry, self.repair_cost_entry, self.repair_paid_entry]:
                entry.delete(0, tk.END)
            self.repair_paid_entry.insert(0, "0")
            self.repair_status_combo.set("قيد التصليح")

            self.refresh_repairs_table()
            self.update_stats()
            messagebox.showinfo("نجاح", "تم حفظ طلب التصليح")
        except ValueError as e:
            messagebox.showerror("خطأ", f"تعذر الحفظ: {e}")

    def update_selected_repair_status(self):
        selected = self.repairs_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "اختر عملية تصليح أولاً")
            return
        item_data = self.repairs_tree.item(selected[0], "values")
        customer, item_name, current_status = item_data[1], item_data[2], item_data[7]
        new_status = "جاهز" if current_status == "قيد التصليح" else "تم التسليم"
        for repair in self.repairs:
            if repair["customer"] == customer and repair["item"] == item_name and repair["status"] == current_status:
                repair["status"] = new_status
                break
        self.refresh_repairs_table()
        messagebox.showinfo("نجاح", f"تم تحديث الحالة إلى: {new_status}")

    def delete_selected_product(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "اختر قطعة أولاً")
            return
        values = self.inventory_tree.item(selected[0], "values")
        category, name, karat = values[0], values[1], values[2]
        matching_item = next((item for item in self.inventory if item["category"] == category and item["name"] == name and str(item["karat"]) == str(karat)), None)
        if matching_item:
            self.inventory.remove(matching_item)
            self.refresh_inventory_table()
            self.refresh_sale_items()
            self.update_stats()
            messagebox.showinfo("نجاح", "تم حذف القطعة")

    def print_last_sale_invoice(self):
        if not self.sales:
            messagebox.showwarning("تنبيه", "لا توجد عملية بيع للطباعة")
            return
        sale = self.sales[-1]
        text = [
            "فاتورة بيع",
            "=" * 40,
            f"رقم الفاتورة: {sale['invoice']}",
            f"التاريخ: {sale['date']}",
            f"الزبون: {sale['customer']}",
            f"القطعة: {sale['item']}",
            f"الكمية: {sale['quantity']}",
            f"الوزن للقطعة: {sale['grams']} غ",
            f"سعر البيع/غ: {self.format_currency(sale['unit_price'])}",
            f"الإجمالي: {self.format_currency(sale['total'])}",
            "=" * 40,
            "شكرا لتعاملكم معنا",
        ]
        self.open_print_window("فاتورة البيع", "\n".join(text))

    def print_selected_repair_receipt(self):
        selected = self.repairs_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "اختر عملية تصليح أولاً")
            return
        values = self.repairs_tree.item(selected[0], "values")
        text = [
            "وصل استلام تصليح",
            "=" * 40,
            f"التاريخ: {values[0]}",
            f"الزبون: {values[1]}",
            f"القطعة: {values[2]}",
            f"الوصف: {values[3]}",
            f"التكلفة: {values[4]}",
            f"المدفوع: {values[5]}",
            f"المتبقي: {values[6]}",
            f"الحالة: {values[7]}",
            "=" * 40,
            "يرجى الاحتفاظ بهذا الوصل",
        ]
        self.open_print_window("وصل التصليح", "\n".join(text))

    def open_print_window(self, title, content):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("520x620")
        text_widget = tk.Text(window, wrap="word", font=("Courier New", 12))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")
        tk.Button(window, text="طباعة", command=lambda: self.send_text_to_printer(content), bg="#2563eb", fg="white").pack(fill="x", padx=10, pady=10)

    def send_text_to_printer(self, content):
        try:
            temp_file = "invoice_print.txt"
            with open(temp_file, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("الطباعة", "تم تجهيز النص للطباعة. يمكنك ربط الدالة بطابعة النظام لاحقاً.")
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تجهيز الطباعة: {e}")

    def refresh_inventory_table(self):
        for row in self.inventory_tree.get_children():
            self.inventory_tree.delete(row)
        for item in self.inventory:
            self.inventory_tree.insert("", tk.END, values=(item["category"], item["name"], item["karat"], item["grams"], self.format_currency(item["buy_price"]), self.format_currency(item["sell_price"]), item["quantity"]))

    def refresh_sales_table(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)
        for sale in self.sales:
            self.sales_tree.insert("", tk.END, values=(sale["invoice"], sale["date"], sale["item"], sale["customer"], sale["quantity"], self.format_currency(sale["total"]), self.format_currency(sale["profit"])))

    def refresh_repairs_table(self):
        for row in self.repairs_tree.get_children():
            self.repairs_tree.delete(row)
        for repair in self.repairs:
            self.repairs_tree.insert("", tk.END, values=(repair["date"], repair["customer"], repair["item"], repair["description"], self.format_currency(repair["cost"]), self.format_currency(repair["paid"]), self.format_currency(repair["remaining"]), repair["status"]))

    def update_stats(self):
        stock_value = sum(item["quantity"] * item["grams"] * item["buy_price"] for item in self.inventory)
        expected_sales = sum(item["quantity"] * item["grams"] * item["sell_price"] for item in self.inventory)
        total_revenue = sum(sale["total"] for sale in self.sales)
        total_profit = sum(sale["profit"] for sale in self.sales)
        total_repairs = sum(repair["cost"] for repair in self.repairs)
        self.stock_value_var.set(self.format_currency(stock_value))
        self.expected_sales_var.set(self.format_currency(expected_sales))
        self.total_revenue_var.set(self.format_currency(total_revenue))
        self.total_profit_var.set(self.format_currency(total_profit))
        self.total_repairs_var.set(self.format_currency(total_repairs))


if __name__ == "__main__":
    root = tk.Tk()
    app = GoldSilverSalesApp(root)
    root.mainloop()
