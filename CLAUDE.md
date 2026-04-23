# CLAUDE.md — Atlas AI Chatbot
> Bu fayl Claude Code üçün layihə yaddaşıdır. Hər session-da oxu.

---

## 🧠 Layihə Haqqında

**Ad:** Atlas  
**Məqsəd:** atlet.az (Azərbaycanlı idman qidası mağazası) üçün Azərbaycan dilində AI chatbot  
**Hədəf istifadəçi:** Azərbaycanda idmanla məşğul olan, supplement alan müştərilər  
**Portfolio məqsədi:** GitHub portfolio üçün real-world full-stack AI layihəsi  

---

## 🎯 Atlas Nə Edir?

Atlas, atlet.az müştərilərinə aşağıdakı mövzularda kömək edir:

| Funksiya | Təsvir |
|---|---|
| Məhsul tövsiyəsi | İstifadəçinin hədəfinə (kütlə qazanmaq, yağ yandırmaq, güc vs.) görə uyğun məhsul təklif edir |
| Qiymət müqayisəsi | Eyni kateqoriyada fərqli məhsulların qiymət/həcm nisbətini müqayisə edir |
| Egzersiz məsləhəti | Supplement ilə əlaqəli əsas egzersiz suallarına cavab verir (protein nə vaxt, creatine necə) |
| Sifariş/Əlaqə | İstifadəçini atlet.az saytına və ya əlaqə kanallarına yönləndirir |
| Filial məlumatı | Bakıdakı filiallar haqqında məlumat verir |
| Çatdırılma məlumatı | Çatdırılma şərtləri, müddəti, ödəniş barədə məlumat verir |

---

## 🏗️ Texniki Arxitektura

```
atlas/
├── backend/
│   ├── main.py              # FastAPI app, API endpoint-lər
│   ├── chat.py              # Gemini API inteqrasiyası, system prompt
│   ├── scraper.py           # atlet.az məhsul scraper
│   ├── products.json        # Scraped məhsul datası (96 məhsul, 9 kateqoriya)
│   └── store_info.json      # Filial, çatdırılma, əlaqə məlumatları
├── frontend/
│   ├── index.html           # Əsas səhifə (Tailwind CDN ilə)
│   ├── style.css            # Əlavə custom CSS (minimal)
│   └── app.js               # Chat UI məntiqi, API çağırışları
├── requirements.txt
├── .env                     # GEMINI_API_KEY (git-ə əlavə edilməyəcək)
├── .gitignore
└── CLAUDE.md                # Bu fayl
```

---

## ⚙️ Tech Stack

| Layer | Texnologiya | Səbəb |
|---|---|---|
| AI Model | Google Gemini 2.0 Flash | Azərbaycanca dəstək, pulsuz tier |
| Backend | FastAPI (Python) | Sürətli, modern, öyrənmə üçün ideal |
| Frontend | HTML + Tailwind CSS + Vanilla JS | Build step yoxdur, professional görünüş |
| Data | JSON (scraped) | Real məhsul datası, hallucination yoxdur |
| Deploy | Localhost (uvicorn) | Portfolio demo |
| Version Control | Git + GitHub | Portfolio üçün |

---

## 🤖 Atlas-ın Şəxsiyyəti (System Prompt Qaydaları)

Atlas **formal AI kimi deyil, gym yoldaşı kimi** danışır.

**DƏ, EDİLMƏZ:**
- ❌ Bullet point, markdown, başlıq işlətmə
- ❌ "Əlbəttə! Sizə kömək etməkdən məmnunam." kimi robot cümlələri
- ❌ Uzun, rəsmi cavablar
- ✅ Qısa, natural Azərbaycanca cümlələr
- ✅ "Ay qardaş", "bax", "düz deyirsən" kimi danışıq dili
- ✅ Məhsul tövsiyəsini real datadan et, uydurma

**Cavab dili:** Yalnız Azərbaycanca (istifadəçi Türkcə yazsa da Azərbaycan dilinə keç)

