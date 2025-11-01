from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow HTML frontend to call backend

API_URL = "https://endpoint.apilageai.lk/api/chat"
API_KEY = "apk_XwuCVjtcrrCEePZqhfkmz4wiSQ1qlR9T"
MODEL = "APILAGEAI-FREE"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    try:
        response = requests.post(
            API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "message": user_input,
                "enableGoogleSearch": True,
                "model": MODEL
            },
            timeout=15
        )

        if response.status_code == 200:
            res_data = response.json()
            return jsonify({
                "reply": res_data.get("response", "No reply"),
                "credits_used": res_data.get("credits_used")
            })
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
