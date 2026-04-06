# -*- coding: utf-8 -*-
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drivewaydz</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            direction: rtl;
        }

        header {
            background: #ffffff;
            border-bottom: 1px solid #e2e8f0;
            padding: 20px 40px;
            position: sticky;
            top: 0;
        }

        .container {
            width: 90%;
            max-width: 1200px;
            margin: auto;
        }

        .hero {
            padding: 60px 20px;
            background: linear-gradient(to left, #e2e8f0, #ffffff);
        }

        .hero h1 {
            font-size: 42px;
            margin-bottom: 15px;
        }

        .hero p {
            font-size: 18px;
            line-height: 1.9;
            color: #475569;
            max-width: 700px;
        }

        .btn {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 24px;
            background: #0f172a;
            color: white;
            text-decoration: none;
            border-radius: 10px;
        }

        .section {
            padding: 50px 20px;
        }

        .section h2 {
            font-size: 32px;
            margin-bottom: 25px;
        }

        .cars {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .card {
            background: white;
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
        }

        .card img {
            width: 100%;
            height: 190px;
            object-fit: cover;
        }

        .card-content {
            padding: 18px;
        }

        .card-content h3 {
            margin: 0 0 10px;
            font-size: 22px;
        }

        .card-content p {
            margin: 6px 0;
            color: #475569;
        }

        .services ul {
            list-style: none;
            padding: 0;
        }

        .services li {
            background: white;
            margin-bottom: 12px;
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .contact {
            background: #0f172a;
            color: white;
            padding: 50px 20px;
        }

        .contact p {
            font-size: 18px;
            line-height: 1.8;
        }

        footer {
            text-align: center;
            padding: 20px;
            background: #ffffff;
            border-top: 1px solid #e2e8f0;
            color: #64748b;
        }
    </style>
</head>
<body>

    <header>
        <div class="container">
            <h2>Drivewaydz</h2>
            <p>وسيط شراء السيارات الصينية في الجزائر</p>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>اشترِ سيارتك الصينية بسهولة مع Drivewaydz</h1>
            <p>
                منصة وسيط بيع سيارات في الجزائر تساعدك على اختيار وطلب ومتابعة شراء
                السيارات الصينية المناسبة لك بأفضل قيمة وخدمة مرافقة احترافية.
            </p>
            <a href="#cars" class="btn">تصفح السيارات</a>
        </div>
    </section>

    <section class="section" id="cars">
        <div class="container">
            <h2>أشهر السيارات الصينية المطلوبة</h2>
            <div class="cars">

                <div class="card">
                    <img src="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80" alt="Chery Tiggo 2 Pro">
                    <div class="card-content">
                        <h3>Chery Tiggo 2 Pro</h3>
                        <p>الفئة: SUV حضرية</p>
                        <p>السعر: ابتداءً من 3,290,000 دج</p>
                    </div>
                </div>

                <div class="card">
                    <img src="https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1200&q=80" alt="Geely Coolray">
                    <div class="card-content">
                        <h3>Geely Coolray</h3>
                        <p>الفئة: SUV شبابية</p>
                        <p>السعر: ابتداءً من 4,650,000 دج</p>
                    </div>
                </div>

                <div class="card">
                    <img src="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80" alt="JAC JS4">
                    <div class="card-content">
                        <h3>JAC JS4</h3>
                        <p>الفئة: SUV عائلية</p>
                        <p>السعر: ابتداءً من 4,180,000 دج</p>
                    </div>
                </div>

                <div class="card">
                    <img src="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80" alt="MG 5">
                    <div class="card-content">
                        <h3>MG 5</h3>
                        <p>الفئة: سيدان</p>
                        <p>السعر: ابتداءً من 3,780,000 دج</p>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <section class="section services">
        <div class="container">
            <h2>خدماتنا</h2>
            <ul>
                <li>استيراد ووساطة في شراء السيارات الصينية الجديدة</li>
                <li>مرافقة كاملة في إجراءات الطلب والتسجيل</li>
                <li>اقتراحات حسب الميزانية والاستعمال</li>
                <li>توفير عروض خاصة للتجار والأفراد</li>
            </ul>
        </div>
    </section>

    <section class="contact">
        <div class="container">
            <h2>تواصل معنا</h2>
            <p>الهاتف: 05 55 55 55 55</p>
            <p>واتساب: 07 77 77 77 77</p>
            <p>البريد: contact@drivewaydz.com</p>
            <p>الجزائر العاصمة، الجزائر</p>
        </div>
    </section>

    <footer>
        جميع الحقوق محفوظة © Drivewaydz
    </footer>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)