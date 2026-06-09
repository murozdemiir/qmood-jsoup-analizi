# QMOOD Tabanlı Yazılım Kalitesi Analizi ve LLM Destekli Değerlendirme
### Analiz Edilen Sistem: jsoup (Açık Kaynak Java HTML Parser) — 11 Sürüm (1.14.1 → 1.22.2)

> **Ders:** Yazılım Mimarileri ve Tasarım Yöntemleri — Dönem Projesi
> **Grup:** <isimler / numaralar>
> **Tarih:** <YYYY-MM-DD>
> **GitHub:** <repo bağlantısı>

---

## 1. Giriş

Yazılım sistemleri zamanla büyür; yeni özellikler eklenir, hatalar düzeltilir ve
bu evrim çoğu zaman tasarım kalitesinde fark edilmeyen bozulmalara (architectural
erosion, technical debt) yol açar. Bu çalışmanın amacı, açık kaynak **jsoup**
kütüphanesinin 11 ardışık sürümünü **QMOOD (Quality Model for Object-Oriented
Design)** modeline göre ölçülebilir metrikler üzerinden analiz ederek kalite
değişimini nicel olarak ortaya koymak ve ardından aynı metrik verilerini farklı
**Büyük Dil Modellerine (LLM)** vererek bu modellerin yazılım kalitesi
yorumlama yeteneklerini karşılaştırmaktır.

**Neden jsoup?** Tek ve sürekli bir git geçmişine, zengin bir nesne yönelimli
tasarıma (`Node` soyut sınıfı → `Element`, `TextNode`, `Comment` vb. güçlü
kalıtım ve polimorfizm hiyerarşisi) ve düzenli sürüm yayınına sahip, yönetilebilir
boyutta (~250–300 sınıf) bir kütüphanedir. Bu özellikler QMOOD'un soyutlama,
kalıtım ve polimorfizm metriklerini anlamlı kılar.

**Katkı/özgünlük:** Yönergenin "hazır analiz sonuçlarının doğrudan kullanılması
yasaktır" kuralı gereği, tüm metrikler `javalang` kütüphanesiyle kaynak koddan
**kendi yazdığımız çözümleyici** ile çıkarılmıştır; SonarQube/CK/Designite gibi
hazır araçların çıktıları kullanılmamıştır.

## 2. Literatür Özeti

- **Chidamber & Kemerer (1994):** İlk yaygın nesne yönelimli metrik takımını
  (DIT, NOC, WMC, CBO, RFC, LCOM) önerdiler. Bu metrikler coupling, cohesion,
  karmaşıklık ve kalıtım derinliğini ölçer.
- **Bansiya & Davis (2002), QMOOD:** Tasarım metriklerini → tasarım özelliklerine
  → kalite niteliklerine bağlayan hiyerarşik bir model kurdular. Altı kalite
  niteliğini (Reusability, Flexibility, Understandability, Functionality,
  Extendibility, Effectiveness) tasarım metriklerinin ağırlıklı toplamı olarak
  formülize ettiler.
- **Teknik borç ve mimari erozyon literatürü:** Yazılım büyüdükçe coupling (CBO/
  DCC) ve karmaşıklığın (WMC/LCOM) artma, cohesion'ın (CAM) azalma eğiliminde
  olduğu; bunun bakım maliyetini yükselttiği gösterilmiştir.
- **LLM ve yazılım kalitesi (güncel):** Büyük dil modellerinin metrik verisinden
  kalite yorumu ve refactoring önerisi üretebildiği, ancak sayısal kanıttan kopuk
  "halüsinasyon" üretebildiği rapor edilmektedir. Bu çalışma bu yönü ampirik
  olarak sınar.

## 3. Yöntem

### 3.1 QMOOD modeli
Tasarım metrikleri → tasarım özellikleri eşlemesi:

| Tasarım Özelliği | Metrik | Açıklama |
|---|---|---|
| Design Size | DSC | Toplam sınıf sayısı |
| Hierarchies | NOH | Kök hiyerarşi sayısı |
| Abstraction | ANA | Ortalama ata sayısı |
| Encapsulation | DAM | (private+protected alan)/toplam alan |
| Coupling | DCC | Ortalama sınıf bağlantısı |
| Cohesion | CAM | Metot parametre tipi uyumu |
| Composition | MOA | ADT (proje sınıfı) tipli alan sayısı |
| Inheritance | MFA | Kalıtılan metot / erişilebilir metot |
| Polymorphism | NOP | Polimorfik metot sayısı |
| Messaging | CIS | Public metot (arayüz) sayısı |
| Complexity | NOM | Sınıf başına metot sayısı |

