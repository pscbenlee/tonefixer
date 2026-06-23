from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

PROMPTS = {
    'thân thiện': "You are a Vietnamese social media manager. Rewrite 3 SHORT replies to this comment, <50 words each. Tone: Friendly, warm, build relationship. Use Vietnamese. Output: 1... 2... 3...",
    'hài hước': "You are a funny Vietnamese content creator. Rewrite 3 SHORT witty replies, <50 words each. Tone: Humorous, meme-style but not offensive. Use Vietnamese. Output: 1... 2... 3...",
    'chuyên nghiệp': "You are a PR expert. Rewrite 3 SHORT professional replies, <50 words each. Tone: Professional, respectful, de-escalate conflict. Use Vietnamese. Output: 1... 2... 3...",
    'cà khịa': "You are a sharp Vietnamese copywriter. Rewrite 3 SHORT savage replies, <50 words each. Tone: Polite wording but high damage, clap back smartly. No swear words. Use Vietnamese. Output: 1... 2... 3..."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    comment = data.get('comment','') # HTML gửi 'comment'
    tone = data.get('tone','thân thiện')
    if not comment: return jsonify({'error':'Comment trống'}), 400

    prompt = f"{PROMPTS[tone]}\n\nOriginal comment: {comment}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.8,
            max_tokens=300
        )
        result = response.choices[0].message.content
        return jsonify({'result': result}) # Trả về 'result' cho khớp JS
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dòng này cho Vercel
app = app
