# QMOOD ve CK Metrikleri Üzerinden jsoup Kütüphanesi Mimari Kalite Analiz Raporu

**Kime:** Mühendislik ve Mimari Değerlendirme Komitesi  
**Kimden:** Kıdemli Yazılım Mimarisi ve Yazılım Kalitesi Uzmanı  
**Konu:** jsoup (Java HTML Parser) Kütüphanesinin Sürümler Arası Evrimi ve Tasarım Kalitesi Değerlendirmesi  
**Format:** UTF-8 / Markdown Görüntüleyicilerle Tam Uyumlu  

---

## Giriş ve Metodoloji
Bu raporda, `jsoup` kütüphanesinin v1.14.1 ile v1.22.2 arasındaki 11 farklı sürümünün mimari kalitesi, **QMOOD (Quality Model for Object-Oriented Design)** ve **CK (Chidamber & Kemerer)** metrik modelleri kullanılarak analiz edilmiştir. Analiz, matematiksel denklemlerin ham veriler üzerindeki izdüşümlerini inceleyerek sistemin büyüme esnasında yapısal bütünlüğünü koruyup koruyamadığını sorgulayan **eleştirel ve kanıt temelli** bir yaklaşımla ele alınmıştır.

---

## 1. Genel Kalite Değerlendirmesi

Sistem genelinde v1.14.1'den v1.22.2'ye doğru gidildikçe ciddi bir hacimsel büyüme söz konusudur. Tasarım boyutu (**DSC**) %27.8 artarak 144.0'dan 184.0'a yükselmiştir. Bu büyüme, QMOOD kalite niteliklerinde doğrusal olmayan, paradoksal yansımalara yol açmıştır.

### İyileşen Kalite Nitelikleri
* **Reusability (Yeniden Kullanılabilirlik):** Ham değeri 73.9693'ten 93.9583'e çıkmış, normalize grafikte %9.25'lik bir iyileşme (`1.0000 -> 1.0925`) kaydedilmiştir.
* **Functionality (İşlevsellik):** Başlangıç baseline'ına göre %7.11'lik bir artış sergilemiştir (`1.0000 -> 1.0711`).
* **Kritik Yorum:** Reusability ve Functionality denklemlerinde `DSC` (Design Size) metriğinin ağırlığı sırasıyla `+0.50` ve `+0.22` gibi pozitif çarpanlara sahiptir. Dolayısıyla bu iki nitelikteki "iyileşme", mimarinin daha modüler veya yeniden kullanılabilir tasarlanmasından değil, **sisteme salt yeni sınıfların eklenmesinden (hacimsel büyümeden) kaynaklanan matematiksel bir illüzyondur.**

### Bozulan Kalite Nitelikleri
* **Understandability (Anlaşılabilirlik):** Sistemin en dramatik çöküş yaşadığı alandır. Başlangıçta -53.1587 olan ham değer, v1.22.2'de -66.6680'e gerileyerek negatif yönde %19.14'lük bir kötüleşme (`-0.9900 -> -1.1914`) göstermiştir. 
* **Gerekçe:** Formüldeki negatif bileşenlerin (büyüyen `DSC`, artan karmaşıklık `NOM: 9.0833 -> 9.5761` ve artan bağlaşım `DCC: 3.2500 -> 3.3804`), pozitif bileşenlerdeki (büyük düşüş yaşayan cohesion `CAM: 0.3633 -> 0.3004`) kazançlardan çok daha baskın olması anlaşılabilirliği yok etmiştir.

### Temel Kalite Metriklerinin Özeti (v1.14.1 vs v1.22.2)

| Metrik Grubu | Metrik | Sürüm 1.14.1 | Sürüm 1.22.2 | Değişim Oranı (%) | Mimari Etki |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **QMOOD Tasarım** | DSC | 144.0000 | 184.0000 | +27.78% | Sistem Hacmi Genişlemesi |
| **QMOOD Tasarım** | DAM | 0.8760 | 0.8057 | -8.03% | Kapsülleme İhlali |
| **QMOOD Tasarım** | CAM | 0.3633 | 0.3004 | -17.31% | Sınıf İçi Uyum Kaybı |
| **CK Ortalamaları**| WMC | 18.0347 | 19.2174 | +6.56% | Metot Karmaşıklığı Artışı |
| **CK Ortalamaları**| LCOM | 126.2014 | 148.6957 | +17.82% | Yapısal Uyumsuzluk/Dağınıklık |

