import gradio as gr
import requests
import uuid

# =========================
# CONFIGURATION
# =========================

API_KEY = "sk-IVxkS6Z85cblhFLAB3CGouVYevcja38ZYtKI2uegfzU"

FLOW_ID = "b2d2422f-16e5-4e24-b470-4465033f1ddc"

# Example:
# BASE_URL = "https://your-langflow-app.onrender.com"

BASE_URL = "https://yhraje-nutri24.hf.space""

API_URL = f"{BASE_URL}/api/v1/run/{FLOW_ID}"


# =========================
# CHAT FUNCTION
# =========================

def chat_with_langflow(message, history):

    payload = {
        "input_value": message,
        "input_type": "chat",
        "output_type": "chat",
        "session_id": str(uuid.uuid4())
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        # Default response
        bot_response = str(data)

        # Extract Langflow text response
        try:
            bot_response = (
                data["outputs"][0]
                ["outputs"][0]
                ["results"]["message"]["text"]
            )
        except Exception:
            pass

        return bot_response

    except requests.exceptions.RequestException as e:
        return f"API Request Error:\n{str(e)}"

    except Exception as e:
        return f"Unexpected Error:\n{str(e)}"


# =========================
# GRADIO UI
# =========================

demo = gr.ChatInterface(
    fn=chat_with_langflow,
    title="Langflow Chatbot",
    description="Chat with your Langflow API"
    
)

# =========================
# APP LAUNCH
# =========================

if __name__ == "__main__":
    demo.launch()