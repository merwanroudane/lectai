"""
ui.py — طبقة العرض المشتركة للمنصة.

تتولى ثلاثة أمور:
  1) تخطيط من اليمين إلى اليسار (RTL) مع شريط جانبي على اليمين.
  2) هوية لونية مختلفة لكل صفحة (ألوان فاتحة متعددة).
  3) قوالب موحّدة للمحتوى حتى يكون العمق متوازناً بين كل الصفحات.

ملاحظة: المحتوى المُمرّر للدوال يُكتب من داخل المشروع فقط،
ويُسمح فيه بوسوم HTML بسيطة مثل <b> و <code> و <br>.
"""
from __future__ import annotations

import html as _html
from typing import Iterable, Sequence

import streamlit as st

from utils.palette import SEMANTIC, Accent, get

# ───────────────────────────────── الثوابت ──────────────────────────────────

DEVELOPER = "د. مروان رودان"
DEVELOPER_LATIN = "Dr Merwan Roudane"
PLATFORM_TITLE = "مفاهيم الذكاء الاصطناعي للباحثين"

FONT_STACK = "'Cairo', 'Segoe UI', Tahoma, sans-serif"
MONO_STACK = "'JetBrains Mono', 'Consolas', monospace"


# ─────────────────────────────── التهيئة و CSS ───────────────────────────────

def _base_css(a: Accent) -> str:
    """CSS أساسي: اتجاه RTL، شريط جانبي يميني، ومتغيّرات لون الصفحة."""
    return """
<style>
/* ===== 1. متغيّرات هوية الصفحة ===== */
:root {
  --acc:      ACC_STRONG;
  --acc-mid:  ACC_MID;
  --acc-soft: ACC_SOFT;
  --acc-tint: ACC_TINT;
  --acc-ink:  ACC_INK;
  --ink:      #1E2749;
  --muted:    #64748B;
  --line:     #E0E6F4;
}

/* ===== 2. تخطيط RTL + الشريط الجانبي على اليمين ===== */
[data-testid="stAppViewContainer"] {
  flex-direction: row-reverse !important;
}
[data-testid="stSidebar"] {
  direction: rtl !important;
  border-left: 1px solid var(--line) !important;
  border-right: none !important;
}
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarNav"] {
  direction: rtl !important;
  text-align: right !important;
}
[data-testid="stSidebarCollapsedControl"] {
  left: auto !important;
  right: 1rem !important;
}
[data-testid="stSidebarCollapseButton"] {
  margin-right: auto !important;
  margin-left: 0 !important;
}
[data-testid="stSidebarResizeHandle"] {
  left: 0 !important;
  right: auto !important;
}

/* ===== 3. اتجاه المحتوى الرئيسي ===== */
[data-testid="stMainBlockContainer"] {
  direction: rtl !important;
  text-align: right !important;
  padding-top: 2.2rem !important;
  max-width: 1180px;
}
[data-testid="stMainBlockContainer"] h1,
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3,
[data-testid="stMainBlockContainer"] h4,
[data-testid="stMainBlockContainer"] h5,
[data-testid="stMainBlockContainer"] h6,
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] li,
[data-testid="stMainBlockContainer"] blockquote {
  direction: rtl;
  text-align: right;
}
[data-testid="stMainBlockContainer"] ul,
[data-testid="stMainBlockContainer"] ol {
  padding-right: 1.4rem;
  padding-left: 0;
}

/* ===== 4. استثناءات: ما يجب أن يبقى من اليسار إلى اليمين ===== */
code, pre, kbd, samp,
[data-testid="stCodeBlock"],
[data-testid="stJson"],
.katex, .katex-display,
[data-testid="stPlotlyChart"], .js-plotly-plot,
[data-testid="stMermaidChart"],
[data-testid="stDataFrame"], [data-testid="stTable"] {
  direction: ltr !important;
}
[data-testid="stMetric"] label,
[data-testid="stMetricLabel"] {
  direction: rtl !important;
  text-align: right !important;
}
.ltr { direction: ltr; display: inline-block; unicode-bidi: isolate; }

/* ===== 5. تنسيق العناوين بلون الصفحة ===== */
[data-testid="stMainBlockContainer"] h2 {
  color: var(--acc-ink);
  border-bottom: 2px solid var(--acc-soft);
  padding-bottom: .4rem;
  margin-top: 2.4rem;
}
[data-testid="stMainBlockContainer"] h3 {
  color: var(--acc);
  margin-top: 1.7rem;
}
[data-testid="stMainBlockContainer"] blockquote {
  border-right: 4px solid var(--acc-mid);
  border-left: none;
  background: var(--acc-tint);
  padding: .7rem 1rem;
  border-radius: 10px;
  color: var(--acc-ink);
}

/* ===== 6. الجداول ===== */
[data-testid="stMainBlockContainer"] table {
  direction: rtl;
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  overflow: hidden;
  border-radius: 12px;
  border: 1px solid var(--line);
  font-size: .95rem;
}
[data-testid="stMainBlockContainer"] thead th {
  background: var(--acc-soft) !important;
  color: var(--acc-ink) !important;
  text-align: right !important;
  font-weight: 700;
  border: none !important;
}
[data-testid="stMainBlockContainer"] tbody td {
  text-align: right !important;
  border-top: 1px solid var(--line) !important;
  vertical-align: top;
}
[data-testid="stMainBlockContainer"] tbody tr:nth-child(even) td {
  background: #FBFCFE;
}

/* ===== 7. التبويبات والموسّعات ===== */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  direction: rtl;
  gap: .25rem;
  flex-wrap: wrap;
}
[data-testid="stExpander"] summary {
  direction: rtl;
  text-align: right;
  font-weight: 600;
}
[data-testid="stExpander"] details {
  border-radius: 12px;
  border-color: var(--line);
}

/* ===== 8. أدوات الإدخال ===== */
[data-testid="stMainBlockContainer"] label,
[data-testid="stWidgetLabel"] {
  direction: rtl !important;
  text-align: right !important;
}
[data-testid="stRadio"] > div,
[data-testid="stCheckbox"] { direction: rtl; }

/* ===== 9. الشريط الجانبي ===== */
[data-testid="stSidebarNav"] span,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li { text-align: right; }

/* ===== 10. تمرير أنيق ===== */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: #CBD5E6; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--acc-mid); }
</style>
""".replace("ACC_STRONG", a.strong).replace("ACC_MID", a.mid).replace(
        "ACC_SOFT", a.soft
    ).replace("ACC_TINT", a.tint).replace("ACC_INK", a.ink)


