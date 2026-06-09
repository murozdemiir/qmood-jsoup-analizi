# Jsoup Kütüphanesi Yazılım Mimarisi ve Kalite Değerlendirmesi

**Rapor Tarihi:** 10 Haziran 2026
**Analiz Kapsamı:** v1.14.1 - v1.22.2 (QMOOD & CK Metrikleri)
**Uzmanlık:** Yazılım Mimarisi ve Kalite Analizi

---

## 1. Genel Kalite Değerlendirmesi
Jsoup kütüphanesi, sürüm gelişimi boyunca `DSC` (Boyut) değerini 144'ten 184'e çıkararak büyüme eğilimi sergilemiştir. Ancak bu büyüme, kalite niteliklerinde dengesiz bir seyir izlemiştir.

* **İyileşenler:** `Reusability` (Yeniden Kullanılabilirlik) belirgin bir artış trendindedir (73.96'dan 93.95'e). Bu, `CIS` (Mesajlaşma) ve `DSC` (Sınıf Sayısı) optimizasyonunun bir sonucudur.
* **Bozulanlar:** `Understandability` (Anlaşılabilirlik), sistemin karmaşıklığının (`NOM`) ve bağlantılılık (`DCC`) değerlerinin artışına bağlı olarak negatif yönde ciddi bir erozyona uğramıştır (-53.15'ten -66.66'ya).



---

## 2. Bakım Yapılabilirlik (Maintainability) Analizi
Bakım yapılabilirlik, sistemin yapısal karmaşıklığı ile doğrudan ilintilidir:

* **Bilişsel Yük:** `Understandability` metriğindeki düşüş, kodun okunabilirliğinin azaldığını gösterir.
* **Bağımlılık Durumu:** `DCC` (Coupling) değerlerinin dalgalı ama genel olarak yüksek seyretmesi ve `CAM` (Cohesion) değerinin 0.36'dan 0.30'a gerilemesi, sistemdeki sınıfların birbirine sıkı sıkıya bağlı olduğunu ve sorumluluk dağılımlarının zayıfladığını kanıtlamaktadır. 
* **Sonuç:** Bakım süreçleri, yeni sürümlerde daha fazla "etki analizi" (impact analysis) gerektirecek şekilde zorlaşmıştır.

---

## 3. Teknik Borç (Technical Debt) Tahmini
Metrik verileri, aşağıdaki noktalarda yoğun bir teknik borç birikimine işaret etmektedir:

| Metrik | Değişim (Başlangıç -> Son) | Teknik Borç Riski |
| :--- | :--- | :--- |
| **LCOM** | 126.20 -> 148.69 | Yüksek (Düşük uyum, Tanrı sınıf riski) |
| **CAM** | 0.3633 -> 0.3004 | Yüksek (Parçalı metot yapısı) |
| **CBO** | 3.25 -> 3.38 | Orta (Artan sınıflar arası bağımlılık) |

---

## 4. Refactoring Önerileri
Sistemin yapısal sağlığını korumak adına şu metrik-temelli adımlar atılmalıdır:

1.  **Extract Class:** LCOM değerindeki artışı dengelemek için, yüksek sorumluluk yüküne sahip sınıflar daha küçük, `CAM` değeri yüksek modüllere bölünmelidir.
2.  **Interface Segregation:** `DCC` (Coupling) değerini aşağı çekmek için, sınıflar arası bağımlılıklar arayüzler (interface) üzerinden soyutlanmalıdır.
3.  **Encapsulation:** `DAM` (Data Access Metric) değerindeki %8'lik düşüşü geri kazanmak için, `public` veri alanları `private` yapılıp, kapsülleme prensibi sıkılaştırılmalıdır.
4.  **Dead/Utility Method Cleanup:** `NOM` ve `WMC` değerlerindeki sürekli artış, kullanılmayan veya `utility` sınıfına devredilebilecek metodların tespit edilerek temizlenmesi gerektiğini gösterir.

---

## 5. Mimari Kalite Yorumu: Mimari Erozyon (Architectural Erosion)
Jsoup, işlevsellik kazanırken yapısal bütünlüğünü kademeli olarak kaybetmektedir. Özellikle **Understandability** değerinin sürekli düşmesi ve **CAM** değerinin zayıflaması, sistemde *architectural erosion* (mimari erozyon) olduğunu gösterir. Yazılımın ölçeklenmesi, tasarım kalitesinin (hygiene) önüne geçmiştir. 

Uzun vadede; sınıfların "tek bir işi yapma" prensibinden uzaklaşması, sistemin esnekliğini (Flexibility) sürdürülebilir olmaktan çıkaracaktır.

---
*Not: Bu analiz, QMOOD ve CK metrik modelleri temel alınarak sayısal kanıtlarla oluşturulmuştur.*