export default async function handler(req, res) {
  if (req.method!== 'POST') {
    return res.status(405).json({ error: 'Chỉ nhận POST' });
  }

  const { text, tone } = req.body;
  const key = process.env.OPENAI_API_KEY;

  if (!key) {
    return res.status(500).json({ error: 'Thiếu OPENAI_API_KEY' });
  }
  if (!text) {
    return res.status(400).json({ error: 'Thiếu text' });
  }

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

    const data = await r.json();

    // Chống crash nếu API trả lỗi
    if (!data.choices ||!data.choices[0]) {
      return res.status(500).json({ error: data.error?.message || 'OpenAI lỗi' });
    }

    const out = data.choices[0].message.content
     .split('\n')
     .filter(x => x.trim())
     .slice(0, 3);

    res.status(200).json({ results: out });
  } catch(e) {
    res.status(500).json({ error: 'Server crash: ' + e.message });
  }
}
