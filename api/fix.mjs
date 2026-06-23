export default async function handler(req, res) {
  if (req.method!== 'POST') return res.status(405).end();

  try {
    const { text, tone } = req.body;
    const key = process.env.OPENAI_API_KEY;

    if (!key) return res.status(500).json({ error: 'Thiếu OPENAI_API_KEY trên Vercel' });
    if (!text) return res.status(400).json({ error: 'Thiếu text' });

    const r = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        messages: [
          {role: 'system', content: `Bạn là trợ lý đổi tone. Viết lại câu theo tone: ${tone}. Trả về đúng 3 phiên bản, mỗi dòng 1 phiên bản, không đánh số.`},
          {role: 'user', content: text}
        ],
        temperature: 0.8
      })
    });

    const data = await r.json();
    if (!r.ok) return res.status(r.status).json({ error: data.error?.message || 'OpenAI lỗi' });

    const content = data.choices[0].message.content;
    const versions = content.split('\n').filter(x => x.trim()).slice(0, 3);

    return res.status(200).json({ versions });

  } catch (e) {
    return res.status(500).json({ error: 'Lỗi server: ' + e.message });
  }
}