def boot(page_key: str = "home") -> Accent:
    """
    تُنادى في أول كل صفحة: تضبط الهوية اللونية وتحقن CSS الخاص بالاتجاه.
    تُعيد كائن الهوية اللونية لاستخدامه في الرسوم.
    """
    a = get(page_key)
    st.html(_base_css(a))
    return a


# ──────────────────────────────── مكوّنات العرض ────────────────────────────────

def hero(
    *,
    accent: Accent,
    eyebrow: str,
    title: str,
    lead: str,
    chips: Sequence[str] = (),
    number: str | None = None,
) -> None:
    """ترويسة الصفحة الملوّنة."""
    chip_html = "".join(
        '<span style="background:rgba(255,255,255,.26);'
        'border:1px solid rgba(255,255,255,.4);color:#fff;border-radius:999px;'
        'padding:.26rem .8rem;font-size:.82rem;font-weight:600;'
        'white-space:nowrap">' + c + "</span>"
        for c in chips
    )
    num_html = ""
    if number:
        num_html = (
            '<div style="position:absolute;inset-inline-start:1.4rem;top:1.1rem;'
            'font-size:4.6rem;font-weight:900;color:rgba(255,255,255,.17);'
            'line-height:1;letter-spacing:-2px">' + number + "</div>"
        )
    st.html(
        f"""
<div dir="rtl" style="position:relative;overflow:hidden;
    background:linear-gradient(115deg,{accent.strong} 0%,{accent.mid} 100%);
    border-radius:20px;padding:1.9rem 1.8rem 1.7rem;margin:.2rem 0 1.6rem;
    box-shadow:0 10px 30px -14px {accent.strong}80;font-family:{FONT_STACK}">
  {num_html}
  <div style="position:absolute;inset-inline-end:-40px;bottom:-60px;width:210px;
       height:210px;border-radius:50%;background:rgba(255,255,255,.10)"></div>
  <div style="position:relative">
    <div style="color:rgba(255,255,255,.88);font-size:.86rem;font-weight:700;
         letter-spacing:.5px;margin-bottom:.45rem">{eyebrow}</div>
    <h1 style="color:#fff;margin:0 0 .6rem;font-size:2.1rem;font-weight:900;
        line-height:1.35;text-shadow:0 2px 10px rgba(0,0,0,.12)">{title}</h1>
    <p style="color:rgba(255,255,255,.95);margin:0 0 1rem;font-size:1.04rem;
       line-height:1.95;max-width:75ch">{lead}</p>
    <div style="display:flex;gap:.5rem;flex-wrap:wrap">{chip_html}</div>
  </div>
</div>
"""
    )


