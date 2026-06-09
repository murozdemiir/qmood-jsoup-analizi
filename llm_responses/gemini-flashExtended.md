# QMOOD Kalite Değerlendirme Raporu: Jsoup Evrimi

**Rol:** Kıdemli Yazılım Mimarisi ve Yazılım Kalitesi Uzmanı  
**Analiz Edilen Sistem:** jsoup (Java HTML Parser)  
**Analiz Kapsamı:** Sürüm 1.14.1 — Sürüm 1.22.2  

---

## 1. Genel Kalite Değerlendirmesi

Jsoup kütüphanesinin 1.14.1 sürümünden 1.22.2 sürümüne uzanan evriminde, **boyut genişlemesine bağlı olarak fonksiyonel yeteneklerin arttığı, ancak yapısal temizliğin feda edildiği** net bir biçimde görülmektedir. 

### İyileşen Kalite Nitelikleri
* **Reusability (Yeniden Kullanılabilirlik):** İlk sürüme göre **%9.25 artış** göstermiştir (1.0000 $\rightarrow$ 1.0925). Ancak bu artış yanıltıcıdır; QMOOD formülündeki DSC (Boyut: 144 $\rightarrow$ 184) ve CIS (Arayüz boyutu: 5.38 $\rightarrow$ 5.45) artışından beslenmektedir. Sistem büyüdüğü için teorik olarak daha fazla eleman sunmaktadır.
* **Functionality (Fonksiyonellik) & Effectiveness (Etkililik):** Fonksiyonellik **%7.11** (1.0000 $\rightarrow$ 1.0711), etkililik ise **%5.04** (1.0000 $\rightarrow$ 1.0504) artmıştır. Kütüphaneye yeni özellikler eklendiği DSC ve polimorfizm (NOP: 5.24 $\rightarrow$ 5.46) artışından doğrulanmaktadır.
* **Flexibility (Esneklik):** **%7.83** yükselmiştir (1.0000 $\rightarrow$ 1.0783). Bu yükselişteki en büyük pay, kompozisyonun (MOA: 0.4167 $\rightarrow$ 0.4891) doğru şekilde artırılmasıdır.

### Bozulan Kalite Nitelikleri
* **Understandability (Anlaşılabilirlik):** **Açık ara en kritik çöküş buradadır.** Ham değer -53.1587'den -66.6680'e gerilemiş, yani anlaşılabilirlik **%20.3 oranında kötüleşmiştir**. QMOOD modelinde anlaşılabilirliği baltalayan karmaşıklık (NOM: 9.08 $\rightarrow$ 9.57) ve boyut (DSC: 144 $\rightarrow$ 184) artarken, tasarımı koruyan kapsülleme (DAM: 0.8760 $\rightarrow$ 0.8057) ve cohesion (CAM: 0.3633 $\rightarrow$ 0.3004) ciddi oranda düşmüştür.

---

## 2. Bakım Yapılabilirlik (Maintainability) Analizi

Veriler ışığında jsoup'un **bakımının sürümler ilerledikçe net bir şekilde zorlaştığı** söylenebilir. Bakım kolaylığını doğrudan etkileyen parametrelerin analizi şu şekildedir:

* **Giderek