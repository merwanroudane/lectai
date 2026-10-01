"""
منصة: مفاهيم الذكاء الاصطناعي للباحثين
من الصفر — وما قبل الصفر

إعداد وتطوير: د. مروان رودان  (Dr Merwan Roudane)

نقطة الدخول: تعريف التنقّل بين الصفحات.
التشغيل:  streamlit run streamlit_app.py
"""
from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="مفاهيم الذكاء الاصطناعي للباحثين",
    page_icon=":material/neurology:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────── تعريف الصفحات ─────────────────────────

P = "app_pages"

pages = {
    "": [
        st.Page(f"{P}/p00_home.py", title="مدخل المنصة",
                icon=":material/home:", default=True),
    ],
    "أولاً · الأرضية المفاهيمية": [
        st.Page(f"{P}/p01_what_is_ai.py", title="ما هو الذكاء الاصطناعي؟",
                icon=":material/neurology:"),
        st.Page(f"{P}/p02_learning.py", title="ما معنى «التعلّم»؟",
                icon=":material/school:"),
        st.Page(f"{P}/p03_algo_model.py", title="الخوارزمية والنموذج والبرنامج",
                icon=":material/function:"),
        st.Page(f"{P}/p04_terminology.py", title="معجم المصطلحات",
                icon=":material/menu_book:"),
    ],
    "ثانياً · الجذور والانتقال": [
        st.Page(f"{P}/p05_history.py", title="تاريخ المفهوم وتطوّره",
                icon=":material/history:"),
        st.Page(f"{P}/p06_stats_to_ml.py", title="من الإحصاء التقليدي إلى تعلّم الآلة",
                icon=":material/compare_arrows:"),
        st.Page(f"{P}/p07_breiman.py", title="ليو بريمان: الثقافتان",
                icon=":material/balance:"),
    ],
    "ثالثاً · الخريطة والأقسام": [
        st.Page(f"{P}/p08_taxonomy.py", title="أقسام الذكاء الاصطناعي وفروعه",
                icon=":material/account_tree:"),
        st.Page(f"{P}/p09_disc_gen.py", title="التمييزي والتوليدي",
                icon=":material/call_split:"),
        st.Page(f"{P}/p10_neural.py", title="الشبكات العصبية والتعلّم العميق",
                icon=":material/hub:"),
        st.Page(f"{P}/p11_llm.py", title="النماذج الكبيرة والذكاء التوليدي",
                icon=":material/forum:"),
    ],
    "رابعاً · التطبيق والتأهيل": [
        st.Page(f"{P}/p12_applications.py", title="التطبيقات في الواقع والبحث",
                icon=":material/public:"),
        st.Page(f"{P}/p13_skills.py", title="المهارات المطلوبة",
                icon=":material/terminal:"),
        st.Page(f"{P}/p14_math.py", title="الأساس الرياضي والإحصائي",
                icon=":material/calculate:"),
    ],
    "خامساً · ما بعد التقنية": [
        st.Page(f"{P}/p15_philosophy.py", title="فلسفة المفهوم",
                icon=":material/psychology:"),
        st.Page(f"{P}/p16_ethics.py", title="الأخلاقيات والقيود والمخاطر",
                icon=":material/gavel:"),
        st.Page(f"{P}/p17_myths.py", title="مغالطات وتصوّرات خاطئة",
                icon=":material/report:"),
    ],
    "سادساً · الخاتمة": [
        st.Page(f"{P}/p18_roadmap.py", title="خطة التعلّم والمصادر",
                icon=":material/map:"),
        st.Page(f"{P}/p19_quiz.py", title="اختبر فهمك",
                icon=":material/quiz:"),
    ],
}

# شعار المنصّة — يُرسم في رأس الشريط الجانبي، فوق قائمة التنقّل
st.logo("assets/logo.svg", size="large")

page = st.navigation(pages, position="sidebar")

# ──────────────── تذييل الشريط الجانبي (بعد التنقّل) ────────────────

with st.sidebar:
    st.html(
        """
<div dir="rtl" style="margin-top:.4rem;padding:.75rem .85rem;background:#FFFFFF;
     border:1px solid #D7DFF4;border-radius:12px;font-family:'Cairo',sans-serif">
  <div style="font-weight:800;color:#2C3692;font-size:.84rem;margin-bottom:.35rem">
    كيف تستفيد من المنصة</div>
  <div style="color:#475569;font-size:.78rem;line-height:1.85">
    اقرأ الصفحات بالترتيب. كل صفحة تنتهي بـ
    <b>خلاصة</b> و<b>جدول مصطلحات</b> و<b>أخطاء شائعة</b>.
    الرسوم التي تحمل شارة <b>&#9654;</b> متحرّكة — شغّلها.
  </div>
</div>

<div dir="rtl" style="margin-top:.7rem;padding:.7rem .85rem;
     background:linear-gradient(135deg,#5B6BE1 0%,#8257D8 55%,#C3449B 100%);
     border-radius:12px;font-family:'Cairo',sans-serif;text-align:center">
  <div style="color:rgba(255,255,255,.88);font-size:.72rem;font-weight:600">
    إعداد وتطوير</div>
  <div style="color:#fff;font-weight:800;font-size:.9rem;margin-top:.15rem">
    د. مروان رودان</div>
  <div style="color:rgba(255,255,255,.82);font-size:.7rem;direction:ltr;
       margin-top:.1rem">Dr Merwan Roudane</div>
</div>
"""
    )

page.run()