def card(
    title: str,
    body: str,
    *,
    accent: Accent | None = None,
    color: str | None = None,
    soft: str | None = None,
    ink: str | None = None,
    icon: str = "",
) -> str:
    """تُعيد HTML لبطاقة واحدة (تُستخدم داخل grid)."""
    c = color or (accent.strong if accent else "#5B6BE1")
    s = soft or (accent.soft if accent else "#EEF0FD")
    k = ink or (accent.ink if accent else "#2C3692")
    ic = ""
    if icon:
        ic = (
            '<div style="font-size:1.45rem;line-height:1;'
            'margin-bottom:.5rem">' + icon + "</div>"
        )
    return f"""
<div style="background:{s};border:1px solid {c}2E;border-inline-start:4px solid {c};
     border-radius:14px;padding:1.05rem 1.1rem;height:100%;font-family:{FONT_STACK}">
  {ic}
  <div style="font-weight:800;color:{k};font-size:1.02rem;margin-bottom:.4rem;
       line-height:1.6">{title}</div>
  <div style="color:#2A3558;font-size:.93rem;line-height:1.85">{body}</div>
</div>
"""


def grid(cards_html: Iterable[str], *, cols: int = 3, gap: str = "0.8rem") -> None:
    """شبكة بطاقات متجاوبة."""
    inner = "".join(cards_html)
    minw = "320px" if cols <= 2 else "240px"
    st.html(
        f"""
<div dir="rtl" style="display:grid;
     grid-template-columns:repeat(auto-fit,minmax({minw},1fr));
     gap:{gap};margin:.5rem 0 1rem">{inner}</div>
"""
    )


_CALLOUT_ICONS = {
    "info": "ℹ︎",
    "good": "✓",
    "warn": "⚠",
    "danger": "✕",
    "neutral": "•",
    "idea": "✦",
}


def callout(kind: str, title: str, body: str) -> None:
    """تنبيه ملوّن: info / good / warn / danger / neutral / idea."""
    c, bg, ink = SEMANTIC.get(kind, SEMANTIC["neutral"])
    icon = _CALLOUT_ICONS.get(kind, "•")
    st.html(
        f"""
<div dir="rtl" style="background:{bg};border:1px solid {c}33;
     border-inline-start:4px solid {c};border-radius:13px;padding:.95rem 1.1rem;
     margin:.9rem 0;font-family:{FONT_STACK}">
  <div style="font-weight:800;color:{ink};margin-bottom:.35rem;font-size:1rem">
    <span style="color:{c};margin-inline-end:.4rem">{icon}</span>{title}
  </div>
  <div style="color:#2A3558;font-size:.94rem;line-height:1.9">{body}</div>
</div>
"""
    )


def quote(text: str, source: str, *, accent: Accent) -> None:
    """اقتباس مُنسّق من مرجع."""
    st.html(
        f"""
<div dir="rtl" style="background:{accent.tint};border:1px solid {accent.strong}26;
     border-radius:15px;padding:1.15rem 1.25rem;margin:1rem 0;
     font-family:{FONT_STACK};position:relative">
  <div style="position:absolute;inset-inline-start:.8rem;top:.2rem;font-size:2.6rem;
       color:{accent.strong}30;font-weight:900;line-height:1">&rdquo;</div>
  <div style="color:{accent.ink};font-size:1rem;line-height:2;font-style:italic;
       padding-inline-start:1.6rem">{text}</div>
  <div style="color:{accent.strong};font-size:.84rem;font-weight:700;margin-top:.6rem;
       padding-inline-start:1.6rem">— {source}</div>
</div>
"""
    )


