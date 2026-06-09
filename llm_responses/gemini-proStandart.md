# Jsoup Kütüphanesi QMOOD ve CK Metrikleri Mimari Kalite Analiz Raporu

## 1. Giriş ve Metodoloji
Bu rapor, açık kaynaklı popüler Java HTML parser kütüphanesi **jsoup**'un `1.14.1` ile `1.22.2` sürümleri arasındaki evrimini nesne yönelimli tasarım metrikleri (CK Metrikleri) ve QMOOD (Quality Model for Object-Oriented Design) kalite nitelikleri çerçevesinde eleştirel ve kanıt temelli olarak değerlendirmektedir. 

Analiz kapsamında kullanılan temel QMOOD denklemleri referans alınmıştır:
* **Reusability** = -0.25*DCC + 0.25*CAM + 0.50*CIS + 0.50*DSC
* **Flexibility** = 0.25*DAM - 0.25*DCC + 0.50*MOA + 0.50*NOP
* **Understandability** = -0.33*(ANA+DCC+NOP+NOM+DSC) + 0.33*(DAM+CAM)
* **Functionality** = 0.12*CAM + 0.22*(NOP+CIS+DSC+NOH)
* **Extendibility** = 0.50*(ANA+MFA+NOP) - 0.50*DCC
* **Effectiveness** = 0.20*(ANA+DAM+MOA+MFA+NOP)

---

## 2. Genel Kalite Değerlendirmesi
Sürümler boyunca jsoup kütüphanesinin genel kalite eğilimi **kontrollü bir işlevsel büyüme (Feature Growth) ve bunun bedeli olarak ortaya çıkan ciddi bir yapısal karmaşıklık (Structural Complexity)** olarak özetlenebilir.

### İyileşen ve Güçlenen Kalite Nitelikleri
* **Reusability (Yeniden Kullanılabilirlik):** İlk sürüm olan 1.14.1'de `73.9693` olan ham değer, son sürüm 1.22.2'de `93.9583` seviyesine ulaşmıştır. Normalize bazda **%9.25'lik bir artış** (1.0000 -> 1.0925) söz konusudur. Bu artışın temel motoru, sistem boyutunun yani sınıf sayısının (**DSC: 144.0 -> 184.0**) artması ve arayüz genişliğinin (**CIS: 5.3819 -> 5.4565**) korunmasıdır.
* **Functionality (İşlevsellik):** Ham değer `36.7011`'den `45.7793`'e çıkarak normalize bazda **%7.11'lik bir kazanç** sağlamıştır. Bu durum, kütüphaneye yeni yetenekler, yeni HTML spesifikasyon destekleri ve parse yetenekleri eklendiğinin sayısal kanıtıdır. 
* **Flexibility (Esneklik):** 1.14.1'de `2.2364` olan esneklik endeksi, dalgalanmalarla birlikte 1.22.2'de `2.3346`'ya yükselerek **%7.83** iyileşmiştir. Bu iyileşme, kompozisyonun (**MOA: 0.4167 -> 0.4891**) ve polimorfizmin (**NOP: 5.2431 -> 5.4674**) daha yoğun kullanılmasından kaynaklanmaktadır.

### Kronik Şekilde Bozulan Kalite Nitelikleri
* **Understandability (Anlaşılabilirlik):** Sistemin en zayıf ve en çok yara alan noktası burasıdır. İlk sürümde zaten negatif olan `-53.1587` değeri, son sürümde **-66.6680** seviyesine gerilemiştir. Kesin bir dille ifade etmek gerekirse, anlaşılabilirlik endeksi **%19.14 oranında kötüleşmiştir** (-0.9900 -> -1.1914). QMOOD anlaşılabilirlik denklemine bakıldığında, negatif çarpanlı metriklerin (özellikle DSC'nin 144'ten 184'e çıkması ve karmaşıklığı temsil eden NOM'un 9.0833'ten 9.5761'e yükselmesi) sistemi aşağı çektiği görülmektedir.

