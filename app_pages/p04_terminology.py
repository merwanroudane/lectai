"""معجم المصطلحات — المرجع الذي يُعاد إليه."""
from __future__ import annotations

import streamlit as st

from utils import glossary as G
from utils import ui

a = ui.boot("terminology")

ui.hero(
    accent=a,
    eyebrow="المحاضرة الرابعة · الأرضية المفاهيمية",
    number="04",
    title="معجم المصطلحات",
    lead=(
        "أكبر عائق أمام الباحث القادم من الإحصاء ليس صعوبة الرياضيات، بل "
        "<b>ازدحام المصطلحات</b>: الشيء الواحد له ثلاثة أسماء، والاسم الواحد "
        "يدلّ على ثلاثة أشياء. هذه الصفحة مرجع دائم — "
        f"<b>{len(G.TERMS)} مصطلحاً</b> في {len(G.CATEGORIES)} تصنيفات، "
        "قابلة للبحث. لا تُقرأ مرّة واحدة، بل يُعاد إليها كلّما اعترضك مصطلح."
    ),
    chips=[
        f"{len(G.TERMS)} مصطلحاً",
        f"{len(G.CATEGORIES)} تصنيفات",
        "بحث فوري",
        "جدول الترجمات المتنازَع عليها",
    ],
)

# ═══════════════════════════ 1. لماذا المصطلح مشكلة ═══════════════════════════

st.markdown("## ١. لماذا تُشكّل المصطلحات عائقاً حقيقياً؟")

ui.section_intro(
    "المشكلة ليست أن المصطلحات كثيرة، بل أنّ حقلين مختلفين — الإحصاء وعلوم "
    "الحاسوب — طوّرا المفاهيم نفسها <b>بالتوازي ودون تنسيق</b>، فنشأت ثلاثة "
    "أنماط من الالتباس. تمييز النمط يُنهي الالتباس فوراً.",
    accent=a,
)

ui.grid(
    [
        ui.card(
            "النمط الأول · مُرادفات عبر الحقول",
            "المفهوم واحد والاسم مختلف باختلاف الحقل. "
            "<br><br>المتغيّر المستقلّ في الاقتصاد القياسي هو "
            "<code>Feature</code> في تعلّم الآلة، و<code>Attribute</code> في "
            "قواعد البيانات، و<code>Covariate</code> في الإحصاء الحيوي، "
            "و<code>Predictor</code> في الأدبيات العامة. "
            "<b>خمسة أسماء، شيء واحد.</b>",
            color="#8257D8", soft="#F2ECFD", ink="#4A2A86", icon="🔁",
        ),
        ui.card(
            "النمط الثاني · اسم واحد بمعانٍ متعدّدة",
            "الكلمة نفسها تدلّ على أشياء مختلفة بحسب السياق. "
            "<br><br>كلمة <code>Bias</code> تعني في الإحصاء <b>تحيّز المُقدِّر</b> "
            "(فرق التوقّع عن القيمة الحقيقية)، وتعني في الشبكات العصبية "
            "<b>الحدّ الثابت</b> في المعادلة، وتعني في أخلاقيات الذكاء "
            "الاصطناعي <b>الإجحاف الاجتماعي</b>. "
            "<b>ثلاثة مفاهيم، اسم واحد.</b>",
            color="#D6455F", soft="#FCEBEF", ink="#851F32", icon="⚠",
        ),
        ui.card(
            "النمط الثالث · ترجمة عربية غير مستقرّة",
            "المصطلح الإنجليزي واحد، والترجمات العربية متعدّدة ومتنافسة. "
            "<br><br><code>Regularization</code> تُترجَم «تنظيم» و«انتظام» "
            "و«تسوية» و«ضبط». "
            "<b>الحلّ العملي:</b> اكتب العربية وبجانبها الإنجليزية بين قوسين "
            "في أوّل ورود، ثم استعمل الإنجليزية. هذا ما تفعله هذه المنصّة.",
            color="#E0832A", soft="#FDF3E3", ink="#8A4A08", icon="🈯",
        ),
    ],
    cols=3,
)

