# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

CAR_LIST = [
    {
        "name": "Chery Tiggo 2 Pro",
        "price": "ابتداءً من 3,290,000 دج",
        "category": "SUV حضرية",
        "description": "اقتصادية، عملية، مناسبة للاستعمال اليومي داخل المدينة.",
        "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "name": "Geely Coolray",
        "price": "ابتداءً من 4,650,000 دج",
        "category": "SUV شبابية",
        "description": "تصميم عصري وتجهيزات متقدمة مع حضور قوي على الطريق.",
        "image": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "name": "JAC JS4",
        "price": "ابتداءً من 4,180,000 دج",
        "category": "SUV عائلية",
        "description": "مساحة ممتازة وراحة مناسبة للعائلة والسفر.",
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "name": "MG 5",
        "price": "ابتداءً من 3,780,000 دج",
        "category": "سيدان",
        "description": "أنيقة وعملية مع توازن ممتاز بين السعر والتجهيزات.",
        "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "name": "DFSK Glory 580",
        "price": "ابتداءً من 4,950,000 دج",
        "category": "SUV عائلية 7 مقاعد",
        "description": "حل ممتاز للعائلات الكبيرة مع مساحة داخلية مريحة.",
        "image": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "name": "BAIC X55",
        "price": "ابتداءً من 5,490,000 دج",
        "category": "SUV متطورة",
        "description": "تصميم فاخر وتقنيات حديثة للباحثين عن تجربة مميزة.",
        "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1200&q=80",
    },
]

SERVICES = [
    "وساطة احترافية لشراء السيارات الصينية الجديدة حسب الطلب.",
    "استشارة شخصية لاختيار أفضل سيارة حسب الميزانية والاستعمال.",
    "مرافقة كاملة في الإجراءات الإدارية والتجارية حتى الاستلام.",
    "خدمة موجهة للأفراد والتجار مع حلول مرنة وسريعة.",
]

STEPS = [
    ("1", "اختر السيارة", "تصفح الموديلات المتوفرة وحدد الفئة المناسبة لك."),
    ("2", "اطلب الاستشارة", "أرسل طلبك وسنعود إليك بعرض مفصل وخيارات متاحة."),
    ("3", "ثبت الطلب", "نتابع معك تفاصيل الطلب وخيارات الدفع والتجهيز."),
    ("4", "استلم سيارتك", "نرافقك حتى مرحلة التسليم داخل الجزائر."),
]

TESTIMONIALS = [
    {
        "name": "أمين - الجزائر العاصمة",
        "text": "خدمة محترفة جداً، التواصل ممتاز والشرح واضح من البداية حتى نهاية الطلب.",
    },
    {
        "name": "ياسين - وهران",
        "text": "وجدت السيارة المناسبة لميزانيتي بسرعة، والمتابعة كانت ممتازة.",
    },
    {
        "name": "سليم - سطيف",
        "text": "واجهة جميلة وخدمة جدية، أعجبتني طريقة عرض السيارات والتفاصيل.",
    },
]

