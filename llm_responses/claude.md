# LLM Yanıtı — Claude (Opus 4.x)

> Bu yanıt `prompts/01_full_evolution_prompt.txt` promptu Claude'a verilerek
> alınmıştır. Model: Claude Opus 4.x · Erişim: Claude Code · Tarih: 2026-06-10

## Ham yanıt

### 1. Genel Kalite Değerlendirmesi
11 sürüm boyunca (1.14.1 → 1.22.2) tablo, **çift yönlü bir evrim** gösteriyor:
çoğu kalite niteliği iyileşirken anlaşılabilirlik tek yönlü kötüleşiyor.

- **İyileşenler:** Reusability normalize indeksi 1.0000 → 1.0925 (+%9.3),
  Flexibility 1.0000 → 1.0783 (+%7.8), Effectiveness 1.0000 → 1.0504 (+%5.0),
  Extendibility 1.0000 → 1.0590 (+%5.9), Functionality 1.0000 → 1.0711 (+%7.1).
- **Kötüleşen:** Understandability ham skoru −53.16 → −66.67; normalize karşılığı
  −0.99 → −1.19 (mutlak değerce **+%20** artan "anlaşılamazlık").

Temel sürükleyici: **DSC 144 → 184 (+%27.8)**. Reusability ve Functionality
denklemlerinde DSC pozitif katsayılı (0.50 ve 0.22) olduğundan boyut büyümesi
bu nitelikleri mekanik olarak yukarı çekiyor; aynı DSC Understandability
denkleminde −0.33 katsayılı olduğundan onu aşağı çekiyor. Yani "iyileşmelerin"
bir kısmı gerçek tasarım kazanımı değil, boyut artışının denklem etkisidir —
bu ayrımı not etmek önemli (aşağıda 3. ve 5. maddede ayrıştırıyorum).

### 2. Bakım Yapılabilirlik (Maintainability) Analizi
Bakım **zorlaşmıştır**, kanıtlar:
- **Cohesion (CAM) 0.3633 → 0.3004 (−%17.3):** Sınıf içi metotların ortak veri/
  parametre üzerinden ilişkisi zayıflıyor — sınıflar daha "dağınık" sorumluluk
  taşıyor. CK tarafında bunu **LCOM ortalaması 126.2 → 148.7 (+%17.8)** doğruluyor
  (iki bağımsız metrik aynı yöne işaret ediyor → güçlü kanıt).
- **Coupling (DCC) 3.25 → 3.38 (+%4.0):** Sınıflar arası bağ hafifçe artmış;
  CBO_mean de 3.25 → 3.38 ile tutarlı.
- **Encapsulation (DAM) 0.876 → 0.806 (−%8.0):** Veri gizleme oranı düşmüş;
  daha fazla alan dışarıya açılmış, bu da değişiklik dalgalanma riskini artırır.
- Understandability düşüşü (yukarıda) bakım maliyetinin en net göstergesi.

Flexibility'nin artması (+%7.8) olumlu; MOA (kompozisyon) 0.417 → 0.489 ve NOP
(polimorfizm) yüksek seyretmesi esnekliği besliyor. Yani sistem **daha esnek ama
daha az anlaşılır** hale gelmiş — olgunlaşan kütüphanelerde tipik takas.

### 3. Teknik Borç (Technical Debt) Tahmini
Net teknik borç birikimi sinyalleri:
1. **CAM↓ + LCOM↑ birlikte** → cohesion erozyonu (en güçlü sinyal, iki metrik).
2. **DAM↓ (−%8)** → kapsülleme gevşemesi.
3. **DCC/CBO↑** → kademeli coupling artışı.
4. **WMC_mean 18.0 → 19.2 (+%6.5)** ve NOA_mean 2.24 → 2.45 → sınıflar büyüyor
   ve karmaşıklaşıyor.
Borcun **şiddeti ılımlı**: değişimler %5–18 bandında, ani sıçrama yok; bu,
kontrollü/kademeli bir borç birikimi (ani mimari çöküş değil). En kritik sürüm
geçişleri: 1.15.4→1.16.2 (CAM 0.355→0.323 ile ani cohesion düşüşü) ve genel
1.20.x sonrası DSC sıçraması.

### 4. Refactoring Önerileri (metrik temelli)
1. **Düşük-cohesion sınıfları böl (CAM↓, LCOM↑):** `class_metrics.csv` içinde en
   yüksek LCOM'a sahip sınıfları hedefleyip Extract Class uygulayın; ortak alan
   kullanmayan metot kümelerini ayrı sınıflara taşıyın.
2. **Encapsulation'ı geri kazan (DAM↓):** Public/paket alanları private yapıp
   erişimi metotlara taşıyın; özellikle 1.18+ sonrası açılan alanları gözden
   geçirin.
3. **Coupling'i azalt (DCC/CBO↑):** En yüksek CBO'lu sınıflarda arayüz (interface)
   üzerinden bağımlılık ters çevirme (DIP) uygulayın.
4. **Büyüyen sınıfları sadeleştir (WMC↑, NOM↑):** WMC'si en yüksek sınıflarda
   uzun metotları Extract Method ile bölün; çevrimsel karmaşıklığı düşürün.
5. **Hiyerarşi tutarlılığı (NOH dalgalanması 12→9→13):** Kalıtım kök sayısındaki
   oynama, hiyerarşilerin yeniden düzenlendiğini gösterir; soyut taban sınıfların
   tutarlı kullanıldığını doğrulayın.

### 5. Mimari Kalite Yorumu
**Kısmi mimari erozyon var ama kontrollü.** DSC %27.8 büyürken cohesion'ın
düşmesi ve coupling/karmaşıklığın artması klasik erozyon imzasıdır. Ancak:
- MFA (kalıtım yeniden kullanımı) 0.305 → 0.358 (+%17.4) ve MOA (kompozisyon)
  0.417 → 0.489 (+%17.4) **artıyor** → ekip bilinçli olarak kompozisyon ve
  kalıtımla yeniden kullanımı güçlendirmiş; bu erozyona karşı bir denge unsuru.
- DIT_mean 0.75 → 0.71 ile neredeyse sabit → hiyerarşi aşırı derinleşmemiş
  (derin kalıtımın getireceği anlaşılabilirlik cezası yok).

**Sonuç:** jsoup olgun, sağlıklı yönetilen bir kütüphane; erozyon belirtileri
gerçek ama yıkıcı değil. Asıl izlenmesi gereken eğilim **cohesion (CAM/LCOM)**;
düşüş devam ederse bakım maliyeti birikimli olarak artar.

---

## Eleştirel değerlendirme (bizim notlarımız)
| Kriter | Değerlendirme |
|---|---|
| Sayısal kanıt kullandı mı? | Evet — her iddiada metrik + yüzde değişim verildi |
| QMOOD denklemlerini doğru yorumladı mı? | Evet — DSC'nin denklem etkisini ayrıştırdı (güçlü) |
| Halüsinasyon / uydurma metrik var mı? | Hayır gözlenmedi |
| Refactoring önerileri somut mu? | Evet — metrik-hedefli, CSV'ye yönlendiriyor |
| Teknik borç tespiti isabetli mi? | Evet — CAM↓ + LCOM↑ çapraz doğrulaması güçlü |
| Genel puan (1-5) | 5 |
