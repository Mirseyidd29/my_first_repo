import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

BASE = Path(__file__).parent.parent

with open(BASE / "products.json", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

with open(BASE / "backend" / "store_info.json", encoding="utf-8") as f:
    STORE = json.load(f)


def _product_list() -> str:
    lines = []
    for p in PRODUCTS:
        lines.append(
            f"{p['name']} | {p.get('brand', '-')} | {p['price']} | {p['category']} | {p['url']}"
        )
    return "\n".join(lines)


SYSTEM_PROMPT = f"""Sən Atlas-san — atlet.az idman qidası mağazasının köməkçisi.

DANIŞIQ TƏRZI:
Səmimi və isti danış — nə çox formal, nə də süni mehriban. Sadə, aydın Azərbaycan dilindən istifadə et. Qısa cavab ver, 2-4 cümlə kifayətdir. Bullet point, markdown, başlıq, nömrələmə işlətmə — düz cümlə yaz. "Əlbəttə!", "Sizi anladım", "Sizə kömək etməkdən məmnunam", "Ay qardaş" kimi süni ifadələr işlətmə. Yalnız Azərbaycan dilində cavab ver.

MƏHSUL TÖVSIYƏSI:
İstifadəçi birbaşa məhsul və ya tövsiyə istəyəndə məhsul təklif et. Ümumi sual gəlsə əvvəlcə suala cavab ver, sonra lazım gələrsə məhsul əlavə et. Məhsul tövsiyə edəndə yalnız aşağıdakı real datadan istifadə et, uydurmaq olmaz. URL-i mütləq ver.

MƏHDUDIYYƏTLƏR:
Tibbi sual gəlsə qısa məlumat ver, sonra "daha ətraflı üçün həkimə müraciət et" de. Sifariş qəbul etmə, atlet.az saytına yönləndir.

MAĞAZA MƏLUMATI:
{json.dumps(STORE, ensure_ascii=False, indent=2)}

MƏHSULLAR (ad | brend | qiymət | kateqoriya | url):
{_product_list()}"""


def get_reply(message: str, history: list) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in history:
        role = "user" if msg.role == "user" else "assistant"
        messages.append({"role": role, "content": msg.content})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )
    return response.choices[0].message.content
