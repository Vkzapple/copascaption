import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import FeatureUnion, Pipeline

DATASET = {
    "id": {
        "food": [
            "Dapatkan promo free upsize!"
            "Ayo dicoba! promo beli 1 dapat 1!"
            "Kamu mau ayam enak dan murah? Beli sekarang!"
            "Launching kopi susu gula aren di kafe baru kami",
            "Nyobain ramen pedas level 5 bareng teman kantor",
            "Resep nasi goreng kampung simple buat sarapan",
            "Review bakso urat paling enak di kota ini",
            "Dessert box coklat lumer untuk akhir pekan",
            "Brunch di cafe estetik sambil ngopi",
            "Menu baru ayam geprek sambal matah",
            "Bikin kue brownies kukus anti gagal",
            "Jajan street food malam di pasar kuliner",
            "Es teh tarik dan pisang goreng hangat saat hujan",
            "Makan malam steak wagyu di restoran favorit",
            "Promo paket sate ayam dan lontong",
        ],
        "travel": [
            "Liburan ke Bali lihat sunset di pantai",
            "Foto selfie di pantai pakai topi jerami",
            "Hiking ke gunung bromo lihat sunrise",
            "Staycation di hotel dengan view kota",
            "Road trip Jakarta ke Bandung bareng sahabat",
            "Jalan-jalan keliling Yogyakarta naik becak",
            "Camping di tepi danau saat akhir pekan",
            "Snorkeling di Raja Ampat air jernih banget",
            "Backpacking ke Jepang lihat bunga sakura",
            "Menjelajah air terjun tersembunyi di hutan",
            "Healing ke pegunungan udara sejuk",
            "Piknik di taman dengan pemandangan indah",
        ],
        "fashion": [
            "OOTD kemeja oversize dengan celana jeans",
            "Koleksi dress floral terbaru musim ini",
            "Mix and match outfit hijab warna pastel",
            "Sneakers baru warna pink buat jalan santai",
            "Tas kulit handmade koleksi terbaru",
            "Tips padu padan batik untuk acara formal",
            "Makeup natural glowing untuk sehari-hari",
            "Skincare routine pagi biar kulit cerah",
            "Gaya streetwear dengan jaket denim vintage",
            "Outfit kondangan simple tapi elegan",
            "Aksesoris kalung emas minimalis",
            "Lookbook lebaran baju couple keluarga",
        ],
        "career": [
            "Pengalaman pertama jadi manajer tim",
            "Tips lolos interview kerja di perusahaan startup",
            "Belajar leadership dari kegagalan proyek",
            "Sertifikasi baru di bidang manajemen proyek",
            "Hari pertama kerja di kantor baru",
            "Cara membangun personal branding di LinkedIn",
            "Webinar karier untuk fresh graduate",
            "Pelajaran dari 5 tahun bekerja remote",
            "Strategi networking untuk profesional muda",
            "Promosi jabatan setelah kerja keras setahun",
            "Tips produktif kerja dari rumah dengan jadwal rapi",
            "Mentoring anggota tim baru di kantor",
        ],
        "tech": [
            "Rilis aplikasi mobile baru buatan tim kami",
            "Belajar coding Python dari nol",
            "Review smartphone terbaru dengan kamera canggih",
            "Tips keamanan data dan password untuk pemula",
            "AI membantu pekerjaan sehari-hari jadi lebih cepat",
            "Setup meja kerja programmer dengan monitor ganda",
            "Tutorial membuat website dengan JavaScript",
            "Hackathon 48 jam bareng developer muda",
            "Gadget laptop gaming spesifikasi tinggi",
            "Update fitur baru di aplikasi kami",
            "Belajar machine learning untuk analisis data",
            "Startup teknologi lokal meluncurkan platform digital",
        ],
        "fitness": [
            "Olahraga pagi lari 5 kilometer di taman",
            "Latihan gym angkat beban hari ini",
            "Yoga santai untuk menenangkan pikiran",
            "Tips diet sehat dan menu salad rendah kalori",
            "Gowes sepeda bareng komunitas akhir pekan",
            "Workout di rumah tanpa alat",
            "Marathon pertama berhasil finish",
            "Meal prep sehat untuk seminggu",
            "Rutinitas stretching sebelum tidur",
            "Berenang pagi biar badan segar",
            "Jaga kesehatan dengan tidur cukup dan minum air putih",
            "Zumba seru bareng teman-teman",
        ],
        "business": [
            "Promo diskon 50 persen khusus akhir pekan",
            "Grand opening toko kami hari Sabtu",
            "Open order produk handmade terbatas",
            "Giveaway berhadiah untuk pengikut setia",
            "Terima kasih pelanggan atas 1000 pesanan",
            "Flash sale produk skincare mulai jam 8 malam",
            "Cerita awal membangun UMKM dari rumah",
            "Katalog produk baru sudah tersedia",
            "Gratis ongkir untuk semua pembelian hari ini",
            "Pre order koleksi baru batch pertama",
            "Kolaborasi brand lokal dengan kreator konten",
            "Tips jualan online supaya laris",
        ],
        "lifestyle": [
            "Hari santai di rumah sambil baca buku",
            "Ulang tahun sahabat dirayakan sederhana",
            "Kumpul keluarga di akhir pekan",
            "Me time malam hari dengan lilin aromaterapi",
            "Dekorasi kamar baru dengan nuansa pastel",
            "Nonton film bareng di bioskop",
            "Kucing lucu tidur di pangkuan",
            "Hujan sore hari ditemani teh hangat",
            "Wisuda akhirnya tiba setelah perjuangan panjang",
            "Bersyukur atas hari yang menyenangkan",
            "Main bareng sahabat sambil tertawa lepas",
            "Anniversary romantis dengan pasangan",
        ],
    },
    "en": {
        "food": [
            "Launching our new brown sugar latte at the cafe",
            "Trying the spiciest ramen with my coworkers",
            "Easy fried rice recipe for a quick breakfast",
            "Review of the best meatball soup in town",
            "Melting chocolate dessert box for the weekend",
            "Aesthetic brunch with fresh coffee",
            "New menu: crispy fried chicken with hot sauce",
            "How to bake fudgy brownies that never fail",
            "Late night street food tour at the food market",
            "Hot tea and fried bananas on a rainy day",
            "Dinner at my favorite steakhouse",
            "Special offer on our chicken satay combo",
        ],
        "travel": [
            "Watching the sunset at the beach in Bali",
            "Selfie at the beach wearing a straw hat",
            "Sunrise hike up the volcano",
            "Staycation at a hotel with a city view",
            "Road trip from Jakarta to Bandung with my best friends",
            "Exploring the old town on a rickshaw",
            "Weekend camping by the lake",
            "Snorkeling in crystal clear water",
            "Backpacking through Japan to see cherry blossoms",
            "Chasing hidden waterfalls in the forest",
            "Healing trip to the cool mountains",
            "Picnic in the park with a beautiful view",
        ],
        "fashion": [
            "OOTD oversized shirt with jeans",
            "Our new floral dress collection is here",
            "Mix and match pastel hijab outfits",
            "New pink sneakers for a casual walk",
            "Handmade leather bag latest collection",
            "Tips for styling batik at formal events",
            "Natural glowing makeup for everyday looks",
            "Morning skincare routine for bright skin",
            "Streetwear style with a vintage denim jacket",
            "Simple but elegant wedding guest outfit",
            "Minimalist gold necklace accessories",
            "Matching family outfits lookbook",
        ],
        "career": [
            "My first experience as a team manager",
            "Tips for passing a startup job interview",
            "Lessons in leadership from a failed project",
            "New certification in project management",
            "First day at my new office",
            "How to build your personal brand on LinkedIn",
            "Career webinar for fresh graduates",
            "What I learned from five years of remote work",
            "Networking strategies for young professionals",
            "Got promoted after a year of hard work",
            "Tips to stay productive working from home",
            "Mentoring new team members at work",
        ],
        "tech": [
            "Releasing our new mobile app built by our team",
            "Learning Python coding from scratch",
            "Review of the latest smartphone with an amazing camera",
            "Data security and password tips for beginners",
            "AI helps me finish daily work faster",
            "Programmer desk setup with dual monitors",
            "Tutorial on building a website with JavaScript",
            "48 hour hackathon with young developers",
            "High spec gaming laptop gadget",
            "New feature update in our app",
            "Learning machine learning for data analysis",
            "Local tech startup launches a digital platform",
        ],
        "fitness": [
            "Morning run of 5 kilometers in the park",
            "Lifting weights at the gym today",
            "Easy yoga session to calm the mind",
            "Healthy diet tips and a low calorie salad menu",
            "Weekend cycling with the community",
            "Home workout with no equipment",
            "Finished my first marathon",
            "Healthy meal prep for the whole week",
            "Stretching routine before bed",
            "Morning swim to feel fresh",
            "Staying healthy with enough sleep and water",
            "Fun zumba class with friends",
        ],
        "business": [
            "50 percent off everything this weekend",
            "Grand opening of our store on Saturday",
            "Limited open order for handmade products",
            "Giveaway with prizes for our loyal followers",
            "Thank you customers for 1000 orders",
            "Skincare flash sale starts at 8 pm",
            "The story of building a small business from home",
            "Our new product catalog is now available",
            "Free shipping on all purchases today",
            "Pre order our first batch of the new collection",
            "Local brand collaboration with content creators",
            "Tips for selling online and getting more sales",
        ],
        "lifestyle": [
            "Lazy Sunday reading a book at home",
            "Celebrating my best friend's birthday simply",
            "Family get together this weekend",
            "Me time at night with an aromatherapy candle",
            "New room decoration with pastel vibes",
            "Movie night at the cinema",
            "Cute cat sleeping on my lap",
            "Rainy afternoon with a cup of warm tea",
            "Graduation day finally arrived after a long journey",
            "Grateful for a wonderful day",
            "Laughing out loud with friends",
            "Romantic anniversary with my partner",
        ],
    },
}

