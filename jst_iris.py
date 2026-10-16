import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("output", exist_ok=True)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
iris = load_iris()
X, y = iris.data, iris.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr); Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)
Ytr = np.eye(3)[ytr]

# Arsitektur 4 - 8 - 3 (input, hidden tanh, output softmax)
W1 = rng.normal(0, .5, (4, 8)); b1 = np.zeros(8)
W2 = rng.normal(0, .5, (8, 3)); b2 = np.zeros(3)

def forward(X):
    h = np.tanh(X @ W1 + b1)
    z = h @ W2 + b2
    e = np.exp(z - z.max(1, keepdims=True))
    return h, e / e.sum(1, keepdims=True)

lr, epochs = 0.1, 300
loss_hist, acc_hist = [], []
for ep in range(epochs):
    h, p = forward(Xtr)
    loss = -np.mean(np.sum(Ytr * np.log(p + 1e-12), axis=1))
    acc = np.mean(p.argmax(1) == ytr)
    loss_hist.append(loss); acc_hist.append(acc)
    dz = (p - Ytr) / len(Xtr)                    # backpropagation
    dW2 = h.T @ dz; db2 = dz.sum(0)
    dh = dz @ W2.T * (1 - h ** 2)
    dW1 = Xtr.T @ dh; db1 = dh.sum(0)
    W2 -= lr * dW2; b2 -= lr * db2; W1 -= lr * dW1; b1 -= lr * db1

_, pte = forward(Xte)
pred = pte.argmax(1)
acc_te = np.mean(pred == yte)
cm = np.zeros((3, 3), int)
for t, p_ in zip(yte, pred): cm[t, p_] += 1

if __name__ == "__main__":
    print("=== JARINGAN SARAF TIRUAN (MLP 4-8-3): KLASIFIKASI IRIS ===")
    print(f"Data latih: {len(Xtr)}, data uji: {len(Xte)}")
    for ep in (0, 50, 100, 200, 299):
        print(f"Epoch {ep+1:3d} | loss = {loss_hist[ep]:.4f} | akurasi latih = {acc_hist[ep]:.3f}")
    print(f"Akurasi data uji: {acc_te*100:.2f}%")
    print("Confusion matrix (baris = aktual, kolom = prediksi):\n", cm)
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    ax[0].plot(loss_hist, color="tab:red"); ax[0].set_title("Loss (cross-entropy)"); ax[0].set_xlabel("Epoch")
    ax[1].plot(acc_hist, color="tab:green"); ax[1].set_title("Akurasi data latih"); ax[1].set_xlabel("Epoch")
    im = ax[2].imshow(cm, cmap="Blues"); ax[2].set_title(f"Confusion matrix (uji, akurasi {acc_te*100:.1f}%)")
    ax[2].set_xticks(range(3)); ax[2].set_yticks(range(3))
    ax[2].set_xticklabels(iris.target_names, rotation=20); ax[2].set_yticklabels(iris.target_names)
    for i in range(3):
        for j in range(3): ax[2].text(j, i, cm[i, j], ha="center", va="center", color="k")
    for a in ax[:2]: a.grid(alpha=.3)
    plt.tight_layout(); plt.savefig("output/jst_hasil.png", dpi=150); plt.show()