def term_table(rows: Sequence[tuple[str, str, str]], *, accent: Accent) -> None:
    """
    جدول المصطلحات الموحّد: (العربية، English، التعريف).
    يظهر في كل صفحة حتى يبني الباحث معجمه تدريجياً.
    """
    body = "".join(
        f"""<tr>
  <td style="padding:.62rem .85rem;font-weight:700;color:{accent.ink};
      white-space:nowrap;border-top:1px solid #E6EBF6">{ar}</td>
  <td style="padding:.62rem .85rem;border-top:1px solid #E6EBF6">
      <span class="ltr" style="font-family:{MONO_STACK};font-size:.84rem;
      background:{accent.soft};color:{accent.ink};padding:.16rem .5rem;
      border-radius:6px;font-weight:600">{en}</span></td>
  <td style="padding:.62rem .85rem;color:#2A3558;font-size:.92rem;line-height:1.8;
      border-top:1px solid #E6EBF6">{df}</td>
</tr>"""
        for ar, en, df in rows
    )
    st.html(
        f"""
<div dir="rtl" style="overflow-x:auto;margin:.6rem 0 1.1rem;font-family:{FONT_STACK}">
<table style="width:100%;border-collapse:separate;border-spacing:0;
       border:1px solid #E0E6F4;border-radius:14px;overflow:hidden;background:#fff">
  <thead><tr style="background:{accent.soft}">
    <th style="padding:.7rem .85rem;text-align:right;color:{accent.ink};
        font-weight:800;font-size:.9rem;width:21%">المصطلح</th>
    <th style="padding:.7rem .85rem;text-align:right;color:{accent.ink};
        font-weight:800;font-size:.9rem;width:21%">English</th>
    <th style="padding:.7rem .85rem;text-align:right;color:{accent.ink};
        font-weight:800;font-size:.9rem">الدلالة الدقيقة</th>
  </tr></thead>
  <tbody>{body}</tbody>
</table></div>
"""
    )


def compare(
    left: tuple[str, str, Sequence[str]],
    right: tuple[str, str, Sequence[str]],
) -> None:
    """
    مقارنة عمودين. كل عمود: (العنوان، اللون، قائمة البنود).
    تُستخدم في صفحات مثل «الإحصاء التقليدي مقابل تعلّم الآلة».
    """

    def col(title: str, c: str, items: Sequence[str]) -> str:
        lis = "".join(
            '<li style="margin:.42rem 0;line-height:1.85;color:#2A3558;'
            'font-size:.93rem">' + i + "</li>"
            for i in items
        )
        return f"""
<div style="background:{c}0F;border:1px solid {c}33;border-top:4px solid {c};
     border-radius:14px;padding:1rem 1.1rem">
  <div style="font-weight:800;color:{c};font-size:1.05rem;
       margin-bottom:.6rem">{title}</div>
  <ul style="margin:0;padding-inline-start:1.15rem">{lis}</ul>
</div>"""

    st.html(
        f"""
<div dir="rtl" style="display:grid;
     grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:.9rem;
     margin:.7rem 0 1.1rem;font-family:{FONT_STACK}">
  {col(*left)}{col(*right)}
</div>
"""
    )


def steps(items: Sequence[tuple[str, str]], *, accent: Accent) -> None:
    """خطوات مرقّمة (عنوان، وصف)."""
    chunks = []
    for i, (t, d) in enumerate(items):
        top = "none" if i == 0 else "1px solid #E6EBF6"
        chunks.append(
            f"""
<div style="display:flex;gap:.85rem;align-items:flex-start;padding:.75rem 0;
     border-top:{top}">
  <div style="flex:0 0 auto;width:34px;height:34px;border-radius:50%;
       background:{accent.strong};color:#fff;display:flex;align-items:center;
       justify-content:center;font-weight:800;font-size:.95rem">{i + 1}</div>
  <div>
    <div style="font-weight:800;color:{accent.ink};margin-bottom:.2rem;
         font-size:1rem">{t}</div>
    <div style="color:#2A3558;font-size:.93rem;line-height:1.85">{d}</div>
  </div>
</div>"""
        )
    st.html(
        f"""
<div dir="rtl" style="background:{accent.tint};border:1px solid {accent.strong}26;
     border-radius:15px;padding:.6rem 1.1rem;margin:.7rem 0 1.1rem;
     font-family:{FONT_STACK}">{''.join(chunks)}</div>
"""
    )


