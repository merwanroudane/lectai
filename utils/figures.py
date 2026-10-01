"""
figures.py — كل الرسوم والمخططات والأنيميشن.

قواعد ثابتة في هذا الملف:
  • خلفية فاتحة دائماً، ولوحة ألوان متعددة.
  • التسميات داخل الرسوم بالإنجليزية (المصطلحات تبقى English).
  • الرسوم المتحركة تحتوي زر ▶ Play صريحاً.
"""
from __future__ import annotations

import warnings

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.palette import CHART_SEQ, PLOT_GRID, PLOT_INK, PLOT_MUTED

# موضع RankWarning تغيّر في numpy 2.0 — ندعم الإصدارين معاً
_RANK_WARNING = getattr(
    getattr(np, "exceptions", np), "RankWarning", RuntimeWarning
)

FONT = "Cairo, Segoe UI, sans-serif"
MONO = "JetBrains Mono, monospace"

C = CHART_SEQ  # لوحة الألوان المتعددة


# ───────────────────────────── أدوات مشتركة ─────────────────────────────

def _base(fig: go.Figure, *, h: int = 420, title: str = "", legend: bool = True) -> go.Figure:
    """تنسيق موحّد فاتح لكل الرسوم."""
    fig.update_layout(
        height=h,
        title=dict(
            text=title,
            font=dict(family=FONT, size=15, color=PLOT_INK),
            x=0.5,
            xanchor="center",
        )
        if title
        else None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FCFDFF",
        font=dict(family=FONT, size=12, color=PLOT_INK),
        margin=dict(l=55, r=25, t=55 if title else 28, b=50),
        showlegend=legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,.75)",
            bordercolor=PLOT_GRID,
            borderwidth=1,
            font=dict(size=11),
        ),
        hoverlabel=dict(font=dict(family=FONT, size=12), bgcolor="white"),
    )
    fig.update_xaxes(
        gridcolor=PLOT_GRID,
        zerolinecolor="#D5DCEF",
        linecolor=PLOT_GRID,
        title_font=dict(size=12, color=PLOT_MUTED),
        tickfont=dict(size=11, color=PLOT_MUTED),
    )
    fig.update_yaxes(
        gridcolor=PLOT_GRID,
        zerolinecolor="#D5DCEF",
        linecolor=PLOT_GRID,
        title_font=dict(size=12, color=PLOT_MUTED),
        tickfont=dict(size=11, color=PLOT_MUTED),
    )
    return fig


def _play(
    fig: go.Figure,
    *,
    frame_ms: int = 420,
    slider_prefix: str = "step: ",
    labels: list[str] | None = None,
) -> go.Figure:
    """يضيف زر Play/Pause ومنزلقاً لرسم يحتوي frames."""
    names = labels or [f.name for f in fig.frames]
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                showactive=False,
                x=0.0,
                xanchor="left",
                y=-0.17,
                yanchor="top",
                pad=dict(t=6, r=6),
                bgcolor="#FFFFFF",
                bordercolor="#C9D2E8",
                borderwidth=1,
                font=dict(family=FONT, size=12, color="#2C3692"),
                buttons=[
                    dict(
                        label="▶  Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=frame_ms, redraw=True),
                                fromcurrent=True,
                                transition=dict(duration=140, easing="cubic-in-out"),
                                mode="immediate",
                            ),
                        ],
                    ),
                    dict(
                        label="❙❙  Pause",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=False),
                                mode="immediate",
                                transition=dict(duration=0),
                            ),
                        ],
                    ),
                ],
            )
        ],
        sliders=[
            dict(
                active=0,
                x=0.14,
                len=0.86,
                y=-0.14,
                yanchor="top",
                pad=dict(t=8, b=6),
                currentvalue=dict(
                    prefix=slider_prefix,
                    font=dict(family=MONO, size=12, color="#2C3692"),
                    visible=True,
                    xanchor="right",
                ),
                bgcolor="#E6EBF6",
                activebgcolor="#5B6BE1",
                bordercolor="#C9D2E8",
                tickcolor="#C9D2E8",
                font=dict(family=MONO, size=10),
                steps=[
                    dict(
                        label=n,
                        method="animate",
                        args=[
                            [n],
                            dict(
                                frame=dict(duration=frame_ms, redraw=True),
                                mode="immediate",
                                transition=dict(duration=140),
                            ),
                        ],
                    )
                    for n in names
                ],
            )
        ],
    )
    fig.update_layout(margin=dict(l=55, r=25, t=55, b=110))
    return fig


# ═════════════════════════ 1. خريطة المجالات ═════════════════════════

@st.cache_data(show_spinner=False)
def nested_fields() -> go.Figure:
    """AI ⊃ ML ⊃ Representation Learning ⊃ Deep Learning — دوائر متداخلة."""
    fig = go.Figure()
    rings = [
        (0.0, 0.0, 4.6, "#5B6BE1", "Artificial Intelligence (AI)", 0.09),
        (0.25, -0.25, 3.5, "#17A074", "Machine Learning (ML)", 0.12),
        (0.45, -0.45, 2.45, "#E0832A", "Representation Learning", 0.15),
        (0.6, -0.6, 1.45, "#D9527E", "Deep Learning (DL)", 0.2),
    ]
    for cx, cy, r, col, label, alpha in rings:
        fig.add_shape(
            type="circle",
            x0=cx - r, y0=cy - r, x1=cx + r, y1=cy + r,
            line=dict(color=col, width=2.5),
            fillcolor=col,
            opacity=alpha,
            layer="below",
        )
        fig.add_annotation(
            x=cx, y=cy + r - 0.33,
            text=f"<b>{label}</b>",
            showarrow=False,
            font=dict(family=FONT, size=12, color=col),
        )

    examples = [
        (-3.0, 2.6, "Rule-based<br>Expert Systems", "#5B6BE1"),
        (-2.3, -2.5, "SVM · Random Forest<br>Linear/Logistic models", "#17A074"),
        (2.6, 1.9, "PCA · Autoencoders<br>Embeddings", "#E0832A"),
        (0.6, -0.6, "CNN · RNN<br>Transformers", "#D9527E"),
    ]
    for x, y, t, col in examples:
        fig.add_annotation(
            x=x, y=y, text=t, showarrow=False,
            font=dict(family=FONT, size=10, color=col),
            bgcolor="rgba(255,255,255,.82)",
            bordercolor=col, borderwidth=1, borderpad=4,
        )

    fig.update_xaxes(range=[-5.4, 5.4], visible=False)
    fig.update_yaxes(range=[-5.4, 5.0], visible=False, scaleanchor="x")
    return _base(fig, h=520, legend=False)


@st.cache_data(show_spinner=False)
def fields_overlap() -> go.Figure:
    """تداخل: Statistics · Computer Science · Domain Knowledge → Data Science."""
    fig = go.Figure()
    sets = [
        (-0.85, 0.5, "#5B6BE1", "Statistics &<br>Mathematics"),
        (0.85, 0.5, "#17A074", "Computer Science<br>& Engineering"),
        (0.0, -0.95, "#E0832A", "Domain<br>Knowledge"),
    ]
    r = 1.55
    for cx, cy, col, label in sets:
        fig.add_shape(
            type="circle",
            x0=cx - r, y0=cy - r, x1=cx + r, y1=cy + r,
            line=dict(color=col, width=2.5),
            fillcolor=col, opacity=0.17, layer="below",
        )
        ly = cy + (r - 0.15) if cy > 0 else cy - (r - 0.15)
        fig.add_annotation(
            x=cx * 1.42, y=ly, text=f"<b>{label}</b>", showarrow=False,
            font=dict(family=FONT, size=11, color=col),
        )
    fig.add_annotation(
        x=0, y=0.02, text="<b>Data Science</b><br><i>AI / ML</i>",
        showarrow=False,
        font=dict(family=FONT, size=13, color="#2C3692"),
        bgcolor="rgba(255,255,255,.88)",
        bordercolor="#5B6BE1", borderwidth=1.5, borderpad=5,
    )
    pairs = [
        (0.0, 1.22, "Machine<br>Learning", "#334155"),
        (-1.25, -0.5, "Classical<br>Statistics", "#334155"),
        (1.25, -0.5, "Software /<br>Data Eng.", "#334155"),
    ]
    for x, y, t, col in pairs:
        fig.add_annotation(
            x=x, y=y, text=t, showarrow=False,
            font=dict(family=FONT, size=9.5, color=col),
        )
    fig.update_xaxes(range=[-3.6, 3.6], visible=False)
    fig.update_yaxes(range=[-3.1, 2.6], visible=False, scaleanchor="x")
    return _base(fig, h=470, legend=False)


# ═════════════════════════ 2. مفهوم التعلّم ═════════════════════════

