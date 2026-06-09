"""
llm_quality_scores.py
---------------------
17 LLM yanitinin ELESTIREL (niteliksel) degerlendirmesi. Yanitlarin tamami
yazarlar tarafindan okunup 8 kriterde 1-5 olceginde puanlanmistir. Bu puanlar
otomatik degil, INSAN denetimiyle verilmistir (yonerge: "LLM ciktilari elestirel
biçimde degerlendirilmelidir"). Bu betik puanlari belgeler, bir CSV ve isi
haritasi uretir.

Kriterler
=========
- SayisalKanit       : Iddialarin metrik + yuzde ile desteklenmesi
- DenklemDogrulugu   : QMOOD denklemlerini dogru yorumlama
- DSC_Artefakt       : Reusability/Functionality artisinin BUYUK olcude DSC
                       (boyut) kaynakli "yapay" oldugunu fark etme (en ayirt
                       edici kriter)
- ZamansalGranulerlik: Yalnizca ilk-vs-son degil; ara surum kirilmalarini
                       (orn. ~1.20.1 dip, 1.21+ toparlanma) yakalama
- HalusinasyonDirenci: Verilmeyen sinif adlari / desteksiz iddia URETMEME
                       (yuksek puan = az halusinasyon)
- RefactoringSomut   : Onerilerin somut ve metrik-hedefli olmasi
- SinirlamaFarkindal : Ortalama metriklerin hotspot gizledigini, istatistik
                       anlamlilik olmadigini vb. kabul etme
- AnalitikDerinlik   : Genel analitik olgunluk
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "figures")

CRITERIA = ["SayisalKanit", "DenklemDogrulugu", "DSC_Artefakt",
            "ZamansalGranulerlik", "HalusinasyonDirenci", "RefactoringSomut",
            "SinirlamaFarkindal", "AnalitikDerinlik"]

# model -> 8 kriter puani (1-5). claude.md (metodoloji tohumu) haric tutuldu;
# Claude modeli kullanicinin topladigi opus/fable/sonnet dosyalariyla temsil ediliyor.
SCORES = {
    "claude_opusHigh":          [5, 5, 5, 5, 5, 5, 5, 5],
    "claude_fableHigh":         [5, 5, 5, 4, 5, 4, 4, 5],
    "chatgpt-thinkMode":        [5, 5, 4, 3, 5, 4, 4, 4],
    "copilot_smart":            [5, 5, 4, 3, 5, 4, 3, 4],
    "claude_sonnetLow":         [5, 5, 4, 3, 3, 4, 3, 4],
    "gemini-proStandart":       [4, 5, 4, 3, 4, 4, 3, 4],
    "copilot_think":            [4, 5, 3, 2, 4, 5, 3, 4],
    "gemini-proExtended":       [3, 4, 3, 3, 4, 4, 3, 3],
    "grok-fast":                [4, 4, 4, 2, 3, 5, 2, 3],
    "deepseek_instantThink":    [4, 4, 3, 2, 4, 4, 3, 3],
    "deepseek_instantStandart": [4, 4, 3, 2, 3, 4, 3, 3],
    "chatgpt-askMode":          [4, 4, 3, 2, 4, 4, 2, 3],
    "deepseek_expert":          [3, 4, 3, 2, 4, 4, 2, 3],
    "gemini-flashStandart":     [3, 3, 3, 2, 3, 4, 2, 3],
    "gemini-flashLite":         [2, 3, 2, 1, 3, 3, 2, 2],
    "gemini-flashExtended":     [2, 3, 2, 1, 3, 1, 1, 2],  # yanit yarida kesik
}


def main():
    rows = []
    for model, sc in SCORES.items():
        r = {"model": model}
        r.update(dict(zip(CRITERIA, sc)))
        r["Toplam"] = sum(sc)
        r["Ortalama"] = round(np.mean(sc), 2)
        rows.append(r)
    df = pd.DataFrame(rows).sort_values("Toplam", ascending=False).reset_index(drop=True)
    df.to_csv(os.path.join(DATA, "llm_qualitative_scores.csv"), index=False)
    print(df.to_string(index=False))

    # isi haritasi
    mat = df.set_index("model")[CRITERIA]
    plt.figure(figsize=(12, 8))
    im = plt.imshow(mat.values, aspect="auto", cmap="RdYlGn", vmin=1, vmax=5)
    plt.colorbar(im, label="Puan (1-5)")
    plt.xticks(range(len(CRITERIA)), CRITERIA, rotation=35, ha="right")
    plt.yticks(range(len(mat)), mat.index)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            plt.text(j, i, int(mat.values[i, j]), ha="center", va="center",
                     fontsize=8)
    plt.title("LLM Yanitlarinin Elestirel Degerlendirmesi (niteliksel puanlar)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_llm_qualitative.png"), dpi=130)
    plt.close()

    # toplam puan sirali bar
    plt.figure(figsize=(11, 6))
    colors = plt.cm.RdYlGn(np.linspace(0.15, 0.9, len(df)))
    plt.barh(df["model"][::-1], df["Toplam"][::-1], color=colors)
    plt.xlabel("Toplam puan (8 kriter x max 5 = 40)")
    plt.title("LLM Yanitlari — Toplam Elestirel Puan Siralamasi")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_llm_ranking.png"), dpi=130)
    plt.close()
    print("\n[OK] data/llm_qualitative_scores.csv + 2 grafik (fig_llm_qualitative, fig_llm_ranking)")


if __name__ == "__main__":
    main()
