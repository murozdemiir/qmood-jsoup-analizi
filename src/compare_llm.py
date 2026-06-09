"""
compare_llm.py
--------------
llm_responses/ altindaki model yanitlarini basit metriklerle karsilastirir
ve bir ozet tablo (data/llm_comparison.csv) + grafik uretir.

Bu otomatik karsilastirma YALNIZCA yuzeysel gostergeler (uzunluk, sayisal kanit
yogunlugu, QMOOD terim kapsami, refactoring oneri sayisi) saglar. Yonergenin
istedigi ELESTIREL degerlendirme insan tarafindan _TEMPLATE.md tablosunda
yapilmalidir. Buradaki skorlar yalnizca tartismayi desteklemek icindir.
"""
import os
import re
import glob
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESP = os.path.join(ROOT, "llm_responses")
DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "figures")

QMOOD_TERMS = ["DSC", "NOH", "ANA", "DAM", "DCC", "CAM", "MOA", "MFA", "NOP",
               "CIS", "NOM", "Reusability", "Flexibility", "Understandability",
               "Functionality", "Extendibility", "Effectiveness", "coupling",
               "cohesion", "technical debt", "teknik borc", "refactor"]


def analyze_response(text):
    words = len(text.split())
    numbers = len(re.findall(r"\b\d+[.,]?\d*\b", text))
    term_cov = sum(1 for t in QMOOD_TERMS if t.lower() in text.lower())
    refactor_hits = len(re.findall(r"refactor|extract|decouple|split|ayir|bol",
                                   text, re.I))
    sections = len(re.findall(r"^\s*\d+[\.\)]\s|^#{1,3}\s", text, re.M))
    return {
        "words": words,
        "number_mentions": numbers,
        "qmood_term_coverage": term_cov,
        "refactor_mentions": refactor_hits,
        "structured_sections": sections,
    }


def main():
    files = [f for f in glob.glob(os.path.join(RESP, "*.md"))
             if not os.path.basename(f).startswith("_")]
    if not files:
        print("[!] llm_responses/ altinda model yaniti (*.md) bulunamadi.")
        print("    Once promptlari modellere verip yanitlari kaydedin.")
        return
    rows = []
    for f in files:
        model = os.path.splitext(os.path.basename(f))[0]
        with open(f, "r", encoding="utf-8") as fh:
            text = fh.read()
        r = {"model": model}
        r.update(analyze_response(text))
        rows.append(r)
    df = pd.DataFrame(rows).sort_values("model")
    df.to_csv(os.path.join(DATA, "llm_comparison.csv"), index=False)
    print(df.to_string(index=False))

    # grafik
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics = ["number_mentions", "qmood_term_coverage", "refactor_mentions",
               "structured_sections"]
    x = range(len(df))
    w = 0.2
    for i, m in enumerate(metrics):
        ax.bar([xi + i * w for xi in x], df[m], width=w, label=m)
    ax.set_xticks([xi + 1.5 * w for xi in x])
    ax.set_xticklabels(df["model"], rotation=30)
    ax.set_title("LLM Yanitlarinin Yuzeysel Karsilastirmasi")
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_llm_comparison.png"), dpi=130)
    print("\n[OK] data/llm_comparison.csv + figures/fig_llm_comparison.png")


if __name__ == "__main__":
    main()