@st.cache_data(show_spinner=False)
def gradient_descent_anim(lr: float = 0.18, n_steps: int = 26) -> go.Figure:
    """
    أنيميشن: الخوارزمية «تتعلّم» = تنزل منحدر دالة الخسارة.
    Loss curve + the parameter sliding to the minimum.
    """
    w = np.linspace(-3.2, 3.2, 400)
    loss = 0.6 * w**2 + 0.25 * np.sin(3 * w) + 1.0

    def dloss(x: float) -> float:
        return 1.2 * x + 0.75 * np.cos(3 * x)

    path_w, cur = [], -2.85
    for _ in range(n_steps):
        path_w.append(cur)
        cur = cur - lr * dloss(cur)
    path_w = np.array(path_w)
    path_l = 0.6 * path_w**2 + 0.25 * np.sin(3 * path_w) + 1.0

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=w, y=loss, mode="lines", name="Loss function  L(w)",
            line=dict(color="#5B6BE1", width=3),
            fill="tozeroy", fillcolor="rgba(91,107,225,.09)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[path_w[0]], y=[path_l[0]], mode="lines+markers",
            name="Descent path",
            line=dict(color="#E0832A", width=2.2, dash="dot"),
            marker=dict(size=7, color="#E0832A"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[path_w[0]], y=[path_l[0]], mode="markers",
            name="Current parameter  w",
            marker=dict(
                size=19, color="#D9527E",
                line=dict(color="white", width=2.5), symbol="circle",
            ),
        )
    )

    frames = []
    for i in range(1, n_steps + 1):
        frames.append(
            go.Frame(
                name=f"{i}",
                data=[
                    go.Scatter(x=w, y=loss),
                    go.Scatter(x=path_w[:i], y=path_l[:i]),
                    go.Scatter(x=[path_w[i - 1]], y=[path_l[i - 1]]),
                ],
                layout=go.Layout(
                    annotations=[
                        dict(
                            x=0.02, y=0.97, xref="paper", yref="paper",
                            xanchor="left",
                            text=(
                                f"<b>iteration</b> = {i}<br>"
                                f"<b>w</b> = {path_w[i-1]:+.4f}<br>"
                                f"<b>L(w)</b> = {path_l[i-1]:.4f}"
                            ),
                            showarrow=False, align="left",
                            font=dict(family=MONO, size=11, color="#2C3692"),
                            bgcolor="rgba(255,255,255,.92)",
                            bordercolor="#5B6BE1", borderwidth=1, borderpad=6,
                        )
                    ]
                ),
            )
        )
    fig.frames = frames
    fig.add_annotation(
        x=0.02, y=0.97, xref="paper", yref="paper", xanchor="left",
        text="<b>iteration</b> = 0<br>اضغط Play", showarrow=False, align="left",
        font=dict(family=MONO, size=11, color="#2C3692"),
        bgcolor="rgba(255,255,255,.92)",
        bordercolor="#5B6BE1", borderwidth=1, borderpad=6,
    )
    fig.update_xaxes(title="parameter  w", range=[-3.3, 3.3])
    fig.update_yaxes(title="Loss  L(w)", range=[0, 7.2])
    _base(fig, h=460, title="Gradient Descent — كيف «تتعلّم» الخوارزمية فعلياً")
    return _play(fig, frame_ms=300, slider_prefix="iteration: ")


@st.cache_data(show_spinner=False)
def loss_surface_3d() -> go.Figure:
    """سطح الخسارة ثلاثي الأبعاد مع مسار النزول."""
    g = np.linspace(-3, 3, 70)
    X, Y = np.meshgrid(g, g)
    Z = 0.45 * X**2 + 0.9 * Y**2 + 0.6 * np.sin(1.6 * X) * np.cos(1.6 * Y) + 1.4

    px, py, lr = [-2.6], [2.4], 0.11
    for _ in range(34):
        x0, y0 = px[-1], py[-1]
        gx = 0.9 * x0 + 0.96 * np.cos(1.6 * x0) * np.cos(1.6 * y0)
        gy = 1.8 * y0 - 0.96 * np.sin(1.6 * x0) * np.sin(1.6 * y0)
        px.append(x0 - lr * gx)
        py.append(y0 - lr * gy)
    px, py = np.array(px), np.array(py)
    pz = (
        0.45 * px**2 + 0.9 * py**2
        + 0.6 * np.sin(1.6 * px) * np.cos(1.6 * py) + 1.4 + 0.12
    )

    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=g, y=g, z=Z, colorscale="Blues_r", opacity=0.9,
            showscale=False, contours=dict(
                z=dict(show=True, usecolormap=True, project_z=True, width=1)
            ),
            name="Loss surface",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=px, y=py, z=pz, mode="lines+markers",
            line=dict(color="#D9527E", width=6),
            marker=dict(size=3.4, color="#E0832A"),
            name="Optimization path",
        )
    )
    fig.update_layout(
        height=520,
        scene=dict(
            xaxis=dict(title="w₁", backgroundcolor="#FCFDFF",
                       gridcolor=PLOT_GRID, color=PLOT_MUTED),
            yaxis=dict(title="w₂", backgroundcolor="#FCFDFF",
                       gridcolor=PLOT_GRID, color=PLOT_MUTED),
            zaxis=dict(title="Loss", backgroundcolor="#FCFDFF",
                       gridcolor=PLOT_GRID, color=PLOT_MUTED),
            camera=dict(eye=dict(x=1.65, y=1.5, z=1.1)),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=11, color=PLOT_INK),
        margin=dict(l=0, r=0, t=42, b=0),
        title=dict(
            text="Loss Surface — فضاء المعاملات الذي تبحث فيه الخوارزمية",
            x=0.5, xanchor="center",
            font=dict(family=FONT, size=15, color=PLOT_INK),
        ),
        legend=dict(orientation="h", y=0.98, x=1, xanchor="right"),
    )
    return fig


@st.cache_data(show_spinner=False)
def overfitting_anim() -> go.Figure:
    """أنيميشن: زيادة تعقيد النموذج → من Underfitting إلى Overfitting."""
    rng = np.random.default_rng(7)
    n = 26
    x = np.sort(rng.uniform(0, 1, n))
    true = lambda t: np.sin(2 * np.pi * t) * 0.9  # noqa: E731
    y = true(x) + rng.normal(0, 0.22, n)

    xs = np.linspace(0, 1, 300)
    xt = np.sort(rng.uniform(0, 1, 40))
    yt = true(xt) + rng.normal(0, 0.22, 40)

    degrees = [1, 2, 3, 4, 6, 9, 12, 16, 20]
    fits, tr_err, te_err = {}, [], []
    # الدرجات العالية سيّئة التكييف عمداً — هذا هو بيت القصيد في الرسم،
    # فنكتم تحذير numpy حتى لا يُلوّث سجلّ التشغيل.
    with warnings.catch_warnings():
        # numpy ≥ 2.0 ينقل RankWarning إلى np.exceptions
        warnings.simplefilter("ignore", _RANK_WARNING)
        _fit = lambda d: np.polyfit(x, y, d)  # noqa: E731
        coefs = {d: _fit(d) for d in degrees}
    for d in degrees:
        co = coefs[d]
        fits[d] = np.polyval(co, xs)
        tr_err.append(float(np.mean((np.polyval(co, x) - y) ** 2)))
        te_err.append(float(np.mean((np.polyval(co, xt) - yt) ** 2)))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs, y=true(xs), mode="lines", name="True function  f(x)",
            line=dict(color="#17A074", width=2.6, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode="markers", name="Training data",
            marker=dict(size=10, color="#5B6BE1",
                        line=dict(color="white", width=1.6)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=xs, y=fits[degrees[0]], mode="lines", name="Fitted model",
            line=dict(color="#D9527E", width=3.4),
        )
    )

    frames = []
    for i, d in enumerate(degrees):
        if te_err[i] > te_err[max(0, i - 1)] and d >= 9:
            verdict, vcol = "Overfitting — حفظ الضجيج", "#D6455F"
        elif d <= 2:
            verdict, vcol = "Underfitting — النموذج أبسط من الظاهرة", "#E0832A"
        else:
            verdict, vcol = "Good fit — توازن مقبول", "#1F9A63"
        frames.append(
            go.Frame(
                name=f"{d}",
                data=[
                    go.Scatter(x=xs, y=true(xs)),
                    go.Scatter(x=x, y=y),
                    go.Scatter(x=xs, y=fits[d], line=dict(color=vcol)),
                ],
                layout=go.Layout(
                    annotations=[
                        dict(
                            x=0.02, y=0.04, xref="paper", yref="paper",
                            xanchor="left", yanchor="bottom",
                            text=(
                                f"<b>polynomial degree</b> = {d}<br>"
                                f"<b>Train MSE</b> = {tr_err[i]:.4f}<br>"
                                f"<b>Test  MSE</b> = {te_err[i]:.4f}<br>"
                                f"<b>{verdict}</b>"
                            ),
                            showarrow=False, align="left",
                            font=dict(family=MONO, size=11, color=vcol),
                            bgcolor="rgba(255,255,255,.93)",
                            bordercolor=vcol, borderwidth=1.4, borderpad=6,
                        )
                    ]
                ),
            )
        )
    fig.frames = frames
    fig.update_xaxes(title="x", range=[-0.03, 1.03])
    fig.update_yaxes(title="y", range=[-1.9, 1.9])
    _base(fig, h=470,
          title="Model Complexity — من Underfitting إلى Overfitting")
    return _play(fig, frame_ms=750, slider_prefix="degree: ")


@st.cache_data(show_spinner=False)
def bias_variance_curve() -> go.Figure:
    """منحنى المقايضة Bias–Variance مع منطقة التعقيد الأمثل."""
    c = np.linspace(0.4, 10, 300)
    bias2 = 7.2 / (c**1.45) + 0.18
    var = 0.055 * c**1.55
    noise = np.full_like(c, 0.42)
    total = bias2 + var + noise
    opt = float(c[int(np.argmin(total))])

    fig = go.Figure()
    for y, nm, col, dash in [
        (bias2, "Bias²  (التحيّز)", "#E0832A", "dash"),
        (var, "Variance  (التباين)", "#5B6BE1", "dash"),
        (noise, "Irreducible noise  (ضجيج لا يُختزل)", "#94A3B8", "dot"),
    ]:
        fig.add_trace(
            go.Scatter(x=c, y=y, mode="lines", name=nm,
                       line=dict(color=col, width=2.4, dash=dash))
        )
    fig.add_trace(
        go.Scatter(
            x=c, y=total, mode="lines", name="Total expected error",
            line=dict(color="#D9527E", width=4),
            fill="tozeroy", fillcolor="rgba(217,82,126,.07)",
        )
    )
    fig.add_vline(
        x=opt, line=dict(color="#17A074", width=2.4, dash="dashdot"),
        annotation_text="optimal complexity", annotation_position="top",
        annotation_font=dict(family=FONT, size=11, color="#0B5B42"),
    )
    fig.add_annotation(
        x=1.35, y=5.6, text="Underfitting<br><i>بسيط جداً</i>", showarrow=False,
        font=dict(family=FONT, size=11, color="#8A4A08"),
        bgcolor="#FDF3E3", bordercolor="#E0832A", borderwidth=1, borderpad=5,
    )
    fig.add_annotation(
        x=8.7, y=5.6, text="Overfitting<br><i>معقّد جداً</i>", showarrow=False,
        font=dict(family=FONT, size=11, color="#2C3692"),
        bgcolor="#EEF0FD", bordercolor="#5B6BE1", borderwidth=1, borderpad=5,
    )
    fig.update_xaxes(title="Model complexity  →")
    fig.update_yaxes(title="Expected prediction error", range=[0, 7])
    return _base(fig, h=440,
                 title="Bias–Variance Tradeoff — المقايضة المركزية في التعلّم")


