import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, Polygon

# ====================== 1. ENGINE FRAME ======================
class Frame:
    """Frame = nama + superclass + slot (atribut:nilai) + contains (frame anak)."""
    def __init__(self, name, superclass=None, contains=None, **slots):
        self.name, self.superclass, self.slots = name, superclass, slots
        self.contains = list(contains or [])

    def get(self, key, default=None):          # pewarisan: cari di diri sendiri, lalu superclass
        if key in self.slots: return self.slots[key]
        if self.superclass is not None: return self.superclass.get(key, default)
        return default

    def tree(self, depth=0, maks=1):           # cetak struktur frame (untuk laporan/screenshot)
        sup = self.superclass.name if self.superclass else "-"
        print("  " * depth + f"{self.name}  (superclass: {sup}, isi: {len(self.contains)} frame)")
        if depth < maks:
            for c in self.contains:
                if c.contains: c.tree(depth + 1, maks)

def render(f, ax):
    """Menggambar sebuah frame sesuai slot 'shape', lalu menggambar semua frame di slot contains."""
    s, g = f.get("shape"), f.get
    col, ec = g("color", "none"), g("edge", "none")
    if s == "rect":   ax.add_patch(Rectangle((g("x"), g("y")), g("w"), g("h"), fc=col, ec=ec, lw=g("lw", 1)))
    elif s == "circle": ax.add_patch(Circle((g("x"), g("y")), g("r"), fc=col, ec=ec, lw=g("lw", 1)))
    elif s == "ellipse": ax.add_patch(Ellipse((g("x"), g("y")), g("w"), g("h"), angle=g("angle", 0), fc=col, ec=ec, lw=g("lw", 1)))
    elif s == "poly": ax.add_patch(Polygon(g("points"), closed=True, fc=col, ec=ec, lw=g("lw", 1)))
    elif s == "line": ax.plot(*zip(*g("points")), color=col, lw=g("lw", 1), alpha=g("alpha", 1), solid_capstyle="round")
    elif s == "arrow": ax.annotate("", xy=g("to"), xytext=g("from"), arrowprops=dict(arrowstyle="-|>", color=col, lw=g("lw", 2)))
    elif s == "text": ax.text(g("x"), g("y"), g("text"), fontsize=g("size", 10), color=col if col != "none" else "k",
                              ha=g("ha", "center"), va="center", weight=g("weight", "normal"))
    for c in f.contains: render(c, ax)

def gambar(root, path, judul="", size=(10, 6)):
    fig, ax = plt.subplots(figsize=size); ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.set_aspect("equal"); ax.axis("off")
    render(root, ax)
    if judul: ax.set_title(judul, fontsize=12, weight="bold")
    plt.tight_layout(); plt.savefig(path, dpi=150); plt.show()

# kelas dasar (superclass)
OBJEK = Frame("objek", edge="#222222", lw=1)
BAGIAN = Frame("bagian", OBJEK, shape="rect")

