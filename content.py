import random
import re

STOPWORDS = {
    "id": {
        "yang", "di", "ke", "dari", "dan", "untuk", "dengan", "pada", "ini", "itu", "saya", "kami", "kita",
        "aku", "akan", "sudah", "lagi", "buat", "bareng", "sambil", "saat", "atau", "juga", "agar", "biar",
        "sebuah", "adalah", "ada", "dalam", "oleh", "para", "tapi", "tetapi", "karena", "jadi", "bisa",
        "banget", "paling", "lebih", "baru", "terbaru", "hari", "sama", "tanpa", "setelah", "sebelum",
        "kamu", "mereka", "dia", "nya", "yg", "dg", "sih", "dong", "deh", "aja", "saja", "sangat", "pakai",
    },
    "en": {
        "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "for", "with", "from", "our", "my",
        "your", "we", "i", "is", "are", "was", "were", "new", "just", "this", "that", "it", "its", "by",
        "as", "be", "so", "here", "today", "now", "out", "all", "has", "have", "had", "up", "us", "me",
        "after", "before", "into", "over", "very", "some", "more", "most", "got", "get",
        "wearing", "everything", "excited", "launching", "trying", "really", "big",
    },
}

STYLES = ("playful", "story", "punchy")
STYLE_LABELS = {
    "id": {
        "playful": "Lucu & Playful",
        "story": "Hangat & Storytelling",
        "punchy": "Singkat & Punchy",
    },
    "en": {
        "playful": "Playful & Fun",
        "story": "Warm & Storytelling",
        "punchy": "Short & Punchy",
    },
}