@st.cache_data(show_spinner=False)
def learning_curve_anim() -> go.Figure:
    """أنيميشن: أثر حجم البيانات على الأداء (Learning Curve)."""
    n = np.arange(10, 1010, 20)
    train = 0.055 + 0.30 * np.exp(-n / 110)
    valid = 0.055 + 1.35 * np.exp(-n / 165) + 0.03

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=[n[0]], y=[train[0]], mode="lines", name="Training error",
                   line=dict(color="#17A074", width=3.2))
    )
    fig.add_trace(
        go.Scatter(x=[n[0]], y=[valid[0]], mode="lines", name="Validation error",
                   line=dict(color="#D9527E", width=3.2))
    )
    fig.add_trace(
        go.Scatter(
            x=[n[0], n[0]], y=[train[0], valid[0]], mode="lines",
            name="Generalization gap",
            line=dict(color="#8257D8", width=2, dash="dot"),
        )
    )
    frames = []
    for i in range(2, len(n) + 1):
        gap = valid[i - 1] - train[i - 1]
        frames.append(
            go.Frame(
                name=f"{n[i-1]}",
                data=[
                    go.Scatter(x=n[:i], y=train[:i]),
                    go.Scatter(x=n[:i], y=valid[:i]),
                    go.Scatter(
                        x=[n[i - 1], n[i - 1]],
                        y=[train[i - 1], valid[i - 1]],
                    ),
                ],
                layout=go.Layout(
                    annotations=[
                        dict(
                            x=0.97, y=0.95, xref="paper", yref="paper",
                            xanchor="right",
                            text=(
                                f"<b>n</b> = {n[i-1]}<br>"
                                f"<b>gap</b> = {gap:.4f}"
                            ),
                            showarrow=False, align="left",
                            font=dict(family=MONO, size=11, color="#4A2A86"),
                            bgcolor="rgba(255,255,255,.92)",
                            bordercolor="#8257D8", borderwidth=1, borderpad=6,
                        )
                    ]
                ),
            )
        )
    fig.frames = frames
    fig.update_xaxes(title="Training set size  n")
    fig.update_yaxes(title="Error", range=[0, 1.5])
    _base(fig, h=440, title="Learning Curve — لماذا البيانات أهم من الخوارزمية غالباً")
    return _play(fig, frame_ms=90, slider_prefix="n = ")


@st.cache_data(show_spinner=False)
def regularization_anim() -> go.Figure:
    """أنيميشن: أثر معامل التنظيم λ على شكل النموذج."""
    rng = np.random.default_rng(11)
    x = np.sort(rng.uniform(0, 1, 24))
    y = np.sin(2 * np.pi * x) * 0.9 + rng.normal(0, 0.2, 24)
    xs = np.linspace(0, 1, 250)

    deg = 14
    Phi = np.vander(x, deg + 1, increasing=True)
    Phis = np.vander(xs, deg + 1, increasing=True)
    lambdas = [0.0, 1e-8, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]

    curves, norms = {}, {}
    for lam in lambdas:
        A = Phi.T @ Phi + lam * np.eye(deg + 1)
        wts = np.linalg.solve(A, Phi.T @ y)
        curves[lam] = Phis @ wts
        norms[lam] = float(np.linalg.norm(wts))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=xs, y=np.sin(2 * np.pi * xs) * 0.9, mode="lines",
                   name="True function",
                   line=dict(color="#17A074", width=2.4, dash="dash"))
    )
    fig.add_trace(
        go.Scatter(x=x, y=y, mode="markers", name="Training data",
                   marker=dict(size=10, color="#5B6BE1",
                               line=dict(color="white", width=1.5)))
    )
    fig.add_trace(
        go.Scatter(x=xs, y=curves[lambdas[0]], mode="lines",
                   name="Regularized fit",
                   line=dict(color="#C3449B", width=3.4))
    )
    frames = []
    for lam in lambdas:
        lbl = "0" if lam == 0 else f"{lam:g}"
        frames.append(
            go.Frame(
                name=lbl,
                data=[
                    go.Scatter(x=xs, y=np.sin(2 * np.pi * xs) * 0.9),
                    go.Scatter(x=x, y=y),
                    go.Scatter(x=xs, y=curves[lam]),
                ],
                layout=go.Layout(
                    annotations=[
                        dict(
                            x=0.02, y=0.04, xref="paper", yref="paper",
                            xanchor="left", yanchor="bottom",
                            text=(
                                f"<b>λ</b> = {lbl}<br>"
                                f"<b>‖w‖₂</b> = {norms[lam]:.2f}"
                            ),
                            showarrow=False, align="left",
                            font=dict(family=MONO, size=11, color="#76215C"),
                            bgcolor="rgba(255,255,255,.93)",
                            bordercolor="#C3449B", borderwidth=1.3, borderpad=6,
                        )
                    ]
                ),
            )
        )
    fig.frames = frames
    fig.update_xaxes(title="x", range=[-0.02, 1.02])
    fig.update_yaxes(title="y", range=[-2.2, 2.2])
    _base(fig, h=450,
          title="Regularization — كيف نكبح التعقيد بمعامل واحد λ")
    return _play(fig, frame_ms=800, slider_prefix="λ = ")


# ═════════════════════════ 3. الخوارزمية مقابل النموذج ═════════════════════════

@st.cache_data(show_spinner=False)
def algo_vs_model_flow() -> go.Figure:
    """مخطط: البيانات + الخوارزمية → (التدريب) → النموذج → التنبؤ."""
    fig = go.Figure()
    boxes = [
        (0.5, 3.1, "Data\n(X, y)", "#5B6BE1", "البيانات"),
        (0.5, 1.5, "Algorithm\n(learning procedure)", "#E0832A", "الخوارزمية"),
        (3.2, 2.3, "Training\n(optimization)", "#8257D8", "التدريب"),
        (5.9, 2.3, "Model\n(fitted parameters)", "#17A074", "النموذج"),
        (8.5, 2.3, "Prediction\nŷ = f(x_new)", "#D9527E", "التنبؤ"),
    ]
    for cx, cy, label, col, ar in boxes:
        fig.add_shape(
            type="rect", x0=cx - 0.95, y0=cy - 0.52, x1=cx + 0.95, y1=cy + 0.52,
            line=dict(color=col, width=2.4), fillcolor=col, opacity=0.14,
            layer="below",
        )
        fig.add_annotation(
            x=cx, y=cy + 0.14,
            text="<b>" + label.replace("\n", "<br>") + "</b>",
            showarrow=False, font=dict(family=FONT, size=11, color=col),
        )
        fig.add_annotation(
            x=cx, y=cy - 0.33, text=f"<i>{ar}</i>", showarrow=False,
            font=dict(family=FONT, size=10, color=PLOT_MUTED),
        )

    arrows = [
        (1.48, 3.1, 2.22, 2.5), (1.48, 1.5, 2.22, 2.1),
        (4.18, 2.3, 4.92, 2.3), (6.88, 2.3, 7.52, 2.3),
    ]
    for x0, y0, x1, y1 in arrows:
        fig.add_annotation(
            x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowsize=1.3, arrowwidth=2.2,
            arrowcolor="#64748B", text="",
        )
    fig.add_annotation(
        x=4.55, y=3.35,
        text="<b>الخوارزمية تُشغَّل مرّة واحدة</b><br>algorithm runs once",
        showarrow=False, font=dict(family=FONT, size=10, color="#8A4A08"),
        bgcolor="#FDF3E3", bordercolor="#E0832A", borderwidth=1, borderpad=4,
    )
    fig.add_annotation(
        x=7.4, y=1.2,
        text="<b>النموذج يُستخدم ملايين المرّات</b><br>model is reused",
        showarrow=False, font=dict(family=FONT, size=10, color="#0B5B42"),
        bgcolor="#E6F7F1", bordercolor="#17A074", borderwidth=1, borderpad=4,
    )
    fig.update_xaxes(range=[-0.8, 9.9], visible=False)
    fig.update_yaxes(range=[0.5, 4.0], visible=False)
    return _base(fig, h=380, legend=False)


@st.cache_data(show_spinner=False)
def params_vs_hyperparams() -> go.Figure:
    """مقارنة بصرية: المعاملات تُتعلَّم، المعاملات الفائقة تُختار."""
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=["Learned from data<br>(Parameters)", "Chosen by researcher<br>(Hyperparameters)"],
            x=[100, 0], orientation="h", name="تُقدَّر من البيانات",
            marker=dict(color="#17A074"), width=0.46,
            text=["weights β, w · tree splits · network weights", ""],
            textposition="inside",
            insidetextfont=dict(family=FONT, size=11, color="white"),
        )
    )
    fig.add_trace(
        go.Bar(
            y=["Learned from data<br>(Parameters)", "Chosen by researcher<br>(Hyperparameters)"],
            x=[0, 100], orientation="h", name="تُحدَّد قبل التدريب",
            marker=dict(color="#E0832A"), width=0.46,
            text=["", "learning rate · depth · λ · k · n_estimators"],
            textposition="inside",
            insidetextfont=dict(family=FONT, size=11, color="white"),
        )
    )
    fig.update_layout(barmode="stack")
    fig.update_xaxes(visible=False, range=[0, 103])
    fig.update_yaxes(tickfont=dict(family=FONT, size=11, color=PLOT_INK))
    return _base(fig, h=250,
                 title="Parameters vs Hyperparameters — فرق جوهري يُخطئ فيه الكثير")


# ═════════════════════════ 4. الإحصاء مقابل تعلّم الآلة ═════════════════════════