KEYWORDS = {
    "id": {
        "food": "kopi makan makanan resep kafe cafe restoran menu masakan nasi mie ramen bakso sate ayam kue brownies dessert camilan jajan minuman teh coklat pizza burger sambal sarapan kuliner enak lezat steak roti es krim gula aren matcha seblak martabak",
        "travel": "liburan pantai gunung hiking wisata pulau hotel penginapan trip traveling jalan-jalan sunset sunrise camping danau air terjun bandara tiket backpacker destinasi healing snorkeling villa bali lombok jepang korea kemah",
        "fashion": "outfit ootd baju dress kemeja celana hijab sepatu sneakers tas aksesoris makeup skincare kosmetik batik jaket rok gaya lookbook kalung jam tangan parfum kacamata",
        "career": "karier kerja pekerjaan kantor interview manajer leadership profesional lowongan linkedin promosi jabatan sertifikasi mentor tim rekan perusahaan magang resign gaji freelance networking",
        "tech": "aplikasi coding program programmer developer software website ai data startup gadget laptop smartphone teknologi digital python javascript server cloud hackathon robot internet bug fitur",
        "fitness": "olahraga lari gym yoga workout diet sehat kesehatan sepeda gowes marathon renang fitness otot stretching zumba kalori protein latihan pilates",
        "business": "promo diskon sale toko jualan umkm pelanggan order giveaway produk katalog preorder ongkir opening brand voucher cashback reseller dropship pembeli harga",
        "lifestyle": "santai keluarga sahabat ulangtahun wisuda anniversary pasangan kucing anjing buku film hujan malam bersyukur bahagia rumah kamar dekorasi metime teman kenangan akhirpekan",
    },
    "en": {
        "food": "coffee food meal recipe cafe restaurant menu cooking rice noodles ramen meatball satay chicken cake brownies dessert snack drink tea chocolate pizza burger sauce breakfast delicious tasty steak bread icecream latte matcha bakery",
        "travel": "vacation beach mountain hiking trip hotel resort island sunset sunrise camping lake waterfall airport ticket backpacker destination healing snorkeling villa journey adventure roadtrip tour sightseeing",
        "fashion": "outfit ootd clothes dress shirt pants hijab shoes sneakers bag accessories makeup skincare cosmetics jacket skirt style lookbook necklace watch perfume sunglasses denim",
        "career": "career job work office interview manager leadership professional vacancy linkedin promotion certification mentor team colleague company internship resign salary freelance networking resume",
        "tech": "app coding programming programmer developer software website ai data startup gadget laptop smartphone technology digital python javascript server cloud hackathon robot internet bug feature",
        "fitness": "exercise running gym yoga workout diet healthy health cycling marathon swimming fitness muscle stretching zumba calories protein training pilates",
        "business": "promo discount sale store shop customer order giveaway product catalog preorder shipping opening brand voucher cashback reseller dropship buyer price",
        "lifestyle": "relax family friends birthday graduation anniversary partner cat dog book movie rain night grateful happy home room decoration metime memories weekend",
    },
}


