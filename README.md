# Income Estimator — Gradio Web Interface

A clean, professional web interface that estimates annual income (above or below $50,000) based on personal and employment information.

## Project Structure

```
Task_4/
├── app.py                   # Gradio UI (front-end only)
├── predictor.py             # Prediction logic (back-end only)
├── income_model.joblib      # Pre-trained model
├── model_columns.joblib     # Training column names
├── adult_income.csv         # Original dataset
├── adult_income_simple.ipynb # Training notebook
└── Task_4.ipynb             # Full analysis notebook
```

## How to Run

### 1. Install dependencies
```bash
pip install gradio joblib pandas scikit-learn
```

### 2. Launch the app
```bash
python app.py
```

### 3. Open in your browser
```
http://127.0.0.1:7860
```

## Input Fields

| Field | Type | Description |
|-------|------|-------------|
| Age | Number | 17 – 90 |
| Sex | Dropdown | Male / Female |
| Race | Dropdown | 5 options |
| Marital Status | Dropdown | 7 options |
| Relationship | Dropdown | 6 options |
| Country of Origin | Dropdown | 42 countries |
| Work Class | Dropdown | 9 options |
| Occupation | Dropdown | 15 options |
| Hours per Week | Number | 1 – 99 |
| Years of Education | Number | 1 – 16 |
| Capital Gain | Number | ≥ 0 |
| Capital Loss | Number | ≥ 0 |

## Output

The app displays the estimated income bracket (`> $50,000` or `≤ $50,000`) along with a confidence percentage.