@st.cache_data(show_spinner=False)
def two_cultures_box() -> go.Figure:
    """الصندوق الأسود لبريمان: x → nature → y، وثقافتان لملئه."""
    fig = go.Figure()

    # صندوق الطبيعة
    fig.add_shape(type="rect", x0=3.6, y0=4.2, x1=6.4, y1=6.0,
                  line=dict(color="#334155", width=2.6),
                  fillcolor="#334155", opacity=0.1)
    fig.add_annotation(x=5.0, y=5.1, text="<b>nature</b><br><i>الطبيعة — مجهولة</i>",
                       showarrow=False,
                       font=dict(family=FONT, size=12, color="#1E2749"))
    for x0, x1, lbl, col in [(1.2, 3.5, "x", "#5B6BE1"), (6.5, 8.8, "y", "#D9527E")]:
        fig.add_annotation(
            x=x1 if lbl == "x" else x1, y=5.1,
            ax=x0, ay=5.1, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowsize=1.4, arrowwidth=2.6,
            arrowcolor=col, text="",
        )
    fig.add_annotation(x=1.0, y=5.1, text="<b>x</b><br><i>المتغيّرات</i>",
                       showarrow=False,
                       font=dict(family=FONT, size=12, color="#5B6BE1"))
    fig.add_annotation(x=9.1, y=5.1, text="<b>y</b><br><i>الاستجابة</i>",
                       showarrow=False,
                       font=dict(family=FONT, size=12, color="#D9527E"))

    # الثقافتان
    cultures = [
        (2.6, 1.9, "#11918F",
         "<b>Data Modeling Culture</b>",
         "linear regression · logistic<br>regression · Cox model",
         "Validation: goodness-of-fit tests",
         "≈ 98% من الإحصائيين"),
        (7.4, 1.9, "#D2603A",
         "<b>Algorithmic Modeling Culture</b>",
         "decision trees · neural nets<br>random forests · SVM",
         "Validation: predictive accuracy",
         "≈ 2% من الإحصائيين"),
    ]
    for cx, cy, col, title, inner, valid, pop in cultures:
        fig.add_shape(type="rect", x0=cx - 2.1, y0=cy - 1.25, x1=cx + 2.1,
                      y1=cy + 1.25, line=dict(color=col, width=2.4),
                      fillcolor=col, opacity=0.1)
        fig.add_annotation(x=cx, y=cy + 0.92, text=title, showarrow=False,
                           font=dict(family=FONT, size=11.5, color=col))
        fig.add_annotation(x=cx, y=cy + 0.33, text=inner, showarrow=False,
                           font=dict(family=MONO, size=9.5, color="#334155"))
        fig.add_annotation(x=cx, y=cy - 0.42, text=f"<i>{valid}</i>",
                           showarrow=False,
                           font=dict(family=FONT, size=9.5, color=PLOT_MUTED))
        fig.add_annotation(x=cx, y=cy - 0.92, text=f"<b>{pop}</b>",
                           showarrow=False,
                           font=dict(family=FONT, size=10, color=col))
        fig.add_annotation(
            x=cx, y=cy + 1.3, ax=5.0, ay=4.15,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=2,
            arrowcolor=col, text="",
        )
    fig.update_xaxes(range=[-0.4, 10.4], visible=False)
    fig.update_yaxes(range=[0.2, 6.9], visible=False)
    return _base(fig, h=470, legend=False)


@st.cache_data(show_spinner=False)
def rashomon_anim() -> go.Figure:
    """
    أنيميشن أثر راشومون: نماذج مختلفة جداً بنفس دقة التنبؤ تقريباً.
    Multiple distinct models, nearly identical error.
    """
    rng = np.random.default_rng(3)
    n = 40
    x1 = rng.normal(0, 1, n)
    x2 = 0.8 * x1 + rng.normal(0, 0.6, n)
    x3 = rng.normal(0, 1, n)
    x4 = 0.7 * x3 + rng.normal(0, 0.7, n)
    y = 1.1 * x1 + 0.9 * x3 + rng.normal(0, 0.45, n)
    X = np.column_stack([x1, x2, x3, x4])
    names = ["x₁", "x₂", "x₃", "x₄"]

    subsets = [(0, 2), (1, 2), (0, 3), (1, 3), (0, 1, 2), (0, 2, 3)]
    models = []
    for s in subsets:
        A = np.column_stack([np.ones(n), X[:, list(s)]])
        beta, *_ = np.linalg.lstsq(A, y, rcond=None)
        resid = y - A @ beta
        rss = float(np.sum(resid**2))
        coefs = {names[k]: float(beta[i + 1]) for i, k in enumerate(s)}
        models.append((s, coefs, rss, A @ beta))
    best = min(m[2] for m in models)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=names, y=[0, 0, 0, 0], name="Estimated coefficient",
               marker=dict(color=C[:4]),
               text=["", "", "", ""], textposition="outside",
               textfont=dict(family=MONO, size=11))
    )
    frames = []
    for i, (s, coefs, rss, _) in enumerate(models):
        vals = [coefs.get(nm, 0.0) for nm in names]
        txt = [f"{v:+.2f}" if v != 0 else "—" for v in vals]
        pct = 100 * (rss - best) / best
        used = " + ".join(names[k] for k in s)
        frames.append(
            go.Frame(
                name=f"M{i+1}",
                data=[go.Bar(x=names, y=vals, text=txt,
                             marker=dict(color=C[:4]))],
                layout=go.Layout(
                    annotations=[
                        dict(
                            x=0.5, y=1.13, xref="paper", yref="paper",
                            xanchor="center",
                            text=(
                                f"<b>Model {i+1}</b>:  y ~ {used}"
                                f"   |   <b>RSS</b> = {rss:.2f}"
                                f"   (+{pct:.1f}% عن الأفضل)"
                            ),
                            showarrow=False,
                            font=dict(family=MONO, size=11.5, color="#82331A"),
                            bgcolor="#FCEEE8", bordercolor="#D2603A",
                            borderwidth=1.2, borderpad=6,
                        )
                    ]
                ),
            )
        )
    fig.frames = frames
    fig.add_hline(y=0, line=dict(color="#94A3B8", width=1.4))
    fig.update_xaxes(title="predictor", tickfont=dict(size=14))
    fig.update_yaxes(title="coefficient value", range=[-0.5, 2.1])
    _base(fig, h=430,
          title="Rashomon Effect — نماذج مختلفة، دقّة واحدة، قصص متناقضة")
    return _play(fig, frame_ms=1100, slider_prefix="model: ")


@st.cache_data(show_spinner=False)
def prediction_vs_inference() -> go.Figure:
    """هدفان مختلفان: Prediction مقابل Inference/Information."""
    fig = go.Figure()
    axes = [
        ("Prediction\n(التنبؤ)", "#5B6BE1",
         ["ŷ accurate on new data", "out-of-sample error", "black box is fine",
          "cross-validation", "Kaggle / production"]),
        ("Inference\n(الاستنتاج)", "#17A074",
         ["β interpretable", "standard errors & CIs", "model must be correct",
          "hypothesis tests", "journals / policy"]),
        ("Causality\n(السببية)", "#E0832A",
         ["effect of intervention", "counterfactuals", "identification strategy",
          "RCT / IV / DiD", "treatment effects"]),
    ]
    for i, (title, col, items) in enumerate(axes):
        x0 = i * 3.4
        fig.add_shape(type="rect", x0=x0, y0=0.3, x1=x0 + 3.0, y1=5.6,
                      line=dict(color=col, width=2.4), fillcolor=col,
                      opacity=0.09, layer="below")
        fig.add_annotation(
            x=x0 + 1.5, y=5.15,
            text="<b>" + title.replace("\n", "<br>") + "</b>",
            showarrow=False, font=dict(family=FONT, size=12.5, color=col),
        )
        for j, it in enumerate(items):
            fig.add_annotation(
                x=x0 + 1.5, y=4.25 - j * 0.72, text=it, showarrow=False,
                font=dict(family=MONO, size=9.6, color="#334155"),
                bgcolor="rgba(255,255,255,.8)", borderpad=3,
            )
    fig.update_xaxes(range=[-0.3, 10.1], visible=False)
    fig.update_yaxes(range=[0, 6.0], visible=False)
    return _base(fig, h=400, legend=False)


@st.cache_data(show_spinner=False)
def in_vs_out_sample() -> go.Figure:
    """الفرق بين الملاءمة داخل العيّنة والأداء خارجها."""
    rng = np.random.default_rng(5)
    x = np.sort(rng.uniform(0, 10, 30))
    y = 1.6 + 0.55 * x + rng.normal(0, 1.1, 30)
    xs = np.linspace(-0.4, 13.5, 200)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # الدرجة 11 مقصودة للتوضيح
        lin = np.polyfit(x, y, 1)
        hi = np.polyfit(x, y, 11)

    fig = go.Figure()
    fig.add_vrect(x0=-0.4, x1=10, fillcolor="#5B6BE1", opacity=0.05,
                  line_width=0, annotation_text="in-sample  (داخل العيّنة)",
                  annotation_position="top left",
                  annotation_font=dict(family=FONT, size=11, color="#2C3692"))
    fig.add_vrect(x0=10, x1=13.5, fillcolor="#D9527E", opacity=0.07,
                  line_width=0, annotation_text="out-of-sample  (خارج العيّنة)",
                  annotation_position="top right",
                  annotation_font=dict(family=FONT, size=11, color="#8A2748"))
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="Observed data",
                             marker=dict(size=9, color="#334155",
                                         line=dict(color="white", width=1.3))))
    fig.add_trace(go.Scatter(x=xs, y=np.polyval(lin, xs), mode="lines",
                             name="Simple model (degree 1)",
                             line=dict(color="#17A074", width=3)))
    fig.add_trace(go.Scatter(x=xs, y=np.polyval(hi, xs), mode="lines",
                             name="Complex model (degree 11)",
                             line=dict(color="#D9527E", width=3, dash="dash")))
    fig.add_annotation(
        x=12.1, y=-3.0,
        text="النموذج المعقّد يتفوّق داخل العيّنة<br>وينفجر خارجها",
        showarrow=False, font=dict(family=FONT, size=10.5, color="#851F32"),
        bgcolor="#FCEBEF", bordercolor="#D6455F", borderwidth=1, borderpad=5,
    )
    fig.update_xaxes(title="x", range=[-0.4, 13.5])
    fig.update_yaxes(title="y", range=[-6, 16])
    return _base(fig, h=440,
                 title="In-sample Fit ≠ Out-of-sample Performance")


