"""
app.py
------
Gradio front-end for income prediction.
Loads the trained model once via predictor.py and keeps UI logic here.
"""

import gradio as gr
from predictor import (
    predict,
    WORKCLASS_OPTIONS,
    MARITAL_OPTIONS,
    OCCUPATION_OPTIONS,
    RELATIONSHIP_OPTIONS,
    RACE_OPTIONS,
    SEX_OPTIONS,
    COUNTRY_OPTIONS,
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
CSS = """
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* ── Page background ── */
.gradio-container {
    background: #f0f4f8 !important;
    min-height: 100vh;
}

/* ── App title block ── */
#app-title {
    text-align: center;
    padding: 2rem 1rem 1rem;
}

#app-title h1 {
    font-size: 1.9rem;
    font-weight: 700;
    color: #1a202c;
    letter-spacing: -0.5px;
    margin-bottom: 0.35rem;
}

#app-title p {
    font-size: 0.95rem;
    color: #718096;
    margin: 0;
}

/* ── Card panels ── */
#form-panel, #result-panel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* ── Section labels inside cards ── */
.section-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #4a5568;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #edf2f7;
    padding-bottom: 0.4rem;
}

/* ── Input labels ── */
label span {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #2d3748 !important;
}

/* ── Submit button ── */
#submit-btn {
    background: #2563eb !important;
    border: none !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 0.7rem 0 !important;
    cursor: pointer !important;
    transition: background 0.2s ease !important;
    width: 100%;
}

#submit-btn:hover {
    background: #1d4ed8 !important;
}

/* ── Result box ── */
#result-box {
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    font-size: 1rem;
    font-weight: 500;
    line-height: 1.6;
    min-height: 80px;
}

/* ── Error messages ── */
.error-msg {
    color: #c53030;
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #edf2f7;
    margin: 1rem 0;
}

/* ── Responsive tweaks ── */
@media (max-width: 640px) {
    #app-title h1 { font-size: 1.4rem; }
    #form-panel, #result-panel { padding: 1.2rem 1rem; }
}
"""

# ── Validation helper ──────────────────────────────────────────────────────────
def _validate(age, education_num, hours_per_week, capital_gain, capital_loss):
    errors = []
    if age is None or age < 17 or age > 90:
        errors.append("• Age must be between 17 and 90.")
    if education_num is None or education_num < 1 or education_num > 16:
        errors.append("• Years of education must be between 1 and 16.")
    if hours_per_week is None or hours_per_week < 1 or hours_per_week > 99:
        errors.append("• Hours per week must be between 1 and 99.")
    if capital_gain is None or capital_gain < 0:
        errors.append("• Capital gain cannot be negative.")
    if capital_loss is None or capital_loss < 0:
        errors.append("• Capital loss cannot be negative.")
    return errors


# ── Main prediction handler ────────────────────────────────────────────────────
def run_prediction(
    age, workclass, education_num, marital_status, occupation,
    relationship, race, sex, capital_gain, capital_loss,
    hours_per_week, native_country
):
    # Validate inputs first
    errors = _validate(age, education_num, hours_per_week, capital_gain, capital_loss)
    if errors:
        msg = "Please fix the following before submitting:\n\n" + "\n".join(errors)
        return gr.update(value=msg, visible=True)

    # Run prediction
    try:
        label, confidence = predict(
            age, workclass, education_num, marital_status, occupation,
            relationship, race, sex, capital_gain, capital_loss,
            hours_per_week, native_country
        )
        if label == ">50K":
            result_text = (
                f"**Estimated Annual Income:  > $50,000**\n\n"
                f"Confidence: {confidence}%"
            )
        else:
            result_text = (
                f"**Estimated Annual Income:  ≤ $50,000**\n\n"
                f"Confidence: {confidence}%"
            )
        return gr.update(value=result_text, visible=True)

    except Exception as exc:
        return gr.update(
            value=f"An unexpected error occurred: {exc}",
            visible=True,
        )


# ── Build UI ───────────────────────────────────────────────────────────────────
with gr.Blocks(title="Income Estimator") as demo:

    # Title
    gr.HTML("""
    <div id="app-title">
        <h1>Income Estimator</h1>
        <p>Fill in the details below and press <strong>Get Estimate</strong> to see the result.</p>
    </div>
    """)

    with gr.Row(equal_height=False):
        # ── Left / Form column ─────────────────────────────────────────────────
        with gr.Column(scale=3, elem_id="form-panel"):

            gr.HTML('<div class="section-label">Personal Details</div>')

            with gr.Row():
                age = gr.Number(
                    label="Age",
                    value=30,
                    minimum=17,
                    maximum=90,
                    precision=0,
                )
                sex = gr.Dropdown(
                    label="Sex",
                    choices=SEX_OPTIONS,
                    value="Male",
                )
                race = gr.Dropdown(
                    label="Race",
                    choices=RACE_OPTIONS,
                    value="White",
                )

            with gr.Row():
                marital_status = gr.Dropdown(
                    label="Marital Status",
                    choices=MARITAL_OPTIONS,
                    value="Never-married",
                )
                relationship = gr.Dropdown(
                    label="Relationship",
                    choices=RELATIONSHIP_OPTIONS,
                    value="Not-in-family",
                )
                native_country = gr.Dropdown(
                    label="Country of Origin",
                    choices=COUNTRY_OPTIONS,
                    value="United-States",
                )

            gr.HTML('<hr class="divider"><div class="section-label">Employment</div>')

            with gr.Row():
                workclass = gr.Dropdown(
                    label="Work Class",
                    choices=WORKCLASS_OPTIONS,
                    value="Private",
                )
                occupation = gr.Dropdown(
                    label="Occupation",
                    choices=OCCUPATION_OPTIONS,
                    value="Adm-clerical",
                )
                hours_per_week = gr.Number(
                    label="Hours per Week",
                    value=40,
                    minimum=1,
                    maximum=99,
                    precision=0,
                )

            gr.HTML('<hr class="divider"><div class="section-label">Education &amp; Finances</div>')

            with gr.Row():
                education_num = gr.Number(
                    label="Years of Education (1 – 16)",
                    value=10,
                    minimum=1,
                    maximum=16,
                    precision=0,
                )
                capital_gain = gr.Number(
                    label="Capital Gain ($)",
                    value=0,
                    minimum=0,
                    precision=0,
                )
                capital_loss = gr.Number(
                    label="Capital Loss ($)",
                    value=0,
                    minimum=0,
                    precision=0,
                )

            submit_btn = gr.Button("Get Estimate", elem_id="submit-btn", variant="primary")

        # ── Right / Result column ──────────────────────────────────────────────
        with gr.Column(scale=2, elem_id="result-panel"):
            gr.HTML('<div class="section-label">Result</div>')

            result_box = gr.Markdown(
                value="Your result will appear here after you press **Get Estimate**.",
                elem_id="result-box",
            )

    # ── Wire up the button ─────────────────────────────────────────────────────
    submit_btn.click(
        fn=run_prediction,
        inputs=[
            age, workclass, education_num, marital_status, occupation,
            relationship, race, sex, capital_gain, capital_loss,
            hours_per_week, native_country,
        ],
        outputs=result_box,
    )


# ── Launch ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(css=CSS)