ui.callout(
    "idea",
    "قاعدة عملية واحدة تُغنيك عن حفظ المعجم",
    "قبل أن تسأل «ما معنى هذا المصطلح؟»، اسأل أولاً: "
    "<b>هل يصف شيئاً يدخل النموذج، أم شيئاً يخرج منه، أم شيئاً يحكم كيفية "
    "بنائه، أم شيئاً يقيس جودته؟</b> "
    "كل مصطلحات تعلّم الآلة تقريباً تقع في واحدة من هذه الأربع. "
    "تحديد الخانة يُقلّص المعنى المحتمل إلى حدّ يجعل التعريف شبه بديهي.",
)

# ═══════════════════════════ 2. المصطلحات المتقابلة ═══════════════════════════

st.markdown("## ٢. جدول الترجمة بين الحقلين")

ui.section_intro(
    "هذا الجدول وحده يحلّ أكثر من نصف مشكلة الباحث القادم من الإحصاء أو "
    "الاقتصاد القياسي. العمود الأيمن ما تعرفه، والأيسر ما ستقرؤه.",
    accent=a,
)

st.markdown(
    """
| في الإحصاء / القياس الاقتصادي | في تعلّم الآلة | ملاحظة دقيقة |
|---|---|---|
| المتغيّر المستقلّ · `Independent variable` | `Feature` / `Input` / `Predictor` | المعنى واحد، لكن «مستقلّ» في ML لا يوحي باستقلال إحصائي |
| المتغيّر التابع · `Dependent variable` | `Target` / `Label` / `Output` / `Response` | `Label` تُستعمل غالباً للتصنيف، و`Target` للانحدار |
| المشاهدة · `Observation` | `Example` / `Instance` / `Sample` / `Data point` | انتبه: `Sample` في ML تعني **مشاهدة واحدة**، وفي الإحصاء تعني **العيّنة كلها** |
| المعاملات · `Coefficients` (β) | `Parameters` / `Weights` | في الشبكات تُسمّى `Weights` دائماً |
| الحدّ الثابت · `Intercept` | `Bias term` | التسمية مُربكة؛ لا علاقة لها بالتحيّز الإحصائي |
| التقدير · `Estimation` | `Training` / `Fitting` / `Learning` | «تدريب» فعل عمليّ، و«تقدير» فعل نظريّ — المضمون الحسابي قد يكون واحداً |
| المواصفة · `Model specification` | `Architecture` / `Model selection` | في الإحصاء تُبرَّر نظرياً، وفي ML تُختار تجريبياً |
| القوّة التفسيرية · `R²` | `Score` / `Accuracy` / `Performance` | ML يقيس على بيانات **لم يرها**؛ R² يُحسب غالباً داخل العيّنة |
| البواقي · `Residuals` | `Errors` / `Loss` | `Loss` دالة تُحسب لتُحسَّن، لا مجرّد فرق يُفحَص |
| الانحدار اللوجستي · `Logit` | `Logistic Regression` (تصنيف) | المعادلة نفسها، لكن ML يصنّفها ضمن **التصنيف** لا الانحدار |
| تعدّد الخطّية · `Multicollinearity` | `Correlated features` | يُقلق الإحصائي كثيراً، ويُقلق مهندس ML أقلّ (لأن هدفه التنبؤ) |
| الاختبار خارج العيّنة · `Out-of-sample` | `Test set` / `Held-out set` | ML جعله إجراءً إلزامياً لا اختيارياً |
| التنقيب عن البيانات · `Data mining` (بمعنى سلبي) | `Exploratory analysis` / `Feature discovery` | الحكم القيمي انقلب بين الحقلين |
| درجات الحرّية · `Degrees of freedom` | `Model capacity` / `Complexity` | المفهوم أوسع في ML ولا يُحسب دائماً بصيغة مغلقة |
| الانكماش · `Shrinkage` (Ridge) | `Regularization` / `Weight decay` | المصطلحات الثلاثة تصف العملية نفسها تقريباً |
"""
)