# ====================== 2. CONTOH: KAMAR MANDI ======================
def scene_kamar_mandi():
    R = lambda n, x, y, w, h, c, **k: Frame(n, BAGIAN, x=x, y=y, w=w, h=h, color=c, **k)
    ubin = [Frame(f"nat v{i}", BAGIAN, shape="line", points=[(i * 10, 16), (i * 10, 60)], color="white", lw=1, alpha=.7) for i in range(1, 10)] + \
           [Frame(f"nat h{i}", BAGIAN, shape="line", points=[(0, 16 + i * 11), (100, 16 + i * 11)], color="white", lw=1, alpha=.7) for i in range(1, 4)]
    pintu = Frame("pintu kamar mandi", OBJEK, contains=[R("daun pintu", 4, 16, 9, 30, "#8b5a2b"), Frame("gagang", BAGIAN, shape="circle", x=11.3, y=30, r=.7, color="#d4af37")])
    wastafel = Frame("wastafel", OBJEK, contains=[
        R("lemari", 20, 16, 16, 10, "#e8e8e8"), R("meja", 19, 26, 18, 1.6, "#ffffff"),
        Frame("bak cuci", BAGIAN, shape="ellipse", x=28, y=27.6, w=11, h=2.8, color="#bfe0ea"),
        R("keran", 27.4, 28.5, 1.2, 3, "#9a9a9a"), R("cermin", 21.5, 34, 13, 12, "#a9dcef", edge="#777777", lw=2)])
    toilet = Frame("toilet", OBJEK, contains=[
        R("dasar", 46, 16, 8, 6, "#ffffff"), R("tangki", 44, 24, 9, 11, "#ffffff"), R("tombol", 47.5, 35, 2, .8, "#9a9a9a"),
        R("dudukan toilet", 43, 22, 14, 2, "#f2f2f2"), Frame("mangkuk", BAGIAN, shape="ellipse", x=51, y=21.2, w=13, h=5, color="#ffffff")])
    bathtub = Frame("bathtub", OBJEK, contains=[
        R("badan bak", 62, 16, 34, 12, "#ffffff"), R("air", 64, 18, 30, 6, "#8fd0f0", edge="none"),
        R("kaki kiri", 63, 14, 3, 2, "#9a9a9a"), R("kaki kanan", 92, 14, 3, 2, "#9a9a9a"), R("keran bak", 94, 28, 2, 4, "#9a9a9a")])
    shower = Frame("shower", OBJEK, contains=[R("tiang", 78.5, 28, 1, 22, "#9a9a9a"),
        Frame("kepala shower", BAGIAN, shape="ellipse", x=76, y=50.5, w=7, h=2.2, color="#9a9a9a")] +
        [Frame(f"tetes {i}", BAGIAN, shape="line", points=[(73 + i * 1.6, 49), (73 + i * 1.6, 44)], color="#3d9be0", lw=1.2) for i in range(5)])
    kamar = Frame("kamar mandi", OBJEK, location="rumah", contains=[
        R("dinding", 0, 16, 100, 44, "#cfe8ec", edge="none"), *ubin, R("lantai", 0, 0, 100, 16, "#b5b5b5", edge="none"),
        pintu, wastafel, toilet, bathtub, shower,
        Frame("judul", BAGIAN, shape="text", x=50, y=55, text="kamar mandi", size=12, weight="bold")])
    print("\n=== STRUKTUR FRAME: KAMAR MANDI ==="); kamar.tree()
    gambar(kamar, "output/scene_kamar_mandi.png", "Frame kamar mandi -> gambar")