TEMPLATES = {
    "id": {
        "food": {
            "playful": [
                "{Topic}? Diet kita tunda dulu ya 🙈 Perut bilang gaskeun, dompet pura-pura tidak dengar!",
                "Alarm bahaya 🚨 {topic}. Pertahanan diet runtuh dalam 3 detik 🤤",
            ],
            "story": [
                "Ada rasa yang selalu bikin kita pulang. Hari ini ceritanya: {topic} 🍽️ Dinikmati pelan-pelan, paling enak bareng orang tersayang.",
                "Dari dapur kecil sampai meja makan penuh tawa. Cerita kali ini tentang {topic} ☕ Siapa yang mau ikut mencicipi?",
            ],
            "punchy": [
                "{Topic}. Satu gigitan, langsung jatuh cinta 😋",
                "Lapar? {Topic} jawabannya 🍜",
            ],
        },
        "travel": {
            "playful": [
                "{Topic}! Badan di sini, hati masih ogah pulang 🏝️ Bos, tolong tambah cuti dong 🥹",
                "Bukti nyata kalau kata 'healing' itu valid ✨ {Topic}. Saldo tipis, bahagia tebal!",
            ],
            "story": [
                "Kadang kita cuma perlu pergi sebentar untuk ingat betapa luasnya dunia. Kali ini: {topic} 🌅 Dan hati terasa jauh lebih ringan.",
                "Langkah kecil, kenangan besar. Hari ini kami menikmati {topic} 🧭 Semoga cerita ini bikin kamu ikut ingin berangkat.",
            ],
            "punchy": [
                "{Topic}. Mood: lagi bahagia 🌴",
                "Ke mana lagi next? {Topic} baru saja jadi favorit 🗺️",
            ],
        },
        "fashion": {
            "playful": [
                "Lemari penuh tapi tetap bilang 'nggak ada baju' 😂 Untung ada inspirasi: {topic} 💃",
                "{Topic}, siap bikin cermin bilang 'cantik banget hari ini' 🪞✨",
            ],
            "story": [
                "Gaya itu cara kita bercerita tanpa bersuara. Hari ini ceritanya lewat {topic} 👗 Percaya diri adalah aksesori terbaik.",
                "Dari detail kecil lahir tampilan yang berkesan. Kali ini kami sorot {topic} 🧵 Menurut kamu bagaimana?",
            ],
            "punchy": [
                "{Topic}. Simple, tapi bikin menoleh 💅",
                "Fit check ✅ {Topic}",
            ],
        },
        "career": {
            "playful": [
                "Update karier: {topic} 🎉 Kopi makin banyak, ilmu juga makin banyak ☕",
                "Kalau kerja keras ada leaderboard-nya, hari ini kami naik peringkat 😄 {Topic}!",
            ],
            "story": [
                "Setiap langkah karier punya pelajaran. Kali ini saya belajar banyak dari {topic} 💼 Prosesnya tidak selalu mulus, tapi selalu berarti.",
                "Beberapa tahun lalu saya tidak membayangkan akan sampai di titik ini. Hari ini: {topic} 🌱 Terima kasih untuk semua yang mendampingi.",
            ],
            "punchy": [
                "{Topic}. Terus belajar, terus bertumbuh 🚀",
                "Satu langkah lagi ke depan: {topic} 📈",
            ],
        },
        "tech": {
            "playful": [
                "Kode jalan di percobaan pertama? Mustahil 😂 Tapi hari ini ada kabar baik: {topic} 💻",
                "{Topic}! Bug kecil mohon minggir, fitur keren mau lewat 🐛✨",
            ],
            "story": [
                "Semua berawal dari satu ide dan layar kosong. Hari ini kami berbagi cerita tentang {topic} 🚀 Perjalanan panjang, tapi seru banget.",
                "Teknologi terbaik adalah yang mempermudah hidup orang banyak. Itulah semangat di balik {topic} 🔧 Kami ingin dengar pendapatmu!",
            ],
            "punchy": [
                "{Topic}. Build, ship, repeat 🛠️",
                "Future mode: ON ⚡ {Topic}",
            ],
        },
        "fitness": {
            "playful": [
                "Otot bilang aduh, semangat bilang lagi dong 💪😅 {Topic}!",
                "Niat awal cuma pemanasan, ujungnya keringetan sekujur badan 🥵 {Topic}!",
            ],
            "story": [
                "Perubahan besar dimulai dari kebiasaan kecil yang dilakukan konsisten. Hari ini aku memilih {topic} 🌿 Pelan tapi pasti.",
                "Ada hari malas, ada hari semangat, yang penting tetap bergerak. Kali ini: {topic} 🏃 Terima kasih buat diri sendiri yang tidak menyerah.",
            ],
            "punchy": [
                "{Topic}. Sehat itu pilihan setiap hari 💥",
                "Keringat hari ini, senyum besok ✅ {Topic}",
            ],
        },
        "business": {
            "playful": [
                "Dompet, mohon bersiap 🛍️ {Topic}! Awas khilaf, tapi khilafnya bahagia 😆",
                "Notifikasi spesial untuk kamu 🔔 {Topic}. Yang cepat dapat, yang lambat nyesel 🏃‍♀️",
            ],
            "story": [
                "Semua bermula dari mimpi kecil dan niat besar. Hari ini kami bangga membagikan kabar: {topic} 💖 Terima kasih sudah jadi bagian perjalanan kami.",
                "Di balik setiap produk ada cerita dan kerja keras. Kali ini kami hadir dengan {topic} 🎁 Semoga bermanfaat untuk kamu.",
            ],
            "punchy": [
                "{Topic}! Jangan sampai ketinggalan 🔥",
                "Hanya kali ini: {topic} 🛒",
            ],
        },
        "lifestyle": {
            "playful": [
                "Hidup ini singkat, makanya {topic} 😌 Sisanya biarkan semesta yang urus!",
                "Plot twist: hari biasa jadi seru gara-gara {topic} 😆✨",
            ],
            "story": [
                "Bahagia ternyata sesederhana ini: {topic} 🌷 Terkadang kita hanya perlu berhenti sejenak dan menikmati.",
                "Hari-hari yang tenang selalu jadi kenangan paling hangat. Hari ini aku menyimpan satu lagi: {topic} 📖",
            ],
            "punchy": [
                "{Topic}. Hati penuh, hidup ringan 💛",
                "Good vibes only ✨ {Topic}",
            ],
        },
    },
    "en": {
        "food": {
            "playful": [
                "{Topic}? Diet starts tomorrow, I swear 🙈 My stomach said yes before my wallet could vote!",
                "Danger alert 🚨 {topic}. Willpower collapsed in 3 seconds 🤤",
            ],
            "story": [
                "Some flavors always feel like coming home. Today's story: {topic} 🍽️ Best enjoyed slowly, and even better with people you love.",
                "From a tiny kitchen to a table full of laughter. This one is all about {topic} ☕ Who wants a taste?",
            ],
            "punchy": [
                "{Topic}. One bite and we're in love 😋",
                "Hungry? {Topic} is the answer 🍜",
            ],
        },
        "travel": {
            "playful": [
                "{Topic}! My body is here, my heart refuses to go home 🏝️ Boss, please approve more leave 🥹",
                "Proof that 'healing' is real ✨ {Topic}. Bank account thin, happiness thick!",
            ],
            "story": [
                "Sometimes you just need to leave for a while to remember how big the world is. This time: {topic} 🌅 And my heart feels so much lighter.",
                "Small steps, big memories. Today we enjoyed {topic} 🧭 Hope this story makes you want to pack your bags.",
            ],
            "punchy": [
                "{Topic}. Mood: happy 🌴",
                "Where to next? {Topic} just became a favorite 🗺️",
            ],
        },
        "fashion": {
            "playful": [
                "Closet full, yet 'nothing to wear' 😂 Good thing there's inspo like this: {topic} 💃",
                "{Topic}, ready to make the mirror say 'wow, look at you' 🪞✨",
            ],
            "story": [
                "Style is how we tell stories without saying a word. Today's story is told through {topic} 👗 Confidence is the best accessory.",
                "Small details create lasting impressions. This time we're spotlighting {topic} 🧵 What do you think?",
            ],
            "punchy": [
                "{Topic}. Simple, but turns heads 💅",
                "Fit check ✅ {Topic}",
            ],
        },
        "career": {
            "playful": [
                "Career update: {topic} 🎉 More coffee, more learning ☕",
                "If hard work had a leaderboard, we just climbed a rank 😄 {Topic}!",
            ],
            "story": [
                "Every career step comes with a lesson. This time I learned a lot from {topic} 💼 The road wasn't always smooth, but it was always worth it.",
                "A few years ago I couldn't have imagined being here. Today: {topic} 🌱 Thank you to everyone who walked this road with me.",
            ],
            "punchy": [
                "{Topic}. Keep learning, keep growing 🚀",
                "One more step forward: {topic} 📈",
            ],
        },
        "tech": {
            "playful": [
                "Code works on the first try? Impossible 😂 But today there's good news: {topic} 💻",
                "{Topic}! Tiny bugs, please step aside, cool features coming through 🐛✨",
            ],
            "story": [
                "It all started with one idea and a blank screen. Today we're sharing the story behind {topic} 🚀 A long journey, but such a fun one.",
                "The best technology makes life easier for many people. That's the spirit behind {topic} 🔧 We'd love to hear your thoughts!",
            ],
            "punchy": [
                "{Topic}. Build, ship, repeat 🛠️",
                "Future mode: ON ⚡ {Topic}",
            ],
        },
        "fitness": {
            "playful": [
                "Muscles say ouch, motivation says again 💪😅 {Topic}!",
                "Planned a quick warm-up, ended up drenched in sweat 🥵 {Topic}!",
            ],
            "story": [
                "Big changes start with small habits done consistently. Today I chose {topic} 🌿 Slow but steady.",
                "Some days are lazy, some days are fired up, what matters is that we keep moving. Today: {topic} 🏃 Thank you to myself for not giving up.",
            ],
            "punchy": [
                "{Topic}. Healthy is a daily choice 💥",
                "Sweat today, smile tomorrow ✅ {Topic}",
            ],
        },
        "business": {
            "playful": [
                "Wallets, please brace yourselves 🛍️ {Topic}! Warning: impulse buys may occur 😆",
                "Special notification just for you 🔔 {Topic}. Early birds win, late birds regret 🏃‍♀️",
            ],
            "story": [
                "It all began with a small dream and a big heart. Today we're proud to share: {topic} 💖 Thank you for being part of our journey.",
                "Behind every product is a story and a lot of hard work. This time we're bringing you {topic} 🎁 We hope you love it.",
            ],
            "punchy": [
                "{Topic}! Don't miss out 🔥",
                "Just this once: {topic} 🛒",
            ],
        },
        "lifestyle": {
            "playful": [
                "Life is short, so {topic} 😌 Let the universe handle the rest!",
                "Plot twist: an ordinary day turned fun thanks to {topic} 😆✨",
            ],
            "story": [
                "Happiness turns out to be this simple: {topic} 🌷 Sometimes we just need to pause and enjoy it.",
                "Quiet days always become the warmest memories. Today I'm saving another one: {topic} 📖",
            ],
            "punchy": [
                "{Topic}. Full heart, light life 💛",
                "Good vibes only ✨ {Topic}",
            ],
        },
    },
}