def build_pipeline():
    features = FeatureUnion([
        ("word", TfidfVectorizer(analyzer="word", ngram_range=(1, 2), sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True)),
    ])
    return Pipeline([("features", features), ("clf", LogisticRegression(C=30, max_iter=3000))])


def sentence_samples():
    texts, categories, languages = [], [], []
    for language, groups in DATASET.items():
        for category, sentences in groups.items():
            for sentence in sentences:
                texts.append(sentence)
                categories.append(category)
                languages.append(language)
    return texts, categories, languages


def keyword_samples():
    texts, categories, languages = [], [], []
    for language, groups in KEYWORDS.items():
        for category, line in groups.items():
            for word in line.split():
                texts.append(word)
                categories.append(category)
                languages.append(language)
    return texts, categories, languages


def exclusive_keywords(texts, languages):
    owners = {}
    for text, language in zip(texts, languages):
        owners.setdefault(text, set()).add(language)
    keep = [i for i, text in enumerate(texts) if len(owners[text]) == 1]
    return [texts[i] for i in keep], [languages[i] for i in keep]


def evaluate(texts, labels, extra_texts, extra_labels):
    scores = []
    folds = StratifiedKFold(n_splits=4, shuffle=True, random_state=7)
    for train_idx, test_idx in folds.split(texts, labels):
        pipeline = build_pipeline()
        pipeline.fit(
            [texts[i] for i in train_idx] + extra_texts,
            [labels[i] for i in train_idx] + extra_labels,
        )
        scores.append(pipeline.score([texts[i] for i in test_idx], [labels[i] for i in test_idx]))
    return sum(scores) / len(scores)


def main():
    texts, categories, languages = sentence_samples()
    kw_texts, kw_categories, kw_languages = keyword_samples()
    lang_kw_texts, lang_kw_labels = exclusive_keywords(kw_texts, kw_languages)

    print(f"Category accuracy (CV): {evaluate(texts, categories, kw_texts, kw_categories):.0%}")
    print(f"Language accuracy (CV): {evaluate(texts, languages, lang_kw_texts, lang_kw_labels):.0%}")

    category_model = build_pipeline()
    category_model.fit(texts + kw_texts, categories + kw_categories)
    language_model = build_pipeline()
    language_model.fit(texts + lang_kw_texts, languages + lang_kw_labels)

    joblib.dump({"category": category_model, "language": language_model}, "model.pkl")
    print("model.pkl saved")


if __name__ == "__main__":
    main()