SITE_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Drivewaydz | وسيط شراء السيارات الصينية في الجزائر</title>
    <meta name="description" content="Drivewaydz منصة احترافية لوساطة وطلب السيارات الصينية في الجزائر مع استشارة ومرافقة كاملة حتى الاستلام." />
    <style>
        :root {
            --bg: #f5f7fb;
            --card: rgba(255,255,255,.92);
            --text: #0f172a;
            --muted: #475569;
            --line: #e2e8f0;
            --primary: #111827;
            --primary-2: #1f2937;
            --accent: #caa55a;
            --success: #16a34a;
            --shadow: 0 18px 45px rgba(15, 23, 42, 0.10);
            --radius-xl: 28px;
            --radius-lg: 22px;
            --radius-md: 16px;
            --container: 1200px;
        }

        * { box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background:
                radial-gradient(circle at top right, rgba(202,165,90,.15), transparent 30%),
                linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
            color: var(--text);
        }

        a { text-decoration: none; color: inherit; }
        img { max-width: 100%; display: block; }
        .container { width: min(92%, var(--container)); margin: auto; }

        .topbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(14px);
            background: rgba(255,255,255,.78);
            border-bottom: 1px solid rgba(226,232,240,.8);
        }

        .nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            padding: 18px 0;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .brand-mark {
            width: 48px;
            height: 48px;
            border-radius: 16px;
            display: grid;
            place-items: center;
            color: white;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--primary-2));
            box-shadow: var(--shadow);
        }

        .brand h1 {
            margin: 0;
            font-size: 22px;
        }

        .brand p {
            margin: 4px 0 0;
            color: var(--muted);
            font-size: 13px;
        }

        .menu {
            display: flex;
            align-items: center;
            gap: 18px;
            flex-wrap: wrap;
        }

        .menu a {
            color: var(--muted);
            font-size: 15px;
            transition: .25s ease;
        }

        .menu a:hover { color: var(--text); }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 14px 22px;
            border-radius: 999px;
            border: 1px solid transparent;
            font-weight: 700;
            transition: .25s ease;
            cursor: pointer;
        }

        .btn-primary {
            color: white;
            background: linear-gradient(135deg, var(--primary), var(--primary-2));
            box-shadow: 0 12px 28px rgba(17,24,39,.18);
        }

        .btn-primary:hover { transform: translateY(-2px); }

        .btn-outline {
            color: var(--text);
            border-color: var(--line);
            background: rgba(255,255,255,.82);
        }

        .hero {
            padding: 70px 0 40px;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.05fr .95fr;
            gap: 34px;
            align-items: center;
        }

        .eyebrow {
            display: inline-flex;
            padding: 10px 16px;
            border-radius: 999px;
            background: rgba(255,255,255,.85);
            border: 1px solid var(--line);
            color: #334155;
            font-size: 14px;
            margin-bottom: 16px;
        }

        .hero h2 {
            margin: 0;
            font-size: clamp(36px, 5vw, 64px);
            line-height: 1.1;
        }

        .hero h2 span { color: var(--accent); }

        .hero p {
            color: var(--muted);
            font-size: 18px;
            line-height: 1.95;
            margin: 18px 0 0;
            max-width: 700px;
        }

        .hero-actions {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            margin-top: 28px;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-top: 30px;
        }

        .stat {
            background: var(--card);
            border: 1px solid rgba(226,232,240,.9);
            border-radius: var(--radius-md);
            padding: 18px;
            box-shadow: var(--shadow);
        }

        .stat strong {
            display: block;
            font-size: 28px;
            margin-bottom: 8px;
        }

        .stat span {
            color: var(--muted);
            font-size: 14px;
        }

        .hero-visual {
            position: relative;
        }

        .hero-card {
            background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(255,255,255,.86));
            border: 1px solid rgba(255,255,255,.85);
            border-radius: 34px;
            overflow: hidden;
            box-shadow: 0 30px 70px rgba(15,23,42,.14);
        }

        .hero-card img {
            width: 100%;
            height: 560px;
            object-fit: cover;
        }

        .floating-badge {
            position: absolute;
            left: 20px;
            bottom: 20px;
            background: rgba(255,255,255,.95);
            border-radius: 18px;
            padding: 14px 16px;
            border: 1px solid var(--line);
            box-shadow: var(--shadow);
        }

        .floating-badge strong { display: block; margin-bottom: 6px; }
        .floating-badge span { color: var(--muted); font-size: 14px; }

        section { padding: 40px 0; }

        .section-head {
            display: flex;
            justify-content: space-between;
            align-items: end;
            gap: 18px;
            margin-bottom: 24px;
        }

        .section-head h3 {
            margin: 0;
            font-size: clamp(28px, 4vw, 42px);
        }

        .section-head p {
            margin: 10px 0 0;
            color: var(--muted);
            line-height: 1.8;
            max-width: 700px;
        }

        .cars-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 22px;
        }

        .car-card {
            background: var(--card);
            border: 1px solid rgba(226,232,240,.95);
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: .25s ease;
        }

        .car-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 24px 55px rgba(15,23,42,.14);
        }

        .car-card img {
            width: 100%;
            height: 235px;
            object-fit: cover;
        }

        .car-body { padding: 20px; }

        .tag {
            display: inline-flex;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 12px;
            background: #eef2ff;
            color: #3730a3;
            margin-bottom: 12px;
            font-weight: 700;
        }

        .car-title-row {
            display: flex;
            align-items: start;
            justify-content: space-between;
            gap: 12px;
        }

        .car-title-row h4 {
            margin: 0;
            font-size: 22px;
        }

        .price {
            color: var(--text);
            font-weight: 800;
            white-space: nowrap;
        }

        .car-body p {
            color: var(--muted);
            line-height: 1.9;
            margin: 12px 0 18px;
        }

        .features-grid,
        .steps-grid,
        .testimonials-grid,
        .contact-grid {
            display: grid;
            gap: 22px;
        }

        .features-grid { grid-template-columns: 1fr 1fr; }
        .steps-grid { grid-template-columns: repeat(4, 1fr); }
        .testimonials-grid { grid-template-columns: repeat(3, 1fr); }
        .contact-grid { grid-template-columns: .9fr 1.1fr; align-items: start; }

        .panel {
            background: var(--card);
            border: 1px solid rgba(226,232,240,.95);
            border-radius: var(--radius-xl);
            padding: 24px;
            box-shadow: var(--shadow);
        }

        .service-item {
            display: flex;
            gap: 14px;
            align-items: start;
            padding: 16px 0;
            border-bottom: 1px solid var(--line);
        }

        .service-item:last-child { border-bottom: none; }

        .dot {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), #e8c981);
            margin-top: 8px;
            flex: 0 0 14px;
        }

        .dark-panel {
            background: linear-gradient(135deg, var(--primary), #0b1220);
            color: white;
        }

        .dark-panel p,
        .dark-panel li,
        .dark-panel small { color: rgba(255,255,255,.8); }

        .step-card {
            position: relative;
            overflow: hidden;
        }

        .step-number {
            width: 56px;
            height: 56px;
            display: grid;
            place-items: center;
            border-radius: 18px;
            background: linear-gradient(135deg, var(--primary), var(--primary-2));
            color: white;
            font-weight: 800;
            font-size: 20px;
            margin-bottom: 16px;
        }

        .step-card h4, .testimonial h4, .contact-box h4 { margin: 0 0 10px; }

        .step-card p, .testimonial p, .contact-box p {
            margin: 0;
            color: var(--muted);
            line-height: 1.9;
        }

        .testimonial .quote {
            font-size: 34px;
            color: var(--accent);
            margin-bottom: 12px;
            line-height: 1;
        }

        .contact-box ul {
            list-style: none;
            padding: 0;
            margin: 18px 0 0;
        }

        .contact-box li {
            margin-bottom: 12px;
            color: rgba(255,255,255,.88);
        }

        form {
            display: grid;
            gap: 16px;
        }

        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        input, textarea, select {
            width: 100%;
            border: 1px solid var(--line);
            background: rgba(255,255,255,.92);
            border-radius: 16px;
            padding: 15px 16px;
            font-size: 15px;
            outline: none;
            transition: .2s ease;
        }

        input:focus, textarea:focus, select:focus {
            border-color: #94a3b8;
            box-shadow: 0 0 0 4px rgba(148,163,184,.15);
        }

        textarea { min-height: 150px; resize: vertical; }

        .success-box {
            margin-bottom: 18px;
            padding: 16px 18px;
            border-radius: 16px;
            background: rgba(22,163,74,.1);
            border: 1px solid rgba(22,163,74,.2);
            color: #166534;
            font-weight: 700;
        }

        .whatsapp-float {
            position: fixed;
            left: 20px;
            bottom: 20px;
            z-index: 1000;
            background: #25D366;
            color: white;
            border-radius: 999px;
            padding: 14px 18px;
            font-weight: 800;
            box-shadow: 0 18px 40px rgba(37,211,102,.28);
        }

        footer {
            padding: 24px 0 40px;
            color: var(--muted);
            text-align: center;
        }

        @media (max-width: 1100px) {
            .hero-grid,
            .features-grid,
            .contact-grid,
            .cars-grid,
            .steps-grid,
            .testimonials-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media (max-width: 820px) {
            .nav,
            .section-head,
            .hero-actions,
            .grid-2,
            .hero-grid,
            .features-grid,
            .contact-grid,
            .cars-grid,
            .steps-grid,
            .testimonials-grid,
            .stats {
                grid-template-columns: 1fr;
                flex-direction: column;
                align-items: stretch;
            }

            .menu { display: none; }
            .hero-card img { height: 360px; }
            .hero { padding-top: 38px; }
            .stat strong { font-size: 24px; }
        }
    </style>
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
                <a href="#testimonials">آراء العملاء</a>
                <a href="#contact" class="btn btn-primary">اطلب استشارة</a>
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
                    <div class="stat"><strong>+40</strong><span>موديل متاح للطلب</span></div>
                    <div class="stat"><strong>48</strong><span>ولاية مغطاة</span></div>
                    <div class="stat"><strong>+250</strong><span>استشارة منجزة</span></div>
                    <div class="stat"><strong>100%</strong><span>مرافقة شخصية</span></div>
                </div>
            </div>
            <div class="hero-visual">
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
                    <p>تشكيلة أولية قابلة للتعديل حسب العلامات والموديلات التي تريد عرضها داخل الموقع.</p>
                </div>
            </div>
            <div class="cars-grid">
                {% for car in cars %}
                <article class="car-card">
                    <img src="{{ car.image }}" alt="{{ car.name }}">
                    <div class="car-body">
                        <span class="tag">{{ car.category }}</span>
                        <div class="car-title-row">
                            <h4>{{ car.name }}</h4>
                            <div class="price">{{ car.price }}</div>
                        </div>
                        <p>{{ car.description }}</p>
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
                        <p>موقع مصمم ليعكس الثقة والاحتراف ويحوّل الزائر إلى عميل فعلي.</p>
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
                <h4>حل مثالي لوسيط سيارات في الجزائر</h4>
                <p>
                    يمكن تطوير هذا الموقع لاحقاً ليشمل لوحة إدارة، إضافة سيارات من قاعدة بيانات، رفع صور حقيقية، وربط مباشر مع واتساب أو البريد الإلكتروني.
                </p>
                <ul>
                    <li>✔ تصميم عصري ومرتب</li>
                    <li>✔ متوافق مع الهاتف</li>
                    <li>✔ سريع وقابل للتطوير</li>
                    <li>✔ جاهز لإضافة طلبات حقيقية</li>
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
                {% for number, title, text in steps %}
                <div class="panel step-card">
                    <div class="step-number">{{ number }}</div>
                    <h4>{{ title }}</h4>
                    <p>{{ text }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <section id="testimonials">
        <div class="container">
            <div class="section-head">
                <div>
                    <h3>آراء العملاء</h3>
                    <p>قسم احترافي يرفع من مصداقية الموقع ويمكن استبداله لاحقاً بآراء حقيقية.</p>
                </div>
            </div>
            <div class="testimonials-grid">
                {% for item in testimonials %}
                <div class="panel testimonial">
                    <div class="quote">“</div>
                    <p>{{ item.text }}</p>
                    <h4 style="margin-top:16px;">{{ item.name }}</h4>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <section id="contact">
        <div class="container contact-grid">
            <div class="panel dark-panel contact-box">
                <h4>ابدأ طلبك الآن</h4>
                <p>أرسل بياناتك وسنقوم بالتواصل معك لتقديم عرض مناسب وخيارات متاحة حسب ميزانيتك.</p>
                <ul>
                    <li>الهاتف: 05 55 55 55 55</li>
                    <li>واتساب: 07 77 77 77 77</li>
                    <li>البريد: contact@drivewaydz.com</li>
                    <li>المدينة: الجزائر العاصمة</li>
                    <li>ساعات العمل: 09:00 - 18:00</li>
                </ul>
            </div>
            <div class="panel">
                {% if success %}
                <div class="success-box">تم إرسال طلبك بنجاح. يمكنك الآن تطوير هذه الخطوة للحفظ في قاعدة بيانات أو الإرسال إلى البريد.</div>
                {% endif %}
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
                            <option value="{{ car.name }}">{{ car.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <textarea name="message" placeholder="اكتب تفاصيل طلبك، الميزانية، أو السيارة التي تبحث عنها"></textarea>
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


@app.route("/")
def home():
    success = request.args.get("success") == "1"
    return render_template_string(
        SITE_HTML,
        cars=CAR_LIST,
        services=SERVICES,
        steps=STEPS,
        testimonials=TESTIMONIALS,
        success=success,
        year=datetime.now().year,
    )


@app.route("/submit-request", methods=["POST"])
def submit_request():
    fullname = request.form.get("fullname", "").strip()
    phone = request.form.get("phone", "").strip()
    city = request.form.get("city", "").strip()
    car_model = request.form.get("car_model", "").strip()
    message = request.form.get("message", "").strip()

    with open("طلبات_العملاء.txt", "a", encoding="utf-8") as file:
        file.write("-" * 70 + "\n")
        file.write(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"الاسم: {fullname}\n")
        file.write(f"الهاتف: {phone}\n")
        file.write(f"الولاية: {city}\n")
        file.write(f"الموديل: {car_model}\n")
        file.write(f"الرسالة: {message}\n")

    return redirect(url_for("home", success=1))


if __name__ == "__main__":
    app.run(debug=True)