HASHTAG_POOL = {
    "id": {
        "food": ["#kuliner", "#makananenak", "#jajanan", "#foodie", "#kulinerindonesia", "#foodstagram", "#yummy", "#nyamnyam", "#cafehits", "#instafood"],
        "travel": ["#travel", "#liburan", "#jalanjalan", "#wisataindonesia", "#traveling", "#healing", "#explore", "#wanderlust", "#holiday", "#pesonaindonesia"],
        "fashion": ["#ootd", "#fashion", "#outfitinspo", "#style", "#lookbook", "#fashionindonesia", "#outfitoftheday", "#stylish", "#trendy", "#mixandmatch"],
        "career": ["#karier", "#leadership", "#profesional", "#pengembangandiri", "#worklife", "#linkedinindonesia", "#careergrowth", "#softskills", "#networking", "#lowongankerja"],
        "tech": ["#teknologi", "#coding", "#developer", "#programming", "#startup", "#inovasi", "#techindonesia", "#ai", "#digital", "#software"],
        "fitness": ["#olahraga", "#hidupsehat", "#fitness", "#workout", "#sehat", "#gayahidupsehat", "#gymlife", "#healthylifestyle", "#semangatpagi", "#lari"],
        "business": ["#promo", "#umkm", "#jualanonline", "#diskon", "#belanjaonline", "#produklokal", "#bisnisonline", "#newarrival", "#supportlocal", "#olshop"],
        "lifestyle": ["#lifestyle", "#harihariku", "#bahagia", "#momenindah", "#syukur", "#vibes", "#aesthetic", "#dailylife", "#goodvibes", "#selfcare"],
    },
    "en": {
        "food": ["#foodie", "#foodstagram", "#yummy", "#instafood", "#delicious", "#foodlover", "#cafevibes", "#eatlocal", "#tasty", "#foodgram"],
        "travel": ["#travel", "#wanderlust", "#explore", "#travelgram", "#adventure", "#vacation", "#holiday", "#traveling", "#getaway", "#traveldiaries"],
        "fashion": ["#ootd", "#fashion", "#outfitinspo", "#style", "#lookbook", "#fashionista", "#outfitoftheday", "#stylish", "#trendy", "#mixandmatch"],
        "career": ["#career", "#leadership", "#professionaldevelopment", "#worklife", "#linkedin", "#careergrowth", "#softskills", "#networking", "#hiring", "#growthmindset"],
        "tech": ["#tech", "#coding", "#developer", "#programming", "#startup", "#innovation", "#ai", "#digital", "#software", "#techcommunity"],
        "fitness": ["#fitness", "#workout", "#healthylifestyle", "#gymlife", "#fitnessmotivation", "#wellness", "#running", "#training", "#stayactive", "#healthy"],
        "business": ["#sale", "#smallbusiness", "#shopsmall", "#promo", "#onlineshopping", "#newarrival", "#supportlocal", "#giveaway", "#discount", "#entrepreneur"],
        "lifestyle": ["#lifestyle", "#dailylife", "#goodvibes", "#happiness", "#vibes", "#aesthetic", "#selfcare", "#momentsofjoy", "#grateful", "#relax"],
    },
}

