import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

DB_NAME = "gold_silver_shop.db"


class Database:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                item_name TEXT NOT NULL,
                purity TEXT NOT NULL,
                weight REAL NOT NULL,
                qty INTEGER NOT NULL,
                buy_price REAL NOT NULL,
                sell_price REAL NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                trans_type TEXT NOT NULL,
                category TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                item_name TEXT NOT NULL,
                purity TEXT NOT NULL,
                weight REAL NOT NULL,
                qty INTEGER NOT NULL,
                gram_price REAL NOT NULL,
                workmanship REAL NOT NULL,
                total REAL NOT NULL,
                notes TEXT
            )
            """
        )
        self.conn.commit()

    def add_inventory(self, data):
        self.conn.execute(
            "INSERT INTO inventory(category, item_name, purity, weight, qty, buy_price, sell_price) VALUES (?, ?, ?, ?, ?, ?, ?)",
            data,
        )
        self.conn.commit()

    def update_inventory_qty(self, item_id, qty):
        self.conn.execute("UPDATE inventory SET qty=? WHERE id=?", (qty, item_id))
        self.conn.commit()

    def delete_inventory(self, item_id):
        self.conn.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        self.conn.commit()

    def fetch_inventory(self):
        return self.conn.execute(
            "SELECT id, category, item_name, purity, weight, qty, buy_price, sell_price FROM inventory ORDER BY id DESC"
        ).fetchall()

    def add_transaction(self, data):
        self.conn.execute(
            """
            INSERT INTO transactions(
                created_at, trans_type, category, customer_name, item_name, purity,
                weight, qty, gram_price, workmanship, total, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data,
        )
        self.conn.commit()

    def fetch_transactions(self):
        return self.conn.execute(
            "SELECT id, created_at, trans_type, category, customer_name, item_name, purity, weight, qty, gram_price, workmanship, total, notes FROM transactions ORDER BY id DESC"
        ).fetchall()

    def totals(self):
        inventory = self.conn.execute(
            "SELECT COALESCE(SUM(weight * qty * buy_price),0), COALESCE(SUM(weight * qty * sell_price),0), COALESCE(SUM(qty),0) FROM inventory"
        ).fetchone()
        sales = self.conn.execute(
            "SELECT COALESCE(SUM(total),0) FROM transactions WHERE trans_type='بيع'"
        ).fetchone()[0]
        purchases = self.conn.execute(
            "SELECT COALESCE(SUM(total),0) FROM transactions WHERE trans_type='شراء'"
        ).fetchone()[0]
        return inventory, sales, purchases


class GoldSilverApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("مجوهرات برطال")
        self.root.geometry("1360x820")
        self.root.configure(bg="#f5f7fb")

        self.invoice_text = ""

        self.build_ui()
        self.refresh_inventory()
        self.refresh_transactions()
        self.refresh_summary()

    def money(self, value):
        return f"{value:,.2f} دج"

    def build_ui(self):
        # عنوان + شعار
        header = tk.Label(
            self.root,
            text="💎 مجوهرات برطال 💎",
            font=("Arial", 26, "bold"),
            bg="#f5f7fb",
            fg="#b45309",
        )
        header.pack(pady=5)

        sub_header = tk.Label(
            self.root,
            text="العنوان: عين قشرة - سكيكدة | هاتف: 0550 00 00 00",
            font=("Arial", 11),
            bg="#f5f7fb",
            fg="#475569",
        )
        sub_header.pack(pady=5)

        self.summary_frame = tk.Frame(self.root, bg="#f5f7fb")
        self.summary_frame.pack(fill="x", padx=10)

        self.stock_buy_var = tk.StringVar()
        self.stock_sell_var = tk.StringVar()
        self.stock_qty_var = tk.StringVar()
        self.sales_var = tk.StringVar()
        self.purchases_var = tk.StringVar()

        for i, (title, var) in enumerate([
            ("قيمة المخزون شراء", self.stock_buy_var),
            ("قيمة المخزون بيع", self.stock_sell_var),
            ("عدد القطع", self.stock_qty_var),
            ("إجمالي المبيعات", self.sales_var),
            ("إجمالي المشتريات", self.purchases_var),
        ]):
            box = tk.Frame(self.summary_frame, bg="white", bd=1, relief="solid", padx=15, pady=10)
            box.grid(row=0, column=i, padx=4, sticky="nsew")
            self.summary_frame.grid_columnconfigure(i, weight=1)
            tk.Label(box, text=title, font=("Arial", 11, "bold"), bg="white").pack()
            tk.Label(box, textvariable=var, font=("Arial", 13), bg="white", fg="#1d4ed8").pack(pady=5)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=12)

        self.tab_inventory = tk.Frame(notebook, bg="#f5f7fb")
        self.tab_sales = tk.Frame(notebook, bg="#f5f7fb")
        self.tab_history = tk.Frame(notebook, bg="#f5f7fb")
        self.tab_invoice = tk.Frame(notebook, bg="#f5f7fb")

        notebook.add(self.tab_inventory, text="المخزون")
        notebook.add(self.tab_sales, text="بيع / شراء")
        notebook.add(self.tab_history, text="السجل")
        notebook.add(self.tab_invoice, text="الطباعة")

        self.build_inventory_tab()
        self.build_sales_tab()
        self.build_history_tab()
        self.build_invoice_tab()

    def build_inventory_tab(self):
        form = tk.LabelFrame(self.tab_inventory, text="إضافة قطعة إلى المخزون", font=("Arial", 12, "bold"), bg="#f5f7fb", padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        labels = ["الصنف", "اسم القطعة", "العيار", "الوزن", "الكمية", "سعر الشراء/غ", "سعر البيع/غ"]
        for i, text in enumerate(labels):
            tk.Label(form, text=text, bg="#f5f7fb").grid(row=i, column=0, sticky="e", pady=4, padx=5)

        self.inv_category = ttk.Combobox(form, values=["ذهب", "فضة"], state="readonly", justify="right")
        self.inv_category.grid(row=0, column=1, padx=5, pady=4)
        self.inv_category.set("ذهب")

        self.inv_name = tk.Entry(form, justify="right")
        self.inv_name.grid(row=1, column=1, padx=5, pady=4)

        self.inv_purity = ttk.Combobox(form, values=["24", "22", "21", "18", "999", "925"], state="readonly", justify="right")
        self.inv_purity.grid(row=2, column=1, padx=5, pady=4)
        self.inv_purity.set("21")

        self.inv_weight = tk.Entry(form, justify="right")
        self.inv_weight.grid(row=3, column=1, padx=5, pady=4)

        self.inv_qty = tk.Entry(form, justify="right")
        self.inv_qty.grid(row=4, column=1, padx=5, pady=4)

        self.inv_buy = tk.Entry(form, justify="right")
        self.inv_buy.grid(row=5, column=1, padx=5, pady=4)

        self.inv_sell = tk.Entry(form, justify="right")
        self.inv_sell.grid(row=6, column=1, padx=5, pady=4)

        tk.Button(form, text="إضافة للمخزون", command=self.add_inventory_item, bg="#2563eb", fg="white", font=("Arial", 12, "bold"), padx=10, pady=8, relief="raised", bd=3).grid(row=7, column=0, columnspan=2, sticky="ew", pady=8)

        table_frame = tk.LabelFrame(self.tab_inventory, text="قائمة المخزون", font=("Arial", 12, "bold"), bg="#f5f7fb")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id", "category", "name", "purity", "weight", "qty", "buy", "sell")
        self.inventory_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=16)
        heads = {
            "id": "رقم",
            "category": "الصنف",
            "name": "القطعة",
            "purity": "العيار",
            "weight": "الوزن",
            "qty": "الكمية",
            "buy": "شراء/غ",
            "sell": "بيع/غ",
        }
        widths = {"id": 60, "category": 90, "name": 140, "purity": 80, "weight": 90, "qty": 80, "buy": 110, "sell": 110}
        for c in cols:
            self.inventory_tree.heading(c, text=heads[c])
            self.inventory_tree.column(c, width=widths[c], anchor="center")
        self.inventory_tree.pack(fill="both", expand=True, padx=5, pady=5)

        btns = tk.Frame(table_frame, bg="#f5f7fb")
        btns.pack(fill="x", padx=5, pady=5)
        tk.Button(btns, text="حذف المحدد", command=self.delete_inventory_item, bg="#dc2626", fg="white", font=("Arial", 12, "bold"), padx=10, pady=8, relief="raised", bd=3).pack(side="right", padx=4)
        tk.Button(btns, text="تحديث الجداول", command=self.refresh_all, bg="#475569", fg="white", font=("Arial", 12, "bold"), padx=10, pady=8, relief="raised", bd=3).pack(side="right", padx=4)

    def build_sales_tab(self):
        wrapper = tk.Frame(self.tab_sales, bg="#f5f7fb")
        wrapper.pack(fill="both", expand=True, padx=10, pady=10)

        form = tk.LabelFrame(wrapper, text="عملية بيع أو شراء", font=("Arial", 12, "bold"), bg="#f5f7fb", padx=10, pady=10)
        form.pack(side="right", fill="y", padx=5)

        labels = ["نوع العملية", "اختر من المخزون", "اسم الزبون", "الكمية", "المصنعية", "ملاحظات"]
        for i, txt in enumerate(labels):
            tk.Label(form, text=txt, bg="#f5f7fb").grid(row=i, column=0, sticky="e", pady=4, padx=5)

        self.trans_type = ttk.Combobox(form, values=["بيع", "شراء"], state="readonly", justify="right")
        self.trans_type.grid(row=0, column=1, padx=5, pady=4)
        self.trans_type.set("بيع")

        self.stock_choice = ttk.Combobox(form, state="readonly", justify="right", width=42)
        self.stock_choice.grid(row=1, column=1, padx=5, pady=4)

        self.customer_name = tk.Entry(form, justify="right")
        self.customer_name.grid(row=2, column=1, padx=5, pady=4)

        self.trans_qty = tk.Entry(form, justify="right")
        self.trans_qty.grid(row=3, column=1, padx=5, pady=4)
        self.trans_qty.insert(0, "1")

        self.workmanship = tk.Entry(form, justify="right")
        self.workmanship.grid(row=4, column=1, padx=5, pady=4)
        self.workmanship.insert(0, "0")

        self.notes = tk.Entry(form, justify="right")
        self.notes.grid(row=5, column=1, padx=5, pady=4)

        tk.Button(form, text="تنفيذ العملية", command=self.execute_transaction, bg="#16a34a", fg="white", font=("Arial", 12, "bold"), padx=10, pady=8, relief="raised", bd=3).grid(row=6, column=0, columnspan=2, sticky="ew", pady=8)
        tk.Button(form, text="إنشاء فاتورة", command=self.open_invoice_tab, bg="#0f766e", fg="white", font=("Arial", 12, "bold"), padx=10, pady=8, relief="raised", bd=3).grid(row=7, column=0, columnspan=2, sticky="ew", pady=4)

        info = tk.LabelFrame(wrapper, text="معاينة المخزون", font=("Arial", 12, "bold"), bg="#f5f7fb")
        info.pack(side="left", fill="both", expand=True, padx=5)

        cols = ("id", "category", "name", "purity", "weight", "qty", "buy", "sell")
        self.stock_preview = ttk.Treeview(info, columns=cols, show="headings", height=18)
        for c in cols:
            self.stock_preview.heading(c, text=c)
            self.stock_preview.column(c, anchor="center", width=100)
        self.stock_preview.pack(fill="both", expand=True, padx=5, pady=5)

    def build_history_tab(self):
        frame = tk.LabelFrame(self.tab_history, text="سجل كل العمليات", font=("Arial", 12, "bold"), bg="#f5f7fb")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id", "date", "type", "category", "customer", "item", "purity", "weight", "qty", "price", "work", "total")
        self.history_tree = ttk.Treeview(frame, columns=cols, show="headings", height=22)
        heads = ["رقم", "التاريخ", "العملية", "الصنف", "الزبون", "القطعة", "العيار", "الوزن", "الكمية", "السعر", "المصنعية", "الإجمالي"]
        widths = [50, 130, 70, 80, 120, 120, 80, 80, 70, 90, 90, 100]
        for c, h, w in zip(cols, heads, widths):
            self.history_tree.heading(c, text=h)
            self.history_tree.column(c, width=w, anchor="center")
        self.history_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def build_invoice_tab(self):
        top = tk.Frame(self.tab_invoice, bg="#f5f7fb")
        top.pack(fill="x", padx=10, pady=10)
        tk.Button(top, text="حفظ الفاتورة TXT", command=self.save_invoice_file, bg="#2563eb", fg="white", font=("Arial", 12, "bold"), padx=10, pady=8, relief="raised", bd=3).pack(side="right", padx=4)
        tk.Button(top, text="طباعة", command=self.print_invoice, bg="#16a34a", fg="white", font=("Arial", 12, "bold"), padx=10, pady=8, relief="raised", bd=3).pack(side="right", padx=4)

        self.invoice_box = tk.Text(self.tab_invoice, font=("Courier New", 12), wrap="word")
        self.invoice_box.pack(fill="both", expand=True, padx=10, pady=10)

    def add_inventory_item(self):
        try:
            data = (
                self.inv_category.get(),
                self.inv_name.get().strip(),
                self.inv_purity.get(),
                float(self.inv_weight.get()),
                int(self.inv_qty.get()),
                float(self.inv_buy.get()),
                float(self.inv_sell.get()),
            )
            if not data[1]:
                raise ValueError("اسم القطعة مطلوب")
            self.db.add_inventory(data)
            for entry in [self.inv_name, self.inv_weight, self.inv_qty, self.inv_buy, self.inv_sell]:
                entry.delete(0, tk.END)
            self.refresh_all()
            messagebox.showinfo("نجاح", "تمت إضافة القطعة للمخزون")
        except ValueError as e:
            messagebox.showerror("خطأ", str(e))

    def selected_inventory_id(self):
        sel = self.inventory_tree.selection()
        if not sel:
            return None
        return int(self.inventory_tree.item(sel[0], "values")[0])

    def delete_inventory_item(self):
        item_id = self.selected_inventory_id()
        if not item_id:
            messagebox.showwarning("تنبيه", "اختر قطعة من الجدول")
            return
        self.db.delete_inventory(item_id)
        self.refresh_all()

    def refresh_inventory(self):
        rows = self.db.fetch_inventory()
        for tree in [self.inventory_tree, self.stock_preview]:
            for i in tree.get_children():
                tree.delete(i)
            for row in rows:
                display = (row[0], row[1], row[2], row[3], row[4], row[5], self.money(row[6]), self.money(row[7]))
                tree.insert("", tk.END, values=display)

        choices = [f"{r[0]} | {r[1]} | {r[2]} | عيار {r[3]} | وزن {r[4]} | كمية {r[5]}" for r in rows]
        self.stock_choice["values"] = choices
        if choices:
            self.stock_choice.current(0)
        else:
            self.stock_choice.set("")

    def refresh_transactions(self):
        rows = self.db.fetch_transactions()
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        for r in rows:
            self.history_tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], self.money(r[9]), self.money(r[10]), self.money(r[11])))

    def refresh_summary(self):
        inventory, sales, purchases = self.db.totals()
        self.stock_buy_var.set(self.money(inventory[0]))
        self.stock_sell_var.set(self.money(inventory[1]))
        self.stock_qty_var.set(str(inventory[2]))
        self.sales_var.set(self.money(sales))
        self.purchases_var.set(self.money(purchases))

    def refresh_all(self):
        self.refresh_inventory()
        self.refresh_transactions()
        self.refresh_summary()

    def parse_stock_choice(self):
        text = self.stock_choice.get().strip()
        if not text:
            raise ValueError("اختر قطعة من المخزون")
        return int(text.split("|")[0].strip())

    def execute_transaction(self):
        try:
            item_id = self.parse_stock_choice()
            rows = self.db.fetch_inventory()
            row = next((r for r in rows if r[0] == item_id), None)
            if not row:
                raise ValueError("العنصر غير موجود")

            trans_type = self.trans_type.get()
            customer = self.customer_name.get().strip() or "زبون مباشر"
            qty = int(self.trans_qty.get())
            workmanship = float(self.workmanship.get() or 0)
            notes = self.notes.get().strip()
            if qty <= 0:
                raise ValueError("الكمية غير صالحة")

            stock_qty = row[5]
            if trans_type == "بيع" and qty > stock_qty:
                raise ValueError("الكمية المطلوبة أكبر من المتوفر")

            category, item_name, purity, weight = row[1], row[2], row[3], row[4]
            gram_price = row[7] if trans_type == "بيع" else row[6]
            total = (weight * qty * gram_price) + workmanship

            if trans_type == "بيع":
                self.db.update_inventory_qty(item_id, stock_qty - qty)
                if stock_qty - qty == 0:
                    self.db.delete_inventory(item_id)
            else:
                self.db.update_inventory_qty(item_id, stock_qty + qty)

            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.add_transaction((created_at, trans_type, category, customer, item_name, purity, weight, qty, gram_price, workmanship, total, notes))
            self.invoice_text = self.generate_invoice(created_at, trans_type, category, customer, item_name, purity, weight, qty, gram_price, workmanship, total, notes)
            self.invoice_box.delete("1.0", tk.END)
            self.invoice_box.insert(tk.END, self.invoice_text)

            self.customer_name.delete(0, tk.END)
            self.trans_qty.delete(0, tk.END)
            self.trans_qty.insert(0, "1")
            self.workmanship.delete(0, tk.END)
            self.workmanship.insert(0, "0")
            self.notes.delete(0, tk.END)

            self.refresh_all()
            messagebox.showinfo("نجاح", "تم تنفيذ العملية وإنشاء الفاتورة")
        except ValueError as e:
            messagebox.showerror("خطأ", str(e))

    def generate_invoice(self, created_at, trans_type, category, customer, item_name, purity, weight, qty, gram_price, workmanship, total, notes):
        return f"""
========================================
         فاتورة محل الذهب والفضة
========================================
التاريخ      : {created_at}
العملية      : {trans_type}
الصنف        : {category}
اسم الزبون   : {customer}
القطعة       : {item_name}
العيار       : {purity}
وزن القطعة   : {weight} غ
الكمية       : {qty}
سعر الغرام   : {self.money(gram_price)}
المصنعية     : {self.money(workmanship)}
----------------------------------------
الإجمالي     : {self.money(total)}
----------------------------------------
ملاحظات      : {notes if notes else '-'}
========================================
شكرا لتعاملكم معنا
""".strip()

    def open_invoice_tab(self):
        if not self.invoice_text:
            messagebox.showwarning("تنبيه", "نفذ عملية أولاً لإنشاء فاتورة")
            return
        self.invoice_box.delete("1.0", tk.END)
        self.invoice_box.insert(tk.END, self.invoice_text)

    def save_invoice_file(self):
        content = self.invoice_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("تنبيه", "لا توجد فاتورة للحفظ")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile="invoice.txt")
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("نجاح", "تم حفظ الفاتورة")

    def print_invoice(self):
        content = self.invoice_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("تنبيه", "لا توجد فاتورة للطباعة")
            return
        temp_path = os.path.abspath("last_invoice.txt")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("طباعة", f"تم تجهيز الفاتورة للطباعة في الملف:\n{temp_path}\nيمكنك طباعتها مباشرة من النظام.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GoldSilverApp(root)
    root.mainloop()