ui.callout(
    "warn",
    "الفخّ الأخطر في الجدول أعلاه",
    "كلمة <code>Sample</code>. في الإحصاء العربي والإنجليزي تعني <b>العيّنة</b> "
    "— مجموعة المشاهدات. في أدبيات تعلّم الآلة (وخصوصاً في وثائق "
    "<code>scikit-learn</code> و<code>PyTorch</code>) تعني غالباً "
    "<b>مشاهدة واحدة</b>. "
    "فعبارة <code>n_samples = 1000</code> تعني «ألف مشاهدة» لا «ألف عيّنة». "
    "هذا الخلط وحده أنتج أخطاء قراءة كثيرة في أوراق تطبيقية.",
)

# ═══════════════════════════ 3. المصطلحات متعددة المعاني ═══════════════════════

st.markdown("## ٣. كلمات تعني أشياء مختلفة بحسب السياق")

ui.section_intro(
    "هذه ليست مصطلحات صعبة، بل مصطلحات <b>مُحمَّلة</b>. "
    "عند قراءتها حدّد السياق أولاً، ثم المعنى.",
    accent=a,
)

ui.steps(
    [
        ("Bias — ثلاثة معانٍ منفصلة تماماً",
         "<b>(١) التحيّز الإحصائي:</b> فرق توقّع المُقدِّر عن القيمة الحقيقية — "
         "مفهوم في المقايضة <code>Bias–Variance</code>. "
         "<br><b>(٢) حدّ الإزاحة:</b> الثابت <code>b</code> في "
         "<code>y = wx + b</code> داخل العصبون — مجرّد معامل. "
         "<br><b>(٣) الإجحاف الاجتماعي:</b> أن يُنتج النظام قرارات مُجحفة بفئة — "
         "مفهوم أخلاقي وقانوني. "
         "<br><b>الثلاثة لا علاقة رياضية بينها.</b>"),
        ("Model — معنيان متباعدان فلسفياً",
         "<b>في الإحصاء:</b> ادّعاء عن <b>آلية توليد البيانات</b> في الواقع، "
         "يُفترض صحّته ثم تُختبر فرضيّاته. "
         "<br><b>في تعلّم الآلة:</b> <b>دالة تقريبية</b> تُقيَّم بنفعها التنبؤي، "
         "ولا تدّعي وصف الآلية. "
         "<br>هذا هو جوهر خلاف بريمان الذي تتناوله المحاضرة السابعة."),
        ("Validation — ثلاثة استعمالات",
         "<b>(١) مجموعة التحقّق</b> <code>Validation set</code>: جزء من البيانات "
         "لضبط المعاملات الفائقة. "
         "<br><b>(٢) التحقّق المتقاطع</b> <code>Cross-validation</code>: إجراء "
         "تقييم بالتدوير. "
         "<br><b>(٣) تصديق النموذج</b> <code>Model validation</code> بالمعنى "
         "الإحصائي: فحص فرضيّات النموذج وجودة الملاءمة."),
        ("Feature — بين الوصف والبناء",
         "<b>متغيّر مُدخَل</b> أحياناً، و<b>تمثيل مُشتقّ</b> أحياناً أخرى. "
         "عبارة <code>Feature Engineering</code> تعني بناء متغيّرات جديدة من "
         "القديمة، وعبارة <code>Feature Learning</code> تعني أن النموذج يبنيها "
         "بنفسه. التمييز بينهما يُحدّد ما إذا كان العمل يدوياً أم آلياً."),
        ("Inference — انقلاب كامل في المعنى",
         "<b>في الإحصاء:</b> الاستدلال — استخلاص خصائص المجتمع من العيّنة "
         "(فترات ثقة، اختبارات). "
         "<br><b>في تعلّم الآلة:</b> <b>مرحلة التشغيل</b> — تمرير مُدخَل جديد "
         "عبر نموذج مُدرَّب للحصول على تنبؤ. "
         "<br>فعبارة <code>inference time</code> لا تعني «وقت الاستدلال "
         "الإحصائي» بل <b>زمن التنبؤ</b>."),
        ("Regression — المعنى الأضيق",
         "في الإحصاء: أي نمذجة لعلاقة بين متغيّرات. "
         "في تعلّم الآلة: <b>تحديداً</b> المسائل التي يكون مُخرَجها عدداً "
         "متّصلاً، في مقابل <code>Classification</code>. "
         "لذلك يُصنَّف <code>Logistic Regression</code> في ML تحت "
         "<b>التصنيف</b> رغم اسمه."),
    ],
    accent=a,
)

