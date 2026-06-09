# QMOOD Tabanlı Yazılım Kalitesi Analizi ve LLM Destekli Değerlendirme

**Ders:** Yazılım Mimarileri ve Tasarım Yöntemleri — Dönem Projesi
**Analiz edilen sistem:** [jsoup](https://github.com/jhy/jsoup) (açık kaynak Java HTML parser)
**İncelenen sürüm sayısı:** 11 (jsoup 1.14.1 → 1.22.2)

## Amaç
Nesne yönelimli bir yazılım sisteminin **11 farklı sürümünü** QMOOD (Quality Model
for Object-Oriented Design) modeline göre analiz ederek yazılımın zaman içindeki
kalite değişimini ölçmek; ardından aynı metrik verilerini farklı **Büyük Dil
Modellerine (LLM)** vererek kalite değerlendirme yeteneklerini karşılaştırmak.

> Hiçbir hazır metrik aracı kullanılmamıştır. Tüm metrikler `javalang` ile
> kaynak koddan **kendi yazdığımız çözümleyici** ile çıkarılmıştır
> (yönerge: "hazır analiz sonuçlarının doğrudan kullanılması yasaktır").

## Klasör yapısı
```
proje/
├── src/
│   ├── fetch_versions.py   # jsoup sürümlerini indirir (git archive)
│   ├── metrics.py          # Java kaynaktan sınıf düzeyi OO metrik çıkarımı
│   ├── qmood.py            # QMOOD tasarım metrikleri + kalite nitelikleri
│   ├── analyze.py          # tüm sürümleri işler, CSV üretir
│   ├── visualize.py        # grafikler (figures/)
│   ├── llm_prompts.py      # LLM promptlarını üretir (prompts/)
│   └── run_all.py          # tüm pipeline'ı çalıştırır
├── data/                   # CSV çıktıları + indirilen kaynak sürümler
├── figures/                # PNG grafikler
├── prompts/                # LLM'lere verilen promptlar
├── llm_responses/          # LLM yanıtları (manuel doldurulur)
└── report/                 # teknik rapor
```

## Çalıştırma
```bash
pip install -r requirements.txt
# Windows'ta Türkçe yol için UTF-8:
#   PowerShell:  $env:PYTHONUTF8=1
python src/run_all.py
```
Tek tek:
```bash
python src/fetch_versions.py   # sürümleri indir
python src/analyze.py          # metrik + QMOOD hesapla -> data/*.csv
python src/visualize.py        # grafikler -> figures/
python src/llm_prompts.py      # promptlar -> prompts/
```

## Hesaplanan metrikler
**CK takımı (sınıf düzeyi):** DIT, NOC, WMC, CBO, RFC, LCOM, NOM, NOA, MPC, DAC
**QMOOD tasarım metrikleri (sistem düzeyi):** DSC, NOH, ANA, DAM, DCC, CAM, MOA,
MFA, NOP, CIS, NOM
**QMOOD kalite nitelikleri:** Reusability, Flexibility, Understandability,
Functionality, Extendibility, Effectiveness

## LLM değerlendirmesi
`prompts/01_full_evolution_prompt.txt` ana prompttur; en az 3 modele
(ChatGPT, Claude, Gemini, DeepSeek, Grok, Llama) verilir. Yanıtlar
`llm_responses/` altına kaydedilip eleştirel olarak karşılaştırılır.

## Referanslar
- J. Bansiya, C. G. Davis, "A Hierarchical Model for Object-Oriented Design
  Quality Assessment," *IEEE TSE*, 2002.
- S. R. Chidamber, C. F. Kemerer, "A Metrics Suite for Object Oriented Design,"
  *IEEE TSE*, 1994.