---

## 2. Bakım Yapılabilirlik (Maintainability) Analizi

Veriler ışığında jsoup kütüphanesinin bakımının sürümler ilerledikçe **net bir şekilde zorlaştığı** görülmektedir. Bakım kolaylığını doğrudan etkileyen üç sacayağı (Understandability, Cohesion, Coupling) negatif sinyaller vermektedir:

* **Anlaşılabilirlik Çöküşü:** Yukarıda belirtildiği üzere, `Understandability` endeksinin -66.66'ya gerilemesi, yeni bir geliştiricinin sistemi öğrenme ve hata çözme maliyetini (cognitive load) ciddi oranda artırmıştır.
* **Cohesion (Uyum) Dağılması:** QMOOD `CAM` metriği 0.3633'ten 0.3004'e düşerken (%17.31 kayıp), CK modelindeki `LCOM` (Lack of Cohesion in Methods) metriği 126.2014'ten 148.6957'ye fırlamıştır (%17.82 artış). Bu durum, sınıfların tek bir sorumluluğa odaklanmaktan çıktığını (Single Responsibility Principle ihlali) ve metotların sınıf değişkenlerini ortak kullanma oranının düştüğünü kanıtlar.
* **Coupling (Bağlaşım) Artışı:** `DCC` (Direct Class Coupling) ve `CBO` (Coupling Between Object Classes) metrikleri eşzamanlı olarak 3.2500'ten 3.3804'e yükselmiştir. Sınıflar arası bağımlılıkların artması, bir sınıfta yapılan değişikliğin domino etkisiyle diğer sınıfları da bozma riskini (fragility) yükseltir.
* **Esneklik (Flexibility) Yanılgısı:** `Flexibility` endeksi %7.83 artmış görünmektedir (`1.0000 -> 1.0783`). Bu artış, kompozisyonun (`MOA: 0.4167 -> 0.4891`) ve polimorfizmin (`NOP: 5.2431 -> 5.4674`) artmasından kaynaklansa da, düşen kapsülleme (`DAM`) ve yükselen bağlaşım nedeniyle pratik bakım süreçlerinde bu "esneklik" bir avantaja dönüşemez.

---

## 3. Teknik Borç (Technical Debt) Tahmini

jsoup kod tabanında bilinçli veya bilinçsiz bir teknik borç birikimi söz konusudur. Metrik eğilimleri bu borcun yapısal köklerini açıkça deşifre etmektedir:

* **Kapsülleme Zafiyeti (Encapsulation Erosion):** `DAM` metriği 0.8760'tan 0.8057'ye (%8.03) gerilemiştir. Sınıflardaki korumalı/özel (private/protected) değişkenlerin oranı azalmış, dışarıya doğrudan açılan alan (public field) veya eksik kapsülleme sayısı artmıştır. Bu durum veri güvenliğini ve nesne yönelimli paradigmanın temelini tehdit eden bir teknik borçtur.
* **Genişleyen Sınıf Arayüzleri ve Karmaşıklık:** Sınıf başına düşen metot sayısı (`NOM`) 9.0833'ten 9.5761'e çıkarken, `WMC` (Weighted Methods per Class) karmaşıklığı 18.0347'den 19.2174'e (%6.56) yükselmiştir. Sınıflar hem genişlemiş hem de içsel mantıkları karmaşıklaşmıştır.
* **Test Edilebilirlik Bariyeri (RFC Artışı):** Sınıfın tetikleyebileceği toplam metot sayısını gösteren `RFC` (Response For a Class) metriği 18.9583'ten 20.4239'u görmüştür. Yüksek RFC, kod patikalarının (code paths) arttığını ve dolayısıyla birim test (unit test) yazmanın, tüm senaryoları kapsamanın zorlaştığını gösterir. Artan LCOM (148.69) ve RFC kombini, biriken test borcuna (Testing Debt) işaret eder.