# ═══════════════════════════ 4. المعجم التفاعلي ═══════════════════════════

st.markdown("## ٤. المعجم الكامل — ابحث وتصفّح")

ui.section_intro(
    "اكتب أيّ جزء من المصطلح بالعربية أو الإنجليزية، أو اختر تصنيفاً "
    "لتصفّحه كاملاً. البحث يشمل نصّ التعريف أيضاً، فيمكنك البحث بالمعنى "
    "لا بالاسم فقط.",
    accent=a,
)

c1, c2 = st.columns([2, 3])
with c1:
    cat = st.selectbox(
        "التصنيف",
        ["الكل"] + list(G.CATEGORIES.keys()),
        key="gl_cat",
    )
with c2:
    q = st.text_input(
        "ابحث",
        placeholder="مثال: overfitting  ·  تنظيم  ·  انحياز  ·  tensor",
        key="gl_q",
    )

rows = G.search(q, cat)

st.html(
    f"""
<div dir="rtl" style="margin:.5rem 0 1rem;padding:.6rem .9rem;background:{a.soft};
     border:1px solid {a.strong}33;border-radius:12px;font-family:{ui.FONT_STACK};
     color:{a.ink};font-weight:700;font-size:.92rem">
  النتائج: {len(rows)} مصطلحاً من أصل {len(G.TERMS)}
</div>"""
)

if not rows:
    ui.callout(
        "neutral",
        "لا نتائج",
        "جرّب جزءاً أقصر من الكلمة، أو ابحث بالإنجليزية، أو اختر «الكل» في "
        "خانة التصنيف.",
    )
else:
    # تجميع النتائج بحسب التصنيف للحفاظ على ترتيب موضوعي
    by_cat: dict[str, list] = {}
    for r in rows:
        by_cat.setdefault(r[2], []).append(r)

    for cname in G.CATEGORIES:
        if cname not in by_cat:
            continue
        strong, soft, ink = G.CATEGORIES[cname]
        items = by_cat[cname]

        st.html(
            f"""
<div dir="rtl" style="margin:1.1rem 0 .5rem;display:flex;align-items:center;
     gap:.6rem;font-family:{ui.FONT_STACK}">
  <span style="width:10px;height:10px;border-radius:50%;background:{strong}"></span>
  <span style="font-weight:800;color:{ink};font-size:1.05rem">{cname}</span>
  <span style="background:{soft};color:{ink};border-radius:999px;
        padding:.1rem .6rem;font-size:.76rem;font-weight:700">{len(items)}</span>
  <span style="flex:1;height:1px;background:{strong}28"></span>
</div>"""
        )

        body = "".join(
            f"""
<div style="background:{soft};border:1px solid {strong}2A;
     border-inline-start:3px solid {strong};border-radius:11px;
     padding:.72rem .85rem">
  <div style="display:flex;justify-content:space-between;align-items:baseline;
       gap:.5rem;flex-wrap:wrap;margin-bottom:.3rem">
    <span style="font-weight:800;color:{ink};font-size:.97rem">{ui.esc(ar)}</span>
    <span style="direction:ltr;font-family:{ui.MONO_STACK};font-size:.8rem;
          color:{strong};font-weight:600">{ui.esc(en)}</span>
  </div>
  <div style="color:#2A3558;font-size:.89rem;line-height:1.8">{ui.esc(d)}</div>
</div>"""
            for ar, en, _c, d in items
        )
        st.html(
            f"""
<div dir="rtl" style="display:grid;gap:.6rem;font-family:{ui.FONT_STACK};
     grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">{body}</div>"""
        )

# ═══════════════════════════ 5. الاختصارات ═══════════════════════════

st.markdown("## ٥. الاختصارات التي ستقابلها يومياً")

