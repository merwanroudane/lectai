"""
لوحة الألوان — لكل صفحة هوية لونية خاصة بها (فاتحة، غير داكنة).
Per-page accent identity. Every accent is a light-safe hue.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Accent:
    """هوية لونية لصفحة واحدة."""

    key: str
    name: str
    strong: str   # اللون الأساسي للعناوين والحدود
    mid: str      # لون متوسط للتدرجات
    soft: str     # خلفية فاتحة جداً للبطاقات
    tint: str     # خلفية أفتح للمناطق الواسعة
    ink: str      # لون نص داكن متناسق مع الهوية


# ترتيب الألوان مقصود: كل صفحة متتالية تختلف بوضوح عن سابقتها
ACCENTS: dict[str, Accent] = {
    "home":        Accent("home", "إنديغو",   "#5B6BE1", "#8C98EC", "#EEF0FD", "#F7F8FE", "#2C3692"),
    "what_is_ai":  Accent("what_is_ai", "سماوي", "#2E9BD6", "#74BEE6", "#E8F5FC", "#F4FAFE", "#15587C"),
    "learning":    Accent("learning", "زمردي", "#17A074", "#5FC2A2", "#E6F7F1", "#F3FBF8", "#0B5B42"),
    "algo_model":  Accent("algo_model", "عنبري", "#E0832A", "#EDAE6E", "#FDF3E3", "#FEF9F1", "#8A4A08"),
    "terminology": Accent("terminology", "بنفسجي", "#8257D8", "#AE8CE7", "#F2ECFD", "#F9F6FE", "#4A2A86"),
    "history":     Accent("history", "وردي",   "#D9527E", "#E88DAA", "#FCEBF2", "#FEF6F9", "#8A2748"),
    "stats_to_ml": Accent("stats_to_ml", "فيروزي", "#11918F", "#5DBAB8", "#E4F4F4", "#F2FAFA", "#07514F"),
    "breiman":     Accent("breiman", "طوبي",  "#D2603A", "#E49579", "#FCEEE8", "#FEF7F4", "#82331A"),
    "taxonomy":    Accent("taxonomy", "أزرق",  "#3B6FD4", "#7E9EE4", "#EAF0FC", "#F5F8FE", "#1D3E82"),
    "disc_gen":    Accent("disc_gen", "أرجواني", "#9B4DCA", "#BE85DD", "#F6ECFB", "#FBF7FD", "#5B2278"),
    "neural":      Accent("neural", "سيان",   "#0E9BA8", "#5CC0C9", "#E3F5F7", "#F2FBFC", "#065860"),
    "llm":         Accent("llm", "ماجنتا",   "#C3449B", "#DA85C1", "#FBEAF5", "#FEF6FB", "#76215C"),
    "apps":        Accent("apps", "أخضر",    "#2E9E4F", "#74C389", "#E9F7EC", "#F4FBF6", "#145C2B"),
    "skills":      Accent("skills", "برتقالي", "#E2762C", "#EEA671", "#FDF0E6", "#FEF8F3", "#8B4009"),
    "math":        Accent("math", "نيلي",     "#6552D0", "#9A8CE2", "#EFECFB", "#F8F6FE", "#372A80"),
    "philosophy":  Accent("philosophy", "خزامى", "#A6508F", "#C389B4", "#F8ECF4", "#FCF7FA", "#632751"),
    "ethics":      Accent("ethics", "قرمزي",  "#D14B4B", "#E38A8A", "#FCEBEB", "#FEF6F6", "#812222"),
    "myths":       Accent("myths", "خردلي",   "#C59A12", "#DCBF5F", "#FBF4E0", "#FEFBF1", "#75590A"),
    "roadmap":     Accent("roadmap", "ورقي",  "#3F9A6A", "#80BF9C", "#EAF6F0", "#F5FBF8", "#1D5B3C"),
    "quiz":        Accent("quiz", "بنفسجي-أزرق", "#5A63D8", "#8E94EA", "#ECEEFC", "#F7F8FE", "#2B3192"),
}

DEFAULT = ACCENTS["home"]


def get(key: str) -> Accent:
    return ACCENTS.get(key, DEFAULT)


# ألوان دلالية مشتركة تُستخدم في البطاقات والتنبيهات
SEMANTIC = {
    "info":    ("#2E9BD6", "#E8F5FC", "#15587C"),
    "good":    ("#1F9A63", "#E7F7EF", "#0C5739"),
    "warn":    ("#E0832A", "#FDF3E3", "#8A4A08"),
    "danger":  ("#D6455F", "#FCEBEF", "#851F32"),
    "neutral": ("#64748B", "#F1F4FA", "#334155"),
    "idea":    ("#8257D8", "#F2ECFD", "#4A2A86"),
}

# لوحة موحدة للرسوم البيانية (Plotly) — متعددة الألوان
CHART_SEQ = [
    "#5B6BE1", "#17A074", "#E0832A", "#D9527E", "#2E9BD6",
    "#8257D8", "#C9A008", "#0E9BA8", "#2E9E4F", "#C3449B",
]

PLOT_BG = "#FFFFFF"
PLOT_GRID = "#E6EBF6"
PLOT_INK = "#1E2749"
PLOT_MUTED = "#64748B"