| Kalite Niteliği | 1.14.1 (Baseline) | 1.22.2 (Son Durum) | Değişim Durumu | Temel Metrik Nedeni |
| :--- | :---: | :---: | :---: | :--- |
| **Reusability** | 1.0000 | 1.0925 | 📈 İyilesti (+%9.25) | DSC (144 -> 184) artışı |
| **Functionality** | 1.0000 | 1.0711 | 📈 İyilesti (+%7.11) | DSC ve NOP artışı |
| **Understandability** | -0.9900 | -1.1914 | 📉 Bozuldu (-%19.14) | DSC ve NOM artışı, CAM düşüşü |
| **Extendibility** | 1.0000 | 1.0590 | 📈 Sınırlı İyileşme | MFA (0.30 -> 0.35) artışı |

---

## 3. Bakım Yapılabilirlik (Maintainability) Analizi
Metrikler ışığında, jsoup projesinde **bakım yapmanın (bug-fix, yeni özellik ekleme, kod okuma) sürümler ilerledikçe zorlaştığı** sonucuna varılmıştır.

1.  **Cohesion (Uyum) Çöküşü:** Sınıfların tek bir sorumluluğa odaklanma derecesini gösteren `CAM` metriği **0.3633'ten 0.3004'e düşmüştür**. Bu düşüşü destekleyen en net CK metriği ise `LCOM_mean` (Lack of Cohesion in Methods) değeridir. LCOM, **126.2014'ten 148.6957'ye fırlamıştır**. Bu durum, sınıfların içindeki metotların artık ortak değişkenleri (state) daha az paylaştığını, yani sınıfların çok amaçlı "torba sınıflara" (Blob/God Class) dönüştüğünü gösterir.
2.  **Coupling (Bağımlılık) Artışı:** Sınıflar arası bağımlılık durumunu ölçen `DCC` metriği **3.2500'den 3.3804'e**, benzer şekilde `CBO_mean` (Coupling Between Object Classes) metriği de **3.2500'den 3.3804'e** yükselmiştir. Sınıfların birbirine daha bağımlı hale gelmesi, kodda yapılacak bir değişikliğin beklenmedik yerleri bozma (Ripple Effect) riskini artırmaktadır.
3.  **Kapsülleme Zafiyeti:** Bakım kolaylığının temel şartı olan bilgi gizleme ilkesi zedelenmiştir. Sınıf içi verilere doğrudan erişimi veya gevşek korumayı temsil eden `DAM` metriği **0.8760'dan 0.8057'ye gerilemiştir**. Sınıfların iç yapısının dış dünyaya açılması bakımı zorlaştıran majör bir etkendir.

---

## 4. Teknik Borç (Technical Debt) Tahmini
jsoup projesinde bilinçli veya bilinçsiz bir teknik borç birikimi mevcuttur. Bu birikimi kanıtlayan metrik eğilimleri şunlardır:

* **Sınıf Başına Yanıt Kümesi Genişlemesi (`RFC_mean`):** Sınıfın çağırabileceği toplam metot sayısını gösteren RFC, **18.9583'ten 20.4239'a** çıkmıştır. Bu durum, sınıfların yürütme yollarının karmaşıklaştığını, dolayısıyla bir sınıfı izole bir şekilde test etmenin (Unit Testing) giderek zorlaştığını kanıtlar.
* **Sınıf Karmaşıklığı Artışı (`WMC_mean`):** Sınıf başına ağırlıklı karmaşıklık **18.0347'den 19.2174'e** yükselmiştir. Sınıflar büyümekte ve iç mantıkları (kontrol yapıları, döngüler vb.) ağırlaşmaktadır.
* **Birlikte Değişen Yapısal Metrikler:** `NOM_mean` (Metot sayısı) 9.08'den 9.57'ye çıkarken, `CAM`'in düşmesi ve `LCOM`'un yükselmesi, refactoring (kod iyileştirme) faaliyetlerinin, yeni özellik ekleme hızının gerisinde kaldığını ve teknik borç faizinin büyüdüğünü net olarak ortaya koymaktadır.