# ═════════════════════════ 5. الأقسام والأنواع ═════════════════════════

@st.cache_data(show_spinner=False)
def supervised_unsupervised_rl() -> go.Figure:
    """ثلاث لوحات: بيانات موسومة، تجميع، وحلقة التعلّم المعزّز."""
    from plotly.subplots import make_subplots

    rng = np.random.default_rng(13)
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=(
            "Supervised — بيانات موسومة (X, y)",
            "Unsupervised — بنية بلا وسوم (X)",
            "Reinforcement — مكافأة من البيئة",
        ),
        horizontal_spacing=0.07,
    )

    a = rng.normal([-1.1, -1.1], 0.62, (34, 2))
    b = rng.normal([1.2, 1.2], 0.62, (34, 2))
    fig.add_trace(go.Scatter(x=a[:, 0], y=a[:, 1], mode="markers",
                             name="class 0", marker=dict(size=8, color="#5B6BE1",
                             line=dict(color="white", width=1))), 1, 1)
    fig.add_trace(go.Scatter(x=b[:, 0], y=b[:, 1], mode="markers",
                             name="class 1", marker=dict(size=8, color="#D9527E",
                             symbol="square", line=dict(color="white", width=1))), 1, 1)
    gx = np.linspace(-3, 3, 10)
    fig.add_trace(go.Scatter(x=gx, y=-gx, mode="lines",
                             name="decision boundary",
                             line=dict(color="#17A074", width=2.6, dash="dash")), 1, 1)

    cl = np.vstack([
        rng.normal([-1.3, 0.9], 0.5, (24, 2)),
        rng.normal([1.4, 1.0], 0.5, (24, 2)),
        rng.normal([0.1, -1.4], 0.5, (24, 2)),
    ])
    fig.add_trace(go.Scatter(x=cl[:, 0], y=cl[:, 1], mode="markers",
                             name="unlabeled points",
                             marker=dict(size=8, color="#64748B",
                             line=dict(color="white", width=1))), 1, 2)
    for cx, cy, col in [(-1.3, 0.9, "#17A074"), (1.4, 1.0, "#E0832A"),
                        (0.1, -1.4, "#8257D8")]:
        fig.add_shape(type="circle", x0=cx - 1.0, y0=cy - 1.0, x1=cx + 1.0,
                      y1=cy + 1.0, line=dict(color=col, width=2.2, dash="dot"),
                      fillcolor=col, opacity=0.09, row=1, col=2)

    loop = [(0.0, 1.2, "Agent", "#5B6BE1"), (0.0, -1.2, "Environment", "#E0832A")]
    for cx, cy, lbl, col in loop:
        fig.add_shape(type="rect", x0=cx - 1.0, y0=cy - 0.42, x1=cx + 1.0,
                      y1=cy + 0.42, line=dict(color=col, width=2.4),
                      fillcolor=col, opacity=0.13, row=1, col=3)
        fig.add_annotation(x=cx, y=cy, text=f"<b>{lbl}</b>", showarrow=False,
                           font=dict(family=FONT, size=11, color=col),
                           row=1, col=3)
    fig.add_annotation(x=1.55, y=0.0, text="action<br><i>aₜ</i>", showarrow=False,
                       font=dict(family=MONO, size=9.5, color="#1F9A63"),
                       row=1, col=3)
    fig.add_annotation(x=-1.55, y=0.0, text="reward rₜ<br>state sₜ",
                       showarrow=False,
                       font=dict(family=MONO, size=9.5, color="#D6455F"),
                       row=1, col=3)
    fig.add_trace(go.Scatter(x=[1.0, 1.0], y=[0.8, -0.8], mode="lines",
                             line=dict(color="#1F9A63", width=2.4),
                             showlegend=False), 1, 3)
    fig.add_trace(go.Scatter(x=[-1.0, -1.0], y=[-0.8, 0.8], mode="lines",
                             line=dict(color="#D6455F", width=2.4),
                             showlegend=False), 1, 3)

    for c in (1, 2, 3):
        fig.update_xaxes(visible=False, row=1, col=c)
        fig.update_yaxes(visible=False, row=1, col=c)
    fig.update_annotations(font=dict(family=FONT, size=11.5, color=PLOT_INK))
    return _base(fig, h=360, legend=False)


@st.cache_data(show_spinner=False)
def disc_vs_gen() -> go.Figure:
    """Discriminative يرسم الحدّ، Generative يصف توزيع كل فئة."""
    from plotly.subplots import make_subplots

    rng = np.random.default_rng(21)
    a = rng.multivariate_normal([-1.15, -0.55], [[0.42, 0.14], [0.14, 0.34]], 90)
    b = rng.multivariate_normal([1.15, 0.65], [[0.40, -0.12], [-0.12, 0.36]], 90)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            "Discriminative — يتعلّم  p(y | x)",
            "Generative — يتعلّم  p(x, y)  ثم يولّد",
        ),
        horizontal_spacing=0.09,
    )
    for cc in (1, 2):
        fig.add_trace(go.Scatter(x=a[:, 0], y=a[:, 1], mode="markers",
                                 name="class A",
                                 marker=dict(size=7, color="#5B6BE1", opacity=0.8,
                                 line=dict(color="white", width=0.7)),
                                 showlegend=(cc == 1)), 1, cc)
        fig.add_trace(go.Scatter(x=b[:, 0], y=b[:, 1], mode="markers",
                                 name="class B",
                                 marker=dict(size=7, color="#D9527E", opacity=0.8,
                                 symbol="square",
                                 line=dict(color="white", width=0.7)),
                                 showlegend=(cc == 1)), 1, cc)

    gx = np.linspace(-3.2, 3.2, 12)
    fig.add_trace(go.Scatter(x=gx, y=-0.95 * gx + 0.05, mode="lines",
                             name="decision boundary",
                             line=dict(color="#17A074", width=3.4)), 1, 1)
    fig.add_annotation(x=0.0, y=-2.5,
                       text="يكفي أن أعرف <b>أين الحدّ</b><br>لا كيف نشأت البيانات",
                       showarrow=False,
                       font=dict(family=FONT, size=10, color="#0B5B42"),
                       bgcolor="#E6F7F1", bordercolor="#17A074",
                       borderwidth=1, borderpad=4, row=1, col=1)

    g = np.linspace(-3.2, 3.2, 90)
    GX, GY = np.meshgrid(g, g)

    def dens(mu, S):
        Si = np.linalg.inv(S)
        d = np.stack([GX - mu[0], GY - mu[1]], -1)
        q = np.einsum("...i,ij,...j", d, Si, d)
        return np.exp(-0.5 * q)

    for mu, S, cs in [
        ([-1.15, -0.55], [[0.42, 0.14], [0.14, 0.34]], "Blues"),
        ([1.15, 0.65], [[0.40, -0.12], [-0.12, 0.36]], "RdPu"),
    ]:
        fig.add_trace(go.Contour(
            x=g, y=g, z=dens(np.array(mu), np.array(S)),
            colorscale=cs, showscale=False, opacity=0.5,
            contours=dict(coloring="lines", start=0.08, end=0.95, size=0.18),
            line=dict(width=2), showlegend=False), 1, 2)
    fig.add_annotation(x=0.0, y=-2.5,
                       text="أعرف <b>توزيع كل فئة</b><br>فأستطيع توليد بيانات جديدة",
                       showarrow=False,
                       font=dict(family=FONT, size=10, color="#76215C"),
                       bgcolor="#FBEAF5", bordercolor="#C3449B",
                       borderwidth=1, borderpad=4, row=1, col=2)

    for cc in (1, 2):
        fig.update_xaxes(title="x₁", range=[-3.2, 3.2], row=1, col=cc)
        fig.update_yaxes(title="x₂", range=[-3.2, 3.2], row=1, col=cc)
    fig.update_annotations(font=dict(family=FONT, size=11.5, color=PLOT_INK))
    return _base(fig, h=420)


@st.cache_data(show_spinner=False)
def clustering_anim() -> go.Figure:
    """أنيميشن k-means: كيف «تكتشف» الخوارزمية البنية بلا وسوم."""
    rng = np.random.default_rng(17)
    pts = np.vstack([
        rng.normal([-1.6, 1.1], 0.46, (40, 2)),
        rng.normal([1.7, 1.3], 0.46, (40, 2)),
        rng.normal([0.1, -1.6], 0.46, (40, 2)),
    ])
    cents = np.array([[-2.6, -2.3], [2.5, -2.4], [-2.4, 2.6]])
    cols = ["#5B6BE1", "#E0832A", "#17A074"]

    history = []
    for _ in range(9):
        d = np.linalg.norm(pts[:, None, :] - cents[None, :, :], axis=2)
        lab = np.argmin(d, axis=1)
        history.append((lab.copy(), cents.copy()))
        for k in range(3):
            if np.any(lab == k):
                cents[k] = pts[lab == k].mean(axis=0)

    fig = go.Figure()
    lab0, c0 = history[0]
    for k in range(3):
        m = lab0 == k
        fig.add_trace(go.Scatter(x=pts[m, 0], y=pts[m, 1], mode="markers",
                                 name=f"cluster {k+1}",
                                 marker=dict(size=8, color=cols[k], opacity=0.78,
                                 line=dict(color="white", width=0.8))))
    fig.add_trace(go.Scatter(x=c0[:, 0], y=c0[:, 1], mode="markers",
                             name="centroids",
                             marker=dict(size=20, color=cols, symbol="x",
                             line=dict(color="#1E2749", width=2.5))))

    frames = []
    for i, (lab, cen) in enumerate(history):
        data = []
        for k in range(3):
            m = lab == k
            data.append(go.Scatter(x=pts[m, 0], y=pts[m, 1]))
        data.append(go.Scatter(x=cen[:, 0], y=cen[:, 1]))
        frames.append(go.Frame(
            name=f"{i+1}", data=data,
            layout=go.Layout(annotations=[dict(
                x=0.02, y=0.97, xref="paper", yref="paper", xanchor="left",
                text=f"<b>iteration</b> = {i+1}", showarrow=False,
                font=dict(family=MONO, size=11, color="#2C3692"),
                bgcolor="rgba(255,255,255,.92)", bordercolor="#5B6BE1",
                borderwidth=1, borderpad=5)])))
    fig.frames = frames
    fig.update_xaxes(title="x₁", range=[-3.4, 3.4])
    fig.update_yaxes(title="x₂", range=[-3.4, 3.4])
    _base(fig, h=440,
          title="k-means — «اكتشاف» بنية بلا أي وسوم مسبقة")
    return _play(fig, frame_ms=850, slider_prefix="iteration: ")