QMOOD kalite nitelik denklemleri:
```
Reusability       = -0.25·DCC + 0.25·CAM + 0.50·CIS + 0.50·DSC
Flexibility       =  0.25·DAM - 0.25·DCC + 0.50·MOA + 0.50·NOP
Understandability = -0.33·(ANA+DCC+NOP+NOM+DSC) + 0.33·(DAM+CAM)
Functionality     =  0.12·CAM + 0.22·(NOP+CIS+DSC+NOH)
Extendibility     =  0.50·(ANA+MFA+NOP) - 0.50·DCC
Effectiveness     =  0.20·(ANA+DAM+MOA+MFA+NOP)
```

### 3.2 Metrik çıkarım aracı (kendi geliştirdiğimiz)
`src/metrics.py`, her `.java` dosyasını `javalang` ile AST'ye çevirir ve sınıf
düzeyinde CK metriklerini (DIT, NOC, WMC, CBO, RFC, LCOM, NOM, NOA, MPC, DAC) ve
QMOOD ek ölçülerini hesaplar. Tanım kararları (tasarım kararları):
- **WMC** = metotların McCabe çevrimsel karmaşıklıkları toplamı.
- **DIT/NOC/CBO** yalnızca **proje içi** sınıflar arası ilişkiler üzerinden
  hesaplanır (harici kütüphane sınıfları sayılmaz) — sürümler arası
  karşılaştırılabilirlik için.
- **LCOM** Chidamber-Kemerer tanımı: alan paylaşmayan metot çifti − paylaşan.
- **DAM/MFA/NOP/CAM** QMOOD'un Bansiya-Davis tanımlarına göre.

`src/qmood.py` bu sınıf düzeyi değerleri sistem düzeyinde toplar (ortalama/
toplam) ve kalite niteliklerini hesaplar.

### 3.3 Normalizasyon
DSC mutlak değeri (yüzlerce sınıf) denklemleri ezdiğinden, QMOOD karşılaştırmalı
çalışmalarının standart yaklaşımı izlenmiş; her tasarım metriği **ilk sürüme
(1.14.1) göre normalize** edilmiştir (baseline = 1.0). Kalite nitelikleri hem
ham hem normalize değerlerle raporlanır; sürümler arası yorum normalize değerler
üzerinden yapılır.

### 3.4 Sürüm seçimi
1.14.1, 1.14.3, 1.15.1, 1.15.4, 1.16.2, 1.17.2, 1.18.3, 1.19.1, 1.20.1, 1.21.2,
1.22.2 — her minor sürümden temsilci alınarak büyüme eğrisi yakalanmıştır.

### 3.5 LLM değerlendirme protokolü
`src/llm_prompts.py` ile üretilen ana prompt (`01_full_evolution_prompt.txt`)
en az 3 modele (ChatGPT, Claude, Gemini, DeepSeek, Grok, Llama) **aynı koşulda**
verilir. Prompt mühendisliği ilkeleri: rol atama, denklemlerin prompt içine
gömülmesi, "sayısal kanıt zorunluluğu", yapılandırılmış 5 başlıklı çıktı.

## 4. Analiz Süreci

`src/analyze.py` 11 sürümün her birini çözümledi. İşlenen sınıf sayısı (iç
sınıflar dahil) **144 → 184** arttı; `src/main/java` dosya sayısı 73 → 91.
Her sürüm için sınıf düzeyi metrikler `data/class_metrics.csv` (toplam ~1.800
satır), sistem düzeyi QMOOD tasarım metrikleri `data/design_metrics.csv`,
CK ortalamaları `data/ck_summary.csv` dosyalarına yazıldı.

Süreç adımları: (1) `fetch_versions.py` ile sürümlerin `src/main/java` ağacının
`git archive` ile çıkarılması; (2) `metrics.py` ile her `.java` dosyasının
`javalang` AST'sinden sınıf düzeyi metrik çıkarımı; (3) `qmood.py` ile sistem
düzeyi toplama ve kalite niteliği hesabı; (4) ilk sürüme (1.14.1) göre
normalizasyon. Çözümlenemeyen dosya gözlenmedi (atlanan dosya = 0).

## 5. Sonuçlar

### Tablo 5.1 — QMOOD Tasarım Metrikleri (ham, seçili sürümler)
| Sürüm | DSC | DCC | CAM | DAM | MOA | MFA | NOP | NOM |
|---|---|---|---|---|---|---|---|---|
| 1.14.1 | 144 | 3.250 | 0.363 | 0.876 | 0.417 | 0.305 | 5.243 | 9.083 |
| 1.16.2 | 152 | 3.303 | 0.323 | 0.856 | 0.408 | 0.335 | 5.645 | 9.632 |
| 1.19.1 | 166 | 3.283 | 0.322 | 0.820 | 0.500 | 0.329 | 5.464 | 9.512 |
| 1.22.2 | 184 | 3.380 | 0.300 | 0.806 | 0.489 | 0.358 | 5.467 | 9.576 |
| **Δ%** | **+27.8** | **+4.0** | **−17.3** | **−8.0** | **+17.4** | **+17.4** | **+4.3** | **+5.4** |

