export default async function handler(req, res) {
  if (req.method!== 'POST') return res.status(405).end();

  const { text, tone } = req.body;
  const key = process.env.OPENAI_API_KEY;

  if (!key) return res.status(500).json({error: 'Thiếu API key'});

  try {
    const r = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json'},
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [{role: 'user', content: `Biến câu này thành 3 phiên bản tone ${tone}: "${text}"`}]
      })
    });
    const data = await r.json();
    const out = data.choices[0].message.content.split('\n').filter(x=>x);
    res.json({results: out.slice(0,3)});
  } catch(e) {
    res.status(500).json({error: 'API lỗi'});
  }
}