ui.section_intro(
    "الاختصارات في هذا الحقل كثيفة إلى درجة أن نصّاً كاملاً قد يمرّ دون أن "
    "تفهم منه شيئاً إن لم تحلّها. هذه هي الأكثر وروداً.",
    accent=a,
)

st.markdown(
    """
| الاختصار | الصيغة الكاملة | ماذا يعني بالعربية |
|---|---|---|
| `AI` | Artificial Intelligence | الذكاء الاصطناعي |
| `ML` | Machine Learning | تعلّم الآلة |
| `DL` | Deep Learning | التعلّم العميق |
| `ANN` | Artificial Neural Network | الشبكة العصبية الاصطناعية |
| `CNN` | Convolutional Neural Network | الشبكة الالتفافية (للصور) |
| `RNN` | Recurrent Neural Network | الشبكة التكرارية (للتسلسلات) |
| `LSTM` | Long Short-Term Memory | ذاكرة طويلة-قصيرة المدى |
| `GAN` | Generative Adversarial Network | الشبكة التوليدية التنافسية |
| `LLM` | Large Language Model | النموذج اللغوي الكبير |
| `NLP` | Natural Language Processing | معالجة اللغة الطبيعية |
| `CV` | Computer Vision | الرؤية الحاسوبية |
| `RL` | Reinforcement Learning | التعلّم المعزّز |
| `SGD` | Stochastic Gradient Descent | النزول التدريجي العشوائي |
| `MSE` | Mean Squared Error | متوسّط مربّع الخطأ |
| `MAE` | Mean Absolute Error | متوسّط الخطأ المطلق |
| `AUC` | Area Under the Curve | المساحة تحت المنحنى (ROC) |
| `ROC` | Receiver Operating Characteristic | منحنى أداء المصنّف |
| `CV` (ثانية) | Cross-Validation | التحقّق المتقاطع — **نفس الاختصار، معنى آخر** |
| `EDA` | Exploratory Data Analysis | التحليل الاستكشافي للبيانات |
| `PCA` | Principal Component Analysis | تحليل المكوّنات الأساسية |
| `SVM` | Support Vector Machine | آلة المتّجهات الداعمة |
| `kNN` | k-Nearest Neighbours | أقرب k جار |
| `RF` | Random Forest | الغابة العشوائية |
| `GBM` | Gradient Boosting Machine | آلة التعزيز التدريجي |
| `XAI` | Explainable AI | الذكاء الاصطناعي القابل للتفسير |
| `AGI` | Artificial General Intelligence | الذكاء الاصطناعي العام |
| `RAG` | Retrieval-Augmented Generation | التوليد المعزّز بالاسترجاع |
| `RLHF` | Reinforcement Learning from Human Feedback | التعلّم المعزّز من تغذية بشرية |
| `GPU` | Graphics Processing Unit | وحدة معالجة الرسوميات |
| `API` | Application Programming Interface | واجهة برمجة التطبيقات |
| `SOTA` | State of the Art | أفضل نتيجة مُسجَّلة حالياً |
| `i.i.d.` | independent and identically distributed | مستقلّة ومتماثلة التوزيع |
"""
)

ui.callout(
    "danger",
    "انتبه: `CV` اختصار لمفهومين شائعين معاً",
    "<code>CV</code> تعني <b>Computer Vision</b> في سياق الصور، وتعني "
    "<b>Cross-Validation</b> في سياق التقييم. "
    "السياق وحده يفصل. القاعدة: إن كانت الجملة عن <b>تقسيم البيانات</b> "
    "فهي التحقّق المتقاطع؛ وإن كانت عن <b>الصور</b> فهي الرؤية الحاسوبية.",
)

# ═══════════════════════════ الخلاصة ═══════════════════════════

