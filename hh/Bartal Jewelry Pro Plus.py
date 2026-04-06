import os
import sqlite3
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime, date

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

DB_NAME = "bartal_jewelry_pro_plus.db"
SHOP_NAME = "مجوهرات برطال"
SHOP_ADDRESS = "عين قشرة - سكيكدة"
SHOP_PHONE = "0550 00 00 00"
APP_PASSWORD = "1234"

BG_COLOR = "#0b0b12"
PANEL_COLOR = "#11131a"
GOLD = "#d4a94f"
GOLD_DARK = "#8f6b27"
TEXT_LIGHT = "#f5f5f5"
MUTED = "#c9c9c9"
BLUE_BTN = "#1f4db8"


class JewelryDB:
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
                quantity INTEGER NOT NULL,
                buy_price REAL NOT NULL,
                sell_price REAL NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                category TEXT NOT NULL,
                item_name TEXT NOT NULL,
                purity TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                weight REAL NOT NULL,
                quantity INTEGER NOT NULL,
                gram_price REAL NOT NULL,
                workmanship REAL NOT NULL,
                total_amount REAL NOT NULL,
                notes TEXT,
                estimated_profit REAL NOT NULL DEFAULT 0
            )
            """
        )
        self.conn.commit()
        self.ensure_profit_column()

    def ensure_profit_column(self):
        columns = [row[1] for row in self.conn.execute("PRAGMA table_info(operations)").fetchall()]
        if "estimated_profit" not in columns:
            self.conn.execute("ALTER TABLE operations ADD COLUMN estimated_profit REAL NOT NULL DEFAULT 0")
            self.conn.commit()

    def add_inventory_item(self, data):
        self.conn.execute(
            "INSERT INTO inventory(category, item_name, purity, weight, quantity, buy_price, sell_price) VALUES (?, ?, ?, ?, ?, ?, ?)",
            data,
        )
        self.conn.commit()

    def update_inventory_item(self, item_id, data):
        self.conn.execute(
            """
            UPDATE inventory
            SET category=?, item_name=?, purity=?, weight=?, quantity=?, buy_price=?, sell_price=?
            WHERE id=?
            """,
            (*data, item_id),
        )
        self.conn.commit()

    def get_inventory(self):
        return self.conn.execute(
            "SELECT id, category, item_name, purity, weight, quantity, buy_price, sell_price FROM inventory ORDER BY id DESC"
        ).fetchall()

    def get_inventory_item(self, item_id):
        return self.conn.execute(
            "SELECT id, category, item_name, purity, weight, quantity, buy_price, sell_price FROM inventory WHERE id=?",
            (item_id,),
        ).fetchone()

    def update_inventory_quantity(self, item_id, quantity):
        self.conn.execute("UPDATE inventory SET quantity=? WHERE id=?", (quantity, item_id))
        self.conn.commit()

    def delete_inventory_item(self, item_id):
        self.conn.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        self.conn.commit()

    def add_operation(self, data):
        self.conn.execute(
            """
            INSERT INTO operations(
                created_at, operation_type, category, item_name, purity, customer_name,
                weight, quantity, gram_price, workmanship, total_amount, notes, estimated_profit
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data,
        )
        self.conn.commit()

    def get_operations(self):
        return self.conn.execute(
            "SELECT id, created_at, operation_type, category, item_name, purity, customer_name, weight, quantity, gram_price, workmanship, total_amount, notes, estimated_profit FROM operations ORDER BY id DESC"
        ).fetchall()

    def search_operations(self, keyword):
        like = f"%{keyword}%"
        return self.conn.execute(
            """
            SELECT id, created_at, operation_type, category, item_name, purity, customer_name, weight, quantity, gram_price, workmanship, total_amount, notes, estimated_profit
            FROM operations
            WHERE customer_name LIKE ? OR item_name LIKE ? OR category LIKE ? OR operation_type LIKE ? OR notes LIKE ?
            ORDER BY id DESC
            """,
            (like, like, like, like, like),
        ).fetchall()

    def summary(self):
        stock = self.conn.execute(
            "SELECT COALESCE(SUM(weight * quantity * buy_price),0), COALESCE(SUM(weight * quantity * sell_price),0), COALESCE(SUM(quantity),0) FROM inventory"
        ).fetchone()
        sales = self.conn.execute(
            "SELECT COALESCE(SUM(total_amount),0) FROM operations WHERE operation_type='بيع'"
        ).fetchone()[0]
        purchases = self.conn.execute(
            "SELECT COALESCE(SUM(total_amount),0) FROM operations WHERE operation_type='شراء'"
        ).fetchone()[0]
        total_profit = self.conn.execute(
            "SELECT COALESCE(SUM(estimated_profit),0) FROM operations WHERE operation_type='بيع'"
        ).fetchone()[0]
        today = date.today().isoformat()
        daily_profit = self.conn.execute(
            "SELECT COALESCE(SUM(estimated_profit),0) FROM operations WHERE operation_type='بيع' AND substr(created_at,1,10)=?",
            (today,),
        ).fetchone()[0]
        current_month = today[:7]
        monthly_profit = self.conn.execute(
            "SELECT COALESCE(SUM(estimated_profit),0) FROM operations WHERE operation_type='بيع' AND substr(created_at,1,7)=?",
            (current_month,),
        ).fetchone()[0]
        return stock, sales, purchases, total_profit, daily_profit, monthly_profit


class LoginWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.on_success = on_success
        self.top = tk.Toplevel(master)
        self.top.title("تسجيل الدخول")
        self.top.geometry("760x520")
        self.top.resizable(False, False)
        self.top.configure(bg=BG_COLOR)
        self.top.grab_set()
        self.top.protocol("WM_DELETE_WINDOW", self.master.destroy)

        outer = tk.Frame(self.top, bg=GOLD_DARK, padx=3, pady=3)
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        page = tk.Frame(outer, bg=BG_COLOR)
        page.pack(fill="both", expand=True)

        tk.Label(
            page,
            text="💎 مجوهرات برطال 💎",
            font=("Arial", 34, "bold"),
            bg=BG_COLOR,
            fg=GOLD,
        ).pack(pady=(28, 8))

        tk.Label(
            page,
            text=SHOP_ADDRESS,
            font=("Arial", 18, "bold"),
            bg=BG_COLOR,
            fg=GOLD,
        ).pack(pady=(0, 18))

        line = tk.Frame(page, bg=GOLD_DARK, height=2)
        line.pack(fill="x", padx=140, pady=(0, 26))

        panel_border = tk.Frame(page, bg=GOLD_DARK, padx=3, pady=3)
        panel_border.pack(pady=10)

        panel = tk.Frame(panel_border, bg="#05070b", width=430, height=250)
        panel.pack()
        panel.pack_propagate(False)

        tk.Label(panel, text="تسجيل الدخول", font=("Arial", 24, "bold"), bg="#05070b", fg=GOLD).pack(pady=(24, 8))
        tk.Frame(panel, bg=GOLD_DARK, height=1).pack(fill="x", padx=16, pady=(0, 18))
        tk.Label(panel, text="أدخل كلمة المرور لدخول البرنامج", font=("Arial", 16, "bold"), bg="#05070b", fg=TEXT_LIGHT).pack(pady=(0, 20))

        row = tk.Frame(panel, bg="#05070b")
        row.pack(pady=8)
        tk.Label(row, text="كلمة المرور:", font=("Arial", 16, "bold"), bg="#05070b", fg=TEXT_LIGHT).pack(side="right", padx=12)

        self.password_entry = tk.Entry(
            row,
            show="*",
            justify="center",
            font=("Arial", 18, "bold"),
            bg="#1a1d25",
            fg=TEXT_LIGHT,
            insertbackground=TEXT_LIGHT,
            relief="solid",
            bd=1,
            width=18,
        )
        self.password_entry.pack(side="right", padx=8)
        self.password_entry.focus_set()

        tk.Button(
            panel,
            text="دخول",
            command=self.check_password,
            bg=BLUE_BTN,
            fg="white",
            activebackground="#163f99",
            activeforeground="white",
            font=("Arial", 18, "bold"),
            width=14,
            pady=8,
            relief="raised",
            bd=2,
            cursor="hand2",
        ).pack(pady=24)

        tk.Frame(panel, bg=GOLD_DARK, height=1).pack(fill="x", padx=16, pady=(0, 14))
        tk.Label(panel, text=f"كلمة المرور الحالية: {APP_PASSWORD}", font=("Arial", 16, "bold"), bg="#05070b", fg=GOLD).pack(pady=(0, 8))

        self.password_entry.bind("<Return>", lambda event: self.check_password())

    def check_password(self):
        if self.password_entry.get() == APP_PASSWORD:
            self.top.destroy()
            self.on_success()
        else:
            messagebox.showerror("خطأ", "كلمة المرور غير صحيحة")
            self.password_entry.delete(0, tk.END)


