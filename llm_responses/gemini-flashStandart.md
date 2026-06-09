# Jsoup Kütüphanesi QMOOD ve CK Metrikleri Mimari Değerlendirme Raporu

Bu rapor, `jsoup` HTML parser kütüphanesinin v1.14.1 ile v1.22.2 sürümleri arasındaki evrimini, sağlanan QMOOD ve Chidamber & Kemerer (CK) metrik setlerine dayanarak eleştirel ve kanıt temelli bir yaklaşımla analiz etmektedir.

---

## 1. Genel Kalite Değerlendirmesi

Sistem boyutunun sürekli büyüdüğü (DSC: 144.0 → 184.0, Sınıf Sayısı: 144 → 184) bu evrim sürecinde, kalite niteliklerinde belirgin bir ayrışma gözlenmektedir.

### İyileşen Kalite Nitelikleri
* **Reusability (Yeniden Kullanılabilirlik):** %9.25 artış göstermiştir (1.0000 → 1.0925). Formüle bakıldığında bu artışın temel sürücüsü, artan sistem boyutudur (DSC: 144 → 184). DCC artışına rağmen, CIS (5.38 → 5.45) ve DSC'deki büyüme bu niteliği yukarı taşımıştır.
* **Functionality (Fonksiyonellik):** %7.11 artış kaydetmiştir (1.0000 → 1.0711). Bu durum, CIS ve NOP metriklerindeki kararlı artış ile açıklanır; kütüphanenin yetenek havuzu genişlemiştir.
* **Flexibility & Effectiveness:** Sırasıyla %7.83 ve %5.04 oranında hafif artışlar göstermiştir. Polimorfizmdeki (NOP: 5.24 → 5.46) artış esnekliği desteklemiştir.

### Bozulan Kalite Nitelikleri
* **Understandability (Anlaşılabilirlik):** **Kritik düzeyde bozulmuştur.** Negatif trend %19.14 oranında derinleşmiştir (-0.9900 → -1.1914). Bu çöküşün nedeni; sistem boyutunun (DSC), metot karmaşıklığının (NOM: 9.08 → 9.57) ve coupling değerinin (DCC: 3.25 → 3.38) aynı anda artması, buna karşın cohesion değerinin (CAM: 0.3633 → 0.3004) ciddi oranda düşmesidir.

---

## 2. Bakım Yapılabilirlik (Maintainability) Analizi

Veriler ışığında, `jsoup` kod tabanının **bakımı net bir şekilde zorlaşmıştır.**

* **Cohesion (Bağdaşıklık) Kaybı:** Sınıf içi odaklanmayı gösteren CAM metriği **%17.3** oranında düşmüştür (0.3633 → 0.3004). CK metriklerindeki LCOM (Lack of Cohesion in Methods) ortalamasının 126.2'den 148.6'ya fırlaması bu kaybı doğrulamaktadır. Sınıflar daha jenerik ve çok amaçlı hale gelmiştir.
* **Coupling (Bağımlılık) Artışı:** Sınıflar arası sıkı bağımlılığı temsil eden DCC (ve CBO) 3.25'ten 3.38'e yükselmiştir. 
* **Sonuç:** Düşük cohesion ve yüksek coupling, esneklik (Flexibility) formülünde kağıt üzerinde hafif bir artış (1.0783) getirse de, pratikte bir sınıfta yapılan değişikliğin sistem geneline yayılma riskini (ripple effect) artırmış ve anlaşılabilirliği (Understandability) baltalamıştır.

---

## 3. Teknik Borç (Technical Debt) Tahmini

Kod tabanında yapısal bir teknik borç birikimi olduğuna dair güçlü sinyaller mevcuttur:

* **WMC (Weighted Methods per Class) Trendi:** Sınıf başına metot karmaşıklığı 18.03'ten 19.21'e çıkmıştır. Sınıf sayısı artarken sınıf içi karmaşıklığın da artması, sorumlulukların iyi dağıtılamadığını gösterir.
* **LCOM Patlaması:** LCOM'un %17.8 artarak 148.6'ya ulaşması, sınıfların "God Class" (Tanrı Sınıf) olma yolunda ilerlediğine veya single responsibility prensibinden saptığına işaret eder.
* **Düşen Soyutlama (ANA):** Soyutlama oranı 0.75'ten 0.70'e gerilemiştir. Tasarım, somut implementasyonlara bağımlı hale gelmektedir.

---

## 4. Refactoring Önerileri

1. **Extract Class (Sınıf Ayırma) - LCOM ve CAM Müdahalesi:**
   * *Gerekçe:* LCOM_mean > 148 ve CAM < 0.30.
   * *Aksiyon:* Cohesion değeri düşük, çok fazla sorumluluk üstlenmiş büyük sınıflar tespit edilmeli, mantıksal olarak ayrılabilir metot ve alanlar yeni alt sınıflara (Component) bölünmelidir.
2. **Reduce Coupling - DCC & CBO Optimizasyonu:**
   * *Gerekçe:* DCC'nin 3.38'e ve RFC'nin (Response for a Class) 20.42'ye yükselmesi.
   * *Aksiyon:* Sınıflar arası doğrudan çağrılar yerine Interface veya Abstract Class kullanımı artırılmalıdır. Tasarım Dependency Inversion prensibine göre modernize edilmelidir.
3. **Method Decomposition - WMC & NOM Regresyonu:**
   * *Gerekçe:* Sınıf başına ortalama metot sayısının (NOM) 9.57'ye ve WMC'nin 19.21'e çıkması.
   * *Aksiyon:* Karmaşık ve uzun metotlar, daha küçük ve okunabilir alt metotlara (Extract Method) bölünerek buralardaki bilişsel yük azaltılmalıdır.

---

## 5. Mimari Kalite Yorumu (Architectural Erosion)

`jsoup` kütüphanesinde **belirgin bir Mimari Aşınma (Architectural Erosion) belirtisi vardır.**

* **Boyut vs. Kalite Çelişkisi:** DSC (144'ten 184'e) büyürken, hiyerarşi derinliği (NOH) 12.0'den 13.0'e çıkmış, ancak kalıtım faktörü (MFA) 0.30'dan 0.35'e yükselmesine rağmen soyutlama (ANA) 0.75'ten 0.70'e düşmüştür.
* **Belirsizlik/Aksaklık noktası:** v1.17.2 ile v1.20.1 sürümleri arasında NOH geçici olarak 9.0'a düşmüş, ardından v1.22.2'de tekrar 13.0'e fırlamıştır. Bu dalgalanma, mimaride kararlı bir hiyerarşik vizyonun sürdürülemediğini, sürümler arasında majör ve plansız yeniden yapılandırmalara gidildiğini göstermektedir.
* **Özet:** Yeni özellikler eklendikçe (DSC ve Functionality artışı), kütüphanenin temel nesne yönelimli tasarım omurgası gevşemiş; sistem daha kırılgan, daha az anlaşılır ve bakımı daha maliyetli bir yapıya evrilmiştir.
