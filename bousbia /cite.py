export default function DrivewayDZWebsite() {
  const cars = [
    {
      name: "Chery Tiggo 2 Pro",
      price: "ابتداءً من 3,290,000 دج",
      category: "SUV حضرية",
      range: "اقتصادية وعملية",
      image:
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",
    },
    {
      name: "Geely Coolray",
      price: "ابتداءً من 4,650,000 دج",
      category: "SUV شبابية",
      range: "تصميم عصري وتجهيزات قوية",
      image:
        "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1200&q=80",
    },
    {
      name: "JAC JS4",
      price: "ابتداءً من 4,180,000 دج",
      category: "SUV عائلية",
      range: "راحة ومساحة ممتازة",
      image:
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
    },
    {
      name: "MG 5",
      price: "ابتداءً من 3,780,000 دج",
      category: "سيدان",
      range: "أنيقة ومناسبة للاستخدام اليومي",
      image:
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",
    },
  ];

  const services = [
    "استيراد ووساطة في شراء السيارات الصينية الجديدة",
    "مرافقة كاملة في إجراءات الطلب والتسجيل",
    "اقتراحات حسب الميزانية والاستعمال",
    "توفير عروض خاصة للتجار والأفراد",
  ];

  const steps = [
    {
      title: "اختر السيارة",
      text: "تصفح التشكيلة وحدد السيارة المناسبة لميزانيتك واحتياجك.",
    },
    {
      title: "اطلب الاستشارة",
      text: "تواصل معنا للحصول على عرض سعر مفصل وخيارات الشحن والتسليم.",
    },
    {
      title: "نرافقك حتى الاستلام",
      text: "نساعدك في جميع مراحل الوساطة، من الطلب إلى التسليم في الجزائر.",
    },
  ];

  const stats = [
    { value: "+250", label: "طلب استشارة" },
    { value: "+40", label: "موديل متاح للطلب" },
    { value: "48 ولاية", label: "خدمة عبر الجزائر" },
    { value: "100%", label: "مرافقة شخصية" },
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900" dir="rtl">
      <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-2xl font-black tracking-tight">Drivewaydz</h1>
            <p className="text-sm text-slate-500">وسيط شراء السيارات الصينية في الجزائر</p>
          </div>
          <nav className="hidden items-center gap-6 md:flex">
            <a href="#cars" className="text-sm font-medium hover:text-slate-600">السيارات</a>
            <a href="#services" className="text-sm font-medium hover:text-slate-600">الخدمات</a>
            <a href="#steps" className="text-sm font-medium hover:text-slate-600">كيف نعمل</a>
            <a href="#contact" className="rounded-full bg-slate-900 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:scale-[1.02]">اطلب سيارة الآن</a>
          </nav>
        </div>
      </header>

      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-100 via-white to-slate-200" />
        <div className="relative mx-auto grid max-w-7xl gap-10 px-6 py-16 md:grid-cols-2 md:items-center md:py-24">
          <div className="space-y-6">
            <span className="inline-flex rounded-full border border-slate-300 bg-white px-4 py-1 text-sm font-medium text-slate-700 shadow-sm">
             "سيارات صينية جديدة - عروض موجهة للسوق الجزائري"
            <div className="space-y-4">
              <h2 className="text-4xl font-black leading-tight md:text-6xl">
                اشترِ سيارتك الصينية بسهولة مع <span className="text-slate-600">Drivewaydz</span>
              </h2>
              <p className="max-w-xl text-lg leading-8 text-slate-600">
                منصة وسيط بيع سيارات في الجزائر تساعدك على اختيار، طلب، ومتابعة شراء السيارات الصينية المناسبة لك بأفضل قيمة وخدمة مرافقة احترافية.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <a href="#cars" className="rounded-2xl bg-slate-900 px-6 py-3 font-semibold text-white shadow-lg shadow-slate-300 transition hover:-translate-y-0.5">
                تصفح السيارات
              </a>
              <a href="#contact" className="rounded-2xl border border-slate-300 bg-white px-6 py-3 font-semibold text-slate-900 transition hover:bg-slate-100">
                احجز استشارة مجانية
              </a>
            </div>
            <div className="grid grid-cols-2 gap-4 pt-4 md:grid-cols-4">
              {stats.map((item) => (
                <div key={item.label} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                  <div className="text-2xl font-black">{item.value}</div>
                  <div className="mt-1 text-sm text-slate-500">{item.label}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <div className="absolute -inset-3 rounded-[2rem] bg-slate-300/40 blur-2xl" />
            <div className="relative overflow-hidden rounded-[2rem] border border-white/60 bg-white p-3 shadow-2xl">
              <img
                src="https://images.unsplash.com/photo-1502161254066-6c74afbf07aa?auto=format&fit=crop&w=1400&q=80"
                alt="سيارة حديثة"
                className="h-[500px] w-full rounded-[1.5rem] object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      <section id="cars" className="mx-auto max-w-7xl px-6 py-16 md:py-20">
        <div className="mb-10 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-bold text-slate-500">التشكيلة المميزة</p>
            <h3 className="mt-2 text-3xl font-black md:text-4xl">أشهر السيارات الصينية المطلوبة</h3>
          </div>
          <p className="max-w-2xl text-slate-600">
            الأسعار المعروضة توضيحية ويمكن تخصيص الطلب حسب الفئة، التجهيزات، وخيارات التسليم داخل الجزائر.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          {cars.map((car) => (
            <div key={car.name} className="group overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-xl">
              <div className="overflow-hidden">
                <img src={car.image} alt={car.name} className="h-56 w-full object-cover transition duration-500 group-hover:scale-105" />
              </div>
              <div className="space-y-3 p-5">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h4 className="text-xl font-extrabold">{car.name}</h4>
                    <p className="text-sm text-slate-500">{car.category}</p>
                  </div>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-700">متوفر للطلب</span>
                </div>
                <p className="text-sm leading-7 text-slate-600">{car.range}</p>
                <div className="flex items-center justify-between border-t border-slate-100 pt-3">
                  <span className="text-base font-black">{car.price}</span>
                  <a href="#contact" className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
                    اطلب الآن
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section id="services" className="bg-white py-16 md:py-20">
        <div className="mx-auto grid max-w-7xl gap-10 px-6 md:grid-cols-[1.1fr_0.9fr] md:items-center">
          <div>
            <p className="text-sm font-bold text-slate-500">لماذا نحن؟</p>
            <h3 className="mt-2 text-3xl font-black md:text-4xl">خدمة وساطة مصممة للزبون الجزائري</h3>
            <div className="mt-8 grid gap-4">
              {services.map((service) => (
                <div key={service} className="flex items-start gap-3 rounded-2xl border border-slate-200 p-4 shadow-sm">
                  <div className="mt-1 h-3 w-3 rounded-full bg-slate-900" />
                  <p className="text-slate-700">{service}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-[2rem] bg-slate-900 p-8 text-white shadow-2xl">
            <p className="text-sm font-bold text-slate-300">عرض خاص</p>
            <h4 className="mt-3 text-3xl font-black leading-tight">
              استشارة أولية مجانية لاختيار أفضل سيارة حسب ميزانيتك
            </h4>
            <p className="mt-4 leading-8 text-slate-300">
              سواء كنت تبحث عن سيارة اقتصادية، SUV عائلية، أو موديل بتجهيزات عالية، سنقترح عليك الخيارات الأنسب مع شرح كامل للتكلفة والإجراءات.
            </p>
            <a href="#contact" className="mt-8 inline-flex rounded-2xl bg-white px-6 py-3 font-bold text-slate-900 transition hover:-translate-y-0.5">
              ابدأ الطلب الآن
            </a>
          </div>
        </div>
      </section>

      <section id="steps" className="mx-auto max-w-7xl px-6 py-16 md:py-20">
        <div className="mb-10 text-center">
          <p className="text-sm font-bold text-slate-500">كيف نعمل</p>
          <h3 className="mt-2 text-3xl font-black md:text-4xl">ثلاث خطوات فقط</h3>
        </div>
        <div className="grid gap-6 md:grid-cols-3">
          {steps.map((step, index) => (
            <div key={step.title} className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-900 text-lg font-black text-white">
                {index + 1}
              </div>
              <h4 className="mt-5 text-2xl font-extrabold">{step.title}</h4>
              <p className="mt-3 leading-8 text-slate-600">{step.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="contact" className="bg-slate-900 py-16 text-white md:py-20">
        <div className="mx-auto grid max-w-7xl gap-10 px-6 md:grid-cols-[0.9fr_1.1fr] md:items-center">
          <div>
            <p className="text-sm font-bold text-slate-300">تواصل معنا</p>
            <h3 className="mt-2 text-3xl font-black md:text-5xl">اطلب سيارتك اليوم مع Drivewaydz</h3>
            <p className="mt-5 max-w-xl leading-8 text-slate-300">
              أرسل بياناتك وسنعود إليك بعرض مناسب، تفاصيل الطلب، ومدة التسليم المتوقعة إلى الجزائر.
            </p>
            <div className="mt-8 space-y-3 text-slate-200">
              <p>الهاتف: 05 55 55 55 55</p>
              <p>واتساب: 07 77 77 77 77</p>
              <p>البريد: contact@drivewaydz.com</p>
              <p>الجزائر العاصمة، الجزائر</p>
            </div>
          </div>

          <div className="rounded-[2rem] bg-white p-6 text-slate-900 shadow-2xl md:p-8">
            <div className="grid gap-4 md:grid-cols-2">
              <input className="rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 transition focus:border-slate-400" placeholder="الاسم الكامل" />
              <input className="rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 transition focus:border-slate-400" placeholder="رقم الهاتف" />
            </div>
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              <input className="rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 transition focus:border-slate-400" placeholder="الولاية" />
              <input className="rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 transition focus:border-slate-400" placeholder="الموديل المطلوب" />
            </div>
            <textarea className="mt-4 min-h-[140px] w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none transition focus:border-slate-400" placeholder="اكتب طلبك أو ميزانيتك أو نوع السيارة التي تبحث عنها" />
            <button className="mt-4 w-full rounded-2xl bg-slate-900 px-6 py-3 font-bold text-white transition hover:opacity-90">
              إرسال الطلب
            </button>
            <p className="mt-3 text-sm text-slate-500">
              هذه واجهة أولية، ويمكن ربطها لاحقاً بواتساب، نموذج Google، أو قاعدة بيانات.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