@st.cache_data(show_spinner=False)
def curse_of_dimensionality() -> go.Figure:
    """لعنة الأبعاد: العيّنة المطلوبة تنفجر مع عدد الأبعاد."""
    d = np.arange(1, 16)
    needed = 10.0**d
    frac_edge = 1 - (0.9**d)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=d, y=needed, name="Points needed for same density (10 per axis)",
        marker=dict(color=needed, colorscale="Purples", showscale=False),
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=d, y=frac_edge * 100, mode="lines+markers",
        name="% of volume in the outer 5% shell",
        line=dict(color="#E0832A", width=3.2),
        marker=dict(size=7), yaxis="y2",
    ))
    fig.update_layout(
        yaxis=dict(title="Sample size needed (log)", type="log",
                   gridcolor=PLOT_GRID,
                   title_font=dict(size=11.5, color="#8257D8"),
                   tickfont=dict(size=10.5, color="#8257D8")),
        yaxis2=dict(title="% volume near the boundary", overlaying="y",
                    side="right", range=[0, 100], showgrid=False,
                    title_font=dict(size=11.5, color="#E0832A"),
                    tickfont=dict(size=10.5, color="#E0832A")),
    )
    fig.update_xaxes(title="number of dimensions  d", dtick=1)
    fig.add_annotation(
        x=11, y=np.log10(1e9),
        text="«كل البيانات تصبح بعيدة عن بعضها»<br>everything is far from everything",
        showarrow=False, font=dict(family=FONT, size=10.5, color="#4A2A86"),
        bgcolor="#F2ECFD", bordercolor="#8257D8", borderwidth=1, borderpad=5,
    )
    return _base(fig, h=430,
                 title="Curse of Dimensionality — ولماذا اعتبرها بريمان نعمة أيضاً")


# ═════════════════════════ 6. الشبكات العصبية ═════════════════════════

@st.cache_data(show_spinner=False)
def network_forward_anim() -> go.Figure:
    """أنيميشن: انتشار الإشارة أماماً ثم رجوع الخطأ (Forward / Backward)."""
    layers = [4, 6, 6, 3, 1]
    names = ["Input\nx", "Hidden 1", "Hidden 2", "Hidden 3", "Output\nŷ"]
    cols = ["#5B6BE1", "#17A074", "#0E9BA8", "#8257D8", "#D9527E"]

    pos: list[list[tuple[float, float]]] = []
    for li, k in enumerate(layers):
        ys = np.linspace(-(k - 1) / 2, (k - 1) / 2, k) * 0.95
        pos.append([(li * 2.2, float(v)) for v in ys])

    edges_x, edges_y = [], []
    for li in range(len(layers) - 1):
        for (x0, y0) in pos[li]:
            for (x1, y1) in pos[li + 1]:
                edges_x += [x0, x1, None]
                edges_y += [y0, y1, None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode="lines",
                             line=dict(color="#DCE3F2", width=0.9),
                             hoverinfo="skip", name="weights  w",
                             showlegend=False))
    for li, layer in enumerate(pos):
        xs = [p[0] for p in layer]
        ys = [p[1] for p in layer]
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="markers", name=names[li].replace("\n", " "),
            marker=dict(size=22, color="#FFFFFF",
                        line=dict(color=cols[li], width=2.6)),
            showlegend=False))
        fig.add_annotation(x=li * 2.2, y=3.5,
                           text="<b>" + names[li].replace("\n", "<br>") + "</b>",
                           showarrow=False,
                           font=dict(family=FONT, size=10.5, color=cols[li]))

    # frames: forward highlight then backward highlight
    n_layers = len(layers)
    frames = []
    seq = [("forward", i) for i in range(n_layers)] + \
          [("backward", i) for i in range(n_layers - 1, -1, -1)]
    for step, (phase, idx) in enumerate(seq):
        data = [go.Scatter(x=edges_x, y=edges_y)]
        for li, layer in enumerate(pos):
            if li == idx:
                mk = dict(size=28, color=cols[li],
                          line=dict(color="#1E2749", width=2.4))
            elif (phase == "forward" and li < idx) or \
                 (phase == "backward" and li > idx):
                mk = dict(size=22, color=cols[li], opacity=0.42,
                          line=dict(color=cols[li], width=2))
            else:
                mk = dict(size=22, color="#FFFFFF",
                          line=dict(color=cols[li], width=2.6))
            data.append(go.Scatter(x=[p[0] for p in layer],
                                   y=[p[1] for p in layer], marker=mk))
        if phase == "forward":
            txt = ("<b>Forward pass</b> — الانتشار الأمامي<br>"
                   "كل طبقة تحوّل التمثيل: <i>a = σ(Wx + b)</i>")
            col = "#17A074"
        else:
            txt = ("<b>Backpropagation</b> — انتشار الخطأ عكسياً<br>"
                   "تُحسب المشتقّات وتُعدَّل الأوزان <i>w ← w − η ∂L/∂w</i>")
            col = "#D6455F"
        frames.append(go.Frame(
            name=f"{step+1}", data=data,
            layout=go.Layout(annotations=[
                dict(x=li * 2.2, y=3.5,
                     text="<b>" + names[li].replace("\n", "<br>") + "</b>",
                     showarrow=False,
                     font=dict(family=FONT, size=10.5, color=cols[li]))
                for li in range(n_layers)
            ] + [
                dict(x=0.5, y=-0.1, xref="paper", yref="paper",
                     xanchor="center", text=txt, showarrow=False,
                     font=dict(family=FONT, size=11, color=col),
                     bgcolor="rgba(255,255,255,.95)", bordercolor=col,
                     borderwidth=1.4, borderpad=6)
            ])))
    fig.frames = frames
    fig.update_xaxes(range=[-1.0, 9.8], visible=False)
    fig.update_yaxes(range=[-3.6, 4.1], visible=False)
    _base(fig, h=470, legend=False,
          title="Neural Network — الانتشار الأمامي وتصحيح الخطأ عكسياً")
    return _play(fig, frame_ms=620, slider_prefix="step: ")


@st.cache_data(show_spinner=False)
def representation_layers() -> go.Figure:
    """التعلّم بالتمثيل: كل طبقة تبني ميزات أعلى تجريداً."""
    fig = go.Figure()
    stages = [
        ("Raw input\nبكسلات / كلمات", "#64748B"),
        ("Edges & corners\nحدود وزوايا", "#5B6BE1"),
        ("Textures & parts\nأنسجة وأجزاء", "#0E9BA8"),
        ("Objects\nأشياء كاملة", "#17A074"),
        ("Concepts\nمفاهيم ومعانٍ", "#D9527E"),
    ]
    for i, (lbl, col) in enumerate(stages):
        x = i * 2.15
        h = 1.1 + i * 0.26
        fig.add_shape(type="rect", x0=x, y0=2.6 - h / 2, x1=x + 1.65,
                      y1=2.6 + h / 2, line=dict(color=col, width=2.4),
                      fillcolor=col, opacity=0.14)
        fig.add_annotation(x=x + 0.82, y=2.6,
                           text="<b>" + lbl.replace("\n", "</b><br><i>") + "</i>",
                           showarrow=False,
                           font=dict(family=FONT, size=10, color=col))
        if i < len(stages) - 1:
            fig.add_annotation(x=x + 2.1, y=2.6, ax=x + 1.7, ay=2.6,
                               xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=3, arrowsize=1.3,
                               arrowwidth=2.2, arrowcolor="#94A3B8", text="")
    fig.add_annotation(
        x=5.0, y=0.85,
        text=("<b>Representation Learning</b> — الفكرة الجوهرية للتعلّم العميق:<br>"
              "الآلة لا تتلقّى الميزات جاهزة، بل <b>تبنيها طبقةً بعد طبقة</b>"),
        showarrow=False, font=dict(family=FONT, size=11, color="#065860"),
        bgcolor="#E3F5F7", bordercolor="#0E9BA8", borderwidth=1.3, borderpad=7,
    )
    fig.add_annotation(
        x=5.0, y=4.5,
        text="Feature Engineering (يدوي) ← → Feature Learning (تلقائي)",
        showarrow=False, font=dict(family=MONO, size=10.5, color="#8A4A08"),
        bgcolor="#FDF3E3", borderpad=5,
    )
    fig.update_xaxes(range=[-0.5, 10.6], visible=False)
    fig.update_yaxes(range=[0.1, 5.0], visible=False)
    return _base(fig, h=380, legend=False)


