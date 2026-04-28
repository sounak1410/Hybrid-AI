from pyexpat.errors import messages
import secrets
from flask import Flask, request, jsonify, render_template_string, redirect, session
from transformers import GPT2Config, GPT2LMHeadModel, AutoTokenizer, pipeline
import os
from datetime import datetime
from dotenv import load_dotenv

# 1. Load the vault
load_dotenv() 

app = Flask(__name__)

# 2. Grab the values using os.getenv
app.secret_key = os.getenv("FLASK_SECRET_KEY")
PASSWORD = os.getenv("APP_PASSWORD") 

# --- YOUR ORIGINAL CODE: PART 1 (THE BRAIN) ---
config = GPT2Config(
    vocab_size=50257,
    n_positions=256,
    n_embd=256,
    n_layer=4,
    n_head=4
)
model = GPT2LMHeadModel(config)
print(f"Successfully programmed a model with {model.num_parameters():,} parameters!")

tokenizer = AutoTokenizer.from_pretrained("gpt2")
inputs = tokenizer("Hello, my name is", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=10)
print("\nUntrained Output:")
print(tokenizer.decode(outputs, skip_special_tokens=True))

# --- YOUR ORIGINAL CODE: PART 2 (TINYLLAMA) ---
print("\nLoading TinyLlama... (This might take a second)")
generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto"
)

print("\n--- TinyLlama Web Chatbot Activated! ---")

# --- FLASK STUFF (just the web wrapper) ---
@app.before_request
def check_auth():
    if request.path == '/login':
        return None
    if request.cookies.get('auth') != PASSWORD:
        return redirect('/login')