---

## 4. Refactoring (Yeniden Yapılandırma) Önerileri

Mevcut metrik kötüleşmelerini durdurmak ve teknik borcu eritmek adına somut, metrik tabanlı şu refactoring hamleleri uygulanmalıdır:

* **Öneri 1: LCOM ve CAM İyileştirmesi İçin "Extract Class" (Sınıf Çıkarma)**
    * *Hedef:* `LCOM`'u tekrar < 130 seviyesine çekmek ve `CAM`'i > 0.35 yapmak.
    * *Aksiyon:* Özellikle v1.20.1 sürümünden sonra tavan yapan LCOM (150.88) değerini düşürmek amacıyla, uyum göstergesi düşük olan büyük sınıflar (God Class) tespit edilmeli, ortak nesne değişkenlerini kullanmayan metot grupları yeni alt sınıflara (Extract Class) bölünmelidir.
* **Öneri 2: DAM Artırımı İçin "Encapsulate Field" (Alanları Kapsülleme)**
    * *Hedef:* `DAM` metriğini eski baseline olan 0.87 seviyesine geri getirmek.
    * *Aksiyon:* Son sürümlerde (özellikle v1.20.1'de 0.7945'e kadar düşen) açıkça görülen kapsülleme kaybını önlemek için, doğrudan erişime açılmış sınıf değişkenleri (`public fields`) private yapılmalı, erişim sadece kontrollü getter/setter metotları veya immütability (bütünsel nesne aktarımı) üzerinden sağlanmalıdır.
* **Öneri 3: WMC ve RFC Azaltımı İçin "Extract Method" ve Gevşek Bağlaşım**
    * *Hedef:* `WMC` ortalamasını < 18.50 ve `RFC` değerini < 19.50 seviyesine indirmek.
    * *Aksiyon:* Sınıf içi karmaşıklığı düşürmek adına uzun ve çoklu sorumluluğa sahip metotlar parçalanmalı (`Extract Method`), sınıfların doğrudan diğer sınıfları çağırma yoğunluğu (`RFC: 20.42`) arayüzler (interface) araya koyularak soyutlaştırılmalıdır.

---

## 5. Mimari Kalite Yorumu (Architectural Erosion)

Sistem büyüdükçe (`DSC: 144 -> 184`), jsoup mimarisinde kontrollü bir genişlemeden ziyade **Mimaride Aşınma (Architectural Erosion)** belirtileri baş göstermiştir. Bu çıkarımın en büyük kanıtları şunlardır:

* **Derinlik Yerine Genişleme (Hiyerarşi Sapması):** En yüksek kalıtım derinliğini simgeleyen `ANA` (Average Inheritance Depth / DIT) metriği 0.7500'ten 0.7065'e düşmüştür (%5.8 kayıp). Sistem kalıtım ağacını derinleştirmek yerine yatayda, plansız sınıflar ekleyerek büyümüştür. 
* **NOH (Number of Hierarchies) Kararsızlığı:** Mimari kararsızlığın en büyük kanıtı `NOH` metriğidir. v1.14.1'de 12.0 olan hiyerarşi sayısı, v1.20.1'de 9.0'a kadar gerilemiş, ardından v1.22.2'de ani bir refleksle 13.0'a fırlamıştır. Hiyerarşi sayısındaki bu dalgalanma, kütüphanenin omurgasını oluşturan temel kalıtım yapısının (Core Architecture) sürümler arasında yapısal kırılmalar yaşadığını ve refactoring süreçlerinin stabil yönetilemediğini doğrulamaktadır.

> **Sonuç Değerlendirmesi:** jsoup işlevsel olarak zenginleşip (`Functionality`) yeni özelliklere kavuşurken, bu büyümenin faturasını içsel tasarım kalitesini (kapsülleme, uyum ve anlaşılabilirlik) kaybederek ödemiştir. Acil bir refactoring döngüsüne girilmediği takdirde, sistemin sonraki sürümlerde "Big Ball of Mud" (Büyük Çamur Topu) anti-pattern'ine evrilme riski kritik düzeydedir.