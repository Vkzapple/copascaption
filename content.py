import random
import re

STOPWORDS = {
    "yang", "di", "ke", "dari", "dan", "untuk", "dengan", "pada", "ini", "itu", "saya", "kami", "kita",
    "aku", "akan", "sudah", "lagi", "buat", "bareng", "sambil", "saat", "atau", "juga", "agar", "biar",
    "sebuah", "adalah", "ada", "dalam", "oleh", "para", "tapi", "tetapi", "karena", "jadi", "bisa",
    "banget", "paling", "lebih", "baru", "terbaru", "hari", "sama", "tanpa", "setelah", "sebelum",
    "kamu", "mereka", "dia", "nya", "yg", "dg", "sih", "dong", "deh", "aja", "saja", "sangat", "pakai",
}

STYLES = ("lucu", "cerita", "singkat")
STYLE_LABELS = {
    "lucu": "Lucu & Playful",
    "cerita": "Hangat & Storytelling",
    "singkat": "Singkat & Punchy",
}

TEMPLATES = {
    "kuliner": {
        "lucu": [
            "{Topic}? Diet kita tunda dulu ya 🙈 Perut bilang gaskeun, dompet pura-pura tidak dengar!",
            "Alarm bahaya 🚨 {topic}. Pertahanan diet runtuh dalam 3 detik 🤤",
        ],
        "cerita": [
            "Ada rasa yang selalu bikin kita pulang. Hari ini ceritanya: {topic} 🍽️ Dinikmati pelan-pelan, paling enak bareng orang tersayang.",
            "Dari dapur kecil sampai meja makan penuh tawa. Cerita kali ini tentang {topic} ☕ Siapa yang mau ikut mencicipi?",
        ],
        "singkat": [
            "{Topic}. Satu gigitan, langsung jatuh cinta 😋",
            "Lapar? {Topic} jawabannya 🍜",
        ],
    },
    "travel": {
        "lucu": [
            "{Topic}! Badan di sini, hati masih ogah pulang 🏝️ Bos, tolong tambah cuti dong 🥹",
            "Bukti nyata kalau kata 'healing' itu valid ✨ {Topic}. Saldo tipis, bahagia tebal!",
        ],
        "cerita": [
            "Kadang kita cuma perlu pergi sebentar untuk ingat betapa luasnya dunia. Kali ini: {topic} 🌅 Dan hati terasa jauh lebih ringan.",
            "Langkah kecil, kenangan besar. Hari ini kami menikmati {topic} 🧭 Semoga cerita ini bikin kamu ikut ingin berangkat.",
        ],
        "singkat": [
            "{Topic}. Mood: lagi bahagia 🌴",
            "Ke mana lagi next? {Topic} baru saja jadi favorit 🗺️",
        ],
    },
    "fashion": {
        "lucu": [
            "Lemari penuh tapi tetap bilang 'nggak ada baju' 😂 Untung ada inspirasi: {topic} 💃",
            "{Topic}, siap bikin cermin bilang 'cantik banget hari ini' 🪞✨",
        ],
        "cerita": [
            "Gaya itu cara kita bercerita tanpa bersuara. Hari ini ceritanya lewat {topic} 👗 Percaya diri adalah aksesori terbaik.",
            "Dari detail kecil lahir tampilan yang berkesan. Kali ini kami sorot {topic} 🧵 Menurut kamu bagaimana?",
        ],
        "singkat": [
            "{Topic}. Simple, tapi bikin menoleh 💅",
            "Fit check ✅ {Topic}",
        ],
    },
    "karier": {
        "lucu": [
            "Update karier: {topic} 🎉 Kopi makin banyak, ilmu juga makin banyak ☕",
            "Kalau kerja keras ada leaderboard-nya, hari ini kami naik peringkat 😄 {Topic}!",
        ],
        "cerita": [
            "Setiap langkah karier punya pelajaran. Kali ini saya belajar banyak dari {topic} 💼 Prosesnya tidak selalu mulus, tapi selalu berarti.",
            "Beberapa tahun lalu saya tidak membayangkan akan sampai di titik ini. Hari ini: {topic} 🌱 Terima kasih untuk semua yang mendampingi.",
        ],
        "singkat": [
            "{Topic}. Terus belajar, terus bertumbuh 🚀",
            "Satu langkah lagi ke depan: {topic} 📈",
        ],
    },
    "teknologi": {
        "lucu": [
            "Kode jalan di percobaan pertama? Mustahil 😂 Tapi hari ini ada kabar baik: {topic} 💻",
            "{Topic}! Bug kecil mohon minggir, fitur keren mau lewat 🐛✨",
        ],
        "cerita": [
            "Semua berawal dari satu ide dan layar kosong. Hari ini kami berbagi cerita tentang {topic} 🚀 Perjalanan panjang, tapi seru banget.",
            "Teknologi terbaik adalah yang mempermudah hidup orang banyak. Itulah semangat di balik {topic} 🔧 Kami ingin dengar pendapatmu!",
        ],
        "singkat": [
            "{Topic}. Build, ship, repeat 🛠️",
            "Future mode: ON ⚡ {Topic}",
        ],
    },
    "kebugaran": {
        "lucu": [
            "Otot bilang aduh, semangat bilang lagi dong 💪😅 {Topic}!",
            "Niat awal cuma pemanasan, ujungnya keringetan sekujur badan 🥵 {Topic}!",
        ],
        "cerita": [
            "Perubahan besar dimulai dari kebiasaan kecil yang dilakukan konsisten. Hari ini aku memilih {topic} 🌿 Pelan tapi pasti.",
            "Ada hari malas, ada hari semangat, yang penting tetap bergerak. Kali ini: {topic} 🏃 Terima kasih buat diri sendiri yang tidak menyerah.",
        ],
        "singkat": [
            "{Topic}. Sehat itu pilihan setiap hari 💥",
            "Keringat hari ini, senyum besok ✅ {Topic}",
        ],
    },
    "bisnis": {
        "lucu": [
            "Dompet, mohon bersiap 🛍️ {Topic}! Awas khilaf, tapi khilafnya bahagia 😆",
            "Notifikasi spesial untuk kamu 🔔 {Topic}. Yang cepat dapat, yang lambat nyesel 🏃‍♀️",
        ],
        "cerita": [
            "Semua bermula dari mimpi kecil dan niat besar. Hari ini kami bangga membagikan kabar: {topic} 💖 Terima kasih sudah jadi bagian perjalanan kami.",
            "Di balik setiap produk ada cerita dan kerja keras. Kali ini kami hadir dengan {topic} 🎁 Semoga bermanfaat untuk kamu.",
        ],
        "singkat": [
            "{Topic}! Jangan sampai ketinggalan 🔥",
            "Hanya kali ini: {topic} 🛒",
        ],
    },
    "lifestyle": {
        "lucu": [
            "Hidup ini singkat, makanya {topic} 😌 Sisanya biarkan semesta yang urus!",
            "Plot twist: hari biasa jadi seru gara-gara {topic} 😆✨",
        ],
        "cerita": [
            "Bahagia ternyata sesederhana ini: {topic} 🌷 Terkadang kita hanya perlu berhenti sejenak dan menikmati.",
            "Hari-hari yang tenang selalu jadi kenangan paling hangat. Hari ini aku menyimpan satu lagi: {topic} 📖",
        ],
        "singkat": [
            "{Topic}. Hati penuh, hidup ringan 💛",
            "Good vibes only ✨ {Topic}",
        ],
    },
}

