# LLM Kalite Değerlendirmelerinin Karşılaştırmalı ve Eleştirel Analizi

> Aynı ana prompt (`prompts/01_full_evolution_prompt.txt`) **16 farklı LLM
> yapılandırmasına** aynı koşulda verilmiştir. Bu belge yanıtların eleştirel
> karşılaştırmasını içerir. Puanlama rubriği ve ham puanlar:
> `src/llm_quality_scores.py`, `data/llm_qualitative_scores.csv`.
> Görseller: `figures/fig_llm_qualitative.png`, `fig_llm_ranking.png`,
> `fig_llm_comparison.png`.

## 1. Test edilen modeller (16 yapılandırma)
| Sağlayıcı | Yapılandırmalar |
|---|---|
| OpenAI ChatGPT | GPT-5.5 *Ask*, *Think* |
| Anthropic Claude | *Opus High*, *Fable High*, *Sonnet Low* |
| Microsoft Copilot | *Smart*, *Think* |
| DeepSeek | *Expert*, *Instant-Standard*, *Instant-Think* |
| Google Gemini | *Pro-Standard*, *Pro-Extended*, *Flash-Standard*, *Flash-Lite*, *Flash-Extended* |
| xAI Grok | *Fast* |

> Claude ailesi, toplanan üç mod (Opus/Fable/Sonnet) ile temsil edilmektedir.

## 2. Değerlendirme rubriği (8 kriter, 1–5)
1. **Sayısal Kanıt** — her iddianın metrik + yüzde ile desteklenmesi
2. **Denklem Doğruluğu** — QMOOD denklemlerini doğru yorumlama
3. **DSC-Artefakt Farkındalığı** — Reusability/Functionality artışının büyük
   ölçüde **boyut (DSC) kaynaklı yapay** olduğunu fark etme *(en ayırt edici)*
4. **Zamansal Granülerlik** — ilk-vs-son ötesinde ara sürüm kırılmalarını
   (≈1.20.1 dip, 1.21+ toparlanma) yakalama
5. **Halüsinasyon Direnci** — verilmeyen sınıf adı / desteksiz iddia ÜRETMEME
6. **Refactoring Somutluğu** — metrik-hedefli, uygulanabilir öneriler
7. **Sınırlama Farkındalığı** — ortalamaların hotspot gizlemesi, istatistik
   anlamlılık yokluğu vb. kabulü
8. **Analitik Derinlik** — genel analitik olgunluk

## 3. Sıralama (toplam puan / 40)
| # | Model | Toplam | Ort. |
|---|---|---|---|
| 1 | **claude_opusHigh** | 40 | 5.00 |
| 2 | claude_fableHigh | 37 | 4.62 |
| 3 | chatgpt-thinkMode | 34 | 4.25 |
| 4 | copilot_smart | 33 | 4.12 |
| 5 | claude_sonnetLow | 31 | 3.88 |
| 5 | gemini-proStandart | 31 | 3.88 |
| 7 | copilot_think | 30 | 3.75 |
| 7 | gemini-flashExtended † | 30 | 3.75 |
| 9 | gemini-proExtended ‡ | 28 | 3.50 |
| 10 | grok-fast | 27 | 3.38 |
| 10 | deepseek_instantThink | 27 | 3.38 |
| 12 | deepseek_instantStandart | 26 | 3.25 |
| 12 | chatgpt-askMode | 26 | 3.25 |
| 14 | deepseek_expert | 25 | 3.12 |
| 15 | gemini-flashStandart | 23 | 2.88 |
| 16 | gemini-flashLite | 18 | 2.25 |

† `gemini-flashExtended` yeniden üretildi: bölüm 1–4 güçlü (zengin sayısal kanıt
— RFC/NOA/CIS dahil —, DSC-artefaktını yakaladı, sınıf adı **uydurmadı**), yalnızca
bölüm 5 yarıda kesik. ‡ `gemini-proExtended` de yeniden üretildi (ilk çalıştırma
eksikti); DSC-artefaktını ve denklemi doğru yaptı ama sınıf adı (Parser/Document)
uydurdu ve sınırlama bölümü yok.

## 4. Bulgular (eleştirel)

### 4.1 Hiçbir model metrik UYDURMADI — ama bazıları SINIF uydurdu
Olumlu ortak nokta: 16 yanıtın **hiçbiri** sayısal metrik değeri halüsine
etmedi; verilen tabloya sadık kaldılar. Bu, "sayısal kanıt zorunluluğu"
prompt kuralının işe yaradığını gösterir.

Asıl halüsinasyon vektörü **sınıf adı uydurmaydı**: `claude_sonnetLow`,
`grok-fast`, `gemini-proStandart`, `deepseek_*` refactoring hedefi olarak
`HtmlTreeBuilder`, `TokenQueue`, `Element`, `Node`, `Parser`, `Document` gibi
sınıfları **isimlendirdi**. Bu sınıflar jsoup'ta gerçekten var (makul tahmin),
**ancak verilen toplu (aggregate) veriden türetilemez** — yani desteksiz
spesifikliktir. En güçlü yanıtlar (`claude_opusHigh`) bunun yerine "sınıf
düzeyi dağılım gerekli" diyerek bu tuzaktan kaçındı.

### 4.2 En ayırt edici kriter: DSC-artefakt farkındalığı
QMOOD'un en kritik yorum inceliği, `Reusability +%27` ve `Functionality +%25`
artışlarının büyük ölçüde **denklemlerdeki DSC (boyut) teriminden** geldiğini —
yani gerçek tasarım iyileşmesi olmadığını — görmektir. Modeller bu konuda
ayrıştı:
- **`claude_opusHigh`** denklemi **sayısal olarak ayrıştırdı**: Reusability'nin
  boyut-dışı "kalite bileşeni" aslında 1.969 → 1.958'e **geriledi**; tüm +20'lik
  artış DSC'den. Bu, en yüksek analitik derinlik.