### Tablo 5.2 — Kalite Nitelikleri (ilk sürüme göre normalize)
| Sürüm | Reusab. | Flexib. | Underst. | Funct. | Extend. | Effect. |
|---|---|---|---|---|---|---|
| 1.14.1 | 1.000 | 1.000 | −0.990 | 1.000 | 1.000 | 1.000 |
| 1.16.2 | 1.014 | 1.018 | −1.097 | 1.005 | 1.070 | 1.022 |
| 1.19.1 | 1.057 | 1.102 | −1.105 | 0.998 | 1.013 | 1.034 |
| 1.22.2 | 1.093 | 1.078 | −1.191 | 1.071 | 1.059 | 1.050 |

### Tablo 5.3 — CK Metrik Ortalamaları (özet)
| Sürüm | WMC | CBO | RFC | LCOM | NOM | NOA |
|---|---|---|---|---|---|---|
| 1.14.1 | 18.03 | 3.25 | 18.96 | 126.2 | 9.08 | 2.24 |
| 1.22.2 | 19.22 | 3.38 | 20.42 | 148.7 | 9.58 | 2.45 |
| **Δ%** | **+6.5** | **+4.0** | **+7.7** | **+17.8** | **+5.4** | **+9.3** |

**Şekiller:** `figures/fig_quality_norm.png` (kalite evrimi),
`fig_design_size.png` (boyut büyümesi), `fig_ck_means.png` (CK evrimi),
`fig_coupling_cohesion.png` (DCC↑ vs CAM↓), `fig_quality_heatmap.png`,
`fig_radar_first_last.png` (ilk vs son tasarım profili).

## 6. Tartışma

### 6.1 Yazılım evrimi yorumu
jsoup **çift yönlü** evrim sergiliyor. Boyut %27.8 büyürken Reusability (+%9.3),
Flexibility (+%7.8), Functionality (+%7.1), Extendibility (+%5.9) ve
Effectiveness (+%5.0) artarken **Understandability mutlak değerce +%20 kötüleşti**.
Bu iyileşmelerin bir kısmı gerçek tasarım kazanımıdır (MOA +%17.4 ve MFA +%17.4
ile kompozisyon/kalıtım yeniden kullanımı bilinçli güçlendirilmiş), bir kısmı ise
DSC'nin denklemlerdeki pozitif katsayısının mekanik etkisidir. Bu ayrım,
QMOOD skorlarını yorumlarken kritik bir incedir.

### 6.2 Teknik borç belirtileri
İki bağımsız metriğin çapraz doğrulaması en güçlü kanıttır:
**CAM −%17.3** ve **LCOM +%17.8** birlikte cohesion erozyonuna işaret eder.
Buna **DAM −%8.0** (kapsülleme gevşemesi), **DCC/CBO +%4.0** (coupling artışı) ve
**WMC +%6.5** (sınıf karmaşıklığı) eşlik eder. Borcun şiddeti ılımlıdır
(değişimler %4–18 bandında, ani sıçrama yok) → kontrollü/kademeli birikim.

### 6.3 LLM değerlendirmelerinin karşılaştırması
Ana prompt (`prompts/01_full_evolution_prompt.txt`) **17 farklı LLM
yapılandırmasına** (ChatGPT-2, Claude-3, Copilot-2, DeepSeek-3, Gemini-5,
Grok-1) **aynı koşulda** verildi. Yanıtlar `llm_responses/` altında. İki
düzeyde karşılaştırma yapıldı: (i) otomatik yüzeysel ölçüm
(`src/compare_llm.py` → `data/llm_comparison.csv`,
`figures/fig_llm_comparison.png`); (ii) **insan denetimli eleştirel puanlama**,
8 kriterde 1–5 (`src/llm_quality_scores.py` →
`data/llm_qualitative_scores.csv`, `figures/fig_llm_qualitative.png`,
`fig_llm_ranking.png`). Detaylı analiz: **`report/llm_karsilastirma.md`**.

**Niteliksel uzlaşı yüksek:** 17 modelin tamamı "dış kalite (Reusability/
Functionality) artarken iç kalite (cohesion/kapsülleme/anlaşılabilirlik)
geriliyor — kontrollü teknik borç" çekirdek anlatısında birleşti; bu, bizim
metrik analizimizle (§5–6) örtüşür. **Hiçbir model metrik değeri uydurmadı**
(sayısal-kanıt prompt kuralının başarısı).