PHOTO_OPENERS = {
    "id": ["Swipe dulu fotonya 📸", "Satu foto, sejuta cerita 📷", "Yang ada di foto ini bukan cuma gaya 🌸"],
    "en": ["Swipe for the full picture 📸", "One photo, a thousand stories 📷", "There's more to this photo than meets the eye 🌸"],
}

LINKEDIN_CLOSERS = {
    "id": [
        "Bagaimana pengalaman Anda? Mari berdiskusi di kolom komentar.",
        "Apa pendapat Anda tentang hal ini? Saya ingin mendengar sudut pandang Anda.",
        "Silakan bagikan insight Anda di kolom komentar.",
    ],
    "en": [
        "How has your experience been? Let's discuss in the comments.",
        "What are your thoughts? I'd love to hear your perspective.",
        "Feel free to share your insights in the comments.",
    ],
}

LANGUAGES = tuple(TEMPLATES)
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


def extract_keywords(text, lang, limit=3):
    tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
    unique = []
    for token in tokens:
        if token not in STOPWORDS[lang] and len(token) > 2 and token not in unique:
            unique.append(token)
    return sorted(unique, key=lambda token: -len(token))[:limit]


def pick_hashtags(category, topic, platform, lang):
    limit = HASHTAG_LIMITS[platform]
    keyword_tags = [f"#{keyword}" for keyword in extract_keywords(topic, lang)]
    keyword_quota = {"Instagram": 3, "LinkedIn": 2, "X": 1}[platform]
    pool = HASHTAG_POOL[lang][category][:]
    random.shuffle(pool)
    tags = []
    for tag in keyword_tags[:keyword_quota] + pool:
        if tag not in tags:
            tags.append(tag)
        if len(tags) == limit:
            break
    return tags


