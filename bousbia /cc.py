# -*- coding: utf-8 -*-
import os
import sqlite3
from functools import wraps
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "drivewaydz-secret-key-change-this"
DATABASE = "drivewaydz.db"
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            image TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT,
            car_model TEXT,
            message TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute("SELECT COUNT(*) AS count FROM cars")
    count = cur.fetchone()["count"]

    if count == 0:
        seed_cars = [
            (
                "Chery Tiggo 2 Pro",
                "ابتداءً من 3,290,000 دج",
                "SUV حضرية",
                "اقتصادية وعملية، مناسبة للاستعمال اليومي داخل المدينة.",
                "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
            (
                "Geely Coolray",
                "ابتداءً من 4,650,000 دج",
                "SUV شبابية",
                "تصميم عصري وتجهيزات متقدمة مع حضور قوي على الطريق.",
                "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1200&q=80",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
            (
                "JAC JS4",
                "ابتداءً من 4,180,000 دج",
                "SUV عائلية",
                "مساحة ممتازة وراحة مناسبة للعائلة والسفر.",
                "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
            (
                "MG 5",
                "ابتداءً من 3,780,000 دج",
                "سيدان",
                "أنيقة وعملية مع توازن ممتاز بين السعر والتجهيزات.",
                "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        ]
        cur.executemany(
            "INSERT INTO cars (name, price, category, description, image, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            seed_cars,
        )

    conn.commit()
    conn.close()


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return func(*args, **kwargs)

    return wrapper


BASE_CSS = """
<style>
    :root {
        --bg: #f4f7fb;
        --card: #ffffff;
        --text: #0f172a;
        --muted: #64748b;
        --line: #e2e8f0;
        --primary: #111827;
        --primary2: #1f2937;
        --gold: #c59b49;
        --danger: #dc2626;
        --success: #16a34a;
        --radius: 22px;
        --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
        --container: 1180px;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
        margin: 0;
        font-family: Arial, Helvetica, sans-serif;
        background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
        color: var(--text);
    }
    a { text-decoration: none; color: inherit; }
    img { max-width: 100%; display: block; }
    .container { width: min(92%, var(--container)); margin: auto; }
    .topbar {
        position: sticky; top: 0; z-index: 1000;
        background: rgba(255,255,255,.85);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--line);
    }
    .nav {
        display: flex; align-items: center; justify-content: space-between;
        padding: 18px 0; gap: 18px;
    }
    .brand { display: flex; align-items: center; gap: 14px; }
    .brand-mark {
        width: 48px; height: 48px; border-radius: 16px;
        display: grid; place-items: center; color: white; font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--primary2));
    }
    .brand h1, .brand h2 { margin: 0; font-size: 22px; }
    .brand p { margin: 4px 0 0; color: var(--muted); font-size: 13px; }
    .menu { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
    .menu a { color: #334155; }
    .btn {
        display: inline-flex; align-items: center; justify-content: center;
        border: none; cursor: pointer; padding: 14px 22px; border-radius: 999px;
        font-weight: 700; transition: .2s ease;
    }
    .btn:hover { transform: translateY(-2px); }
    .btn-primary { background: linear-gradient(135deg, var(--primary), var(--primary2)); color: white; }
    .btn-outline { background: white; border: 1px solid var(--line); color: var(--text); }
    .btn-danger { background: var(--danger); color: white; }
    .hero { padding: 70px 0 40px; }
    .hero-grid { display: grid; grid-template-columns: 1.05fr .95fr; gap: 34px; align-items: center; }
    .eyebrow {
        display: inline-flex; padding: 10px 16px; border-radius: 999px;
        border: 1px solid var(--line); background: white; color: #334155; margin-bottom: 16px;
    }
    .hero h2 { margin: 0; font-size: clamp(34px, 5vw, 62px); line-height: 1.08; }
    .hero h2 span { color: var(--gold); }
    .hero p { color: #475569; font-size: 18px; line-height: 1.9; }
    .hero-actions { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 24px; }
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 28px; }
    .stat, .panel, .car-card {
        background: rgba(255,255,255,.94); border: 1px solid var(--line);
        border-radius: var(--radius); box-shadow: var(--shadow);
    }
    .stat { padding: 18px; }
    .stat strong { display: block; font-size: 28px; margin-bottom: 6px; }
    .stat span { color: var(--muted); font-size: 14px; }
    .hero-card { overflow: hidden; border-radius: 34px; box-shadow: 0 30px 60px rgba(15,23,42,.15); }
    .hero-card img { width: 100%; height: 560px; object-fit: cover; }
    .floating-badge {
        position: absolute; left: 18px; bottom: 18px; background: rgba(255,255,255,.95);
        border: 1px solid var(--line); border-radius: 18px; padding: 14px 16px; box-shadow: var(--shadow);
    }
    section { padding: 40px 0; }
    .section-head { display: flex; justify-content: space-between; align-items: end; gap: 18px; margin-bottom: 24px; }
    .section-head h3 { margin: 0; font-size: clamp(28px, 4vw, 40px); }
    .section-head p { margin: 10px 0 0; color: var(--muted); line-height: 1.8; }
    .cars-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }
    .car-card { overflow: hidden; transition: .2s ease; }
    .car-card:hover { transform: translateY(-5px); }
    .car-card img { width: 100%; height: 235px; object-fit: cover; }
    .car-body { padding: 20px; }
    .tag {
        display: inline-flex; padding: 8px 12px; border-radius: 999px; font-size: 12px;
        background: #eef2ff; color: #3730a3; margin-bottom: 12px; font-weight: 700;
    }
    .car-title-row { display: flex; justify-content: space-between; gap: 12px; align-items: start; }
    .car-title-row h4 { margin: 0; font-size: 22px; }
    .price { font-weight: 800; white-space: nowrap; }
    .car-body p { color: var(--muted); line-height: 1.9; }
    .features-grid, .steps-grid, .contact-grid, .admin-grid, .login-wrap { display: grid; gap: 22px; }
    .features-grid { grid-template-columns: 1fr 1fr; }
    .steps-grid { grid-template-columns: repeat(4, 1fr); }
    .contact-grid { grid-template-columns: .9fr 1.1fr; align-items: start; }
    .admin-grid { grid-template-columns: 1fr 1fr; align-items: start; }
    .panel { padding: 24px; }
    .dark-panel { background: linear-gradient(135deg, var(--primary), #0b1220); color: white; }
    .dark-panel p, .dark-panel li, .dark-panel small { color: rgba(255,255,255,.82); }
    .service-item { display: flex; gap: 14px; padding: 16px 0; border-bottom: 1px solid var(--line); }
    .service-item:last-child { border-bottom: none; }
    .dot { width: 14px; height: 14px; border-radius: 50%; background: linear-gradient(135deg, var(--gold), #e8c981); margin-top: 8px; }
    .step-number {
        width: 56px; height: 56px; border-radius: 18px; display: grid; place-items: center;
        background: linear-gradient(135deg, var(--primary), var(--primary2)); color: white; font-weight: 800; margin-bottom: 16px;
    }
    .contact-box ul, .admin-list { list-style: none; padding: 0; margin: 18px 0 0; }
    .contact-box li, .admin-list li { margin-bottom: 12px; }
    form { display: grid; gap: 16px; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    input, textarea, select {
        width: 100%; padding: 14px 16px; border-radius: 16px; border: 1px solid var(--line);
        background: white; font-size: 15px; outline: none;
    }
    textarea { min-height: 130px; resize: vertical; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 12px 10px; border-bottom: 1px solid var(--line); text-align: right; vertical-align: top; }
    th { color: var(--muted); font-size: 14px; }
    .flash {
        padding: 14px 16px; border-radius: 16px; margin-bottom: 14px; font-weight: 700;
        border: 1px solid rgba(22,163,74,.2); background: rgba(22,163,74,.1); color: #166534;
    }
    .flash.error { border-color: rgba(220,38,38,.2); background: rgba(220,38,38,.08); color: #991b1b; }
    .login-wrap { min-height: 100vh; place-items: center; }
    .login-card { width: min(94%, 460px); }
    .muted { color: var(--muted); }
    .small { font-size: 13px; }
    .admin-top {
        display: flex; justify-content: space-between; align-items: center; gap: 14px; margin-bottom: 20px;
    }
    .actions { display: flex; gap: 8px; flex-wrap: wrap; }
    .thumb { width: 68px; height: 48px; object-fit: cover; border-radius: 10px; border: 1px solid var(--line); }
    .empty { color: var(--muted); padding: 16px 0; }
    .whatsapp-float {
        position: fixed; left: 20px; bottom: 20px; z-index: 1000; background: #25D366; color: white;
        border-radius: 999px; padding: 14px 18px; font-weight: 800; box-shadow: 0 18px 40px rgba(37,211,102,.28);
    }
    footer { padding: 24px 0 40px; color: var(--muted); text-align: center; }
    @media (max-width: 1100px) {
        .hero-grid, .features-grid, .contact-grid, .cars-grid, .steps-grid, .admin-grid { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 820px) {
        .menu { display: none; }
        .hero-grid, .features-grid, .contact-grid, .cars-grid, .steps-grid, .admin-grid, .stats, .grid-2 {
            grid-template-columns: 1fr;
        }
        .nav, .section-head, .hero-actions, .admin-top { flex-direction: column; align-items: stretch; }
        .hero-card img { height: 360px; }
    }
</style>
"""


HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Drivewaydz | وسيط شراء السيارات الصينية في الجزائر</title>
    <meta name="description" content="Drivewaydz منصة احترافية لوساطة وطلب السيارات الصينية في الجزائر." />
    {{ css|safe }}
</head>
<body>
    <div class="topbar">
        <div class="container nav">
            <div class="brand">
                <div class="brand-mark">D</div>
                <div>
                    <h1>Drivewaydz</h1>
                    <p>وسيط السيارات الصينية في الجزائر</p>
                </div>
            </div>
            <div class="menu">
                <a href="#cars">السيارات</a>
                <a href="#services">الخدمات</a>
                <a href="#steps">كيف نعمل</a>
                <a href="#contact">تواصل</a>
                <a href="{{ url_for('admin_login') }}" class="btn btn-outline">لوحة التحكم</a>
            </div>
        </div>
    </div>

    <header class="hero">
        <div class="container hero-grid">
            <div>
                <div class="eyebrow">سيارات صينية جديدة • خدمة احترافية موجهة للسوق الجزائري</div>
                <h2>اشترِ سيارتك بثقة مع <span>Drivewaydz</span></h2>
                <p>
                    منصة احترافية لوساطة وطلب السيارات الصينية في الجزائر، تمنحك تجربة واضحة وسريعة تبدأ من اختيار الموديل المناسب وتنتهي بمرافقة كاملة حتى الاستلام.
                </p>
                <div class="hero-actions">
                    <a href="#cars" class="btn btn-primary">تصفح السيارات</a>
                    <a href="#contact" class="btn btn-outline">اطلب عرض سعر</a>
                </div>
                <div class="stats">
                    <div class="stat"><strong>{{ cars_count }}</strong><span>موديل متاح</span></div>
                    <div class="stat"><strong>48</strong><span>ولاية مغطاة</span></div>
                    <div class="stat"><strong>{{ requests_count }}</strong><span>طلب مسجل</span></div>
                    <div class="stat"><strong>100%</strong><span>مرافقة شخصية</span></div>
                </div>
            </div>
            <div style="position:relative">
                <div class="hero-card">
                    <img src="https://images.unsplash.com/photo-1502161254066-6c74afbf07aa?auto=format&fit=crop&w=1400&q=80" alt="Drivewaydz" />
                </div>
                <div class="floating-badge">
                    <strong>استشارة أولية مجانية</strong>
                    <span>نساعدك تختار السيارة المناسبة حسب ميزانيتك واحتياجك</span>
                </div>
            </div>
        </div>
    </header>

    <section id="cars">
        <div class="container">
            <div class="section-head">
                <div>
                    <h3>أحدث السيارات المطلوبة</h3>
                    <p>يمكنك إدارة هذه السيارات مباشرة من لوحة التحكم وإضافة أو تعديل أو حذف أي موديل.</p>
                </div>
            </div>
            <div class="cars-grid">
                {% for car in cars %}
                <article class="car-card">
                    <img src="{{ car['image'] }}" alt="{{ car['name'] }}">
                    <div class="car-body">
                        <span class="tag">{{ car['category'] }}</span>
                        <div class="car-title-row">
                            <h4>{{ car['name'] }}</h4>
                            <div class="price">{{ car['price'] }}</div>
                        </div>
                        <p>{{ car['description'] }}</p>
                        <a class="btn btn-primary" href="#contact">اطلب هذا الموديل</a>
                    </div>
                </article>
                {% endfor %}
            </div>
        </div>
    </section>

    <section id="services">
        <div class="container features-grid">
            <div class="panel">
                <div class="section-head" style="margin-bottom:12px;">
                    <div>
                        <h3>لماذا Drivewaydz؟</h3>
                        <p>واجهة قوية، سرعة، ثقة، ومتابعة احترافية لكل طلب.</p>
                    </div>
                </div>
                {% for item in services %}
                <div class="service-item">
                    <div class="dot"></div>
                    <div>{{ item }}</div>
                </div>
                {% endfor %}
            </div>
            <div class="panel dark-panel contact-box">
                <h3 style="margin-top:0;">موقع أعمال متكامل</h3>
                <p>النسخة الحالية فيها لوحة تحكم كاملة، قاعدة بيانات SQLite، وتسجيل طلبات العملاء وإدارة السيارات من داخل الموقع.</p>
                <ul>
                    <li>✔ إضافة سيارات جديدة</li>
                    <li>✔ تعديل وحذف الموديلات</li>
                    <li>✔ عرض طلبات العملاء</li>
                    <li>✔ تسجيل دخول للأدمن</li>
                </ul>
            </div>
        </div>
    </section>

    <section id="steps">
        <div class="container">
            <div class="section-head">
                <div>
                    <h3>كيف نعمل؟</h3>
                    <p>رحلة واضحة وسهلة تبني الثقة مع العميل من أول زيارة.</p>
                </div>
            </div>
            <div class="steps-grid">
                <div class="panel"><div class="step-number">1</div><h4>اختر السيارة</h4><p class="muted">تصفح الموديلات المتوفرة وحدد الفئة المناسبة لك.</p></div>
                <div class="panel"><div class="step-number">2</div><h4>اطلب الاستشارة</h4><p class="muted">أرسل طلبك وسنعاود الاتصال بك بسرعة.</p></div>
                <div class="panel"><div class="step-number">3</div><h4>ثبت الطلب</h4><p class="muted">نتابع معك خيارات الدفع والتجهيز والمرافقة.</p></div>
                <div class="panel"><div class="step-number">4</div><h4>استلم سيارتك</h4><p class="muted">مرافقة حتى التسليم داخل الجزائر.</p></div>
            </div>
        </div>
    </section>

    <section id="contact">
        <div class="container contact-grid">
            <div class="panel dark-panel contact-box">
                <h3 style="margin-top:0;">ابدأ طلبك الآن</h3>
                <p>أرسل بياناتك وسنقوم بالتواصل معك لتقديم عرض مناسب وخيارات متاحة حسب ميزانيتك.</p>
                <ul>
                    <li>الهاتف: 05 55 55 55 55</li>
                    <li>واتساب: 07 77 77 77 77</li>
                    <li>البريد: contact@drivewaydz.com</li>
                    <li>المدينة: الجزائر العاصمة</li>
                </ul>
            </div>
            <div class="panel">
                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        {% for category, message in messages %}
                            <div class="flash {{ 'error' if category == 'error' else '' }}">{{ message }}</div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                <form method="POST" action="{{ url_for('submit_request') }}">
                    <div class="grid-2">
                        <input type="text" name="fullname" placeholder="الاسم الكامل" required>
                        <input type="text" name="phone" placeholder="رقم الهاتف" required>
                    </div>
                    <div class="grid-2">
                        <input type="text" name="city" placeholder="الولاية">
                        <select name="car_model">
                            <option value="">اختر الموديل المطلوب</option>
                            {% for car in cars %}
                                <option value="{{ car['name'] }}">{{ car['name'] }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <textarea name="message" placeholder="اكتب تفاصيل طلبك أو الميزانية أو نوع السيارة"></textarea>
                    <button type="submit" class="btn btn-primary">إرسال الطلب</button>
                </form>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">جميع الحقوق محفوظة © Drivewaydz {{ year }}</div>
    </footer>

    <a class="whatsapp-float" href="https://wa.me/213777777777" target="_blank">واتساب</a>
</body>
</html>
"""


LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل دخول الأدمن</title>
    {{ css|safe }}
</head>
<body>
    <div class="login-wrap container">
        <div class="panel login-card">
            <div class="brand" style="margin-bottom:20px;">
                <div class="brand-mark">D</div>
                <div>
                    <h2>لوحة تحكم Drivewaydz</h2>
                    <p>تسجيل دخول الأدمن</p>
                </div>
            </div>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="flash {{ 'error' if category == 'error' else '' }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            <form method="POST">
                <input type="text" name="username" placeholder="اسم المستخدم" required>
                <input type="password" name="password" placeholder="كلمة المرور" required>
                <button class="btn btn-primary" type="submit">دخول</button>
            </form>
            <p class="muted small">البيانات الافتراضية: admin / 123456</p>
            <a href="{{ url_for('home') }}" class="btn btn-outline">العودة للموقع</a>
        </div>
    </div>
</body>
</html>
"""


ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم</title>
    {{ css|safe }}
</head>
<body>
    <div class="topbar">
        <div class="container nav">
            <div class="brand">
                <div class="brand-mark">D</div>
                <div>
                    <h2>لوحة التحكم</h2>
                    <p>إدارة السيارات والطلبات</p>
                </div>
            </div>
            <div class="menu">
                <a href="{{ url_for('home') }}">عرض الموقع</a>
                <a href="{{ url_for('admin_dashboard') }}">لوحة التحكم</a>
                <a href="{{ url_for('admin_logout') }}" class="btn btn-danger">تسجيل الخروج</a>
            </div>
        </div>
    </div>

    <section>
        <div class="container">
            <div class="admin-top">
                <div>
                    <h3 style="margin:0; font-size:34px;">لوحة تحكم كاملة</h3>
                    <p class="muted">من هنا يمكنك إضافة السيارات، تعديلها، حذفها، ومراجعة طلبات العملاء.</p>
                </div>
                <div class="actions">
                    <a class="btn btn-outline" href="{{ url_for('home') }}" target="_blank">فتح الموقع</a>
                    <a class="btn btn-primary" href="#add-car">إضافة سيارة</a>
                </div>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="flash {{ 'error' if category == 'error' else '' }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="admin-grid">
                <div class="panel" id="add-car">
                    <h3 style="margin-top:0;">{{ 'تعديل سيارة' if edit_car else 'إضافة سيارة جديدة' }}</h3>
                    <form method="POST" action="{{ url_for('save_car') }}">
                        <input type="hidden" name="car_id" value="{{ edit_car['id'] if edit_car else '' }}">
                        <input type="text" name="name" placeholder="اسم السيارة" value="{{ edit_car['name'] if edit_car else '' }}" required>
                        <div class="grid-2">
                            <input type="text" name="price" placeholder="السعر" value="{{ edit_car['price'] if edit_car else '' }}" required>
                            <input type="text" name="category" placeholder="الفئة" value="{{ edit_car['category'] if edit_car else '' }}" required>
                        </div>
                        <input type="text" name="image" placeholder="رابط الصورة" value="{{ edit_car['image'] if edit_car else '' }}">
                        <textarea name="description" placeholder="وصف السيارة">{{ edit_car['description'] if edit_car else '' }}</textarea>
                        <div class="actions">
                            <button class="btn btn-primary" type="submit">{{ 'حفظ التعديلات' if edit_car else 'إضافة السيارة' }}</button>
                            {% if edit_car %}
                                <a class="btn btn-outline" href="{{ url_for('admin_dashboard') }}">إلغاء</a>
                            {% endif %}
                        </div>
                    </form>
                </div>

                <div class="panel dark-panel">
                    <h3 style="margin-top:0;">إحصائيات سريعة</h3>
                    <ul class="admin-list">
                        <li>عدد السيارات: <strong>{{ cars|length }}</strong></li>
                        <li>عدد الطلبات: <strong>{{ requests|length }}</strong></li>
                        <li>آخر دخول: <strong>{{ now }}</strong></li>
                        <li>حساب الأدمن: <strong>admin</strong></li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <section>
        <div class="container">
            <div class="section-head">
                <div>
                    <h3>السيارات الحالية</h3>
                    <p>إدارة كاملة للموديلات المعروضة في الصفحة الرئيسية.</p>
                </div>
            </div>
            <div class="panel">
                {% if cars %}
                <table>
                    <thead>
                        <tr>
                            <th>الصورة</th>
                            <th>الاسم</th>
                            <th>الفئة</th>
                            <th>السعر</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for car in cars %}
                        <tr>
                            <td><img class="thumb" src="{{ car['image'] }}" alt="{{ car['name'] }}"></td>
                            <td>{{ car['name'] }}</td>
                            <td>{{ car['category'] }}</td>
                            <td>{{ car['price'] }}</td>
                            <td>
                                <div class="actions">
                                    <a class="btn btn-outline" href="{{ url_for('admin_dashboard', edit=car['id']) }}">تعديل</a>
                                    <a class="btn btn-danger" href="{{ url_for('delete_car', car_id=car['id']) }}" onclick="return confirm('هل تريد حذف هذه السيارة؟')">حذف</a>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                    <div class="empty">لا توجد سيارات حالياً.</div>
                {% endif %}
            </div>
        </div>
    </section>

    <section>
        <div class="container">
            <div class="section-head">
                <div>
                    <h3>طلبات العملاء</h3>
                    <p>كل الطلبات المرسلة من واجهة الموقع تظهر هنا.</p>
                </div>
            </div>
            <div class="panel">
                {% if requests %}
                <table>
                    <thead>
                        <tr>
                            <th>الاسم</th>
                            <th>الهاتف</th>
                            <th>الولاية</th>
                            <th>الموديل</th>
                            <th>الرسالة</th>
                            <th>التاريخ</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for req in requests %}
                        <tr>
                            <td>{{ req['fullname'] }}</td>
                            <td>{{ req['phone'] }}</td>
                            <td>{{ req['city'] }}</td>
                            <td>{{ req['car_model'] }}</td>
                            <td>{{ req['message'] }}</td>
                            <td>{{ req['created_at'] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                    <div class="empty">لا توجد طلبات بعد.</div>
                {% endif %}
            </div>
        </div>
    </section>
</body>
</html>
"""


@app.route("/")
def home():
    conn = get_db_connection()
    cars = conn.execute("SELECT * FROM cars ORDER BY id DESC").fetchall()
    requests_count = conn.execute("SELECT COUNT(*) AS c FROM requests").fetchone()["c"]
    conn.close()

    services = [
        "وساطة احترافية لشراء السيارات الصينية الجديدة حسب الطلب.",
        "استشارة شخصية لاختيار أفضل سيارة حسب الميزانية والاستعمال.",
        "مرافقة كاملة في الإجراءات الإدارية والتجارية حتى الاستلام.",
        "خدمة موجهة للأفراد والتجار مع حلول مرنة وسريعة.",
    ]

    return render_template_string(
        HOME_TEMPLATE,
        css=BASE_CSS,
        cars=cars,
        services=services,
        cars_count=len(cars),
        requests_count=requests_count,
        year=datetime.now().year,
    )


@app.route("/submit-request", methods=["POST"])
def submit_request():
    fullname = request.form.get("fullname", "").strip()
    phone = request.form.get("phone", "").strip()
    city = request.form.get("city", "").strip()
    car_model = request.form.get("car_model", "").strip()
    message = request.form.get("message", "").strip()

    if not fullname or not phone:
        flash("يرجى ملء الاسم ورقم الهاتف.", "error")
        return redirect(url_for("home") + "#contact")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO requests (fullname, phone, city, car_model, message, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (fullname, phone, city, car_model, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()

    flash("تم إرسال طلبك بنجاح. سنتواصل معك قريباً.")
    return redirect(url_for("home") + "#contact")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            flash("تم تسجيل الدخول بنجاح.")
            return redirect(url_for("admin_dashboard"))

        flash("بيانات الدخول غير صحيحة.", "error")

    return render_template_string(LOGIN_TEMPLATE, css=BASE_CSS)


@app.route("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    flash("تم تسجيل الخروج.")
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    edit_id = request.args.get("edit", "").strip()
    conn = get_db_connection()
    cars = conn.execute("SELECT * FROM cars ORDER BY id DESC").fetchall()
    requests_list = conn.execute("SELECT * FROM requests ORDER BY id DESC").fetchall()
    edit_car = None

    if edit_id.isdigit():
        edit_car = conn.execute("SELECT * FROM cars WHERE id = ?", (edit_id,)).fetchone()

    conn.close()

    return render_template_string(
        ADMIN_TEMPLATE,
        css=BASE_CSS,
        cars=cars,
        requests=requests_list,
        edit_car=edit_car,
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/admin/save-car", methods=["POST"])
@admin_required
def save_car():
    car_id = request.form.get("car_id", "").strip()
    name = request.form.get("name", "").strip()
    price = request.form.get("price", "").strip()
    category = request.form.get("category", "").strip()
    image = request.form.get("image", "").strip() or "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1200&q=80"
    description = request.form.get("description", "").strip()

    if not name or not price or not category:
        flash("يرجى ملء الاسم والسعر والفئة.", "error")
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()

    if car_id.isdigit():
        conn.execute(
            "UPDATE cars SET name = ?, price = ?, category = ?, description = ?, image = ? WHERE id = ?",
            (name, price, category, description, image, car_id),
        )
        flash("تم تعديل السيارة بنجاح.")
    else:
        conn.execute(
            "INSERT INTO cars (name, price, category, description, image, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (name, price, category, description, image, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        flash("تمت إضافة السيارة بنجاح.")

    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-car/<int:car_id>")
@admin_required
def delete_car(car_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    flash("تم حذف السيارة بنجاح.")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