**Ayrışma derinlikte oldu (en ayırt edici kriter: DSC-artefakt farkındalığı):**
- En güçlü yanıt `claude_opusHigh` (40/40) denklemi sayısal ayrıştırarak
  Reusability'nin boyut-dışı kalite bileşeninin aslında **gerilediğini**
  (1.969→1.958) gösterdi, 1.20.1 dip / 1.21+ toparlanma ara dinamiğini yakaladı
  ve **VERİ 3 normalize Understandability işaret tutarsızlığımızı** tespit etti.
- Asıl halüsinasyon vektörü **sınıf adı uydurmaydı**: bazı modeller toplu
  veriden türetilemeyecek sınıf adlarını (`Parser`, `Element`, `TokenQueue`…)
  refactoring hedefi olarak isimlendirdi (desteksiz spesifiklik).
- Şüpheli öneriler: bazı modeller polimorfizmi (NOP) düşürmeyi önerdi — QMOOD'da
  NOP üç niteliği pozitif beslediğinden bu genelde yanlış tavsiyedir.
- **Kademe etkisi sağlayıcıdan baskın:** üst kademe "reasoning" modları (Claude
  High, ChatGPT/Copilot Think/Smart, Gemini Pro) belirgin biçimde daha derin;
  Gemini Flash kademesi en zayıf grup (biri yanıtı yarıda kesti).

**Meta-bulgu (prompt mühendisliği):** Modeller `+%27` (ham) ile `+%9.25`
(normalize) yüzdeleri arasında, hangi tablomuza tutunduklarına göre çatallandı —
veri sunum biçiminin LLM çıkarımını doğrudan yönlendirdiğini gösterir.

**Pratik çıkarım:** Metrik yorumu için LLM kullanılacaksa üst kademe reasoning
modu seçilmeli ve çıktı **sınıf düzeyi veriyle çapraz doğrulanmalıdır**.

### 6.4 Tehditler ve sınırlamalar
- `javalang` bazı yeni Java sözdizimlerini çözümleyemeyebilir (bu veri setinde
  atlanan dosya = 0).
- Metrik tanım kararları (örn. DIT/CBO'nun yalnızca **proje içi** ilişkiler
  üzerinden sayılması) mutlak değerleri etkiler; ancak sürümler arası **eğilim**
  geçerli kalır.
- LLM yanıtları stokastiktir; tekrar çalıştırmada değişebilir — bu yüzden
  eleştirel değerlendirme insan denetimiyle yapılmıştır.
- **Normalize Understandability işaret tutarsızlığı (LLM tarafından tespit):**
  Understandability denklemi sistemde negatif değer ürettiğinden, ilk sürüme
  oranla normalizasyon (raw/baseline) baseline'ı +1.0 yerine −0.99 gösterir.
  Bu yalnızca bir **gösterim** etkisidir; yorumlar ham değerler ve mutlak
  yüzde değişim üzerinden yapıldığından sonuçları etkilemez. Görselde de
  Understandability ayrı eksende ham değerle sunulmuştur (`fig_quality_norm`).

## 7. Sonuç ve Gelecek Çalışmalar
jsoup, 1.14→1.22 boyunca **olgun ve kontrollü yönetilen** bir kütüphanedir:
yeniden kullanılabilirlik ve esneklik artarken anlaşılabilirlik kademeli olarak
azalmış, cohesion en belirgin teknik borç eğilimini oluşturmuştur. QMOOD modeli
bu çift yönlü evrimi nicel olarak yakalayabilmiştir.

**Gelecek çalışmalar:** (1) çoklu proje karşılaştırması (örn. bir C# ve bir Java
sistem); (2) LLM yanıtlarının API üzerinden otomatik, çok-tekrarlı toplanması ve
istatistiksel anlamlılık testi; (3) metrik eğilimleri ile gerçek hata/bakım
kayıtları (issue/commit) arasındaki korelasyonun incelenmesi.

## Referanslar
1. J. Bansiya, C. G. Davis, "A Hierarchical Model for Object-Oriented Design
   Quality Assessment," *IEEE Transactions on Software Engineering*, 28(1), 2002.
2. S. R. Chidamber, C. F. Kemerer, "A Metrics Suite for Object Oriented Design,"
   *IEEE TSE*, 20(6), 1994.
3. T. J. McCabe, "A Complexity Measure," *IEEE TSE*, SE-2(4), 1976.
4. jsoup — https://github.com/jhy/jsoup
5. javalang — https://github.com/c2nes/javalang