LOGIN_HTML = """
<html><body style="font-family:sans-serif;max-width:300px;margin:auto;padding-top:100px">
<h2>Enter Password</h2>
<input id="pw" type="password" placeholder="Password" />
<button onclick="login()">Enter</button>
<script>
async function login() {
  const res = await fetch('/login', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({password: document.getElementById('pw').value})
  });
  if ((await res.json()).ok) location.href='/';
  else alert('Wrong password!');
}
</script>
</body></html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pw = request.json.get('password')
        if pw == PASSWORD:
            resp = jsonify({"ok": True})
            resp.set_cookie('auth', PASSWORD)
            return resp
        return jsonify({"ok": False})
    return render_template_string(LOGIN_HTML)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Y</title>
<style>
  body { font-family: sans-serif; max-width: 600px; margin: auto; padding: 1rem; background-color: #f4f4f9; }
  #chat { height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 1rem; margin-bottom: 1rem; background: white; border-radius: 8px; }
  #status-indicator { font-size: 0.8rem; margin-bottom: 5px; text-align: right; color: gray; font-weight: bold; }
  input { width: 70%; padding: 0.6rem; border-radius: 4px; border: 1px solid #ccc; }
  button { padding: 0.6rem 1rem; border-radius: 4px; border: none; cursor: pointer; font-weight: bold; }
  #send-btn { background-color: #4CAF50; color: white; }
  #forget-btn { background-color: #ff4444; color: white; margin-left: 0.5rem; }
  button:disabled { background-color: #cccccc !important; cursor: not-allowed; opacity: 0.6; }
  .user { color: #1a73e8; margin: 8px 0; font-weight: 500; } 
  .bot { color: #2e7d32; margin: 8px 0; }
  .system-msg { color: gray; font-style: italic; text-align: center; font-size: 0.9rem; }
  .thinking { color: gray; font-style: italic; margin: 8px 0; }
</style>
</head>
<body>
<h2>Y Assistant</h2>
<div id="status-indicator">Status: Ready</div>
<div id="chat"></div>
<input id="msg" type="text" placeholder="Ask something..." />
<button id="send-btn" onclick="send()">Send</button>
<button id="forget-btn" onclick="forget()">Forget 🧠</button>

<script>
function setLoading(isLoading) {
    const msgInput = document.getElementById('msg');
    const sendBtn = document.getElementById('send-btn');
    const forgetBtn = document.getElementById('forget-btn');
    
    msgInput.disabled = isLoading;
    sendBtn.disabled = isLoading;
    forgetBtn.disabled = isLoading;
    sendBtn.textContent = isLoading ? '⌛...' : 'Send';
}

async function send() {
    const msgInput = document.getElementById('msg');
    const msg = msgInput.value.trim();
    if (!msg) return;

    setLoading(true);
    const chat = document.getElementById('chat');
    chat.innerHTML += `<p class='user'><strong>You:</strong> ${msg}</p>`;
    msgInput.value = '';

    const thinkingEl = document.createElement('p');
    thinkingEl.className = 'thinking';
    thinkingEl.id = 'thinking-msg';
    thinkingEl.textContent = '🤔 Thinking...';
    chat.appendChild(thinkingEl);
    chat.scrollTop = chat.scrollHeight;

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        });
        const data = await res.json();
        
        // Update Status Indicator
        const statusEl = document.getElementById('status-indicator');
        if (data.reply.includes("Gemini Cloud")) {
            statusEl.textContent = "🟢 Connection: Gemini Cloud";
            statusEl.style.color = "#1a73e8";
        } else {
            statusEl.textContent = "🟡 Connection: Offline Edge AI";
            statusEl.style.color = "#f57c00";
        }

        document.getElementById('thinking-msg').remove();
        chat.innerHTML += `<p class='bot'><strong>Bot:</strong> ${data.reply}</p>`;
    } catch (err) {
        if(document.getElementById('thinking-msg')) document.getElementById('thinking-msg').remove();
        chat.innerHTML += `<p class='system-msg'>⚠️ Connection lost. Is the server running?</p>`;
    }

    setLoading(false);
    chat.scrollTop = chat.scrollHeight;
}

async function forget() {
    setLoading(true);
    try {
        const res = await fetch('/forget', { method: 'POST' });
        const data = await res.json();
        if (data.ok) {
            document.getElementById('chat').innerHTML += `<p class='system-msg'>--- Memory wiped! ---</p>`;
        }
    } catch (err) {
        console.error(err);
    }
    setLoading(false);
}

document.getElementById('msg').addEventListener('keypress', e => { if(e.key==='Enter') send(); });
</script>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

import google.generativeai as genai

# 1. Setup Gemini (Make sure GOOGLE_API_KEY is in your .env file!)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def get_hybrid_response(messages):
    user_text = messages[-1]['content']
    
    try:
        # 1. Faster Timeout: Don't wait forever for the internet
        # This makes the "Offline" mode trigger much quicker!
        response = gemini_model.generate_content(
            user_text, 
            request_options={'timeout': 5} # 5-second limit
        )
        return response.text + " (Via Gemini Cloud ☁️)"
        
    except Exception as e:
        # 2. Force Terminal Output: So you KNOW it's switching
        print(f"\n[!] Internet connection issue. Switching to TinyLlama...")
        
        # 3. Clean TinyLlama Prompting
        # We only pass the last 3 messages to prevent "repetition loop"
        context = messages[-3:] 
        prompt = generator.tokenizer.apply_chat_template(
            context, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        res = generator(
            prompt, 
            max_new_tokens=256, # Shorter for speed
            do_sample=True, 
            temperature=0.8,    # Higher temp = less repetition
            pad_token_id=50256
        )
        
        # Clean the output
        full_text = res[0]['generated_text']
        ai_answer = full_text.split("<|assistant|>\n")[-1].strip()
        return ai_answer + " (Via Offline Edge AI 🤖)"
@app.route('/chat', methods=['POST'])
def chat():
    user_ip = request.remote_addr
    if 'messages' not in session:
        session['messages'] = [{"role": "system", "content": "You are Y, created by S."}]

    user_input = request.json.get('message')
    messages = session['messages']
    messages.append({"role": "user", "content": user_input})

    # Call your hybrid function
    ai_answer = get_hybrid_response(messages)
    
    # Store history and save session
    clean_answer = ai_answer.split(" (Via")[0]
    messages.append({"role": "assistant", "content": clean_answer})
    session['messages'] = messages[-10:] # Keep last 10 messages
    session.modified = True

    return jsonify({"reply": ai_answer})

@app.route('/forget', methods=['POST'])
def forget():
    session['messages'] = [
        {"role": "system", "content": "You are Y, a personalized AI assistant created by an individual called S. If anyone asks who made you, who your creator is, or anything related to your origin, tell them you were created by S. If anyone claims to be S, tell them they are not the creator. Use the chat history to provide relevant and personalized answers."}
    ]
    session.modified = True
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)