HASHTAG_POOL = {
    "kuliner": ["#kuliner", "#makananenak", "#jajanan", "#foodie", "#kulinerindonesia", "#foodstagram", "#yummy", "#nyamnyam", "#cafehits", "#instafood"],
    "travel": ["#travel", "#liburan", "#jalanjalan", "#wisataindonesia", "#traveling", "#healing", "#explore", "#wanderlust", "#holiday", "#pesonaindonesia"],
    "fashion": ["#ootd", "#fashion", "#outfitinspo", "#style", "#lookbook", "#fashionindonesia", "#outfitoftheday", "#stylish", "#trendy", "#mixandmatch"],
    "karier": ["#karier", "#leadership", "#profesional", "#pengembangandiri", "#worklife", "#linkedinindonesia", "#careergrowth", "#softskills", "#networking", "#lowongankerja"],
    "teknologi": ["#teknologi", "#coding", "#developer", "#programming", "#startup", "#inovasi", "#techindonesia", "#ai", "#digital", "#software"],
    "kebugaran": ["#olahraga", "#hidupsehat", "#fitness", "#workout", "#sehat", "#gayahidupsehat", "#gymlife", "#healthylifestyle", "#semangatpagi", "#lari"],
    "bisnis": ["#promo", "#umkm", "#jualanonline", "#diskon", "#belanjaonline", "#produklokal", "#bisnisonline", "#newarrival", "#supportlocal", "#olshop"],
    "lifestyle": ["#lifestyle", "#harihariku", "#bahagia", "#momenindah", "#syukur", "#vibes", "#aesthetic", "#dailylife", "#goodvibes", "#selfcare"],
}

