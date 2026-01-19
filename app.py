from flask import Flask, request, jsonify
import joblib
import pandas as pd
import traceback

app = Flask(__name__)

model = joblib.load("churn_pipeline.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Expected columns from training
        expected_cols = model.feature_names_in_

        # Build input row
        input_row = {col: data.get(col, None) for col in expected_cols}
        input_df = pd.DataFrame([input_row])

        prob = model.predict_proba(input_df)[0][1]

        return jsonify({
            "churn_probability": float(prob)
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
