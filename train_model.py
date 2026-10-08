import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import FeatureUnion, Pipeline

DATASET = {
    "kuliner": [
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
    "karier": [
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
    "teknologi": [
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
    "kebugaran": [
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
    "bisnis": [
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
}


KEYWORDS = {
    "kuliner": "kopi makan makanan resep kafe cafe restoran menu masakan nasi mie ramen bakso sate ayam kue brownies dessert camilan jajan minuman teh coklat pizza burger sambal sarapan kuliner enak lezat steak roti es krim gula aren matcha seblak martabak",
    "travel": "liburan pantai gunung hiking wisata pulau hotel penginapan trip traveling jalan-jalan sunset sunrise camping danau air terjun bandara tiket backpacker destinasi healing snorkeling villa bali lombok jepang korea kemah",
    "fashion": "outfit ootd baju dress kemeja celana hijab sepatu sneakers tas aksesoris makeup skincare kosmetik batik jaket rok gaya lookbook kalung jam tangan parfum kacamata",
    "karier": "karier kerja pekerjaan kantor interview manajer leadership profesional lowongan linkedin promosi jabatan sertifikasi mentor tim rekan perusahaan magang resign gaji freelance networking",
    "teknologi": "aplikasi coding program programmer developer software website ai data startup gadget laptop smartphone teknologi digital python javascript server cloud hackathon robot internet bug fitur",
    "kebugaran": "olahraga lari gym yoga workout diet sehat kesehatan sepeda gowes marathon renang fitness otot stretching zumba kalori protein latihan pilates",
    "bisnis": "promo diskon sale toko jualan umkm pelanggan order giveaway produk katalog preorder ongkir opening brand voucher cashback reseller dropship pembeli harga",
    "lifestyle": "santai keluarga sahabat ulangtahun wisuda anniversary pasangan kucing anjing buku film hujan malam bersyukur bahagia rumah kamar dekorasi metime teman kenangan akhirpekan",
}


def build_pipeline():
    features = FeatureUnion([
        ("word", TfidfVectorizer(analyzer="word", ngram_range=(1, 2), sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True)),
    ])
    return Pipeline([("features", features), ("clf", LogisticRegression(C=30, max_iter=3000))])


def keyword_samples():
    texts, labels = [], []
    for label, line in KEYWORDS.items():
        for word in line.split():
            texts.append(word)
            labels.append(label)
    return texts, labels


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
    texts = [text for items in DATASET.values() for text in items]
    labels = [label for label, items in DATASET.items() for _ in items]
    extra_texts, extra_labels = keyword_samples()
    print(f"Akurasi cross-validation: {evaluate(texts, labels, extra_texts, extra_labels):.0%}")
    pipeline = build_pipeline()
    pipeline.fit(texts + extra_texts, labels + extra_labels)
    joblib.dump(pipeline, "model.pkl")
    print("model.pkl tersimpan")


if __name__ == "__main__":
    main()