# ====================== 3. FUZZY: KEBUN + PENYIRAMAN ======================
def scene_fuzzy(suhu=35, lembap=30):
    from fuzzy_penyiraman import infer
    durasi = infer(suhu, lembap)
    t = suhu / 45; w = lembap / 100
    tanah_c = tuple(np.array([0.85, 0.72, 0.52]) * (1 - w) + np.array([0.33, 0.22, 0.13]) * w)
    daun_c = tuple(np.array([0.78, 0.74, 0.25]) * (1 - w) + np.array([0.15, 0.6, 0.2]) * w)   # layu -> segar
    R = lambda n, x, y, w_, h, c, **k: Frame(n, BAGIAN, x=x, y=y, w=w_, h=h, color=c, **k)
    tanaman = []
    for i, px in enumerate([14, 28, 42, 56, 70]):
        tinggi = 9 + 7 * w
        daun = [Frame(f"daun {i}{j}", BAGIAN, shape="ellipse", x=px + d * 3.2, y=18 + tinggi * .8, w=6, h=2.6, angle=30 * d * (1 if w > .4 else 2.5), color=daun_c) for j, d in enumerate((-1, 1))]
        tanaman.append(Frame(f"tanaman {i+1}", OBJEK, contains=[R("batang", px - .4, 18, .8, tinggi, "#3f7a2a", edge="none")] + daun))
    retak = [Frame(f"retakan {i}", BAGIAN, shape="line", points=[(a, 17), (a + 2, 12), (a - 1, 7)], color="#6b4e2e", lw=1.2) for i, a in enumerate([10, 25, 40, 55, 70, 85])] if lembap < 40 else []
    n_tetes = int(durasi / 2.5)
    tetes = [Frame(f"tetes {i}", BAGIAN, shape="circle", x=35 + 4.2 * (i % 6) * (1 if i % 2 else -1) * .8 + (i // 3), y=45 - (i * 1.5) % 14, r=.55, color="#2f8fe0", edge="none") for i in range(n_tetes)]
    sprinkler = Frame("sprinkler", OBJEK, contains=[R("tiang", 34.4, 18, 1.2, 20, "#555555"), Frame("kepala", BAGIAN, shape="circle", x=35, y=40, r=2.2, color="#888888")] + tetes)
    termo = Frame("thermometer", OBJEK, contains=[R("tabung", 90, 30, 2.4, 16, "#ffffff"), R("isi merkuri", 90.3, 30.3, 1.8, 15 * t, "#d62828", edge="none"),
        Frame("bulb", BAGIAN, shape="circle", x=91.2, y=29.5, r=2.4, color="#d62828")])
    matahari = Frame("matahari", OBJEK, shape="circle", x=80, y=52, r=3 + 3 * t, color=(1, 0.8 - .5 * t, 0.1), edge="#e08a00")
    kebun = Frame("sistem penyiraman", OBJEK, contains=[
        R("langit", 0, 18, 100, 42, "#bfe3f7", edge="none"), Frame("tanah", BAGIAN, shape="rect", x=0, y=0, w=100, h=18, color=tanah_c, edge="none"),
        matahari, termo, *retak, *tanaman, sprinkler,
        Frame("t1", BAGIAN, shape="text", x=79, y=44, text=f"Suhu {suhu} °C", size=10),
        Frame("t2", BAGIAN, shape="text", x=50, y=9, text=f"Kelembapan tanah {lembap} %  (kering)" if lembap < 40 else f"Kelembapan tanah {lembap} %", size=10, color="white" if w > .5 else "black"),
        Frame("t3", BAGIAN, shape="text", x=50, y=2.5, text=f"Durasi penyiraman (fuzzy) = {durasi:.2f} menit", size=11, weight="bold", color="white" if w > .5 else "black")])
    print("\n=== STRUKTUR FRAME: SISTEM PENYIRAMAN ==="); kebun.tree()
    gambar(kebun, "output/scene_fuzzy.png", f"Frame sistem fuzzy -> kebun (suhu {suhu} °C, tanah {lembap} %)")

# ====================== 4. JST: BUNGA IRIS -> JARINGAN -> KELAS ======================
def scene_jst():
    import jst_iris as J
    X_raw = J.sc.inverse_transform(J.Xte)
    idx = next(i for i in range(len(J.yte)) if J.yte[i] == 1 and J.pred[i] == 1)      # contoh versicolor yang benar
    fitur, prob = X_raw[idx], J.pte[idx]
    kelas = J.iris.target_names; warna = ["#8e44ad", "#2980b9", "#c0392b"]; pk = int(prob.argmax())
    pl, pw = fitur[2], fitur[3]
    petal = [Frame(f"petal {k}", BAGIAN, shape="ellipse", x=14 + np.cos(np.deg2rad(a)) * pl * 1.5, y=36 + np.sin(np.deg2rad(a)) * pl * 1.5,
                   w=pl * 3.2, h=pw * 5 + 2, angle=a, color=warna[pk], edge="#222222") for k, a in enumerate(range(90, 450, 72))]
    bunga = Frame("bunga iris", OBJEK, contains=[Frame("tangkai", BAGIAN, shape="rect", x=13.4, y=8, w=1.2, h=16, color="#3f7a2a", edge="none"),
        Frame("sepal", BAGIAN, shape="ellipse", x=14, y=26, w=fitur[1] * 4 + 4, h=fitur[0] * 1.2, color="#5cae4a", edge="#222222"), *petal,
        Frame("pusat", BAGIAN, shape="circle", x=14, y=36, r=1.6, color="#f1c40f"),
        Frame("ft", BAGIAN, shape="text", x=14, y=4, text=f"sepal {fitur[0]:.1f}x{fitur[1]:.1f} | petal {fitur[2]:.1f}x{fitur[3]:.1f} cm", size=8)])
    xs = [40, 62, 86]; ukuran = [4, 8, 3]; node = {}; garis = []; nodes = []
    for L, (x, n) in enumerate(zip(xs, ukuran)):
        ys = np.linspace(48, 14, n) if n > 3 else np.linspace(40, 22, n) if n == 4 else np.linspace(38, 20, n)
        if n == 8: ys = np.linspace(51, 9, n)
        if n == 4: ys = np.linspace(42, 18, n)
        if n == 3: ys = np.linspace(40, 20, n)
        node[L] = [(x, y) for y in ys]
    for L in range(2):
        for a in node[L]:
            for b in node[L + 1]: garis.append(Frame("bobot", BAGIAN, shape="line", points=[a, b], color="#bbbbbb", lw=.5))
    for L in range(3):
        for k, (x, y) in enumerate(node[L]):
            c = "#ffffff"
            if L == 0: c = "#f9e79f"
            if L == 2: c = "#58d68d" if k == pk else "#fadbd8"
            nodes.append(Frame(f"neuron {L}{k}", BAGIAN, shape="circle", x=x, y=y, r=1.7, color=c, edge="#222222"))
    lab = [Frame("l1", BAGIAN, shape="text", x=40, y=56, text="input (4)", size=9), Frame("l2", BAGIAN, shape="text", x=62, y=56, text="hidden (8, tanh)", size=9),
           Frame("l3", BAGIAN, shape="text", x=86, y=56, text="output (3, softmax)", size=9)]
    klas = [Frame(f"k{k}", BAGIAN, shape="text", x=93.5, y=node[2][k][1], text=f"{kelas[k]}\n{prob[k]*100:.1f}%", size=7.5, ha="left", weight="bold" if k == pk else "normal") for k in range(3)]
    jst = Frame("jst iris", OBJEK, contains=[Frame("latar", BAGIAN, shape="rect", x=0, y=0, w=100, h=60, color="#fdfefe", edge="none"), bunga, *garis, *nodes, *lab, *klas,
        Frame("hasil", BAGIAN, shape="text", x=50, y=2.5, text=f"Prediksi JST: {kelas[pk]} (aktual: {kelas[J.yte[idx]]})", size=11, weight="bold", color="#1e8449")])
    print("\n=== STRUKTUR FRAME: JST IRIS ==="); jst.tree()
    gambar(jst, "output/scene_jst.png", "Frame JST -> bunga iris masuk jaringan, keluar kelas", (11, 6))

# ====================== 5. GA: PETA PENGANTARAN ======================
def scene_ga():
    import ga_rute as G
    G.init_pop(1); min(G.init_pop(100), key=G.jarak)          # menyamakan urutan angka acak dengan ga_rute.py
    best, hb, _ = G.jalankan()
    P = lambda p: (4 + 0.92 * p[0], 4 + 0.50 * p[1])
    pts = [P(G.KOTA[i]) for i in best]
    rute = [Frame(f"jalan {k}", BAGIAN, shape="line", points=[pts[k], pts[(k + 1) % 15]], color="#7f8c8d", lw=6, alpha=.6) for k in range(15)]
    panah = [Frame(f"arah {k}", BAGIAN, shape="arrow", **{"from": pts[k], "to": pts[(k + 1) % 15]}, color="#1f4fd8", lw=1.6) for k in range(15)]
    rumah = []
    for k, (x, y) in enumerate(pts):
        if k == 0: continue
        rumah += [Frame(f"rumah {k}", BAGIAN, shape="rect", x=x - 1.3, y=y - 1.1, w=2.6, h=2.2, color="#f5cba7"),
                  Frame(f"atap {k}", BAGIAN, shape="poly", points=[(x - 1.7, y + 1.1), (x + 1.7, y + 1.1), (x, y + 3)], color="#c0392b"),
                  Frame(f"label {k}", BAGIAN, shape="text", x=x, y=y - 2.6, text=f"T{best[k]+1}", size=7.5)]
    x0, y0 = pts[0]
    gudang = Frame("gudang", OBJEK, contains=[Frame("bangunan", BAGIAN, shape="rect", x=x0 - 3, y=y0 - 2, w=6, h=4, color="#d35400"), Frame("atap g", BAGIAN, shape="poly", points=[(x0 - 3.5, y0 + 2), (x0 + 3.5, y0 + 2), (x0, y0 + 4.5)], color="#7e2e00"),
        Frame("lg", BAGIAN, shape="text", x=x0, y=y0 - 3.6, text=f"Gudang (T{best[0]+1})", size=8, weight="bold")])
    truk = Frame("truk", OBJEK, contains=[Frame("bak", BAGIAN, shape="rect", x=x0 + 4, y=y0 - 1.5, w=4, h=2.6, color="#2980b9"), Frame("kabin", BAGIAN, shape="rect", x=x0 + 8, y=y0 - 1.5, w=2, h=1.8, color="#1b4f72"),
        Frame("roda1", BAGIAN, shape="circle", x=x0 + 5.3, y=y0 - 1.6, r=.6, color="black"), Frame("roda2", BAGIAN, shape="circle", x=x0 + 9, y=y0 - 1.6, r=.6, color="black")])
    peta = Frame("ga rute pengantaran", OBJEK, contains=[Frame("rumput", BAGIAN, shape="rect", x=0, y=0, w=100, h=60, color="#d5f0c1", edge="none"), *rute, *panah, *rumah, gudang, truk,
        Frame("jr", BAGIAN, shape="text", x=50, y=57, text=f"Rute terbaik GA: {hb[-1]:.2f} km (15 titik, 200 generasi)", size=11, weight="bold")])
    print("\n=== STRUKTUR FRAME: GA RUTE PENGANTARAN ==="); peta.tree()
    gambar(peta, "output/scene_ga.png", "Frame GA -> peta pengantaran dan rute terbaik", (11, 6.6))

if __name__ == "__main__":
    scene_kamar_mandi(); scene_fuzzy(); scene_jst(); scene_ga()