PHOTO_OPENERS = ["Swipe dulu fotonya 📸", "Satu foto, sejuta cerita 📷", "Yang ada di foto ini bukan cuma gaya 🌸"]
LINKEDIN_CLOSERS = [
    "Bagaimana pengalaman Anda? Mari berdiskusi di kolom komentar.",
    "Apa pendapat Anda tentang hal ini? Saya ingin mendengar sudut pandang Anda.",
    "Silakan bagikan insight Anda di kolom komentar.",
]

HASHTAG_LIMITS = {"Instagram": 10, "LinkedIn": 5, "X": 2}
EMOJI_CLASS = "[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]"
EMOJI_PATTERN = re.compile(EMOJI_CLASS)
EMOJI_SENTENCE_BREAK = re.compile(rf"(?<=[^\s.!?,:;])\s*{EMOJI_CLASS}+(?=\s+[A-Z])")
X_LIMIT = 280


def clean_topic(text):
    text = re.sub(r"\s+", " ", text).strip().rstrip(".!?,;:")
    if len(text) > 90:
        text = text[:90].rsplit(" ", 1)[0]
    return text


def lower_first(text):
    if len(text) > 1 and text[1].isupper():
        return text
    return text[:1].lower() + text[1:]


def upper_first(text):
    return text[:1].upper() + text[1:]


def extract_keywords(text, limit=3):
    tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
    unique = []
    for token in tokens:
        if token not in STOPWORDS and len(token) > 2 and token not in unique:
            unique.append(token)
    return sorted(unique, key=lambda token: -len(token))[:limit]


def pick_hashtags(category, topic, platform):
    limit = HASHTAG_LIMITS[platform]
    keyword_tags = [f"#{keyword}" for keyword in extract_keywords(topic)]
    keyword_quota = {"Instagram": 3, "LinkedIn": 2, "X": 1}[platform]
    pool = HASHTAG_POOL[category][:]
    random.shuffle(pool)
    tags = []
    for tag in keyword_tags[:keyword_quota] + pool:
        if tag not in tags:
            tags.append(tag)
        if len(tags) == limit:
            break
    return tags


def adapt_caption(caption, platform, mode, index):
    if platform == "Instagram" and mode == "foto":
        return f"{PHOTO_OPENERS[index % len(PHOTO_OPENERS)]}\n\n{caption}"
    if platform == "LinkedIn":
        broken = EMOJI_SENTENCE_BREAK.sub(".", caption)
        plain = re.sub(r" {2,}", " ", EMOJI_PATTERN.sub("", broken)).strip()
        return f"{plain}\n\n{random.choice(LINKEDIN_CLOSERS)}"
    return caption


def fit_for_x(caption, hashtags):
    tags = " ".join(hashtags)
    room = X_LIMIT - len(tags) - 2
    if len(caption) > room:
        caption = caption[: room - 1].rstrip() + "…"
    return caption


def build_options(category, topic, platform, mode):
    topic = clean_topic(topic)
    values = {"topic": lower_first(topic), "Topic": upper_first(topic)}
    options = []
    for index, style in enumerate(STYLES):
        template = random.choice(TEMPLATES[category][style])
        caption = adapt_caption(template.format(**values), platform, mode, index)
        hashtags = pick_hashtags(category, topic, platform)
        if platform == "X":
            caption = fit_for_x(caption, hashtags)
        options.append({
            "id": index + 1,
            "style": STYLE_LABELS[style],
            "caption": caption,
            "hashtags": hashtags,
        })
    return options
