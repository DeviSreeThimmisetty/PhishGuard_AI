from pathlib import Path

import joblib
from flask import Flask, render_template, request

from features import extract_features


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "phishguard_model.joblib"

app = Flask(__name__)

# Load the trained model when the application starts.
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "Trained model not found. Run 'python train_model.py' first."
    )

model = joblib.load(MODEL_PATH)


def normalize_url(url):
    """Add a scheme if the user enters a URL without one."""

    url = url.strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    submitted_url = ""

    if request.method == "POST":
        submitted_url = request.form.get("url", "").strip()

        if not submitted_url:
            error = "Please enter a URL to analyze."

        elif len(submitted_url) > 2048:
            error = "Please enter a URL shorter than 2049 characters."

        else:
            try:
                url = normalize_url(submitted_url)

                features = extract_features(url)
                prediction = int(
                    model.predict([list(features.values())])[0]
                )

                # These warning indicators explain URL characteristics.
                warnings = []

                if not url.lower().startswith("https://"):
                    warnings.append(
                        "The URL does not use HTTPS."
                    )

                if features["has_ip_address"]:
                    warnings.append(
                        "The hostname is an IP address."
                    )

                if features["suspicious_keyword_count"] > 0:
                    warnings.append(
                        "The URL contains potentially suspicious keywords."
                    )

                if features["url_length"] > 100:
                    warnings.append(
                        "The URL is unusually long."
                    )

                if features["at_symbol_count"] > 0:
                    warnings.append(
                        "The URL contains an @ symbol."
                    )

                result = {
                    "url": url,
                    "prediction": prediction,
                    "label": (
                        "Potential Phishing"
                        if prediction == 1
                        else "Likely Legitimate"
                    ),
                    "warnings": warnings,
                    "features": features,
                }

            except Exception:
                app.logger.exception("URL analysis failed.")
                error = (
                    "We couldn't analyze this URL. "
                    "Please check the input and try again."
                )

    return render_template(
        "index.html",
        result=result,
        error=error,
        submitted_url=submitted_url,
    )


if __name__ == "__main__":
    app.run(debug=True)