from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

PROMPTS = {
    'Firm': "You are an executive coach for US office workers. User got an angry email from boss/client. Rewrite 3 SHORT replies, <80 words each. Tone: Firm, no apology, give clear ETA and ask 1 clarifying question. Sound like McKinsey consultant. Output format: 1.... 2.... 3....",
    'Polite No': "You are an executive coach. User got a stupid request. Rewrite 3 SHORT replies, <80 words. Tone: Polite rejection. Say no but offer alternative. Never say 'I don't have bandwidth'. Output: 1.... 2.... 3....",
    'Delay': "You are an executive coach. User needs more time. Rewrite 3 SHORT replies, <80 words. Tone: Buy time professionally. Blame process/data, not yourself. Give new ETA. Output: 1.... 2.... 3....",
    'Professional Warning': "You are an HR-compliant manager. User needs to warn employee about performance. Rewrite 3 SHORT replies, <80 words. Tone: Document pattern, state impact, mention next step. No insults, no illegal threats. Output: 1.... 2.... 3....",
    'Direct': "You are a direct US manager. User needs to give clear order. Rewrite 3 SHORT replies, <80 words. Tone: Blunt, specific, deadline. No fluff. Output: 1.... 2.... 3....",
    'Savage': "You are a McKinsey Partner. User needs to criticize subordinate. Rewrite 3 replies, <80 words. Tone: Polite wording but high damage. Point out gap vs expectation. No swear words. Output: 1.... 2.... 3...."
}

HTML = '''<!DOCTYPE html><html><head><title>ToneFixer</title>
<style>body{font-family:Arial;max-width:700px;margin:40px auto;padding:20px}
textarea{width:100%;height:140px;margin:10px 0;padding:10px}button{background:#4F46E5;color:white;padding:12px 24px;border:none;border-radius:8px;cursor:pointer}
select,button{font-size:16px}.result{background:#f3f4f6;padding:15px;margin-top:20px;white-space:pre-wrap}</style></head>
<body><h2>ToneFixer - Rewrite Your Angry Email</h2>
<textarea id="email" placeholder="Paste the angry email you received..."></textarea><br>
<select id="tone">{% for k in tones %}<option>{{k}}</option>{% endfor %}</select>
<button onclick="gen()">Generate 3 Replies</button>
<div id="result" class="result"></div>
<script>
async function gen(){
  const res = await fetch('/generate',{method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({email:document.getElementById('email').value,tone:document.getElementById('tone').value})});
  const data = await res.json();
  document.getElementById('result').innerText = data.result || data.error;
}
</script></body></html>'''

@app.route('/')
def index():
    return render_template_string(HTML, tones=PROMPTS.keys())

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    email_text = data.get('email','')
    tone = data.get('tone','Firm')
    if not email_text: return jsonify({'error':'Email trống'}), 400

    prompt = f"{PROMPTS[tone]}\n\nOriginal email: {email_text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=400
        )
        result = response.choices[0].message.content
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dòng này cho Vercel
app = app
