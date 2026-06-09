# jsoup Kütüphanesi — QMOOD Tabanlı Kanıt Temelli Kalite Değerlendirmesi

**Kapsam:** Sürüm `1.14.1` → `1.22.2` (11 sürüm)
**Yöntem:** QMOOD (Bansiya & Davis, 2002) kalite nitelikleri + CK metrik ortalamaları
**Temel uyarı:** Tüm metrikler **sistem düzeyi ortalamalardır**; dağılımı (hotspot'ları) gizler. Sabit bir ortalama, birkaç aşırı sınıfı maskeleyebilir. Yorumlar bu sınırlamayı dikkate alır.

---

## 0. Yönetici Özeti

İki tür eğilim birbirinden ayrılmalıdır:

- **Boyut-bağımlı nitelikler** (Reusability, Functionality, Understandability) belirgin "değişti" gibi görünür, ancak bu değişimin büyük kısmı denklemlerdeki `DSC` (boyut) teriminden kaynaklanır — gerçek tasarım iyileşmesi değildir.
- **Boyut-bağımsız nitelikler** (Flexibility, Extendibility, Effectiveness) gerçek tasarım davranışını yansıtır ve **mütevazı (+%3–4) bir iyileşme** gösterir.

Asıl endişe veren içsel (sınıf-içi) eğilim: **kohezyon erozyonu** (CAM −%17.3, LCOM +%17.8) ve **kapsülleme zayıflaması** (DAM −%8.0). Kuplaj artışı (DCC/CBO +%4) ise sınırlıdır.

---

## 1. Genel Kalite Değerlendirmesi

### 1.1 Ham nitelik değişimleri (1.14.1 → 1.22.2)

| Nitelik | 1.14.1 | 1.22.2 | Δ | Yorum |
|---|---:|---:|---:|---|
| Reusability | 73.97 | 93.96 | **+%27.0** | Yanıltıcı — boyut kaynaklı (aş. bkz.) |
| Functionality | 36.70 | 45.78 | **+%24.7** | Yanıltıcı — boyut kaynaklı |
| Understandability | −53.16 | −66.67 | **−%25.4 (büyüklük)** | Hem boyut hem kohezyon kaynaklı kötüleşme |
| Flexibility | 2.2364 | 2.3346 | +%4.4 | Gerçek iyileşme (boyut-bağımsız) |
| Extendibility | 1.5240 | 1.5756 | +%3.4 | Gerçek, ortada zirve yaptı |
| Effectiveness | 1.5181 | 1.5653 | +%3.1 | Gerçek iyileşme |

> **Not (VERI 3 tutarsızlığı):** Normalize edilmiş Understandability sütunu negatif baz değerinin işaret tutarsızlığı nedeniyle güvenilir değildir (örn. baz sürüm 1.0 yerine −0.99 görünür). Yorumlar **ham değerlere** dayandırılmıştır.

### 1.2 Neden "Reusability +%27" gerçek bir iyileşme DEĞİL?

`Reusability = −0.25·DCC + 0.25·CAM + 0.50·CIS + 0.50·DSC`

Denklemi **boyut terimi** ile **kalite terimi** olarak ayrıştırdığımızda:

| Sürüm | Boyut payı (0.50·DSC) | Kalite payı (−0.25·DCC + 0.25·CAM + 0.50·CIS) |
|---|---:|---:|
| 1.14.1 | 72.00 | **1.969** |
| 1.22.2 | 92.00 | **1.958** |

Toplam +20'lik artışın **tamamı** boyut büyümesinden (DSC 144→184) gelir; tasarım kalitesi bileşeni aslında hafifçe **gerilemiştir** (1.969 → 1.958). Aynı boyut-domination etkisi `Functionality` (0.22·DSC terimi) ve `Understandability` (−0.33·DSC terimi) için de geçerlidir. Bu nedenle bu üç nitelik, kalite kanıtı olarak tek başına kullanılamaz.

### 1.3 İyileşen vs. bozulan tasarım metrikleri

| İyileşenler | Δ | | Bozulanlar | Δ |
|---|---:|---|---|---:|
| MOA (kompozisyon) | +%17.4 | | CAM (kohezyon) | **−%17.3** |
| MFA (kalıtım kullanımı) | +%17.4 | | DAM (kapsülleme) | −%8.0 |
| NOP (polimorfizm) | +%4.3 | | ANA (soyutlama) | −%5.8 |
| | | | DCC (kuplaj) | +%4.0 |
| | | | NOM (karmaşıklık) | +%5.4 |

**Sonuç:** Sürüm geçmişi boyunca takım, kompozisyon/polimorfizm yönünde ilerlemiş (esneklik artışını besleyen olumlu hamle), ancak bunun bedeli sınıf-içi kohezyonun ve kapsüllemenin gerilemesi olmuştur.

---

## 2. Bakım Yapılabilirlik (Maintainability) Analizi

Bakım kolaylığını üç eksende okuyoruz: **anlaşılabilirlik**, **kuplaj**, **kohezyon**.

### 2.1 Anlaşılabilirlik — boyuttan arındırılmış kanıt
Ham Understandability'nin büyük kısmı boyuttandır. Boyuttan bağımsız **olumlu bileşeni** olan `0.33·(DAM + CAM)` izole edildiğinde:

- 1.14.1: `0.33·(0.876 + 0.363) = 0.409`
- 1.22.2: `0.33·(0.806 + 0.300) = 0.365` → **−%10.7**

Yani boyut etkisi çıkarıldığında bile, kavranabilirliği besleyen kapsülleme+kohezyon bileşeni gerçek anlamda gerilemiştir.

### 2.2 Kuplaj
DCC 3.2500 → 3.3804 (**+%4.0**), CK karşılığı CBO ile birebir aynı (+%4.0), MPC 17.34 → 18.23 (+%5.1). Kuplaj artışı **ölçülü** ve kademelidir — bakımı zorlaştıran ana faktör bu değildir.

### 2.3 Kohezyon — asıl bakım riski
CAM 0.3633 → 0.3004 (**−%17.3**) ve LCOM 126.2 → 148.7 (**+%17.8**) **birbirini doğrular**. İki bağımsız metrik aynı yönü gösterdiğinde sinyal güçlüdür: sınıflar zamanla daha az tutarlı sorumluluklar barındırmaktadır.

**Bakım hükmü:** Bakım yapılabilirlik **net olarak hafifçe gerilemiştir**; baskın neden kuplaj patlaması değil, **kohezyon erozyonu** ve **kapsülleme zayıflamasıdır** (DAM −%8.0, eşzamanlı NOA +%9.4 → sınıf başına daha fazla alan).

---

## 3. Teknik Borç (Technical Debt) Tahmini

Teknik borç birikimine işaret eden eğilimler (hepsi sayısal kanıtla):

1. **Kohezyon borcu (en güçlü sinyal):** LCOM +%17.8, CAM −%17.3. Sınıflar şişen, dağınık sorumluluk taşıyan birimlere dönüşüyor.
2. **Sınıf karmaşıklığı borcu:** WMC 18.03 → 19.22 (+%6.6), RFC 18.96 → 20.42 (+%7.7), NOM +%5.4. Sınıf başına metot ağırlığı ve yanıt kümesi büyüyor.
3. **Kapsülleme borcu:** DAM −%8.0 ve NOA +%9.4 birlikte; daha fazla alan, daha az korunaklı erişim olasılığına işaret eder.
4. **Soyutlama incelmesi:** ANA −%5.8, DIT 0.75 → 0.71. Yeni eklenen somut sınıflar soyut ata/arayüz oranını seyreltiyor.

### 3.1 Borç birikiminde kırılma noktası: ~1.20.1
Birden çok metrik aynı sürümde en kötü değerini alıyor:
`ANA` min (0.6824), `DAM` min (0.7945), `LCOM` zirve (150.88), `NOH` min (9).
Sonrasında **1.21.2 / 1.22.2'de kısmi toparlanma** görülüyor: ANA 0.7207'ye, MFA 0.3655 zirvesine, NOH 11→13'e döndü. Bu desen, 1.21 civarında **bilinçli bir refactoring/temizlik çabasına** işaret eder — borç tamamen kontrolsüz birikmemiştir.

---

## 4. Refactoring Önerileri (Somut, Metrik Temelli)

1. **God-class avı (LCOM/CAM hedefli).** LCOM +%17.8 ve CAM −%17.3'ün ana taşıyıcısı muhtemelen birkaç büyük sınıftır. WMC ortalaması ~19'un belirgin üzerindeki sınıfları tespit edip *Extract Class*/*Extract Method* ile sorumlulukları ayırın. Hedef: CAM'ı en az 1.16 düzeyine (~0.36) geri çekmek.
2. **Kapsüllemeyi geri kazanma (DAM hedefli).** DAM 0.876 → 0.806 düşerken NOA +%9.4 arttı. Public/paket-görünür alanları denetleyip private alan + erişimci modeline taşıyın; *Encapsulate Field*.
3. **Sınıf büyümesine tavan (WMC/RFC/NOM hedefli).** WMC +%6.6, RFC +%7.7. Sınıf başına metot/yanıt eşiği için statik analiz kapısı (ör. CI'da WMC üst sınırı) koyun; eşiği aşan sınıfları böl.
4. **Kuplajı arayüzle yönetme (DCC/MPC vs CIS).** DCC +%4.0 ve MPC +%5.1 artarken CIS yalnızca +%1.4 arttı; yani arayüz tasarımı, doğan bağımlılıklara ayak uyduramadı. Yoğun bağımlılıklar için *facade*/arayüz katmanı ekleyerek doğrudan sınıf kuplajını gevşetin.
5. **Soyutlama oranını koruma (ANA hedefli).** Yeni somut sınıflar eklendikçe ANA seyreliyor. 1.21+ toparlanması bunun mümkün olduğunu gösteriyor; yeni alt sistemler için uygun soyut ata/arayüz tanımlamayı tasarım kuralı haline getirin.

---

## 5. Mimari Kalite Yorumu (Architectural Erosion)

Sistem büyürken (DSC 144 → 184, **+%27.8**) erozyon belirtisi **var ama hafiftir** ve niteliği önemlidir:

- **Topolojik (sınıflar arası) erozyon sınırlı:** DCC/CBO yalnızca +%4 arttı; bu, boyut büyümesine göre ölçülü bir kuplaj artışıdır. Sistem "kuplaj patlaması" yaşamıyor.
- **Asıl erozyon sınıf-içi düzeyde:** Kohezyon (CAM/LCOM) ve kapsülleme (DAM) gerilemesi, mimari bozulmanın **modül topolojisinde değil, sınıf tasarımı kalitesinde** yoğunlaştığını gösterir.
- **Sağlıklı mimari kayma:** DIT sığ kalıp hafifçe düşerken (0.75 → 0.71), MOA ve DAC +%17.4 arttı. Bu, **kalıtım yerine kompozisyon** yönünde bilinçli bir tercih olarak okunabilir ve genelde olumlu bir mimari işarettir; Flexibility (+%4.4) ve Effectiveness (+%3.1) artışını da bu besliyor.
- **Aktif yönetişim kanıtı:** 1.20.1 dip noktasını izleyen 1.21–1.22 toparlanması (ANA, MFA, NOH yukarı), denetimsiz çürümeden çok, izlenen ve müdahale edilen bir mimariye işaret eder.

**Mimari hüküm:** Klasik erozyon imzası (boyut↑ + kohezyon↓ + kuplaj↑) mevcuttur, fakat **şiddeti düşüktür** ve kuplajdan çok kohezyon/kapsülleme eksenindedir. Kohezyon ve kapsülleme hedefli refactoring ile tersine çevrilebilir niteliktedir.

---

## Belirsizlikler ve Sınırlamalar

- Tüm değerler **ortalamadır**; tekil hotspot sınıfları gizleyebilir. Kesin teşhis için sınıf düzeyi dağılım (en yüksek LCOM/WMC sınıfları) gereklidir.
- QMOOD denklemlerinin boyut-bağımlı nitelikleri (Reusability/Functionality/Understandability) ölçek büyüdükçe yanıltıcıdır; bu rapor onları kalite kanıtı olarak değil, **boyutun gölgesinde** yorumlamıştır.
- VERI 3'teki normalize Understandability sütununda işaret tutarsızlığı saptanmıştır; ham değerler esas alınmıştır.
- %4–8 aralığındaki değişimler kademelidir; istatistiksel anlamlılık için sürüm-içi varyans verisi mevcut değildir.

---

*Tüm yüzde değişimler 1.14.1 baz alınarak 1.22.2 ile karşılaştırmadan hesaplanmıştır. Δ% = (son − baz) / baz × 100.*
