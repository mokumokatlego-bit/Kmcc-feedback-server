from flask import Flask, request, jsonify
from feedback_engine import init_db, process_incoming_feedback

app = Flask(__name__)

init_db()

@app.route("/", methods=["GET"])
def home():
    return "K.M.C.C. Feedback Server is active and running!"

@app.route("/webhook", methods=["POST"])
def incoming_webhook():
    data = request.get_json() or {}
    source = data.get("source", "WhatsApp")
    customer_id = data.get("customer_id", "Unknown")
    message = data.get("message", "")

    if not message:
        return jsonify({"status": "error", "message": "No message provided"}), 400

    category, response_msg = process_incoming_feedback(source, customer_id, message)

    return jsonify({
        "status": "success",
        "category_detected": category,
        "reply_to_send": response_msg
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
