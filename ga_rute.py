import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)
import numpy as np, random
import matplotlib.pyplot as plt

random.seed(7); rng = np.random.default_rng(7)
N = 15
KOTA = rng.uniform(0, 100, (N, 2))          # koordinat 15 titik antar (km)
D = np.linalg.norm(KOTA[:, None] - KOTA[None], axis=2)

def jarak(rute):
    return sum(D[rute[i], rute[(i + 1) % N]] for i in range(N))

def init_pop(n): return [random.sample(range(N), N) for _ in range(n)]

def seleksi(pop, k=5):                       # tournament selection
    return min(random.sample(pop, k), key=jarak)

def crossover(p1, p2):                       # order crossover (OX)
    a, b = sorted(random.sample(range(N), 2))
    anak = [None] * N; anak[a:b] = p1[a:b]
    sisa = [g for g in p2 if g not in anak]
    idx = 0
    for i in range(N):
        if anak[i] is None: anak[i] = sisa[idx]; idx += 1
    return anak

def mutasi(r, pm=0.2):                       # swap mutation
    r = r[:]
    if random.random() < pm:
        i, j = random.sample(range(N), 2); r[i], r[j] = r[j], r[i]
    return r

def jalankan(pop_size=100, gen=200, elit=2):
    pop = init_pop(pop_size); hist_best = []; hist_avg = []
    for g in range(gen):
        pop.sort(key=jarak)
        hist_best.append(jarak(pop[0])); hist_avg.append(np.mean([jarak(p) for p in pop]))
        baru = pop[:elit]
        while len(baru) < pop_size:
            baru.append(mutasi(crossover(seleksi(pop), seleksi(pop))))
        pop = baru
    pop.sort(key=jarak)
    return pop[0], hist_best, hist_avg

if __name__ == "__main__":
    acak = init_pop(1)[0]
    awal_terbaik = min(init_pop(100), key=jarak)
    best, hb, ha = jalankan()
    print("=== ALGORITMA GENETIKA: OPTIMASI RUTE PENGANTARAN (15 TITIK) ===")
    print("Parameter: populasi=100, generasi=200, tournament=5, elitisme=2, pm=0.2")
    print(f"Jarak rute acak            : {jarak(acak):.2f} km")
    print(f"Jarak terbaik generasi 1   : {hb[0]:.2f} km")
    print(f"Jarak terbaik generasi 200 : {hb[-1]:.2f} km")
    print(f"Penghematan vs rute acak   : {(1 - hb[-1]/jarak(acak))*100:.1f}%")
    print("Rute terbaik:", " -> ".join(f"T{i+1}" for i in best + [best[0]]))
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
    ax[0].plot(hb, label="Terbaik"); ax[0].plot(ha, label="Rata-rata", alpha=.6)
    ax[0].set_title("Konvergensi GA"); ax[0].set_xlabel("Generasi"); ax[0].set_ylabel("Jarak total (km)")
    ax[0].legend(); ax[0].grid(alpha=.3)
    r = best + [best[0]]
    ax[1].plot(KOTA[r, 0], KOTA[r, 1], "-o", color="tab:blue")
    for i, (x, y) in enumerate(KOTA): ax[1].annotate(f"T{i+1}", (x, y), textcoords="offset points", xytext=(5, 5))
    ax[1].set_title(f"Rute terbaik ({hb[-1]:.1f} km)"); ax[1].grid(alpha=.3)
    plt.tight_layout(); plt.savefig("output/ga_hasil.png", dpi=150); plt.show()