def takeaways(items: Sequence[str], *, accent: Accent) -> None:
    """صندوق «الخلاصة» — يظهر في نهاية كل صفحة."""
    lis = "".join(
        '<li style="margin:.5rem 0;line-height:1.9;color:#1F2A4D;'
        'font-size:.96rem">' + t + "</li>"
        for t in items
    )
    st.html(
        f"""
<div dir="rtl" style="background:linear-gradient(135deg,{accent.soft} 0%,#FFFFFF 100%);
     border:1px solid {accent.strong}33;border-radius:17px;padding:1.2rem 1.3rem;
     margin:1.6rem 0 .8rem;font-family:{FONT_STACK}">
  <div style="font-weight:900;color:{accent.ink};font-size:1.12rem;margin-bottom:.5rem;
       display:flex;align-items:center;gap:.5rem">
    <span style="display:inline-flex;width:28px;height:28px;border-radius:8px;
         background:{accent.strong};color:#fff;align-items:center;
         justify-content:center;font-size:.95rem">&#10003;</span>
    خلاصة الصفحة
  </div>
  <ul style="margin:.3rem 0 0;padding-inline-start:1.3rem">{lis}</ul>
</div>
"""
    )


def pitfalls(items: Sequence[tuple[str, str]]) -> None:
    """أخطاء شائعة: (التصوّر الخاطئ، التصحيح)."""
    rows = "".join(
        f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;
     border-top:1px solid #F0DADF">
  <div style="padding:.7rem .9rem;background:#FDF0F2">
    <span style="color:#D6455F;font-weight:800;margin-inline-end:.35rem">&#10007;</span>
    <span style="color:#7A2033;font-size:.93rem;line-height:1.8">{bad}</span></div>
  <div style="padding:.7rem .9rem;background:#EDF8F2">
    <span style="color:#1F9A63;font-weight:800;margin-inline-end:.35rem">&#10003;</span>
    <span style="color:#0C5739;font-size:.93rem;line-height:1.8">{good}</span></div>
</div>"""
        for bad, good in items
    )
    st.html(
        f"""
<div dir="rtl" style="border:1px solid #E6EBF6;border-radius:15px;overflow:hidden;
     margin:.8rem 0 1.1rem;font-family:{FONT_STACK}">
  <div style="display:grid;grid-template-columns:1fr 1fr">
    <div style="padding:.6rem .9rem;background:#FCE7EB;font-weight:800;
         color:#851F32;font-size:.92rem">تصوّر خاطئ شائع</div>
    <div style="padding:.6rem .9rem;background:#E2F5EB;font-weight:800;
         color:#0C5739;font-size:.92rem">التصحيح الدقيق</div>
  </div>
  {rows}
</div>
"""
    )


def sources(items: Sequence[tuple[str, str]], *, accent: Accent) -> None:
    """المصادر: (الوصف، المرجع)."""
    lis = "".join(
        '<li style="margin:.4rem 0;line-height:1.8;color:#2A3558;font-size:.9rem">'
        + txt
        + ' <span class="ltr" style="color:'
        + accent.strong
        + ";font-family:"
        + MONO_STACK
        + ';font-size:.8rem">'
        + ref
        + "</span></li>"
        for txt, ref in items
    )
    st.html(
        f"""
<div dir="rtl" style="background:#FAFBFE;border:1px dashed {accent.strong}40;
     border-radius:14px;padding:.95rem 1.1rem;margin:1rem 0;
     font-family:{FONT_STACK}">
  <div style="font-weight:800;color:{accent.ink};margin-bottom:.35rem;
       font-size:.98rem">المصادر والمراجع لهذه الصفحة</div>
  <ul style="margin:0;padding-inline-start:1.2rem">{lis}</ul>
</div>
"""
    )


def stat_row(items: Sequence[tuple[str, str, str]], *, accent: Accent) -> None:
    """صف أرقام/حقائق: (القيمة، العنوان، التوضيح)."""
    cells = "".join(
        f"""
<div style="background:#fff;border:1px solid {accent.strong}2E;border-radius:14px;
     padding:.9rem 1rem;text-align:center">
  <div class="ltr" style="font-size:1.7rem;font-weight:900;color:{accent.strong};
       line-height:1.2">{v}</div>
  <div style="font-weight:700;color:{accent.ink};font-size:.92rem;
       margin-top:.2rem">{t}</div>
  <div style="color:#64748B;font-size:.82rem;line-height:1.7;
       margin-top:.25rem">{d}</div>
</div>"""
        for v, t, d in items
    )
    st.html(
        f"""
<div dir="rtl" style="display:grid;
     grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.7rem;
     margin:.7rem 0 1.1rem;font-family:{FONT_STACK}">{cells}</div>
"""
    )


def timeline_block(items: Sequence[tuple[str, str, str]], *, accent: Accent) -> None:
    """خط زمني رأسي: (التاريخ، العنوان، الشرح)."""
    rows = "".join(
        f"""
<div style="position:relative;padding-inline-start:1.6rem;padding-bottom:1.05rem">
  <div style="position:absolute;inset-inline-start:-6px;top:.3rem;width:13px;
       height:13px;border-radius:50%;background:{accent.strong};
       box-shadow:0 0 0 4px {accent.soft}"></div>
  <div class="ltr" style="font-family:{MONO_STACK};font-size:.8rem;font-weight:700;
       color:{accent.strong}">{d}</div>
  <div style="font-weight:800;color:{accent.ink};font-size:1rem;
       margin:.12rem 0 .25rem">{t}</div>
  <div style="color:#2A3558;font-size:.93rem;line-height:1.85">{b}</div>
</div>"""
        for d, t, b in items
    )
    st.html(
        f"""
<div dir="rtl" style="border-inline-start:2px solid {accent.soft};
     margin:.8rem .4rem 1.1rem;padding-inline-start:.4rem;
     font-family:{FONT_STACK}">{rows}</div>
"""
    )


def anim_hint(text: str = "اضغط على زر ▶ Play أسفل الرسم لمشاهدة الحركة") -> None:
    """تلميح أن الرسم متحرّك."""
    st.html(
        f"""
<div dir="rtl" style="display:inline-flex;align-items:center;gap:.45rem;
     background:#EEF0FD;border:1px solid #5B6BE133;border-radius:999px;
     padding:.3rem .85rem;margin:.1rem 0 .6rem;font-family:{FONT_STACK};
     font-size:.84rem;color:#2C3692;font-weight:600">
  <span style="color:#5B6BE1">&#9654;</span>{text}</div>
"""
    )


def section_intro(text: str, *, accent: Accent) -> None:
    """فقرة تمهيدية بارزة تحت عنوان قسم."""
    st.html(
        f"""
<div dir="rtl" style="color:{accent.ink};font-size:1.01rem;line-height:2;
     background:{accent.tint};border-radius:12px;padding:.85rem 1.05rem;
     margin:.5rem 0 1rem;font-family:{FONT_STACK};
     border-inline-start:3px solid {accent.mid}">{text}</div>
"""
    )


def page_footer(*, accent: Accent, prev_hint: str = "", next_hint: str = "") -> None:
    """تذييل موحّد مع اعتماد المطوّر."""
    nav = ""
    if prev_hint or next_hint:
        prev_txt = ("السابق: " + prev_hint) if prev_hint else ""
        next_txt = ("التالي: " + next_hint) if next_hint else ""
        nav = f"""
<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;
     margin-bottom:.8rem;font-size:.9rem">
  <div style="color:#64748B">{prev_txt}</div>
  <div style="color:{accent.strong};font-weight:700">{next_txt}</div>
</div>"""
    st.html(
        f"""
<div dir="rtl" style="margin-top:2.2rem;padding-top:1rem;
     border-top:1px solid #E6EBF6;font-family:{FONT_STACK}">
  {nav}
  <div style="text-align:center;color:#8A95AD;font-size:.84rem;line-height:1.9">
    {PLATFORM_TITLE} — إعداد وتطوير
    <b style="color:{accent.strong}">{DEVELOPER}</b>
    <span class="ltr" style="color:#A3ACC2">({DEVELOPER_LATIN})</span>
  </div>
</div>
"""
    )


def esc(s: str) -> str:
    """تهريب نص غير موثوق قبل إدراجه في HTML."""
    return _html.escape(s, quote=True)