---

## 5. Somut Refactoring Önerileri

### Öneri 1: "Extract Class" (Sınıf Bölme) ile Cohesion İyileştirmesi
* **Gerekçe:** `LCOM_mean` değerinin 148.69'a fırlaması ve `CAM` değerinin 0.30'a gerilemesi.
* **Aksiyon:** Özellikle HTML ağaç yapısını yöneten veya parsing kurallarını içeren devasa sınıflar (örneğin `Element` veya `Parser` sınıfları incelenmeli), birbiriyle ilişkisiz metot grupları ve field'lar belirlenerek alt sınıflara veya yardımcı (utility/helper) sınıflara bölünmelidir. Hedef, sistem genelinde `CAM` değerini tekrar 0.35'in üzerine taşımaktır.

### Öneri 2: "Encapsulate Field" (Alanları Kapsülleme) ile Bilgi Gizleme
* **Gerekçe:** `DAM` metriğinin 0.8760'dan 0.8057'ye düşmesi.
* **Aksiyon:** Sınıflarda doğrudan erişime açık (public veya package-private) tanımlanmış olan field'lar `private` hale getirilmeli, erişim strictly getter/setter veya daha iyisi nesne yönelimli davranış metotları (Tell, Don't Ask prensibi) üzerinden sağlanmalıdır.

### Öneri 3: "Extract Interface / Dependency Inversion" (Arayüz Çıkarma)
* **Gerekçe:** `DCC` ve `CBO_mean` metriklerinin 3.38'e yükselmesi, `ANA` (Soyutlama) metriğinin 0.75'ten 0.70'e düşmesi.
* **Aksiyon:** Sınıfların birbirlerinin somut (concrete) hallerine bağımlı olduğu yerler tespit edilmeli, araya abstract sınıflar veya interface'ler eklenmelidir. Böylece coupling düşürülecek ve esneklik mimari olarak garanti altına alınacaktır.

---

## 6. Mimari Kalite Yorumu (Architectural Erosion)
Sistemde net bir **Mimari Bozulma (Architectural Erosion)** emaresi mevcuttur. Bir yazılım projesi sağlıklı büyüdüğünde sınıf sayısının (DSC) artması doğaldır; ancak bu büyümeye soyutlama seviyelerinin ve hiyerarşik düzenin de eşlik etmesi gerekir. jsoup projesinde ise şu çelişki göze çarpmaktadır:

* Sınıf sayısı (**DSC**) **144'ten 184'e (%27.7 artış)** çıkarken;
* Sınıf Kalıtım Derinliği Ortalama Değeri (**DIT_mean**) **0.7500'den 0.7065'e gerilemiştir**.
* Sistem genelindeki soyutlama oranı (**ANA**) **0.7500'den 0.7065'e düşmüştür**.
* En yüksek hiyerarşi seviyesi sayısı (**NOH**) **12.0'den 13.0'e dalgalanmış, kararlı bir derinleşme gösterememiştir**.

### Sonuç
Bu sayılar bize mimarinin **"yatayda düzleştiğini" (flat architecture)** ve yeni eklenen özelliklerin derin, iyi tasarlanmış nesne yönelimli soyutlamalar yerine, mevcut sınıfların içine metotlar yığılarak ya da sisteme bağımsız, düz ve birbirine sıkı sıkıya bağlı somut sınıflar eklenerek çözüldüğünü göstermektedir. Proje liderlerinin acilen "Feature Freeze" (Özellik Dondurma) ilan edip, mimariyi temizlemek adına kapsamlı bir yapısal refactoring döngüsü başlatması önerilir.