- `claude_fableHigh`, `chatgpt-thinkMode`, `copilot_smart`, `gemini-proStandart`
  artışın "yanıltıcı/boyut kaynaklı" olduğunu **niteliksel** olarak belirtti.
- Zayıf yanıtlar (`gemini-flashStandart`) tersine, Reusability artışını "CIS
  optimizasyonu" gibi **yanlış** bir nedene bağladı (CIS yalnızca +%1.4 arttı).

### 4.3 Zamansal granülerlik — çoğu model "ilk vs son"da takıldı
Yanıtların çoğu yalnızca 1.14.1 ↔ 1.22.2 uçlarını kıyasladı. Yalnızca iki
Claude yanıtı (`opusHigh`, `fableHigh`) **ara dinamikleri** yakaladı: 1.20.1'de
çoklu metriğin dip yapması (ANA min, DAM min, LCOM zirve, NOH=9) ve **1.21.2+
toparlanması** (ANA, MFA, NOH yukarı) → ekibin bilinçli bir temizlik yaptığı
çıkarımı. Bu, ham veride gerçekten mevcut ve en değerli içgörüdür.

### 4.4 Bir LLM, BİZİM veri hatamızı yakaladı
`claude_opusHigh`, VERİ 3'teki **normalize Understandability sütununun işaret
tutarsızlığını** tespit etti (negatif baseline yüzünden 1.0 yerine −0.99
görünüyor). Bu, gerçek bir metodolojik gözlemdir ve raporumuzun §6.4
sınırlamalarına eklenmiştir — LLM'in veri **kalitesini** eleştirebildiğinin
kanıtı.

### 4.5 Şüpheli/yanlış öneriler (eleştiri)
- `deepseek_instantStandart` ve birkaç model **NOP'u düşürmeyi** önerdi
  (5.47→5.20). Oysa polimorfizm QMOOD'da Flexibility/Extendibility/
  Effectiveness'i **pozitif** besler; düşürmek genelde yanlış tavsiyedir.
- `grok-fast`, `Node→Element` kalıtımını kompozisyonla değiştirmeyi önerdi;
  ancak MFA artışı sağlıklı ve DIT zaten sığ (0.71) — bu öneri verinin işaret
  ettiğinin tersi yönde.

### 4.6 Tutarlılık ve "raw vs normalize" çatallanması
Modeller iki farklı yüzde kullandı: bazıları `+%27` (ham, VERİ 2'den),
bazıları `+%9.25` (normalize, VERİ 3'ten). İkisi de **bizim tablolarımızdan**
gelir — yani hata değil, **hangi tabloya tutundukları** sonucu değiştirdi. Bu,
veri sunum biçiminin LLM çıkarımını yönlendirdiğini gösteren önemli bir
meta-bulgudur (prompt mühendisliği dersi).

### 4.7 Belirleyici olan: model "kademesi" değil, çalıştırma MODU
İlk bakışta "üst kademe model daha iyi" denebilir; ancak veri daha incedir.
Asıl belirleyici, **akıl yürütme / uzun düşünme (reasoning/extended) modunun**
açık olması:
- Her ailede reasoning/extended yapılandırması, temel/lite yapılandırmayı geçti:
  ChatGPT *Think* (34) > *Ask* (26); Claude *High* modları (40/37) tepe;
  Copilot *Smart/Think* (33/30) üst sıralar; DeepSeek *Instant-Think* ≥ diğerleri.
- **En çarpıcı kanıt Gemini ailesi içinde:** `Flash-Extended` (30) güçlü çıkıp
  Pro sürümlerine yaklaşırken, `Flash-Lite` (18) ve `Flash-Standard` (23) en
  zayıf ikiliyi oluşturdu. Yani **aynı "Flash kademesi" içinde** extended modu
  ile lite/standart modu arasında 12 puanlık uçurum var.
- Çıkarım: kalite farkı sağlayıcı veya Pro/Flash etiketinden çok, **modelin akıl
  yürütmeye ne kadar "bütçe" ayırdığından** geliyor. Pratik öneri: metrik yorumu
  için **mutlaka reasoning/extended modu** seçilmeli.
- Not: en zayıf iki yanıt (Flash-Lite, Flash-Standard) hâlâ doğru çekirdek
  anlatıyı verdi — yani basit modlar bile "kaba" sonucu buluyor; üst modların
  katkısı **derinlik, halüsinasyondan kaçınma ve nüans**ta.

## 5. Genel sonuç
16 modelin **niteliksel uzlaşısı yüksekti**: hepsi "fonksiyonel/yeniden
kullanılabilirlik dış kalitesi artarken iç kalite (cohesion/kapsülleme/
anlaşılabilirlik) geriliyor; kontrollü teknik borç" çekirdek anlatısında
birleşti — ve bu, bizim metrik analizimizle (§5–6) **örtüşüyor**. Ayrışma
**derinlikte** oldu: DSC-artefaktını sayısal ayrıştırma, zamansal kırılmaları
görme, halüsinasyondan kaçınma ve sınırlamaları kabul etme eksenlerinde
**akıl yürütme/uzun düşünme (reasoning/extended) modları** öne çıktı — bu fark,
model "kademesinden" (Pro/Flash) çok modun kendisinden geliyor (§4.7: aynı Flash
ailesinde Extended 30, Lite 18). Pratik çıkarım: **metrik yorumu için LLM
kullanılacaksa reasoning/extended modu seçilmeli ve çıktı sınıf düzeyi veriyle
çapraz doğrulanmalıdır** (aksi halde makul ama desteksiz sınıf-düzeyi iddialar
sızıyor).