class JewelryApp:
    def __init__(self, root):
        self.root = root
        self.db = JewelryDB()
        self.last_receipt = ""

        self.root.title(SHOP_NAME)
        self.root.geometry("1520x900")
        self.root.configure(bg=BG_COLOR)
        self.root.withdraw()

        LoginWindow(self.root, self.start_app)

    def start_app(self):
        self.root.deiconify()
        self.build_ui()
        self.refresh_all()

    def money(self, value):
        return f"{value:,.2f} دج"

    def styled_button(self, parent, text, command, bg, fg="white", width=18):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            font=("Arial", 12, "bold"),
            padx=12,
            pady=10,
            width=width,
            relief="raised",
            bd=3,
            cursor="hand2",
            highlightbackground=GOLD_DARK,
            highlightthickness=1,
        ),
            padx=12,
            pady=8,
            width=width,
            relief="raised",
            bd=3,
            cursor="hand2",
        )

    def build_ui(self):
        header_frame = tk.Frame(self.root, bg=BG_COLOR)
        header_frame.pack(fill="x", pady=8)

        tk.Label(
            header_frame,
            text="💎 مجوهرات برطال 💎",
            font=("Arial", 26, "bold"),
            bg=BG_COLOR,
            fg=GOLD,
        ).pack()

        tk.Label(
            header_frame,
            text=f"العنوان: {SHOP_ADDRESS} | {SHOP_PHONE}",
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg=TEXT_LIGHT,
        ).pack(pady=3)

        self.build_summary_boxes()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.inventory_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.operation_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.history_tab = tk.Frame(self.notebook, bg=BG_COLOR)
        self.receipt_tab = tk.Frame(self.notebook, bg=BG_COLOR)

        self.notebook.add(self.inventory_tab, text="المخزون")
        self.notebook.add(self.operation_tab, text="بيع وشراء")
        self.notebook.add(self.history_tab, text="السجل")
        self.notebook.add(self.receipt_tab, text="الوصل والطباعة")

        self.build_inventory_tab()
        self.build_operation_tab()
        self.build_history_tab()
        self.build_receipt_tab()

    def build_summary_boxes(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(fill="x", padx=10)

        self.stock_buy_var = tk.StringVar()
        self.stock_sell_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.sales_var = tk.StringVar()
        self.purchases_var = tk.StringVar()
        self.total_profit_var = tk.StringVar()
        self.daily_profit_var = tk.StringVar()
        self.monthly_profit_var = tk.StringVar()

        items = [
            ("قيمة المخزون شراء", self.stock_buy_var),
            ("قيمة المخزون بيع", self.stock_sell_var),
            ("عدد القطع", self.qty_var),
            ("إجمالي المبيعات", self.sales_var),
            ("إجمالي المشتريات", self.purchases_var),
            ("الربح الكلي", self.total_profit_var),
            ("ربح اليوم", self.daily_profit_var),
            ("ربح الشهر", self.monthly_profit_var),
        ]

        for i, (title, var) in enumerate(items):
            box = tk.Frame(frame, bg=PANEL_COLOR, relief="solid", bd=1, padx=10, pady=8, highlightbackground=GOLD_DARK, highlightthickness=1)
            box.grid(row=0, column=i, sticky="nsew", padx=3)
            frame.grid_columnconfigure(i, weight=1)
            tk.Label(box, text=title, font=("Arial", 10, "bold"), bg=PANEL_COLOR, fg=TEXT_LIGHT).pack()
            tk.Label(box, textvariable=var, font=("Arial", 13, "bold"), fg=GOLD, bg=PANEL_COLOR).pack(pady=5)

    def build_inventory_tab(self):
        top = tk.Frame(self.inventory_tab, bg=BG_COLOR)
        top.pack(fill="x", padx=10, pady=10)

        form = tk.LabelFrame(top, text="إضافة / تعديل قطعة", font=("Arial", 12, "bold"), bg=BG_COLOR, padx=10, pady=10)
        form.pack(side="right", fill="y", padx=5)

        labels = ["الصنف", "اسم القطعة", "العيار", "الوزن (غ)", "الكمية", "سعر الشراء/غ", "سعر البيع/غ"]
        for i, label in enumerate(labels):
            tk.Label(form, text=label, bg=BG_COLOR, font=("Arial", 11, "bold")).grid(row=i, column=0, sticky="e", padx=5, pady=4)

        self.inv_category = ttk.Combobox(form, values=["ذهب", "فضة"], state="readonly", justify="right")
        self.inv_category.grid(row=0, column=1, padx=5, pady=4)
        self.inv_category.set("ذهب")

        self.inv_name = tk.Entry(form, justify="right", font=("Arial", 11))
        self.inv_name.grid(row=1, column=1, padx=5, pady=4)

        self.inv_purity = ttk.Combobox(form, values=["24", "22", "21", "18", "999", "925"], state="readonly", justify="right")
        self.inv_purity.grid(row=2, column=1, padx=5, pady=4)
        self.inv_purity.set("21")

        self.inv_weight = tk.Entry(form, justify="right", font=("Arial", 11))
        self.inv_weight.grid(row=3, column=1, padx=5, pady=4)

        self.inv_quantity = tk.Entry(form, justify="right", font=("Arial", 11))
        self.inv_quantity.grid(row=4, column=1, padx=5, pady=4)

        self.inv_buy = tk.Entry(form, justify="right", font=("Arial", 11))
        self.inv_buy.grid(row=5, column=1, padx=5, pady=4)

        self.inv_sell = tk.Entry(form, justify="right", font=("Arial", 11))
        self.inv_sell.grid(row=6, column=1, padx=5, pady=4)

        self.editing_item_id = None

        btn_frame = tk.Frame(form, bg=BG_COLOR)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=8)
        self.styled_button(btn_frame, "إضافة للمخزون", self.add_inventory_item, "#2563eb").pack(side="right", padx=4)
        self.styled_button(btn_frame, "تعديل المحدد", self.edit_selected_inventory, "#0f766e").pack(side="right", padx=4)
        self.styled_button(btn_frame, "حفظ التعديل", self.save_inventory_edit, "#f59e0b", fg="black").pack(side="right", padx=4)
        self.styled_button(btn_frame, "تفريغ الحقول", self.clear_inventory_entries, "#64748b").pack(side="right", padx=4)

        table_frame = tk.LabelFrame(top, text="قائمة المخزون", font=("Arial", 12, "bold"), bg=BG_COLOR)
        table_frame.pack(side="left", fill="both", expand=True, padx=5)

        cols = ("id", "category", "name", "purity", "weight", "quantity", "buy", "sell")
        self.inventory_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=18)
        heads = {
            "id": "رقم",
            "category": "الصنف",
            "name": "القطعة",
            "purity": "العيار",
            "weight": "الوزن",
            "quantity": "الكمية",
            "buy": "شراء/غ",
            "sell": "بيع/غ",
        }
        widths = {"id": 55, "category": 85, "name": 140, "purity": 80, "weight": 80, "quantity": 75, "buy": 110, "sell": 110}
        for c in cols:
            self.inventory_tree.heading(c, text=heads[c])
            self.inventory_tree.column(c, width=widths[c], anchor="center")
        self.inventory_tree.pack(fill="both", expand=True, padx=5, pady=5)

        bottom_btns = tk.Frame(table_frame, bg=BG_COLOR)
        bottom_btns.pack(fill="x", padx=5, pady=5)
        self.styled_button(bottom_btns, "حذف القطعة المحددة", self.delete_selected_inventory, "#dc2626").pack(side="right", padx=4)
        self.styled_button(bottom_btns, "تحديث", self.refresh_all, "#2563eb").pack(side="right", padx=4)

    def build_operation_tab(self):
        wrapper = tk.Frame(self.operation_tab, bg=BG_COLOR)
        wrapper.pack(fill="both", expand=True, padx=10, pady=10)

        form = tk.LabelFrame(wrapper, text="تنفيذ عملية بيع أو شراء", font=("Arial", 12, "bold"), bg=BG_COLOR, padx=10, pady=10)
        form.pack(side="right", fill="y", padx=5)

        labels = ["نوع العملية", "القطعة من المخزون", "اسم الزبون", "الكمية", "المصنعية", "ملاحظات"]
        for i, label in enumerate(labels):
            tk.Label(form, text=label, bg=BG_COLOR, font=("Arial", 11, "bold")).grid(row=i, column=0, sticky="e", padx=5, pady=4)

        self.op_type = ttk.Combobox(form, values=["بيع", "شراء"], state="readonly", justify="right")
        self.op_type.grid(row=0, column=1, padx=5, pady=4)
        self.op_type.set("بيع")

        self.stock_select = ttk.Combobox(form, state="readonly", justify="right", width=42)
        self.stock_select.grid(row=1, column=1, padx=5, pady=4)

        self.customer_entry = tk.Entry(form, justify="right", font=("Arial", 11))
        self.customer_entry.grid(row=2, column=1, padx=5, pady=4)

        self.op_quantity = tk.Entry(form, justify="right", font=("Arial", 11))
        self.op_quantity.grid(row=3, column=1, padx=5, pady=4)
        self.op_quantity.insert(0, "1")

        self.workmanship_entry = tk.Entry(form, justify="right", font=("Arial", 11))
        self.workmanship_entry.grid(row=4, column=1, padx=5, pady=4)
        self.workmanship_entry.insert(0, "0")

        self.notes_entry = tk.Entry(form, justify="right", font=("Arial", 11))
        self.notes_entry.grid(row=5, column=1, padx=5, pady=4)

        buttons = tk.Frame(form, bg=BG_COLOR)
        buttons.grid(row=6, column=0, columnspan=2, pady=8)
        self.styled_button(buttons, "تنفيذ العملية", self.execute_operation, "#16a34a").pack(side="right", padx=4)
        self.styled_button(buttons, "إنشاء وصل", self.show_receipt_tab, "#f59e0b", fg="black").pack(side="right", padx=4)

        preview = tk.LabelFrame(wrapper, text="معاينة المخزون", font=("Arial", 12, "bold"), bg=BG_COLOR)
        preview.pack(side="left", fill="both", expand=True, padx=5)

        cols = ("id", "category", "name", "purity", "weight", "quantity", "buy", "sell")
        self.stock_tree = ttk.Treeview(preview, columns=cols, show="headings", height=18)
        heads = ["رقم", "الصنف", "القطعة", "العيار", "الوزن", "الكمية", "شراء/غ", "بيع/غ"]
        for c, h in zip(cols, heads):
            self.stock_tree.heading(c, text=h)
            self.stock_tree.column(c, width=105, anchor="center")
        self.stock_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def build_history_tab(self):
        top = tk.Frame(self.history_tab, bg=BG_COLOR)
        top.pack(fill="x", padx=10, pady=8)

        tk.Label(top, text="بحث في السجل", bg=BG_COLOR, font=("Arial", 11, "bold")).pack(side="right", padx=5)
        self.search_entry = tk.Entry(top, justify="right", font=("Arial", 11), width=30)
        self.search_entry.pack(side="right", padx=5)
        self.styled_button(top, "بحث", self.search_history, "#2563eb", width=10).pack(side="right", padx=4)
        self.styled_button(top, "عرض الكل", self.refresh_transactions, "#64748b", width=10).pack(side="right", padx=4)

        frame = tk.LabelFrame(self.history_tab, text="سجل العمليات", font=("Arial", 12, "bold"), bg=BG_COLOR)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id", "date", "type", "category", "item", "purity", "customer", "weight", "quantity", "price", "work", "total", "profit")
        self.history_tree = ttk.Treeview(frame, columns=cols, show="headings", height=22)
        titles = ["رقم", "التاريخ", "العملية", "الصنف", "القطعة", "العيار", "الزبون", "الوزن", "الكمية", "السعر", "المصنعية", "الإجمالي", "الربح"]
        widths = [50, 135, 80, 80, 120, 70, 120, 75, 70, 95, 95, 110, 100]
        for c, t, w in zip(cols, titles, widths):
            self.history_tree.heading(c, text=t)
            self.history_tree.column(c, width=w, anchor="center")
        self.history_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def build_receipt_tab(self):
        top = tk.Frame(self.receipt_tab, bg=BG_COLOR)
        top.pack(fill="x", padx=10, pady=8)
        self.styled_button(top, "حفظ الوصل TXT", self.save_receipt_txt, "#2563eb", width=14).pack(side="right", padx=4)
        self.styled_button(top, "حفظ الوصل PDF", self.save_receipt_pdf, "#7c3aed", width=14).pack(side="right", padx=4)
        self.styled_button(top, "طباعة الوصل", self.print_receipt, "#16a34a", width=14).pack(side="right", padx=4)

        self.receipt_box = tk.Text(self.receipt_tab, font=("Courier New", 12), wrap="word")
        self.receipt_box.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_inventory_entries(self):
        self.editing_item_id = None
        for entry in [self.inv_name, self.inv_weight, self.inv_quantity, self.inv_buy, self.inv_sell]:
            entry.delete(0, tk.END)
        self.inv_category.set("ذهب")
        self.inv_purity.set("21")

    def add_inventory_item(self):
        try:
            category = self.inv_category.get()
            name = self.inv_name.get().strip()
            purity = self.inv_purity.get()
            weight = float(self.inv_weight.get())
            quantity = int(self.inv_quantity.get())
            buy_price = float(self.inv_buy.get())
            sell_price = float(self.inv_sell.get())

            if not name:
                raise ValueError("اسم القطعة مطلوب")
            if weight <= 0 or quantity <= 0 or buy_price < 0 or sell_price < 0:
                raise ValueError("تحقق من القيم المدخلة")

            self.db.add_inventory_item((category, name, purity, weight, quantity, buy_price, sell_price))
            self.clear_inventory_entries()
            self.refresh_all()
            messagebox.showinfo("نجاح", "تمت إضافة القطعة إلى المخزون")
        except ValueError as e:
            messagebox.showerror("خطأ", str(e))

    def get_selected_inventory_id(self):
        sel = self.inventory_tree.selection()
        if not sel:
            return None
        return int(self.inventory_tree.item(sel[0], "values")[0])

    def edit_selected_inventory(self):
        item_id = self.get_selected_inventory_id()
        if not item_id:
            messagebox.showwarning("تنبيه", "اختر قطعة من المخزون")
            return
        row = self.db.get_inventory_item(item_id)
        if not row:
            messagebox.showerror("خطأ", "العنصر غير موجود")
            return
        self.editing_item_id = item_id
        _, category, item_name, purity, weight, quantity, buy_price, sell_price = row
        self.inv_category.set(category)
        self.inv_name.delete(0, tk.END)
        self.inv_name.insert(0, item_name)
        self.inv_purity.set(purity)
        self.inv_weight.delete(0, tk.END)
        self.inv_weight.insert(0, str(weight))
        self.inv_quantity.delete(0, tk.END)
        self.inv_quantity.insert(0, str(quantity))
        self.inv_buy.delete(0, tk.END)
        self.inv_buy.insert(0, str(buy_price))
        self.inv_sell.delete(0, tk.END)
        self.inv_sell.insert(0, str(sell_price))
        messagebox.showinfo("تعديل", "تم تحميل بيانات القطعة في الحقول. عدلها ثم اضغط حفظ التعديل")

    def save_inventory_edit(self):
        if not self.editing_item_id:
            messagebox.showwarning("تنبيه", "اختر قطعة للتعديل أولا")
            return
        try:
            data = (
                self.inv_category.get(),
                self.inv_name.get().strip(),
                self.inv_purity.get(),
                float(self.inv_weight.get()),
                int(self.inv_quantity.get()),
                float(self.inv_buy.get()),
                float(self.inv_sell.get()),
            )
            if not data[1]:
                raise ValueError("اسم القطعة مطلوب")
            self.db.update_inventory_item(self.editing_item_id, data)
            self.clear_inventory_entries()
            self.refresh_all()
            messagebox.showinfo("نجاح", "تم حفظ التعديل")
        except ValueError as e:
            messagebox.showerror("خطأ", str(e))

    def delete_selected_inventory(self):
        item_id = self.get_selected_inventory_id()
        if not item_id:
            messagebox.showwarning("تنبيه", "اختر قطعة من المخزون")
            return
        self.db.delete_inventory_item(item_id)
        self.refresh_all()
        messagebox.showinfo("تم", "تم حذف القطعة")

    def refresh_inventory(self):
        rows = self.db.get_inventory()
        for tree in [self.inventory_tree, self.stock_tree]:
            for item in tree.get_children():
                tree.delete(item)
            for row in rows:
                display = (row[0], row[1], row[2], row[3], row[4], row[5], self.money(row[6]), self.money(row[7]))
                tree.insert("", tk.END, values=display)

        choices = [f"{r[0]} | {r[1]} | {r[2]} | عيار {r[3]} | وزن {r[4]} | كمية {r[5]}" for r in rows]
        self.stock_select["values"] = choices
        if choices:
            self.stock_select.current(0)
        else:
            self.stock_select.set("")

    def refresh_transactions(self):
        rows = self.db.get_operations()
        self.fill_history_tree(rows)

    def fill_history_tree(self, rows):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        for row in rows:
            self.history_tree.insert(
                "",
                tk.END,
                values=(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                    row[7], row[8], self.money(row[9]), self.money(row[10]), self.money(row[11]), self.money(row[13])
                ),
            )

    def search_history(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.refresh_transactions()
            return
        rows = self.db.search_operations(keyword)
        self.fill_history_tree(rows)

    def refresh_summary(self):
        stock, sales, purchases, total_profit, daily_profit, monthly_profit = self.db.summary()
        self.stock_buy_var.set(self.money(stock[0]))
        self.stock_sell_var.set(self.money(stock[1]))
        self.qty_var.set(str(stock[2]))
        self.sales_var.set(self.money(sales))
        self.purchases_var.set(self.money(purchases))
        self.total_profit_var.set(self.money(total_profit))
        self.daily_profit_var.set(self.money(daily_profit))
        self.monthly_profit_var.set(self.money(monthly_profit))

    def refresh_all(self):
        self.refresh_inventory()
        self.refresh_transactions()
        self.refresh_summary()

    def get_selected_stock_id(self):
        text = self.stock_select.get().strip()
        if not text:
            raise ValueError("اختر قطعة من المخزون")
        return int(text.split("|")[0].strip())

    def execute_operation(self):
        try:
            item_id = self.get_selected_stock_id()
            item = self.db.get_inventory_item(item_id)
            if not item:
                raise ValueError("العنصر غير موجود")

            op_type = self.op_type.get()
            customer = self.customer_entry.get().strip() or "زبون مباشر"
            quantity = int(self.op_quantity.get())
            workmanship = float(self.workmanship_entry.get() or 0)
            notes = self.notes_entry.get().strip()

            if quantity <= 0:
                raise ValueError("الكمية غير صالحة")

            _, category, item_name, purity, weight, stock_qty, buy_price, sell_price = item

            if op_type == "بيع" and quantity > stock_qty:
                raise ValueError("الكمية المطلوبة أكبر من المخزون")

            gram_price = sell_price if op_type == "بيع" else buy_price
            total = (weight * quantity * gram_price) + workmanship
            estimated_profit = ((sell_price - buy_price) * weight * quantity) + workmanship if op_type == "بيع" else 0
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if op_type == "بيع":
                new_qty = stock_qty - quantity
            else:
                new_qty = stock_qty + quantity

            if new_qty <= 0:
                self.db.delete_inventory_item(item_id)
            else:
                self.db.update_inventory_quantity(item_id, new_qty)

            self.db.add_operation((
                current_date,
                op_type,
                category,
                item_name,
                purity,
                customer,
                weight,
                quantity,
                gram_price,
                workmanship,
                total,
                notes,
                estimated_profit,
            ))

            self.last_receipt = self.generate_receipt(
                current_date, op_type, category, item_name, purity,
                customer, weight, quantity, gram_price, workmanship, total, notes
            )
            self.receipt_box.delete("1.0", tk.END)
            self.receipt_box.insert(tk.END, self.last_receipt)

            self.customer_entry.delete(0, tk.END)
            self.op_quantity.delete(0, tk.END)
            self.op_quantity.insert(0, "1")
            self.workmanship_entry.delete(0, tk.END)
            self.workmanship_entry.insert(0, "0")
            self.notes_entry.delete(0, tk.END)

            self.refresh_all()
            self.notebook.select(self.receipt_tab)
            messagebox.showinfo("نجاح", "تم تنفيذ العملية وإنشاء وصل الاستلام")
        except ValueError as e:
            messagebox.showerror("خطأ", str(e))

    def generate_receipt(self, current_date, op_type, category, item_name, purity, customer, weight, quantity, gram_price, workmanship, total, notes):
        return f"""
========================================
        وصل استلام - {SHOP_NAME}
========================================
التاريخ       : {current_date}
المحل         : {SHOP_NAME}
العنوان       : {SHOP_ADDRESS}
الهاتف        : {SHOP_PHONE}
----------------------------------------
نوع العملية   : {op_type}
الصنف         : {category}
القطعة        : {item_name}
العيار        : {purity}
اسم الزبون    : {customer}
وزن القطعة    : {weight} غ
الكمية        : {quantity}
سعر الغرام    : {self.money(gram_price)}
المصنعية      : {self.money(workmanship)}
----------------------------------------
الإجمالي      : {self.money(total)}
الملاحظات     : {notes if notes else '-'}
========================================
        شكرا لزيارتكم ومرحبا بكم
========================================
""".strip()

    def show_receipt_tab(self):
        if not self.last_receipt:
            messagebox.showwarning("تنبيه", "نفذ عملية أولا لإنشاء وصل")
            return
        self.notebook.select(self.receipt_tab)

    def save_receipt_txt(self):
        content = self.receipt_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("تنبيه", "لا يوجد وصل للحفظ")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile="وصل_استلام.txt",
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("نجاح", "تم حفظ الوصل")

    def save_receipt_pdf(self):
        content = self.receipt_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("تنبيه", "لا يوجد وصل للحفظ")
            return
        if not REPORTLAB_AVAILABLE:
            messagebox.showwarning("تنبيه", "مكتبة reportlab غير مثبتة. ثبتها بالأمر: pip install reportlab")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="وصل_استلام.pdf",
        )
        if not path:
            return

        c = canvas.Canvas(path, pagesize=A4)
        width, height = A4
        y = height - 50
        c.setFont("Helvetica", 12)
        for line in content.splitlines():
            c.drawString(40, y, line)
            y -= 18
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 50
        c.save()
        messagebox.showinfo("نجاح", "تم حفظ الوصل PDF")

    def print_receipt(self):
        content = self.receipt_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("تنبيه", "لا يوجد وصل للطباعة")
            return
        path = os.path.abspath("wasl_istilam.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("تم", f"تم تجهيز الوصل للطباعة في الملف:\n{path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = JewelryApp(root)
    root.mainloop()
