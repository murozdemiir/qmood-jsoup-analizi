"""
llm_prompts.py
--------------
QMOOD metrik verilerinden LLM'lere verilecek yapilandirilmis promptlari uretir.
Yonerge: en az 3 LLM (ChatGPT, Gemini, Claude, DeepSeek, Llama, Grok...) ayni
prompt ile beslenip kalite degerlendirmeleri karsilastirilacaktir.

Uretilen dosyalar (prompts/ altinda):
  00_system_prompt.txt        -> tum modellere verilecek ortak sistem/rol promptu
  01_full_evolution_prompt.txt-> tum surumlerin ozet tablosu + analiz istegi
  02_version_<v>_prompt.txt   -> tek surum derin inceleme promptu (son 3 surum)
  03_diff_<a>_to_<b>_prompt.txt-> ardisik surum farki promptu
  PROMPTS_README.md           -> prompt muhendisligi sureci aciklamasi
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "prompts")
os.makedirs(OUT, exist_ok=True)


SYSTEM_PROMPT = """\
ROL: Sen kidemli bir yazilim mimarisi ve yazilim kalitesi uzmanisin.
Nesne yonelimli tasarim metrikleri ve QMOOD (Quality Model for Object-Oriented
Design, Bansiya & Davis 2002) modeli konusunda deneyimlisin.

GOREV: Sana acik kaynak 'jsoup' (Java HTML parser) kutuphanesinin farkli
surumlerinden cikarilmis QMOOD tasarim metrikleri ve kalite nitelikleri
verilecek. Bu sayisal verilere dayanarak ELESTIREL ve KANIT TEMELLI bir kalite
degerlendirmesi yapacaksin.

QMOOD KALITE NITELIK DENKLEMLERI (referans):
  Reusability       = -0.25*DCC + 0.25*CAM + 0.50*CIS + 0.50*DSC
  Flexibility       =  0.25*DAM - 0.25*DCC + 0.50*MOA + 0.50*NOP
  Understandability = -0.33*(ANA+DCC+NOP+NOM+DSC) + 0.33*(DAM+CAM)
  Functionality     =  0.12*CAM + 0.22*(NOP+CIS+DSC+NOH)
  Extendibility     =  0.50*(ANA+MFA+NOP) - 0.50*DCC
  Effectiveness     =  0.20*(ANA+DAM+MOA+MFA+NOP)
Tasarim metrikleri: DSC(boyut), NOH(hiyerarsi), ANA(soyutlama), DAM(kapsulleme),
DCC(coupling), CAM(cohesion), MOA(kompozisyon), MFA(kalitim), NOP(polimorfizm),
CIS(mesajlasma/arayuz), NOM(karmasiklik).

KURALLAR:
- Yorumlarini DAIMA verilen sayilara dayandir; sayisal kanit goster.
- Sadece 'iyi/kotu' deme; HANGI metrigin neden degistigini acikla.
- Belirsizlik varsa belirt. Abartma yapma.
"""

ANALYSIS_REQUEST = """\
LUTFEN ASAGIDAKILERI URET:
1. GENEL KALITE DEGERLENDIRMESI: Surumler boyunca genel kalite egilimi nedir?
   Hangi kalite nitelikleri iyilesti, hangileri bozuldu? Sayilarla acikla.
2. BAKIM YAPILABILIRLIK (Maintainability) ANALIZI: Understandability,
   Flexibility ve coupling/cohesion isiginda bakim kolaylasti mi zorlasti mi?
3. TEKNIK BORC (Technical Debt) TAHMINI: Hangi metrik egilimleri teknik borc
   birikimine isaret ediyor? (orn. artan DCC, artan WMC/LCOM, dusen CAM)
4. REFACTORING ONERILERI: Somut, metrik-temelli 3-5 refactoring onerisi.
5. MIMARI KALITE YORUMU: Yazilim buyudukce (DSC artarken) mimari bozulma
   (architectural erosion) belirtisi var mi?