@st.cache_data(show_spinner=False)
def attention_heatmap() -> go.Figure:
    """مفهوم الانتباه: كل كلمة توزّع وزناً على باقي الكلمات."""
    toks = ["The", "researcher", "read", "the", "paper", "because", "it", "was", "new"]
    n = len(toks)
    rng = np.random.default_rng(42)
    W = rng.random((n, n)) * 0.18
    links = {(6, 4): 0.82, (6, 1): 0.1, (2, 1): 0.62, (4, 2): 0.48,
             (8, 4): 0.55, (5, 2): 0.4, (7, 6): 0.5, (3, 4): 0.45, (1, 1): 0.3}
    for (i, j), v in links.items():
        W[i, j] = v
    W = W / W.sum(axis=1, keepdims=True)

    fig = go.Figure(go.Heatmap(
        z=W, x=toks, y=toks, colorscale="Purples",
        colorbar=dict(title=dict(text="attention<br>weight", font=dict(size=10)),
                      thickness=12, len=0.8, tickfont=dict(size=9)),
        hovertemplate="query: %{y}<br>key: %{x}<br>weight: %{z:.3f}<extra></extra>",
    ))
    fig.update_xaxes(title="attends to  (key)", side="bottom",
                     tickfont=dict(family=MONO, size=11))
    fig.update_yaxes(title="token  (query)", autorange="reversed",
                     tickfont=dict(family=MONO, size=11))
    fig.add_annotation(
        x=4, y=-1.4,
        text="«it» تنتبه بقوّة إلى «paper» — هكذا يُحلّ الإرجاع الضمنيّ",
        showarrow=False, font=dict(family=FONT, size=10.5, color="#4A2A86"),
        bgcolor="#F2ECFD", bordercolor="#8257D8", borderwidth=1, borderpad=5,
    )
    return _base(fig, h=460, legend=False,
                 title="Attention — ما معنى أن النموذج «ينتبه»")


@st.cache_data(show_spinner=False)
def embedding_space() -> go.Figure:
    """فضاء التمثيل: المعنى يصبح موقعاً هندسياً."""
    words = {
        "king": (2.4, 2.1, "#5B6BE1"), "queen": (2.0, 2.9, "#5B6BE1"),
        "man": (1.0, 0.6, "#5B6BE1"), "woman": (0.6, 1.4, "#5B6BE1"),
        "regression": (-2.4, 2.0, "#17A074"), "estimator": (-2.0, 2.6, "#17A074"),
        "variance": (-2.8, 1.3, "#17A074"), "panel": (-1.6, 1.6, "#17A074"),
        "Paris": (1.6, -2.2, "#E0832A"), "France": (2.4, -1.6, "#E0832A"),
        "Rome": (0.6, -2.6, "#E0832A"), "Italy": (1.4, -2.9, "#E0832A"),
        "neuron": (-1.0, -1.9, "#D9527E"), "layer": (-1.6, -2.4, "#D9527E"),
        "gradient": (-2.2, -1.5, "#D9527E"),
    }
    fig = go.Figure()
    for w, (x, y, c) in words.items():
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers+text", text=[w],
            textposition="top center",
            textfont=dict(family=MONO, size=10.5, color=c),
            marker=dict(size=11, color=c, opacity=0.85,
                        line=dict(color="white", width=1.4)),
            showlegend=False, hovertemplate=f"{w}<extra></extra>"))
    for a, b, col in [("man", "king", "#8257D8"), ("woman", "queen", "#8257D8"),
                      ("Paris", "France", "#C9A008"), ("Rome", "Italy", "#C9A008")]:
        x0, y0, _ = words[a]
        x1, y1, _ = words[b]
        fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y",
                           axref="x", ayref="y", showarrow=True, arrowhead=2,
                           arrowsize=1.1, arrowwidth=1.7, arrowcolor=col,
                           opacity=0.75, text="")
    fig.add_annotation(
        x=0, y=3.6,
        text=("<b>Embedding space</b> — المعنى يصبح <b>متجهاً</b>:<br>"
              "الكلمات المترابطة تتجاور، والعلاقات تصبح <b>اتجاهات</b> ثابتة"),
        showarrow=False, font=dict(family=FONT, size=10.5, color="#2C3692"),
        bgcolor="#EEF0FD", bordercolor="#5B6BE1", borderwidth=1.2, borderpad=6,
    )
    fig.update_xaxes(title="dimension 1  (مُختزَل)", range=[-4.0, 4.0])
    fig.update_yaxes(title="dimension 2  (مُختزَل)", range=[-4.0, 4.3])
    return _base(fig, h=470, legend=False)


@st.cache_data(show_spinner=False)
def scaling_curve() -> go.Figure:
    """قوانين القياس: الأداء يتحسّن بقانون قوة مع الحجم."""
    n = np.logspace(1, 6, 120)
    for_params = 2.6 * n ** (-0.095) + 0.42
    for_data = 3.1 * n ** (-0.115) + 0.40
    for_compute = 2.2 * n ** (-0.082) + 0.45

    fig = go.Figure()
    for y, nm, col in [
        (for_params, "scaling with model size  (N params)", "#5B6BE1"),
        (for_data, "scaling with data  (D tokens)", "#17A074"),
        (for_compute, "scaling with compute  (C FLOPs)", "#E0832A"),
    ]:
        fig.add_trace(go.Scatter(x=n, y=y, mode="lines", name=nm,
                                 line=dict(color=col, width=3.2)))
    fig.update_xaxes(title="scale  (log)", type="log")
    fig.update_yaxes(title="Loss  (log)", type="log")
    fig.add_annotation(
        x=np.log10(3e4), y=np.log10(1.6),
        text=("خط مستقيم على مقياس لوغاريتمي مزدوج<br>"
              "= <b>قانون قوة</b> (power law)"),
        showarrow=False, font=dict(family=FONT, size=10.5, color="#2C3692"),
        bgcolor="#EEF0FD", bordercolor="#5B6BE1", borderwidth=1, borderpad=5,
    )
    fig.add_annotation(
        x=np.log10(5e5), y=np.log10(0.46),
        text="عوائد متضائلة لكن غير منعدمة<br>diminishing, not vanishing",
        showarrow=False, font=dict(family=FONT, size=10, color="#8A4A08"),
        bgcolor="#FDF3E3", bordercolor="#E0832A", borderwidth=1, borderpad=5,
    )
    return _base(fig, h=430,
                 title="Scaling Laws — لماذا صار «الأكبر» أفضل، وحدود ذلك")


# ═════════════════════════ 7. التاريخ ═════════════════════════

@st.cache_data(show_spinner=False)
def ai_eras_chart() -> go.Figure:
    """منحنى الاهتمام/التمويل عبر العقود مع الشتاءات."""
    yr = np.array([1950, 1956, 1960, 1966, 1970, 1974, 1980, 1984, 1987,
                   1990, 1993, 1997, 2000, 2006, 2012, 2017, 2020, 2022,
                   2024, 2026])
    interest = np.array([10, 42, 55, 62, 70, 26, 34, 72, 68, 24, 20, 38,
                         33, 45, 72, 86, 92, 99, 100, 100])

    fig = go.Figure()
    winters = [
        (1974, 1980, "AI Winter I", "#94A3B8"),
        (1987, 1993, "AI Winter II", "#94A3B8"),
    ]
    for x0, x1, lbl, col in winters:
        fig.add_vrect(x0=x0, x1=x1, fillcolor=col, opacity=0.18, line_width=0,
                      annotation_text=lbl, annotation_position="top",
                      annotation_font=dict(family=FONT, size=10, color="#475569"))
    springs = [
        (1956, 1974, "Symbolic AI", "#5B6BE1"),
        (1980, 1987, "Expert Systems", "#E0832A"),
        (1993, 2010, "Statistical ML", "#17A074"),
        (2012, 2020, "Deep Learning", "#D9527E"),
        (2020, 2026.5, "Foundation Models", "#8257D8"),
    ]
    for x0, x1, lbl, col in springs:
        fig.add_vrect(x0=x0, x1=x1, fillcolor=col, opacity=0.08, line_width=0,
                      annotation_text=lbl, annotation_position="bottom",
                      annotation_font=dict(family=FONT, size=10, color=col))
    fig.add_trace(go.Scatter(
        x=yr, y=interest, mode="lines+markers",
        name="Interest / funding / capability (conceptual)",
        line=dict(color="#5B6BE1", width=3.4, shape="spline"),
        marker=dict(size=8, color="#5B6BE1",
                    line=dict(color="white", width=1.6)),
        fill="tozeroy", fillcolor="rgba(91,107,225,.08)"))
    marks = {
        1956: "Dartmouth", 1966: "ELIZA", 1986: "Backprop",
        1997: "Deep Blue", 2012: "AlexNet", 2017: "Transformer",
        2022: "ChatGPT", 2024: "Nobel ×2",
    }
    for x, t in marks.items():
        i = int(np.argmin(np.abs(yr - x)))
        fig.add_annotation(x=yr[i], y=interest[i] + 7, text=f"<b>{t}</b>",
                           showarrow=True, arrowhead=0, arrowwidth=1,
                           arrowcolor="#CBD5E6", ay=-16,
                           font=dict(family=MONO, size=9, color="#334155"))
    fig.update_xaxes(title="year", dtick=10, range=[1948, 2029])
    fig.update_yaxes(title="relative interest (conceptual scale)", range=[0, 120])
    return _base(fig, h=460,
                 title="موجات الذكاء الاصطناعي — ربيعان، شتاءان، ثم انفجار")


# ═════════════════════════ 8. المهارات والخطة ═════════════════════════

@st.cache_data(show_spinner=False)
def skills_radar() -> go.Figure:
    """رادار: المستوى المطلوب من كل مهارة بحسب هدف الباحث."""
    cats = ["Python", "Statistics", "Linear Algebra", "Calculus",
            "Command line / Git", "Data wrangling", "Visualization",
            "ML concepts"]
    profiles = {
        "قارئ ناقد للأدبيات (Reader)": ([2, 4, 2, 1, 1, 2, 3, 3], "#5B6BE1"),
        "باحث مُطبِّق (Applied researcher)": ([4, 4, 3, 2, 3, 4, 4, 4], "#17A074"),
        "مُطوِّر طرائق (Method developer)": ([5, 5, 5, 4, 4, 4, 3, 5], "#D9527E"),
    }
    fig = go.Figure()
    for nm, (vals, col) in profiles.items():
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]], fill="toself",
            name=nm, line=dict(color=col, width=2.6),
            opacity=0.42))
    fig.update_layout(
        polar=dict(
            bgcolor="#FCFDFF",
            radialaxis=dict(visible=True, range=[0, 5], dtick=1,
                            gridcolor=PLOT_GRID, tickfont=dict(size=9.5),
                            angle=90),
            angularaxis=dict(gridcolor=PLOT_GRID,
                             tickfont=dict(family=MONO, size=10)),
        ),
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=11, color=PLOT_INK),
        margin=dict(l=70, r=70, t=70, b=70),
        title=dict(text="المهارات المطلوبة — بحسب الدور لا بحسب «الكل أو لا شيء»",
                   x=0.5, xanchor="center",
                   font=dict(family=FONT, size=14, color=PLOT_INK)),
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center",
                    font=dict(size=10.5)),
    )
    return fig


