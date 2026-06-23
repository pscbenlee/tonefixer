export default async function handler(req, res) {
  if (req.method!== 'POST') {
    return res.status(405).json({ error: 'Chỉ nhận POST' });
  }

  let body;
  try {
    body = typeof req.body === 'string'? JSON.parse(req.body) : req.body;
  } catch {
    return res.status(400).json({ error: 'Body JSON sai' });
  }

  const { text, tone } = body;
  const key = process.env.OPENAI_API_KEY;

  if (!key) return res.status(500).json({ error: 'Thiếu OPENAI_API_KEY' });
  if (!text) return res.status(400).json({ error: 'Thiếu text' });

  try {
    const r = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${key}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [{
          role: 'user',
          content: `Biến câu sau thành 3 phiên bản tone ${tone}, mỗi câu 1 dòng: "${text}"`
        }]
      })
    });

    if (!r.ok) {
      const err = await r.json();
      return res.status(500).json({ error: err.error?.message || 'OpenAI lỗi' });
    }

    const data = await r.json();
    const out = data.choices[0].message.content
     .split('\n')
     .filter(x => x.trim())
     .slice(0, 3);

    res.status(200).json({ results: out });
  } catch(e) {
    res.status(500).json({ error: 'Server crash: ' + e.message });
  }
}