Yanitini bolumlenmis ve oz tut. Her iddiayi bir metrik degisimiyle gerekce goster.
"""


def fmt_table(df, cols=None):
    if cols:
        df = df[cols]
    return df.to_string(index=False)


def main():
    quality_norm = pd.read_csv(os.path.join(DATA, "quality_norm.csv"))
    quality_raw = pd.read_csv(os.path.join(DATA, "quality_raw.csv"))
    design = pd.read_csv(os.path.join(DATA, "design_metrics.csv"))
    ck = pd.read_csv(os.path.join(DATA, "ck_summary.csv"))

    versions = list(quality_norm["version"])

    # 00 sistem promptu
    with open(os.path.join(OUT, "00_system_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(SYSTEM_PROMPT)

    # 01 tum evrim promptu
    design_cols = ["version"] + ["DSC", "NOH", "ANA", "DAM", "DCC", "CAM",
                                 "MOA", "MFA", "NOP", "CIS", "NOM"]
    with open(os.path.join(OUT, "01_full_evolution_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(SYSTEM_PROMPT + "\n")
        f.write("=" * 70 + "\n")
        f.write("VERI 1 — QMOOD TASARIM METRIKLERI (ham, sistem duzeyi ortalama)\n")
        f.write("=" * 70 + "\n")
        f.write(fmt_table(design, design_cols) + "\n\n")
        f.write("=" * 70 + "\n")
        f.write("VERI 2 — QMOOD KALITE NITELIKLERI (ham)\n")
        f.write("=" * 70 + "\n")
        f.write(fmt_table(quality_raw) + "\n\n")
        f.write("=" * 70 + "\n")
        f.write("VERI 3 — KALITE NITELIKLERI (ilk surume gore normalize, 1.0=baseline)\n")
        f.write("=" * 70 + "\n")
        f.write(fmt_table(quality_norm) + "\n\n")
        f.write("=" * 70 + "\n")
        f.write("VERI 4 — CK METRIK ORTALAMALARI (surum basina)\n")
        f.write("=" * 70 + "\n")
        ck_cols = ["version", "num_classes"] + \
            [c for c in ck.columns if c.endswith("_mean")]
        f.write(fmt_table(ck, ck_cols) + "\n\n")
        f.write(ANALYSIS_REQUEST)

    # 02 son 3 surum derin inceleme
    for v in versions[-3:]:
        drow = design[design["version"] == v]
        crow = ck[ck["version"] == v]
        qrow = quality_raw[quality_raw["version"] == v]
        with open(os.path.join(OUT, f"02_version_{v}_prompt.txt"), "w", encoding="utf-8") as f:
            f.write(SYSTEM_PROMPT + "\n")
            f.write(f"TEK SURUM DERIN INCELEME — jsoup {v}\n")
            f.write("-" * 50 + "\n")
            f.write("QMOOD tasarim metrikleri:\n")
            f.write(fmt_table(drow, design_cols) + "\n\n")
            f.write("CK metrik ortalamalari:\n")
            f.write(fmt_table(crow) + "\n\n")
            f.write("Kalite nitelikleri (ham):\n")
            f.write(fmt_table(qrow) + "\n\n")
            f.write("ISTEK: Bu surumun kalitesini degerlendirin. En zayif 2 "
                    "kalite niteligini ve sorumlu metrikleri belirleyin. "
                    "3 somut refactoring onerisi verin.\n")

    # 03 ardisik surum farklari (ilk->ikinci, sondan-onceki->son)
    pairs = [(versions[0], versions[1]), (versions[-2], versions[-1])]
    for a, b in pairs:
        da = design[design["version"] == a].iloc[0]
        db = design[design["version"] == b].iloc[0]
        with open(os.path.join(OUT, f"03_diff_{a}_to_{b}_prompt.txt"), "w", encoding="utf-8") as f:
            f.write(SYSTEM_PROMPT + "\n")
            f.write(f"SURUM FARKI ANALIZI — jsoup {a} -> {b}\n")
            f.write("-" * 50 + "\n")
            f.write(f"{'Metrik':6s} {a:>12s} {b:>12s} {'Degisim%':>10s}\n")
            for k in ["DSC", "NOH", "ANA", "DAM", "DCC", "CAM", "MOA", "MFA",
                      "NOP", "CIS", "NOM"]:
                va, vb = da[k], db[k]
                pct = ((vb - va) / va * 100) if va else 0
                f.write(f"{k:6s} {va:12.3f} {vb:12.3f} {pct:9.1f}%\n")
            f.write("\nISTEK: Bu iki surum arasindaki tasarim metrigi "
                    "degisimlerini yorumlayin. Kalite acisindan bu degisim "
                    "olumlu mu olumsuz mu? Teknik borc isareti var mi?\n")

    # README — prompt muhendisligi sureci
    with open(os.path.join(OUT, "PROMPTS_README.md"), "w", encoding="utf-8") as f:
        f.write(PROMPTS_README)

    print("[OK] Promptlar uretildi -> prompts/")
    print("Dosyalar:")
    for fn in sorted(os.listdir(OUT)):
        print("  ", fn)


PROMPTS_README = """\
# Prompt Muhendisligi Sureci

Bu klasordeki promptlar, QMOOD metrik verilerini farkli LLM modellerine ayni
kosullar altinda vermek icin tasarlanmistir. Amac, modellerin yazilim kalite
degerlendirme yeteneklerini KARSILASTIRMAKTIR.

## Tasarim ilkeleri
1. **Rol atama (persona):** Her prompt, modele "kidemli yazilim kalite uzmani"
   rolu verir. Bu, daha tutarli ve teknik yanitlar uretir.
2. **Baglam saglama:** QMOOD denklemleri ve metrik tanimlari prompt icine
   gomulur; model harici bilgiye guvenmek zorunda kalmaz.
3. **Kanit zorunlulugu:** Model her iddiayi bir metrik degisimine baglamak
   zorundadir ("sayisal kanit goster"). Bu, halusinasyonu azaltir.
4. **Yapilandirilmis cikti:** 5 sabit baslik istenir; boylece modeller arasi
   karsilastirma kolaylasir.
5. **Esit kosul:** Tum modellere AYNI prompt verilir (00 + 01). Farkliliklar
   yalnizca modelden kaynaklanir.

## Kullanim
- `01_full_evolution_prompt.txt`: ANA PROMPT. Tum modellere bunu verin.
- `02_version_*`: Tek surum derinlemesine inceleme (opsiyonel ek sorgu).
- `03_diff_*`: Ardisik surum farki yorumu (opsiyonel ek sorgu).

## Onerilen modeller (>=3)
ChatGPT (GPT-4o/5), Claude, Gemini, DeepSeek, Grok, Llama.
Her modelin yanitini `llm_responses/<model>.md` altina kaydedin; sonra
`compare_llm.py` (veya manuel) ile karsilastirin.

## Eklestirel degerlendirme
Her LLM yaniti icin not edin:
- Sayisal kanit kullandi mi? (evet/kismi/hayir)
- QMOOD denklemlerini dogru yorumladi mi?
- Halusinasyon/uydurma metrik var mi?
- Refactoring onerileri somut mu?
"""


if __name__ == "__main__":
    main()
