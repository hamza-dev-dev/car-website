import os
import sqlite3
from datetime import datetime
from io import BytesIO
from urllib.parse import quote

from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template_string,
    request,
    send_file,
    url_for,
)
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "cars.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
WHATSAPP_NUMBER = "213671554101"
SITE_NAME = "DriveWaydz"
ADMIN_PASSWORD = "admin123"

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


BASE_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
        }
        a { text-decoration: none; }
        .container { width: min(1180px, 92%); margin: auto; }
        .nav {
            background: rgba(15, 23, 42, 0.95);
            position: sticky;
            top: 0;
            z-index: 50;
            border-bottom: 1px solid rgba(255,255,255,.08);
        }
        .nav-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            padding: 18px 0;
        }
        .logo { font-size: 26px; font-weight: bold; color: #fff; }
        .menu { display: flex; gap: 18px; flex-wrap: wrap; }
        .menu a { color: #cbd5e1; }
        .hero {
            padding: 64px 0 42px;
            background: linear-gradient(135deg, #111827, #1d4ed8);
        }
        .hero-grid {
            display: grid;
            grid-template-columns: 1.2fr .8fr;
            gap: 28px;
            align-items: center;
        }
        .hero h1 { font-size: 42px; margin: 0 0 14px; color: #fff; }
        .hero p { font-size: 18px; line-height: 1.9; color: #e2e8f0; }
        .btn {
            display: inline-block;
            padding: 12px 18px;
            border-radius: 12px;
            font-weight: bold;
            margin-left: 10px;
            margin-top: 10px;
            border: 0;
            cursor: pointer;
        }
        .btn-primary { background: #22c55e; color: white; }
        .btn-secondary { background: white; color: #0f172a; }
        .btn-danger { background: #dc2626; color: white; }
        .btn-dark { background: #1e293b; color: white; }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 22px;
        }
        .card {
            background: #111827;
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,.25);
        }
        .card img {
            width: 100%;
            height: 220px;
            object-fit: cover;
            display: block;
        }
        .card-body { padding: 18px; }
        .price { color: #22c55e; font-size: 24px; font-weight: bold; }
        .meta { color: #cbd5e1; line-height: 1.8; font-size: 14px; }
        .section { padding: 48px 0; }
        .section h2 { font-size: 30px; margin-bottom: 18px; color: #fff; }
        .section p.lead { color: #cbd5e1; margin-bottom: 26px; }
        iframe { width: 100%; border: 0; border-radius: 14px; min-height: 220px; }
        .testimonial, .panel {
            padding: 18px;
            background: #111827;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,.08);
        }
        form {
            background: #111827;
            padding: 24px;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,.08);
        }
        label { display: block; margin-bottom: 8px; font-weight: bold; }
        input, textarea, select {
            width: 100%;
            margin-bottom: 14px;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid #334155;
            background: #0f172a;
            color: #fff;
        }
        textarea { min-height: 110px; }
        .footer {
            border-top: 1px solid rgba(255,255,255,.08);
            padding: 26px 0;
            color: #94a3b8;
        }
        .contract-box {
            background: white;
            color: #111827;
            padding: 35px;
            border-radius: 18px;
            line-height: 2;
        }
        .whatsapp-float {
            position: fixed;
            left: 20px;
            bottom: 20px;
            background: #22c55e;
            color: white;
            padding: 14px 18px;
            border-radius: 999px;
            font-weight: bold;
            box-shadow: 0 8px 20px rgba(0,0,0,.35);
        }
        .flash-wrap { margin: 18px 0; }
        .flash {
            padding: 12px 14px;
            border-radius: 12px;
            margin-bottom: 10px;
            background: #1e293b;
            color: #fff;
        }
        .table-wrap {
            overflow-x: auto;
            background: #111827;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,.08);
        }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 14px; text-align: right; border-bottom: 1px solid rgba(255,255,255,.08); }
        th { color: #fff; background: #0b1220; }
        tr:last-child td { border-bottom: 0; }
        .actions { display: flex; gap: 8px; flex-wrap: wrap; }
        .small { color: #94a3b8; font-size: 13px; }
        .thumb { width: 90px; height: 65px; object-fit: cover; border-radius: 10px; }
        @media (max-width: 900px) {
            .hero-grid { grid-template-columns: 1fr; }
            .hero h1 { font-size: 32px; }
            .nav-inner { flex-direction: column; gap: 10px; }
        }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="container nav-inner">
            <div class="logo">{{ site_name }}</div>
            <div class="menu">
                <a href="{{ url_for('home') }}">الرئيسية</a>
                <a href="{{ url_for('cars_page') }}">السيارات</a>
                <a href="{{ url_for('clients_page') }}">فيديوهات الزبائن</a>
                <a href="{{ url_for('contract_form') }}">تحرير عقد</a>
                <a href="{{ url_for('admin_login') }}">لوحة التحكم</a>
            </div>
        </div>
    </nav>

    <div class="container flash-wrap">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for msg in messages %}
                    <div class="flash">{{ msg }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    {{ content|safe }}

    <div class="footer">
        <div class="container">
            © {{ year }} {{ site_name }} - جميع الحقوق محفوظة
        </div>
    </div>

    <a class="whatsapp-float" target="_blank" href="https://wa.me/{{ whatsapp_number }}?text={{ quote('السلام عليكم، أريد الاستفسار عن السيارات المعروضة') }}">
        واتساب مباشر
    </a>
</body>
</html>
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            year INTEGER,
            mileage TEXT,
            fuel TEXT,
            transmission TEXT,
            description TEXT,
            video TEXT,
            image_filename TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS client_videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            city TEXT,
            video_url TEXT NOT NULL,
            comment TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    db.commit()
    seed_data()


def seed_data():
    db = get_db()
    count = db.execute("SELECT COUNT(*) AS total FROM cars").fetchone()["total"]
    if count == 0:
        now = datetime.now().isoformat()
        db.executemany(
            """
            INSERT INTO cars (name, price, year, mileage, fuel, transmission, description, video, image_filename, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "Toyota Corolla 2020",
                    "3,250,000 DZD",
                    2020,
                    "58,000 km",
                    "Essence",
                    "Automatique",
                    "سيارة نظيفة واقتصادية ومناسبة للاستعمال اليومي.",
                    "https://www.youtube.com/embed/ysz5S6PUM-U",
                    "",
                    now,
                ),
                (
                    "Hyundai Tucson 2021",
                    "5,480,000 DZD",
                    2021,
                    "34,000 km",
                    "Diesel",
                    "Automatique",
                    "SUV مريحة وعائلية مع تجهيزات ممتازة.",
                    "https://www.youtube.com/embed/tgbNymZ7vqY",
                    "",
                    now,
                ),
            ],
        )
        db.executemany(
            """
            INSERT INTO client_videos (client_name, city, video_url, comment, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                ("Ahmed", "Oran", "https://www.youtube.com/embed/ysz5S6PUM-U", "استلمت السيارة في الوقت المحدد والخدمة ممتازة.", now),
                ("Yacine", "Alger", "https://www.youtube.com/embed/tgbNymZ7vqY", "تعامل احترافي والسيارة مطابقة للوصف.", now),
            ],
        )
        db.commit()


@app.before_request
def before_request():
    init_db()


def render_page(title, content):
    return render_template_string(
        BASE_HTML,
        title=title,
        site_name=SITE_NAME,
        content=content,
        year=datetime.now().year,
        whatsapp_number=WHATSAPP_NUMBER,
        quote=quote,
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(file_storage):
    if not file_storage or not file_storage.filename:
        return ""
    if not allowed_file(file_storage.filename):
        raise ValueError("صيغة الصورة غير مدعومة")
    filename = secure_filename(file_storage.filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    final_name = f"{timestamp}_{filename}"
    file_storage.save(os.path.join(app.config["UPLOAD_FOLDER"], final_name))
    return final_name


def image_url(filename):
    if filename:
        return url_for("static", filename=f"uploads/{filename}")
    return "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1400&q=80"


def fetch_all_cars():
    return get_db().execute("SELECT * FROM cars ORDER BY id DESC").fetchall()


def fetch_car(car_id):
    return get_db().execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()


def fetch_client_videos():
    return get_db().execute("SELECT * FROM client_videos ORDER BY id DESC").fetchall()


def is_admin():
    return request.cookies.get("admin_auth") == ADMIN_PASSWORD


def require_admin():
    if not is_admin():
        flash("يرجى تسجيل الدخول إلى لوحة التحكم أولاً")
        return redirect(url_for("admin_login"))
    return None


@app.route("/")
def home():
    cars = fetch_all_cars()[:3]
    content = render_template_string(
        """
        <section class="hero">
            <div class="container hero-grid">
                <div>
                    <h1>موقع احترافي لعرض وبيع السيارات</h1>
                    <p>
                        اعرض سياراتك من خلال قاعدة بيانات SQLite، أضف الصور الحقيقية من المتصفح،
                        وأنشئ عقود PDF جاهزة للطباعة مع زر واتساب مباشر.
                    </p>
                    <a class="btn btn-primary" target="_blank" href="https://wa.me/{{ whatsapp_number }}?text={{ quote('السلام عليكم، أريد سيارة من عندكم') }}">تواصل عبر واتساب</a>
                    <a class="btn btn-secondary" href="{{ url_for('cars_page') }}">عرض السيارات</a>
                </div>
                <div>
                    <img style="width:100%; border-radius:22px; height:400px; object-fit:cover;" src="https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1400&q=80" alt="cars">
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2>أحدث السيارات</h2>
                <p class="lead">هذه السيارات يتم جلبها مباشرة من قاعدة البيانات.</p>
                <div class="card-grid">
                    {% for car in cars %}
                    <div class="card">
                        <img src="{{ image_url(car['image_filename']) }}" alt="{{ car['name'] }}">
                        <div class="card-body">
                            <h3>{{ car['name'] }}</h3>
                            <div class="price">{{ car['price'] }}</div>
                            <p class="meta">السنة: {{ car['year'] }}<br>العداد: {{ car['mileage'] }}<br>الوقود: {{ car['fuel'] }}</p>
                            <a class="btn btn-primary" href="{{ url_for('car_detail', car_id=car['id']) }}">تفاصيل السيارة</a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
        """,
        cars=cars,
        image_url=image_url,
        whatsapp_number=WHATSAPP_NUMBER,
        quote=quote,
    )
    return render_page("الرئيسية", content)


@app.route("/cars")
def cars_page():
    cars = fetch_all_cars()
    content = render_template_string(
        """
        <section class="section">
            <div class="container">
                <h2>السيارات المعروضة</h2>
                <p class="lead">كل سيارة فيها صور حقيقية، تفاصيل كاملة، وفيديو وزر واتساب مباشر.</p>
                <div class="card-grid">
                    {% for car in cars %}
                    <div class="card">
                        <img src="{{ image_url(car['image_filename']) }}" alt="{{ car['name'] }}">
                        <div class="card-body">
                            <h3>{{ car['name'] }}</h3>
                            <div class="price">{{ car['price'] }}</div>
                            <p class="meta">
                                السنة: {{ car['year'] }}<br>
                                العداد: {{ car['mileage'] }}<br>
                                نوع الوقود: {{ car['fuel'] }}<br>
                                ناقل الحركة: {{ car['transmission'] }}
                            </p>
                            <a class="btn btn-secondary" href="{{ url_for('car_detail', car_id=car['id']) }}">عرض التفاصيل</a>
                            <a class="btn btn-primary" target="_blank" href="https://wa.me/{{ whatsapp_number }}?text={{ quote('السلام عليكم، أنا مهتم بـ ' + car['name']) }}">واتساب</a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
        """,
        cars=cars,
        image_url=image_url,
        whatsapp_number=WHATSAPP_NUMBER,
        quote=quote,
    )
    return render_page("السيارات", content)


@app.route("/cars/<int:car_id>")
def car_detail(car_id):
    car = fetch_car(car_id)
    if not car:
        return "Car not found", 404
    content = render_template_string(
        """
        <section class="section">
            <div class="container">
                <div class="hero-grid">
                    <div>
                        <img style="width:100%; border-radius:22px; height:420px; object-fit:cover;" src="{{ image_url(car['image_filename']) }}" alt="{{ car['name'] }}">
                    </div>
                    <div>
                        <h2>{{ car['name'] }}</h2>
                        <div class="price">{{ car['price'] }}</div>
                        <p class="meta">
                            السنة: {{ car['year'] }}<br>
                            العداد: {{ car['mileage'] }}<br>
                            الوقود: {{ car['fuel'] }}<br>
                            ناقل الحركة: {{ car['transmission'] }}
                        </p>
                        <p>{{ car['description'] }}</p>
                        <a class="btn btn-primary" target="_blank" href="https://wa.me/{{ whatsapp_number }}?text={{ quote('السلام عليكم، أريد الاستفسار عن ' + car['name']) }}">التواصل عبر واتساب</a>
                        <a class="btn btn-secondary" href="{{ url_for('contract_form', car_name=car['name']) }}">تحرير عقد للزبون</a>
                    </div>
                </div>
            </div>
        </section>

        {% if car['video'] %}
        <section class="section">
            <div class="container">
                <h2>فيديو السيارة</h2>
                <iframe src="{{ car['video'] }}" allowfullscreen></iframe>
            </div>
        </section>
        {% endif %}
        """,
        car=car,
        image_url=image_url,
        whatsapp_number=WHATSAPP_NUMBER,
        quote=quote,
    )
    return render_page(car["name"], content)


@app.route("/clients")
def clients_page():
    items = fetch_client_videos()
    content = render_template_string(
        """
        <section class="section">
            <div class="container">
                <h2>فيديوهات الزبائن الذين استلموا سياراتهم</h2>
                <p class="lead">قسم لبناء الثقة وإبراز التجارب الحقيقية.</p>
                <div class="card-grid">
                    {% for item in items %}
                    <div class="testimonial">
                        <iframe src="{{ item['video_url'] }}" allowfullscreen></iframe>
                        <h3>{{ item['client_name'] }}{% if item['city'] %} - {{ item['city'] }}{% endif %}</h3>
                        <p>{{ item['comment'] }}</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
        """,
        items=items,
    )
    return render_page("فيديوهات الزبائن", content)


@app.route("/contract", methods=["GET", "POST"])
def contract_form():
    if request.method == "POST":
        buyer_name = request.form.get("buyer_name", "").strip()
        buyer_id = request.form.get("buyer_id", "").strip()
        car_name = request.form.get("car_name", "").strip()
        chassis = request.form.get("chassis", "").strip()
        price = request.form.get("price", "").strip()
        payment = request.form.get("payment", "").strip()
        date = request.form.get("date", "").strip()

        if request.form.get("action") == "pdf":
            return generate_contract_pdf(
                buyer_name=buyer_name,
                buyer_id=buyer_id,
                car_name=car_name,
                chassis=chassis,
                price=price,
                payment=payment,
                date=date,
            )

        content = render_template_string(
            """
            <section class="section">
                <div class="container">
                    <h2>العقد الجاهز</h2>
                    <div class="contract-box">
                        <h3 style="text-align:center;">عقد بيع سيارة</h3>
                        <p><strong>الطرف الأول:</strong> {{ site_name }}</p>
                        <p><strong>الطرف الثاني:</strong> {{ buyer_name }}</p>
                        <p><strong>رقم تعريف الزبون:</strong> {{ buyer_id }}</p>
                        <p><strong>موضوع العقد:</strong> بيع السيارة التالية للزبون:</p>
                        <p>
                            <strong>السيارة:</strong> {{ car_name }}<br>
                            <strong>رقم الهيكل:</strong> {{ chassis }}<br>
                            <strong>السعر:</strong> {{ price }}<br>
                            <strong>طريقة الدفع:</strong> {{ payment }}
                        </p>
                        <p>
                            <strong>الشروط:</strong><br>
                            1. يقر المشتري بأنه عاين السيارة ووافق على حالتها الحالية.<br>
                            2. تم الاتفاق على السعر النهائي المذكور أعلاه دون أي نزاع لاحق.<br>
                            3. تنتقل مسؤولية السيارة إلى المشتري بعد التسليم الكامل واستلام الوثائق.<br>
                            4. يتحمل المشتري جميع الإجراءات الإدارية والقانونية بعد التسليم ما لم يُنص على غير ذلك.<br>
                        </p>
                        <p><strong>تاريخ العقد:</strong> {{ date }}</p>
                        <br><br>
                        <div style="display:flex; justify-content:space-between; gap: 12px; flex-wrap: wrap;">
                            <div>توقيع البائع: __________</div>
                            <div>توقيع المشتري: __________</div>
                        </div>
                    </div>
                    <br>
                    <form method="post">
                        <input type="hidden" name="buyer_name" value="{{ buyer_name }}">
                        <input type="hidden" name="buyer_id" value="{{ buyer_id }}">
                        <input type="hidden" name="car_name" value="{{ car_name }}">
                        <input type="hidden" name="chassis" value="{{ chassis }}">
                        <input type="hidden" name="price" value="{{ price }}">
                        <input type="hidden" name="payment" value="{{ payment }}">
                        <input type="hidden" name="date" value="{{ date }}">
                        <button class="btn btn-primary" type="submit" name="action" value="pdf">تحميل PDF</button>
                        <a class="btn btn-secondary" href="{{ url_for('contract_form') }}">إنشاء عقد جديد</a>
                    </form>
                </div>
            </section>
            """,
            site_name=SITE_NAME,
            buyer_name=buyer_name,
            buyer_id=buyer_id,
            car_name=car_name,
            chassis=chassis,
            price=price,
            payment=payment,
            date=date,
        )
        return render_page("العقد الجاهز", content)

    prefilled_car = request.args.get("car_name", "")
    content = render_template_string(
        """
        <section class="section">
            <div class="container">
                <h2>تحرير عقد مع الزبون</h2>
                <p class="lead">املأ البيانات ثم اعرض العقد أو حمّله PDF جاهز للطباعة.</p>
                <form method="post">
                    <label>اسم الزبون</label>
                    <input name="buyer_name" required>

                    <label>رقم بطاقة التعريف / جواز السفر</label>
                    <input name="buyer_id" required>

                    <label>اسم السيارة</label>
                    <input name="car_name" value="{{ prefilled_car }}" required>

                    <label>رقم الهيكل</label>
                    <input name="chassis" required>

                    <label>السعر</label>
                    <input name="price" required>

                    <label>طريقة الدفع</label>
                    <select name="payment" required>
                        <option value="نقداً">نقداً</option>
                        <option value="تحويل بنكي">تحويل بنكي</option>
                        <option value="دفعات / أقساط">دفعات / أقساط</option>
                    </select>

                    <label>تاريخ العقد</label>
                    <input type="date" name="date" required>

                    <button class="btn btn-secondary" type="submit">معاينة العقد</button>
                    <button class="btn btn-primary" type="submit" name="action" value="pdf">تحميل PDF مباشرة</button>
                </form>
            </div>
        </section>
        """,
        prefilled_car=prefilled_car,
    )
    return render_page("تحرير عقد", content)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            response = redirect(url_for("admin_dashboard"))
            response.set_cookie("admin_auth", ADMIN_PASSWORD, max_age=60 * 60 * 8, httponly=True)
            flash("تم تسجيل الدخول بنجاح")
            return response
        flash("كلمة المرور غير صحيحة")

    content = render_template_string(
        """
        <section class="section">
            <div class="container" style="max-width: 560px;">
                <h2>تسجيل دخول لوحة التحكم</h2>
                <p class="lead">كلمة المرور الافتراضية: admin123 — غيّرها داخل الكود قبل النشر.</p>
                <form method="post">
                    <label>كلمة المرور</label>
                    <input type="password" name="password" required>
                    <button class="btn btn-primary" type="submit">دخول</button>
                </form>
            </div>
        </section>
        """
    )
    return render_page("دخول الإدارة", content)


@app.route("/admin/logout")
def admin_logout():
    response = redirect(url_for("admin_login"))
    response.delete_cookie("admin_auth")
    flash("تم تسجيل الخروج")
    return response


@app.route("/admin")
def admin_dashboard():
    guard = require_admin()
    if guard:
        return guard
    cars = fetch_all_cars()
    items = fetch_client_videos()
    content = render_template_string(
        """
        <section class="section">
            <div class="container">
                <div style="display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; align-items:center;">
                    <div>
                        <h2>لوحة التحكم</h2>
                        <p class="lead">إضافة السيارات، رفع الصور، وإدارة فيديوهات الزبائن.</p>
                    </div>
                    <div>
                        <a class="btn btn-primary" href="{{ url_for('admin_add_car') }}">إضافة سيارة</a>
                        <a class="btn btn-secondary" href="{{ url_for('admin_add_client_video') }}">إضافة فيديو زبون</a>
                        <a class="btn btn-danger" href="{{ url_for('admin_logout') }}">خروج</a>
                    </div>
                </div>

                <div class="section" style="padding-bottom: 24px;">
                    <h2>السيارات</h2>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>الصورة</th>
                                    <th>الاسم</th>
                                    <th>السعر</th>
                                    <th>السنة</th>
                                    <th>الإجراءات</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for car in cars %}
                                <tr>
                                    <td><img class="thumb" src="{{ image_url(car['image_filename']) }}" alt="{{ car['name'] }}"></td>
                                    <td>{{ car['name'] }}</td>
                                    <td>{{ car['price'] }}</td>
                                    <td>{{ car['year'] }}</td>
                                    <td>
                                        <div class="actions">
                                            <a class="btn btn-dark" href="{{ url_for('admin_edit_car', car_id=car['id']) }}">تعديل</a>
                                            <a class="btn btn-danger" href="{{ url_for('admin_delete_car', car_id=car['id']) }}" onclick="return confirm('هل أنت متأكد من حذف السيارة؟');">حذف</a>
                                        </div>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="section" style="padding-top: 0;">
                    <h2>فيديوهات الزبائن</h2>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>الاسم</th>
                                    <th>المدينة</th>
                                    <th>التعليق</th>
                                    <th>الإجراءات</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in items %}
                                <tr>
                                    <td>{{ item['client_name'] }}</td>
                                    <td>{{ item['city'] }}</td>
                                    <td>{{ item['comment'] }}</td>
                                    <td>
                                        <a class="btn btn-danger" href="{{ url_for('admin_delete_client_video', video_id=item['id']) }}" onclick="return confirm('هل أنت متأكد من حذف الفيديو؟');">حذف</a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>
        """,
        cars=cars,
        items=items,
        image_url=image_url,
    )
    return render_page("لوحة التحكم", content)


@app.route("/admin/cars/add", methods=["GET", "POST"])
def admin_add_car():
    guard = require_admin()
    if guard:
        return guard
    if request.method == "POST":
        try:
            image_filename = save_uploaded_image(request.files.get("image"))
            db = get_db()
            db.execute(
                """
                INSERT INTO cars (name, price, year, mileage, fuel, transmission, description, video, image_filename, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request.form.get("name", "").strip(),
                    request.form.get("price", "").strip(),
                    int(request.form.get("year", 0) or 0),
                    request.form.get("mileage", "").strip(),
                    request.form.get("fuel", "").strip(),
                    request.form.get("transmission", "").strip(),
                    request.form.get("description", "").strip(),
                    request.form.get("video", "").strip(),
                    image_filename,
                    datetime.now().isoformat(),
                ),
            )
            db.commit()
            flash("تمت إضافة السيارة بنجاح")
            return redirect(url_for("admin_dashboard"))
        except ValueError as exc:
            flash(str(exc))

    content = render_template_string(CAR_FORM_TEMPLATE, car=None, action_url=url_for("admin_add_car"), title_text="إضافة سيارة")
    return render_page("إضافة سيارة", content)


@app.route("/admin/cars/<int:car_id>/edit", methods=["GET", "POST"])
def admin_edit_car(car_id):
    guard = require_admin()
    if guard:
        return guard
    car = fetch_car(car_id)
    if not car:
        flash("السيارة غير موجودة")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        try:
            image_filename = car["image_filename"]
            uploaded = request.files.get("image")
            if uploaded and uploaded.filename:
                image_filename = save_uploaded_image(uploaded)
            db = get_db()
            db.execute(
                """
                UPDATE cars
                SET name = ?, price = ?, year = ?, mileage = ?, fuel = ?, transmission = ?, description = ?, video = ?, image_filename = ?
                WHERE id = ?
                """,
                (
                    request.form.get("name", "").strip(),
                    request.form.get("price", "").strip(),
                    int(request.form.get("year", 0) or 0),
                    request.form.get("mileage", "").strip(),
                    request.form.get("fuel", "").strip(),
                    request.form.get("transmission", "").strip(),
                    request.form.get("description", "").strip(),
                    request.form.get("video", "").strip(),
                    image_filename,
                    car_id,
                ),
            )
            db.commit()
            flash("تم تعديل السيارة بنجاح")
            return redirect(url_for("admin_dashboard"))
        except ValueError as exc:
            flash(str(exc))

    content = render_template_string(CAR_FORM_TEMPLATE, car=car, action_url=url_for("admin_edit_car", car_id=car_id), title_text="تعديل سيارة")
    return render_page("تعديل سيارة", content)


@app.route("/admin/cars/<int:car_id>/delete")
def admin_delete_car(car_id):
    guard = require_admin()
    if guard:
        return guard
    car = fetch_car(car_id)
    if car:
        if car["image_filename"]:
            try:
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], car["image_filename"]))
            except OSError:
                pass
        db = get_db()
        db.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        db.commit()
        flash("تم حذف السيارة")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/clients/add", methods=["GET", "POST"])
def admin_add_client_video():
    guard = require_admin()
    if guard:
        return guard
    if request.method == "POST":
        db = get_db()
        db.execute(
            """
            INSERT INTO client_videos (client_name, city, video_url, comment, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                request.form.get("client_name", "").strip(),
                request.form.get("city", "").strip(),
                request.form.get("video_url", "").strip(),
                request.form.get("comment", "").strip(),
                datetime.now().isoformat(),
            ),
        )
        db.commit()
        flash("تمت إضافة فيديو الزبون")
        return redirect(url_for("admin_dashboard"))

    content = render_template_string(
        """
        <section class="section">
            <div class="container" style="max-width: 760px;">
                <h2>إضافة فيديو زبون</h2>
                <form method="post">
                    <label>اسم الزبون</label>
                    <input name="client_name" required>

                    <label>المدينة</label>
                    <input name="city">

                    <label>رابط الفيديو المضمن (YouTube embed)</label>
                    <input name="video_url" placeholder="https://www.youtube.com/embed/..." required>

                    <label>تعليق</label>
                    <textarea name="comment"></textarea>

                    <button class="btn btn-primary" type="submit">حفظ</button>
                    <a class="btn btn-secondary" href="{{ url_for('admin_dashboard') }}">رجوع</a>
                </form>
            </div>
        </section>
        """
    )
    return render_page("إضافة فيديو زبون", content)


@app.route("/admin/clients/<int:video_id>/delete")
def admin_delete_client_video(video_id):
    guard = require_admin()
    if guard:
        return guard
    db = get_db()
    db.execute("DELETE FROM client_videos WHERE id = ?", (video_id,))
    db.commit()
    flash("تم حذف فيديو الزبون")
    return redirect(url_for("admin_dashboard"))


CAR_FORM_TEMPLATE = """
<section class="section">
    <div class="container" style="max-width: 760px;">
        <h2>{{ title_text }}</h2>
        <form method="post" enctype="multipart/form-data">
            <label>اسم السيارة</label>
            <input name="name" value="{{ car['name'] if car else '' }}" required>

            <label>السعر</label>
            <input name="price" value="{{ car['price'] if car else '' }}" required>

            <label>السنة</label>
            <input type="number" name="year" value="{{ car['year'] if car else '' }}">

            <label>العداد</label>
            <input name="mileage" value="{{ car['mileage'] if car else '' }}">

            <label>الوقود</label>
            <input name="fuel" value="{{ car['fuel'] if car else '' }}">

            <label>ناقل الحركة</label>
            <input name="transmission" value="{{ car['transmission'] if car else '' }}">

            <label>وصف السيارة</label>
            <textarea name="description">{{ car['description'] if car else '' }}</textarea>

            <label>رابط فيديو السيارة (YouTube embed)</label>
            <input name="video" value="{{ car['video'] if car else '' }}" placeholder="https://www.youtube.com/embed/...">

            <label>صورة السيارة</label>
            <input type="file" name="image" accept=".png,.jpg,.jpeg,.webp,.gif">
            {% if car and car['image_filename'] %}
                <p class="small">الصورة الحالية:</p>
                <img class="thumb" style="width: 180px; height: 120px;" src="{{ image_url(car['image_filename']) }}" alt="{{ car['name'] }}">
            {% endif %}

            <button class="btn btn-primary" type="submit">حفظ</button>
            <a class="btn btn-secondary" href="{{ url_for('admin_dashboard') }}">رجوع</a>
        </form>
    </div>
</section>
"""


def draw_arabic_like_line(pdf, font_name, page_width, y_mm, text):
    pdf.drawRightString(page_width - 20 * mm, y_mm * mm, text)


def register_pdf_font():
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("ArabicFont", path))
                return "ArabicFont"
            except Exception:
                continue
    return "Helvetica"


def generate_contract_pdf(buyer_name, buyer_id, car_name, chassis, price, payment, date):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    page_width, page_height = A4
    font_name = register_pdf_font()
    pdf.setTitle("Car Contract")
    pdf.setFont(font_name, 16)
    draw_arabic_like_line(pdf, font_name, page_width, 280, "عقد بيع سيارة")

    pdf.setFont(font_name, 12)
    lines = [
        f"الطرف الأول: {SITE_NAME}",
        f"الطرف الثاني: {buyer_name}",
        f"رقم تعريف الزبون: {buyer_id}",
        f"السيارة: {car_name}",
        f"رقم الهيكل: {chassis}",
        f"السعر: {price}",
        f"طريقة الدفع: {payment}",
        f"تاريخ العقد: {date}",
        "",
        "الشروط:",
        "1- يقر المشتري بأنه عاين السيارة ووافق على حالتها الحالية.",
        "2- تم الاتفاق على السعر النهائي المذكور أعلاه دون أي نزاع لاحق.",
        "3- تنتقل مسؤولية السيارة إلى المشتري بعد التسليم الكامل واستلام الوثائق.",
        "4- يتحمل المشتري جميع الإجراءات الإدارية والقانونية بعد التسليم.",
        "",
        "توقيع البائع: _____________",
        "توقيع المشتري: _____________",
    ]

    y = 265
    for line in lines:
        draw_arabic_like_line(pdf, font_name, page_width, y, line)
        y -= 10

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="contract.pdf", mimetype="application/pdf")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)