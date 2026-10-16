import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)
import numpy as np
import matplotlib.pyplot as plt

def tri(x, a, b, c):
    """Fungsi keanggotaan segitiga."""
    x = np.asarray(x, dtype=float)
    left = np.where(b != a, (x - a) / (b - a + 1e-12), 1.0)
    right = np.where(c != b, (c - x) / (c - b + 1e-12), 1.0)
    return np.clip(np.minimum(left, right), 0, 1)

def trap(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    left = (x - a) / (b - a + 1e-12)
    right = (d - x) / (d - c + 1e-12)
    return np.clip(np.minimum(np.minimum(left, 1), right), 0, 1)

# Semesta pembicaraan
X_SUHU = np.linspace(0, 45, 451)
X_LEMBAP = np.linspace(0, 100, 1001)
X_DURASI = np.linspace(0, 30, 601)

# Himpunan fuzzy
SUHU = {"Dingin": lambda x: trap(x, -1, 0, 15, 25),
        "Normal": lambda x: tri(x, 18, 27, 36),
        "Panas":  lambda x: trap(x, 30, 37, 45, 46)}
LEMBAP = {"Kering": lambda x: trap(x, -1, 0, 25, 45),
          "Lembap": lambda x: tri(x, 30, 50, 70),
          "Basah":  lambda x: trap(x, 55, 75, 100, 101)}
DURASI = {"Singkat": lambda x: trap(x, -1, 0, 5, 12),
          "Sedang":  lambda x: tri(x, 8, 15, 22),
          "Lama":    lambda x: trap(x, 18, 25, 30, 31)}

# Basis aturan: (suhu, lembap) -> durasi
ATURAN = [("Dingin", "Kering", "Sedang"), ("Dingin", "Lembap", "Singkat"), ("Dingin", "Basah", "Singkat"),
          ("Normal", "Kering", "Lama"),   ("Normal", "Lembap", "Sedang"),  ("Normal", "Basah", "Singkat"),
          ("Panas", "Kering", "Lama"),    ("Panas", "Lembap", "Sedang"),   ("Panas", "Basah", "Singkat")]

def infer(suhu, lembap, detail=False):
    mu_s = {k: float(f(suhu)) for k, f in SUHU.items()}
    mu_l = {k: float(f(lembap)) for k, f in LEMBAP.items()}
    agg = np.zeros_like(X_DURASI)
    fired = []
    for s, l, d in ATURAN:
        alpha = min(mu_s[s], mu_l[l])            # operator AND = MIN
        if alpha > 0:
            fired.append((s, l, d, alpha))
        agg = np.maximum(agg, np.minimum(alpha, DURASI[d](X_DURASI)))  # implikasi MIN, agregasi MAX
    z = float((agg * X_DURASI).sum() / (agg.sum() + 1e-12))            # defuzzifikasi centroid
    return (z, mu_s, mu_l, fired, agg) if detail else z

def plot_all(suhu, lembap, path):
    z, mu_s, mu_l, fired, agg = infer(suhu, lembap, True)
    fig, ax = plt.subplots(1, 3, figsize=(15, 3.8))
    for k, f in SUHU.items(): ax[0].plot(X_SUHU, f(X_SUHU), label=k)
    ax[0].axvline(suhu, color="k", ls="--"); ax[0].set_title("Suhu (°C)")
    for k, f in LEMBAP.items(): ax[1].plot(X_LEMBAP, f(X_LEMBAP), label=k)
    ax[1].axvline(lembap, color="k", ls="--"); ax[1].set_title("Kelembapan tanah (%)")
    for k, f in DURASI.items(): ax[2].plot(X_DURASI, f(X_DURASI), alpha=.4, label=k)
    ax[2].fill_between(X_DURASI, agg, color="tab:orange", alpha=.5, label="Hasil agregasi")
    ax[2].axvline(z, color="r", label=f"Centroid = {z:.2f} mnt"); ax[2].set_title("Durasi penyiraman (menit)")
    for a in ax: a.legend(fontsize=8); a.set_ylim(0, 1.05); a.grid(alpha=.3)
    plt.tight_layout(); plt.savefig(path, dpi=150); plt.show()

def plot_surface(path):
    S, L = np.meshgrid(np.linspace(0, 45, 30), np.linspace(0, 100, 30))
    Z = np.vectorize(infer)(S, L)
    fig = plt.figure(figsize=(6.5, 4.8)); ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(S, L, Z, cmap="viridis"); ax.set_xlabel("Suhu (°C)"); ax.set_ylabel("Kelembapan (%)")
    ax.set_zlabel("Durasi (menit)"); ax.set_title("Permukaan kontrol fuzzy")
    plt.tight_layout(); plt.savefig(path, dpi=150); plt.show()

if __name__ == "__main__":
    suhu, lembap = 35, 30
    z, mu_s, mu_l, fired, _ = infer(suhu, lembap, True)
    print("=== FUZZY MAMDANI: DURASI PENYIRAMAN ===")
    print(f"Input: suhu = {suhu} C, kelembapan tanah = {lembap} %")
    print("Derajat keanggotaan suhu     :", {k: round(v, 3) for k, v in mu_s.items()})
    print("Derajat keanggotaan kelembapan:", {k: round(v, 3) for k, v in mu_l.items()})
    print("Aturan yang aktif:")
    for s, l, d, a in fired: print(f"  JIKA suhu {s} DAN tanah {l} MAKA durasi {d}  (alpha = {a:.3f})")
    print(f"Output (centroid): {z:.2f} menit")
    for s_, l_ in [(20, 80), (27, 50), (40, 10)]:
        print(f"Uji suhu={s_}, lembap={l_} -> {infer(s_, l_):.2f} menit")
    plot_all(suhu, lembap, "output/fuzzy_hasil.png"); plot_surface("output/fuzzy_surface.png")