@st.cache_data(show_spinner=False)
def roadmap_gantt() -> go.Figure:
    """خطة 12 أسبوعاً لبناء الأساس المفاهيمي والعملي."""
    tasks = [
        ("المفاهيم والمصطلحات الأساسية", 1, 2, "#5B6BE1"),
        ("Python للتحليل (pandas, numpy)", 1, 4, "#17A074"),
        ("إحصاء ورياضيات مُستهدَفة", 2, 5, "#E0832A"),
        ("سطر الأوامر و Git والبيئات", 3, 4, "#0E9BA8"),
        ("التعلّم المُراقَب عملياً", 5, 8, "#D9527E"),
        ("التقييم والتحقّق المتقاطع", 6, 9, "#8257D8"),
        ("التعلّم غير المُراقَب والتخفيض", 8, 10, "#C9A008"),
        ("شبكات عصبية ومفاهيم عميقة", 9, 11, "#2E9E4F"),
        ("النماذج التوليدية و LLMs", 10, 12, "#C3449B"),
        ("مشروع بحثي متكامل", 10, 12, "#D2603A"),
    ]
    fig = go.Figure()
    for i, (nm, s, e, col) in enumerate(tasks):
        fig.add_trace(go.Bar(
            x=[e - s + 1], y=[nm], base=[s - 1], orientation="h",
            marker=dict(color=col, line=dict(color="white", width=1.4)),
            name=nm, showlegend=False, width=0.62,
            text=[f"W{s}–W{e}"], textposition="inside",
            insidetextfont=dict(family=MONO, size=10, color="white"),
            hovertemplate=f"{nm}<br>weeks {s}–{e}<extra></extra>"))
    fig.update_xaxes(title="أسبوع  (week)", dtick=1, range=[0, 12],
                     tickvals=list(range(13)))
    fig.update_yaxes(autorange="reversed",
                     tickfont=dict(family=FONT, size=11, color=PLOT_INK))
    return _base(fig, h=460, legend=False,
                 title="خطة 12 أسبوعاً — من الصفر إلى أرضية صلبة")


@st.cache_data(show_spinner=False)
def workflow_pipeline() -> go.Figure:
    """دورة عمل مشروع تعلّم آلة كاملة."""
    steps_ = [
        ("1. Problem\nصياغة السؤال", "#5B6BE1"),
        ("2. Data\nجمع وتنظيف", "#17A074"),
        ("3. Features\nتمثيل", "#0E9BA8"),
        ("4. Model\nاختيار وتدريب", "#E0832A"),
        ("5. Evaluate\nتقييم خارج العيّنة", "#D9527E"),
        ("6. Interpret\nتفسير", "#8257D8"),
        ("7. Deploy\nنشر ومراقبة", "#2E9E4F"),
    ]
    fig = go.Figure()
    for i, (lbl, col) in enumerate(steps_):
        ang = np.pi / 2 - i * (2 * np.pi / len(steps_))
        x, y = 2.6 * np.cos(ang), 2.6 * np.sin(ang)
        fig.add_shape(type="circle", x0=x - 0.78, y0=y - 0.78, x1=x + 0.78,
                      y1=y + 0.78, line=dict(color=col, width=2.6),
                      fillcolor=col, opacity=0.14)
        fig.add_annotation(x=x, y=y,
                           text="<b>" + lbl.replace("\n", "</b><br>"),
                           showarrow=False,
                           font=dict(family=FONT, size=9.4, color=col))
        nx_ = 2.6 * np.cos(np.pi / 2 - (i + 1) * (2 * np.pi / len(steps_)))
        ny_ = 2.6 * np.sin(np.pi / 2 - (i + 1) * (2 * np.pi / len(steps_)))
        fig.add_annotation(
            x=nx_ * 0.76, y=ny_ * 0.76, ax=x * 0.76, ay=y * 0.76,
            xref="x", yref="y", axref="x", ayref="y", showarrow=True,
            arrowhead=3, arrowsize=1.1, arrowwidth=1.9,
            arrowcolor="#B9C4DC", text="")
    fig.add_annotation(x=0, y=0,
                       text="<b>دورة متكرّرة</b><br><i>iterative loop</i>",
                       showarrow=False,
                       font=dict(family=FONT, size=11, color="#1E2749"),
                       bgcolor="rgba(255,255,255,.9)", bordercolor="#CBD5E6",
                       borderwidth=1, borderpad=6)
    fig.update_xaxes(range=[-4.2, 4.2], visible=False)
    fig.update_yaxes(range=[-4.2, 4.2], visible=False, scaleanchor="x")
    return _base(fig, h=480, legend=False)


@st.cache_data(show_spinner=False)
def applications_treemap() -> go.Figure:
    """تطبيقات الذكاء الاصطناعي بحسب القطاع."""
    import plotly.express as px

    sectors = {
        "الاقتصاد والمالية": ["التنبؤ بالتضخّم", "مخاطر الائتمان", "كشف الغشّ",
                              "تسعير الأصول", "التداول الخوارزمي"],
        "الصحة والطب": ["تشخيص الصور", "اكتشاف الدواء", "تنبؤ المخاطر",
                        "AlphaFold وبنية البروتين"],
        "العلوم الطبيعية": ["الفيزياء الحسابية", "المناخ والطقس",
                            "علم الفلك", "الكيمياء الحسابية"],
        "العلوم الاجتماعية": ["تحليل النصوص", "استخراج المواقف",
                              "بيانات الأقمار كبديل", "الشبكات الاجتماعية"],
        "الصناعة والخدمات": ["الصيانة التنبّؤية", "سلاسل التوريد",
                             "التوصية", "الرؤية الحاسوبية"],
        "اللغة والمعرفة": ["الترجمة الآلية", "التلخيص",
                           "البحث الدلالي", "المساعدات البحثية"],
    }
    labels, parents, values, colors = ["AI Applications"], [""], [0], ["#FFFFFF"]
    for i, (sec, items) in enumerate(sectors.items()):
        labels.append(sec)
        parents.append("AI Applications")
        values.append(0)
        colors.append(C[i % len(C)])
        for it in items:
            labels.append(it)
            parents.append(sec)
            values.append(1)
            colors.append(C[i % len(C)])
    fig = go.Figure(go.Treemap(
        labels=labels, parents=parents, values=values,
        marker=dict(colors=colors, line=dict(color="white", width=2)),
        textfont=dict(family=FONT, size=12, color="white"),
        tiling=dict(packing="squarify"),
        hovertemplate="%{label}<extra></extra>",
        branchvalues="total",
    ))
    fig.update_layout(
        height=520, paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=4, r=4, t=46, b=4),
        font=dict(family=FONT, size=12, color=PLOT_INK),
        title=dict(text="خريطة التطبيقات — أين يُستخدم الذكاء الاصطناعي فعلياً",
                   x=0.5, xanchor="center",
                   font=dict(family=FONT, size=14, color=PLOT_INK)),
    )
    return fig


@st.cache_data(show_spinner=False)
def interpretability_tradeoff() -> go.Figure:
    """موقع النماذج على محوري الدقّة والقابلية للتفسير."""
    models = [
        ("Linear / Logistic regression", 1.0, 5.0, "#5B6BE1"),
        ("Decision tree (shallow)", 1.6, 4.6, "#5B6BE1"),
        ("GAM / Spline models", 2.4, 4.2, "#17A074"),
        ("Sparse optimal trees", 3.0, 4.3, "#17A074"),
        ("Random Forest", 3.9, 2.4, "#E0832A"),
        ("Gradient Boosting", 4.3, 2.1, "#E0832A"),
        ("SVM (kernel)", 3.6, 1.9, "#C9A008"),
        ("Deep Neural Network", 4.7, 1.2, "#D9527E"),
        ("Large Language Model", 5.0, 0.6, "#8257D8"),
    ]
    fig = go.Figure()
    for nm, acc, interp, col in models:
        fig.add_trace(go.Scatter(
            x=[acc], y=[interp], mode="markers+text", text=[nm],
            textposition="top center",
            textfont=dict(family=MONO, size=9.6, color=col),
            marker=dict(size=16, color=col, opacity=0.85,
                        line=dict(color="white", width=2)),
            showlegend=False,
            hovertemplate=f"{nm}<br>accuracy≈{acc}<br>interpretability≈{interp}<extra></extra>"))
    fig.add_annotation(
        x=1.5, y=1.0, text="منطقة غير مرغوبة<br>(لا دقّة ولا تفسير)",
        showarrow=False, font=dict(family=FONT, size=10, color="#64748B"),
        bgcolor="#F1F4FA", borderpad=5)
    fig.add_annotation(
        x=4.4, y=4.7,
        text=("<b>الهدف الحديث</b>: نماذج دقيقة وقابلة للتفسير معاً<br>"
              "(ردّ Rudin على مقايضة Occam لدى Breiman)"),
        showarrow=False, font=dict(family=FONT, size=10, color="#0B5B42"),
        bgcolor="#E6F7F1", bordercolor="#17A074", borderwidth=1.2, borderpad=6)
    fig.update_xaxes(title="Predictive accuracy  →", range=[0.3, 5.7],
                     showticklabels=False)
    fig.update_yaxes(title="Interpretability  →", range=[0.0, 5.6],
                     showticklabels=False)
    return _base(fig, h=470, legend=False,
                 title="Accuracy vs Interpretability — الخريطة التي يجب أن يعرفها الباحث")
