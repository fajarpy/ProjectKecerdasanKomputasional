import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROW = 0.42
def draw(frames, links, path, size=(11, 6.5), title=""):
    fig, ax = plt.subplots(figsize=size); ax.set_xlim(0, size[0]); ax.set_ylim(-0.6, size[1]); ax.axis("off")
    pos = {}
    for name, (x, y, w, title_f, slots) in frames.items():
        h = ROW * (len(slots) + 1)
        ax.add_patch(Rectangle((x, y - h), w, h, fill=False, lw=1.4))
        ax.text(x + .08, y - ROW / 2, title_f, va="center", fontsize=10, weight="bold")
        for i, (k, v) in enumerate(slots):
            yy = y - ROW * (i + 1)
            ax.plot([x, x + w], [yy, yy], color="k", lw=.8)
            ax.text(x + .08, yy - ROW / 2, f"{k}:", va="center", fontsize=8.5)
            ax.text(x + w * .42, yy - ROW / 2, v, va="center", fontsize=8.5)
        pos[name] = (x, y, w, h)
    for n, (src, idx, dst) in enumerate(links):
        x, y, w, h = pos[src]; yy = y - ROW * (idx + 1) - ROW / 2
        x2, y2, w2, h2 = pos[dst]
        tx, ty = x2, y2 - ROW / 2
        sx = x + w; mx = sx + 0.35 + 0.35 * n
        ax.plot([sx, mx, mx], [yy, yy, ty], color="k", lw=1.1)
        ax.annotate("", xy=(tx, ty), xytext=(mx, ty), arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k", shrinkA=0, shrinkB=0))
    if title: ax.set_title(title, fontsize=11, weight="bold")
    plt.tight_layout(); plt.savefig(path, dpi=150); plt.show()

def frame_fuzzy():
    f = {"sis": (0.2, 6.2, 3.4, "sistem penyiraman", [("superclass", "sistem kontrol"), ("metode", "Mamdani"), ("defuzzifikasi", "centroid"),
            ("contains", "(variabel suhu"), ("", "variabel kelembapan"), ("", "variabel durasi)"), ("rules", "9 aturan JIKA-MAKA")]),
         "suhu": (5.2, 6.2, 3.0, "variabel suhu", [("superclass", "input"), ("semesta", "0-45 °C"), ("himpunan", "dingin, normal, panas")]),
         "lem": (5.2, 4.2, 3.0, "variabel kelembapan", [("superclass", "input"), ("semesta", "0-100 %"), ("himpunan", "kering, lembap, basah")]),
         "dur": (5.2, 2.2, 3.0, "variabel durasi", [("superclass", "output"), ("semesta", "0-30 menit"), ("himpunan", "singkat, sedang, lama")]),
         "aturan": (0.2, 2.4, 3.4, "aturan R3", [("superclass", "rule"), ("if suhu", "normal"), ("and tanah", "kering"), ("then durasi", "lama")])}
    draw(f, [("sis", 3, "suhu"), ("sis", 4, "lem"), ("sis", 5, "dur")], "output/frame_fuzzy.png", (9.2, 7.4), "Frame: Sistem Fuzzy Penyiraman Tanaman")

def frame_jst():
    f = {"jst": (0.2, 6.2, 3.4, "jst iris", [("superclass", "multilayer perceptron"), ("tugas", "klasifikasi"), ("pelatihan", "backpropagation"), ("optimizer", "gradient descent"),
            ("contains", "(lapisan input"), ("", "lapisan hidden"), ("", "lapisan output)")]),
         "in": (5.2, 6.2, 3.2, "lapisan input", [("superclass", "layer"), ("neuron", "4"), ("fitur", "sepal & petal (p, l)")]),
         "hid": (5.2, 4.2, 3.2, "lapisan hidden", [("superclass", "layer"), ("neuron", "8"), ("aktivasi", "tanh")]),
         "out": (5.2, 2.2, 3.2, "lapisan output", [("superclass", "layer"), ("neuron", "3"), ("aktivasi", "softmax"), ("kelas", "setosa, versicolor, virginica")]),
         "data": (0.2, 2.6, 3.4, "dataset iris", [("superclass", "data"), ("jumlah", "150 sampel"), ("latih : uji", "70 : 30")])}
    draw(f, [("jst", 4, "in"), ("jst", 5, "hid"), ("jst", 6, "out")], "output/frame_jst.png", (9.2, 7.4), "Frame: Jaringan Saraf Tiruan Klasifikasi Iris")

def frame_ga():
    f = {"ga": (0.2, 6.2, 3.4, "ga rute pengantaran", [("superclass", "algoritma evolusi"), ("masalah", "TSP 15 titik"), ("populasi", "100 individu"), ("generasi", "200"),
            ("contains", "(kromosom"), ("", "fungsi fitness"), ("", "operator genetika)")]),
         "kro": (5.2, 6.2, 3.2, "kromosom", [("superclass", "individu"), ("representasi", "permutasi titik"), ("contoh", "[7,13,4,3,...]")]),
         "fit": (5.2, 4.2, 3.2, "fungsi fitness", [("superclass", "evaluasi"), ("rumus", "total jarak rute"), ("tujuan", "minimalkan")]),
         "op": (5.2, 2.2, 3.2, "operator genetika", [("superclass", "operator"), ("seleksi", "tournament (k=5)"), ("crossover", "order crossover"), ("mutasi", "swap, pm = 0.2"), ("elitisme", "2 individu")]),
         "hasil": (0.2, 2.6, 3.4, "solusi terbaik", [("superclass", "hasil"), ("jarak", "389,20 km"), ("hemat", "46,2 % vs acak")])}
    draw(f, [("ga", 4, "kro"), ("ga", 5, "fit"), ("ga", 6, "op")], "output/frame_ga.png", (9.2, 7.4), "Frame: Algoritma Genetika Optimasi Rute")

if __name__ == "__main__":
    frame_fuzzy(); frame_jst(); frame_ga()