ui.takeaways(
    [
        "<b>معظم «صعوبة» الذكاء الاصطناعي على الباحث الإحصائي صعوبة مصطلحية "
        "لا رياضية.</b> أنت تعرف المفهوم تحت اسم آخر في الغالب.",
        "ثلاثة أنماط التباس: <b>مُرادفات عبر الحقول</b>، و<b>اسم واحد بمعانٍ "
        "متعدّدة</b>، و<b>ترجمة عربية غير مستقرّة</b>. تحديد النمط يحلّ المشكلة.",
        "<code>Sample</code> تعني في ML <b>مشاهدة واحدة</b> غالباً، لا العيّنة "
        "كلها. و<code>Inference</code> تعني <b>زمن التنبؤ</b> لا الاستدلال.",
        "<code>Bias</code> ثلاث كلمات مختلفة تحمل اللفظ نفسه: تحيّز إحصائي، "
        "وحدّ ثابت، وإجحاف اجتماعي.",
        "الممارسة الكتابية السليمة: <b>العربية ثم الإنجليزية بين قوسين في أول "
        "ورود</b>، ثم الإنجليزية وحدها. لا تخترع ترجمة جديدة.",
        "لا تحفظ المعجم. <b>عُد إليه.</b> الفهم يتراكم بالاستعمال لا بالحفظ.",
    ],
    accent=a,
)

st.markdown("## أخطاء شائعة في هذه المرحلة")

ui.pitfalls(
    [
        ("«أترجم كل مصطلح إلى العربية حتى لو لم تستقرّ الترجمة»",
         "الترجمة غير المستقرّة تُعزل قارئك عن الأدبيات. "
         "اكتب العربية والإنجليزية معاً، فالهدف أن يستطيع القارئ "
         "<b>البحث</b> عن المصطلح لاحقاً."),
        ("«Logistic Regression انحدار، فهو من مسائل الانحدار»",
         "في تصنيف تعلّم الآلة هو <b>مُصنِّف</b>، لأن مُخرَجه فئة لا عدد متّصل. "
         "الاسم تاريخي، والتصنيف وظيفي."),
        ("«Bias في الشبكة العصبية مشكلة يجب التخلّص منها»",
         "إنه <b>معامل الإزاحة</b>، جزء ضروري من المعادلة. "
         "خلطُه بالتحيّز الإحصائي أو الاجتماعي خطأ كامل."),
        ("«n_samples = 1000 تعني ألف عيّنة»",
         "تعني <b>ألف مشاهدة</b> — عيّنة واحدة فيها ألف صفّ."),
        ("«Validation و Test مترادفان»",
         "<b>التحقّق</b> يُستعمل مراراً لضبط المعاملات الفائقة، "
         "و<b>الاختبار</b> يُفتح <b>مرّة واحدة</b> في النهاية. "
         "خلطهما يُفسد التقييم كلّه."),
        ("«حفظتُ المعجم فصرتُ أفهم الحقل»",
         "المصطلح بوّابة لا غاية. الفهم يأتي من رؤية المفهوم يعمل داخل مثال، "
         "وهو ما تفعله المحاضرات التالية."),
    ]
)

ui.sources(
    [
        ("Hastie, Tibshirani &amp; Friedman — <i>The Elements of Statistical "
         "Learning</i> — الفصل الأول يُقابل بين مفردات الحقلين صراحةً",
         "ISBN 978-0387848570"),
        ("Breiman, L. (2001) — <i>Statistical Modeling: The Two Cultures</i>, "
         "<i>Statistical Science</i> 16(3) — مصدر الاختلاف في معنى «النموذج»",
         "doi:10.1214/ss/1009213726"),
        ("Russell, S. &amp; Norvig, P. — <i>Artificial Intelligence: A Modern "
         "Approach</i>, 4th ed. — المسرد في آخر الكتاب",
         "ISBN 978-0134610993"),
        ("Goodfellow, Bengio &amp; Courville (2016) — <i>Deep Learning</i>, "
         "MIT Press — مفردات الشبكات العصبية",
         "ISBN 978-0262035613"),
        ("وثائق <code>scikit-learn</code> — قسم "
         "<i>Glossary of Common Terms and API Elements</i> — "
         "المرجع العملي لاستعمال المصطلح في الكود",
         "scikit-learn.org/stable/glossary.html"),
    ],
    accent=a,
)

ui.page_footer(
    accent=a,
    prev_hint="الخوارزمية والنموذج والبرنامج",
    next_hint="تاريخ المفهوم وتطوّره",
)
