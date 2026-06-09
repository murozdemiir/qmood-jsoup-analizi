"""
visualize.py
------------
analyze.py ciktilarindan grafikler uretir (figures/ altina PNG).

Uretilen grafikler:
  1. fig_quality_norm.png   -> 6 QMOOD kalite niteliginin surumlere gore egrisi (normalize)
  2. fig_design_size.png    -> DSC (sinif sayisi) ve ort. NOM buyume egrisi
  3. fig_ck_means.png       -> CK metrik ortalamalarinin surumlere gore degisimi
  4. fig_coupling_cohesion.png -> DCC (coupling) ve CAM (cohesion) karsi karsiya
  5. fig_quality_heatmap.png-> kalite nitelikleri x surum isi haritasi (normalize)
  6. fig_radar_first_last.png -> ilk vs son surum tasarim metrikleri radar
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

QUALITIES = ["Reusability", "Flexibility", "Understandability",
             "Functionality", "Extendibility", "Effectiveness"]
DESIGN = ["DSC", "NOH", "ANA", "DAM", "DCC", "CAM", "MOA", "MFA", "NOP", "CIS", "NOM"]
CK = ["DIT", "NOC", "WMC", "CBO", "RFC", "LCOM", "NOM", "NOA", "MPC", "DAC"]


def load():
    return (pd.read_csv(os.path.join(DATA, "quality_norm.csv")),
            pd.read_csv(os.path.join(DATA, "design_metrics.csv")),
            pd.read_csv(os.path.join(DATA, "ck_summary.csv")),
            pd.read_csv(os.path.join(DATA, "quality_raw.csv")))


def fig_quality_norm(qn):
    """Her kalite niteligini KENDI ilk surum degerine gore indeksler (hepsi 1.0
    baslar). Understandability degerleri negatif oldugundan (QMOOD denklemi geregi)
    ayri eksende ham deger olarak gosterilir; boylece 'asagi = kotulesen
    anlasilabilirlik' yonu net okunur."""
    x = list(range(len(qn)))
    pos = ["Reusability", "Flexibility", "Functionality",
           "Extendibility", "Effectiveness"]
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 6))

    # Sol panel: pozitif nitelikler, kendi baseline'ina gore indeks (yukari=iyi)
    for q in pos:
        base = qn[q].iloc[0]
        idx = qn[q] / base if base else qn[q]
        axL.plot(x, idx, marker="o", label=q)
    axL.axhline(1.0, color="gray", ls="--", lw=1, alpha=.6)
    axL.set_xticks(x)
    axL.set_xticklabels(qn["version"], rotation=45)
    axL.set_ylabel("Kendi baseline'ina gore indeks (1.0 = ilk surum)")
    axL.set_title("Pozitif kalite nitelikleri (yukari = iyilesme)")
    axL.legend(fontsize=9)
    axL.grid(alpha=.3)

    # Sag panel: Understandability ham degeri (asagi = kotulesen anlasilabilirlik)
    axR.plot(x, qn["Understandability"], marker="o", color="#2ca02c")
    axR.set_xticks(x)
    axR.set_xticklabels(qn["version"], rotation=45)
    axR.set_ylabel("Understandability (ham QMOOD skoru)")
    axR.set_title("Understandability (asagi = anlasilabilirlik dusuyor)")
    axR.grid(alpha=.3)

    fig.suptitle("jsoup — QMOOD Kalite Niteliklerinin Surumlere Gore Evrimi",
                 fontsize=13)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIG, "fig_quality_norm.png"), dpi=130)
    plt.close()


def fig_design_size(dm):
    fig, ax1 = plt.subplots(figsize=(11, 6))
    x = range(len(dm))
    ax1.bar(x, dm["DSC"], color="#4C72B0", alpha=.7, label="DSC (sinif sayisi)")
    ax1.set_ylabel("DSC — Toplam sinif sayisi", color="#4C72B0")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(dm["version"], rotation=45)
    ax2 = ax1.twinx()
    ax2.plot(x, dm["NOM"], color="#C44E52", marker="o", label="NOM (ort. metot)")
    ax2.set_ylabel("NOM — Sinif basina ort. metot", color="#C44E52")
    plt.title("jsoup — Tasarim Boyutu Buyumesi (Design Size & Complexity)")
    fig.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_design_size.png"), dpi=130)
    plt.close()


def fig_ck_means(ck):
    plt.figure(figsize=(11, 6))
    x = range(len(ck))
    for m in ["WMC", "CBO", "RFC", "LCOM", "DIT", "NOM"]:
        col = f"{m}_mean"
        if col in ck:
            plt.plot(x, ck[col], marker="o", label=m)
    plt.xticks(x, ck["version"], rotation=45)
    plt.ylabel("Sinif basina ortalama deger")
    plt.title("jsoup — CK Metrik Ortalamalarinin Evrimi")
    plt.legend(ncol=3)
    plt.grid(alpha=.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_ck_means.png"), dpi=130)
    plt.close()


def fig_coupling_cohesion(dm):
    fig, ax1 = plt.subplots(figsize=(11, 6))
    x = range(len(dm))
    ax1.plot(x, dm["DCC"], color="#C44E52", marker="s", label="DCC (coupling)")
    ax1.set_ylabel("DCC — Ortalama coupling", color="#C44E52")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(dm["version"], rotation=45)
    ax2 = ax1.twinx()
    ax2.plot(x, dm["CAM"], color="#55A868", marker="o", label="CAM (cohesion)")
    ax2.set_ylabel("CAM — Ortalama cohesion", color="#55A868")
    plt.title("jsoup — Coupling (DCC) vs Cohesion (CAM)")
    fig.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_coupling_cohesion.png"), dpi=130)
    plt.close()


def fig_heatmap(qn):
    data = qn[QUALITIES].T.values
    plt.figure(figsize=(11, 5))
    im = plt.imshow(data, aspect="auto", cmap="RdYlGn")
    plt.colorbar(im, label="Normalize indeks")
    plt.yticks(range(len(QUALITIES)), QUALITIES)
    plt.xticks(range(len(qn)), qn["version"], rotation=45)
    for i in range(len(QUALITIES)):
        for j in range(len(qn)):
            plt.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center",
                     fontsize=7)
    plt.title("jsoup — QMOOD Kalite Nitelikleri Isi Haritasi (normalize)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_quality_heatmap.png"), dpi=130)
    plt.close()


def fig_radar(dm):
    cols = [f"{d}_norm" for d in DESIGN]
    first = dm.iloc[0][cols].values.astype(float)
    last = dm.iloc[-1][cols].values.astype(float)
    angles = np.linspace(0, 2 * np.pi, len(DESIGN), endpoint=False).tolist()
    angles += angles[:1]
    first = np.concatenate([first, first[:1]])
    last = np.concatenate([last, last[:1]])
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, first, marker="o", label=f"ilk ({dm.iloc[0]['version']})")
    ax.fill(angles, first, alpha=.1)
    ax.plot(angles, last, marker="o", label=f"son ({dm.iloc[-1]['version']})")
    ax.fill(angles, last, alpha=.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DESIGN)
    ax.set_title("jsoup — Tasarim Metrikleri: ilk vs son surum (normalize)")
    ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_radar_first_last.png"), dpi=130)
    plt.close()


def main():
    qn, dm, ck, qr = load()
    fig_quality_norm(qn)
    fig_design_size(dm)
    fig_ck_means(ck)
    fig_coupling_cohesion(dm)
    fig_heatmap(qn)
    fig_radar(dm)
    print("[OK] 6 grafik uretildi -> figures/")


if __name__ == "__main__":
    main()