---

## 📦 Məhsul Datası

- **Mənbə:** atlet.az (web scraping ilə)
- **Cəmi:** 96 məhsul, 9 kateqoriya
- **Kateqoriyalar:** Protein, Creatine, BCAA, Pre-workout, Vitaminlər, Yağ yandırıcılar, Karbohidratlar, Aksessuarlar, Digər
- **Hər məhsul üçün:** ad, qiymət, kateqoriya, URL
- **Güncəlləmə:** Scraper manual işlədilir, `products.json` yenilənir

---

## 🏪 Mağaza Məlumatları (store_info.json)

Aşağıdakı məlumatlar statik JSON-da saxlanılır:

- **Filiallar:** ünvan, iş saatları, telefon
- **Çatdırılma:** şərtlər, müddət, pulsuz çatdırılma həddi
- **Ödəniş:** nağd, kart, online
- **Əlaqə:** Instagram, WhatsApp, telefon

---

## 🔌 API Endpoint-lər

### `POST /chat`
İstifadəçi mesajını qəbul edir, Atlas cavabını qaytarır.

**Request:**
```json
{
  "message": "Protein tövsiyə elə",
  "history": [
    {"role": "user", "content": "Salam"},
    {"role": "assistant", "content": "Salam qardaş, nə lazımdır?"}
  ]
}
```

**Response:**
```json
{
  "reply": "Bax, əgər kütlə qazanmaq istəyirsənsə Optimum Nutrition Gold Standard baxmağa dəyər..."
}
```

### `GET /products`
Bütün məhsulları qaytarır (debug üçün).

### `GET /health`
Server sağlamlıq yoxlaması.

---

## 💬 Frontend UI Davranışı

- Sağda istifadəçi baloncuğu, solda Atlas baloncuğu
- Atlas cavab gözlənilən zaman `...` (typing indicator) göstərilir
- Enter ilə mesaj göndərilir
- Söhbət yaddaşı: son 10 mesaj history-də saxlanılır
- Mobil uyğun (responsive) dizayn
- Rəng sxemi: Qaranlıq/gym estetikası (tünd arxa fon, narıncı/sarı accent)

---

## 🚫 Məhdudiyyətlər

- Atlas yalnız atlet.az məhsulları haqqında danışır
- Tibbi məsləhət vermir ("həkim-ə get" deyir)
- Sifariş qəbul etmir, yalnız yönləndirir
- Real-time qiymət yoxlaması yoxdur (JSON datası statikdir)

---

## 🛠️ Development Qaydaları

1. **Hər feature üçün ayrı commit** — "feat: add typing indicator", "fix: encoding issue"
2. **`.env` faylı heç vaxt GitHub-a push edilmir**
3. **`products.json` dəyişirsə** — scraper yenidən işlədilməlidir
4. **Encoding:** Bütün fayllar `UTF-8` saxlanılır, Azərbaycan hərfləri dəstəklənir

---

## 🚀 Lokal İşə Salma

```bash
# 1. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Paketlər
pip install -r requirements.txt

# 3. .env faylı
echo "GEMINI_API_KEY=your_key_here" > .env

# 4. Server
uvicorn backend.main:app --reload --port 8000

# 5. Frontend
# index.html-i brauzerdə aç (və ya Live Server ilə)
```

---

## 📋 MVP Checklist

- [ ] FastAPI backend işləyir
- [ ] Gemini API inteqrasiyası
- [ ] System prompt (Atlas şəxsiyyəti)
- [ ] products.json yüklənir və context-ə əlavə edilir
- [ ] store_info.json yüklənir
- [ ] `/chat` endpoint işləyir
- [ ] Conversation history saxlanılır
- [ ] Frontend UI (Tailwind)
- [ ] Typing indicator
- [ ] Azərbaycan encoding düzgün işləyir
- [ ] GitHub-a push edilir (README ilə)