def adapt_caption(caption, platform, mode, index, lang):
    if platform == "Instagram" and mode == "photo":
        openers = PHOTO_OPENERS[lang]
        return f"{openers[index % len(openers)]}\n\n{caption}"
    if platform == "LinkedIn":
        broken = EMOJI_SENTENCE_BREAK.sub(".", caption)
        plain = re.sub(r" {2,}", " ", EMOJI_PATTERN.sub("", broken)).strip()
        return f"{plain}\n\n{random.choice(LINKEDIN_CLOSERS[lang])}"
    return caption


def fit_for_x(caption, hashtags):
    tags = " ".join(hashtags)
    room = X_LIMIT - len(tags) - 2
    if len(caption) > room:
        caption = caption[: room - 1].rstrip() + "…"
    return caption


def build_options(category, topic, platform, mode, lang):
    topic = clean_topic(topic)
    values = {"topic": lower_first(topic), "Topic": upper_first(topic)}
    options = []
    for index, style in enumerate(STYLES):
        template = random.choice(TEMPLATES[lang][category][style])
        caption = adapt_caption(template.format(**values), platform, mode, index, lang)
        hashtags = pick_hashtags(category, topic, platform, lang)
        if platform == "X":
            caption = fit_for_x(caption, hashtags)
        options.append({
            "id": index + 1,
            "style": STYLE_LABELS[lang][style],
            "caption": caption,
            "hashtags": hashtags,
        })
    return options