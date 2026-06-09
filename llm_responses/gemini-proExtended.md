# jsoup Mimari Kalite ve Metrik Değerlendirme Raporu (v1.14.1 - v1.22.2)

Bir kıdemli yazılım mimarisi ve kalite uzmanı olarak, jsoup kütüphanesinin `1.14.1` sürümünden `1.22.2` sürümüne kadar olan evrimini QMOOD ve CK metrikleri üzerinden inceledim. Projenin doğal büyüme sürecinde bazı metriklerde iyileşmeler görülse de, altta yatan yapısal bozulmalar dikkat çekicidir. 

Aşağıda sayısal verilere dayalı, kanıt temelli mimari kalite değerlendirme raporunu bulabilirsiniz.

---

## 1. GENEL KALİTE DEĞERLENDİRMESİ

Sürümler boyunca jsoup kütüphanesi yapısal olarak büyümüş (**DSC**: 144.0'dan 184.0'a), bu büyüme bazı kalite niteliklerini kağıt üzerinde yukarı çekerken, kodun anlaşılabilirliğine ciddi zarar vermiştir.

* **İyileşen Nitelikler:** * **Reusability (Yeniden Kullanılabilirlik)** (Normalize: $1.0000 \rightarrow 1.0925$) ve **Functionality (İşlevsellik)** (Normalize: $1.0000 \rightarrow 1.0711$) artmıştır. Ancak QMOOD denklemlerine baktığımızda, bu artışın temel sebebi mimarinin "daha iyi" tasarlanması değil, doğrudan sınıf sayısının (**DSC** ve **NOP**) artmasıdır. Sistem büyüdükçe fonksiyon seti genişlemiştir.
  * **Flexibility (Esneklik)** (Normalize: $1.0000 \rightarrow 1.0783$) bir miktar iyileşmiştir. Bunun arkasındaki sayısal kanıt, **MOA (Kompozisyon)** değerinin $0.4167$'den $0.4891$'e çıkmasıdır. Geliştiriciler nesneleri birbirine bağlarken kompozisyon kullanımını artırmış, bu da esnekliğe pozitif yansımıştır.

* **Bozulan Nitelikler:** * **Understandability (Anlaşılabilirlik)** açık ara en çok darbe alan niteliktir (Ham değer: $-53.15 \rightarrow -66.66$, Normalize: $-0.99 \rightarrow -1.19$). Denkleme göre anlaşılabilirliği düşüren ana faktörler; artan boyut (**DSC**), artan metot sayısı (**NOM**: $9.08 \rightarrow 9.57$) ve azalan kapsülleme (**DAM**: $0.8760 \rightarrow 0.8057$) değerleridir.

---

## 2. BAKIM YAPILABİLİRLİK (MAINTAINABILITY) ANALİZİ

Bakım yapılabilirlik, birbiriyle yarışan iki ana kuvvet (Esneklik ve Anlaşılabilirlik) ile Bağlaşım/Uyum (Coupling/Cohesion) metriklerinin bir fonksiyonudur. **Verilere göre jsoup'un bakımı sürümler ilerledikçe zorlaşmıştır.**

* **Coupling (Bağlaşım - DCC & CBO):** Sınıflar arası bağımlılık artmıştır. **DCC/CBO** değeri $3.25$'ten $3.38$'e yükselmiştir. Sınıflar artık birbirine daha sıkı sıkıya bağlıdır, bu da bir modüldeki değişikliğin diğerini bozma riskini artırır.
* **Cohesion (Uyum - CAM & LCOM):** Bakım zorluğunu kanıtlayan en net tablo buradadır. Sınıf içi uyum (**CAM**) $0.3633$'ten $0.3004$'e düşmüştür. Bunu doğrulayan CK metriği **LCOM** (Lack of Cohesion of Methods) ise $126.20$'den **$148.69$**'a fırlamıştır. LCOM'un bu kadar yüksek olması ve artması, sınıfların tek bir amaca hizmet etmediğini (Single Responsibility Principle ihlali), alakasız metot ve verilerin aynı sınıflara yığıldığını gösterir.

**Sonuç:** Esneklik (Flexibility) kompozisyon artışıyla kağıt üzerinde hafif iyileşse de; karmaşıklaşan sınıflar, düşen uyum ve artan bağımlılıklar projenin bakım maliyetini ciddi şekilde artırmıştır.

---

## 3. TEKNİK BORÇ (TECHNICAL DEBT) TAHMİNİ

Teknik borcun birikmekte olduğunu gösteren çok belirgin üç metrik eğilimi bulunmaktadır:

1. **"God Class" (Şişkin Sınıf) Oluşumu (Artan WMC ve LCOM):** Sınıf başına düşen karmaşıklık (**WMC**) $18.03$'ten $19.21$'e çıkarken, yukarıda bahsedilen **LCOM** $126$'dan $148$'e sıçramıştır. Sınıflar fonksiyonellik eklendikçe bölünmek yerine şişirilmiş, bu da gizli bir teknik borç dağı yaratmıştır.
2. **Kapsülleme Zafiyeti (Düşen DAM):** Veri erişim metriklerini ölçen **DAM** (Data Access Metric) $0.8760$'dan $0.8057$'ye gerilemiştir. Yeni eklenen kodlarda internal state'in (iç durumun) yeterince korunmadığı, public/protected alanların dışarı sızdığı görülmektedir.
3. **Arayüz/Sınıf Dengesizliği (Düşen ANA):** Soyutlama seviyesi (**ANA**) $0.75$'ten $0.70$'e düşmüştür. Sisteme yeni eklenen sınıfların (DSC artışı) büyük çoğunluğu somut (concrete) sınıflardır. Arayüz ve soyut sınıflar üzerinden programlama pratiği zayıflamıştır.

---

## 4. REFACTORING ÖNERİLERİ

Yukarıdaki metrik tablosunu tersine çevirmek için uygulanması gereken öncelikli refactoring adımları şunlardır:

* **Extract Class (Sınıf Çıkartma):** * *Hedef Metrik:* **LCOM** ($148.69 \rightarrow$ düşürmek) ve **CAM** ($0.30 \rightarrow$ yükseltmek).
  * *Aksiyon:* Özellikle LCOM değeri proje ortalamasının çok üzerinde olan "Parser" veya "Document" gibi merkezi sınıfları analiz edip, içlerindeki bağımsız sorumlulukları (örneğin ağ işlemleri, ağaç işleme, hata yönetimi) yeni alt sınıflara bölün.
* **Encapsulate Field (Alanı Kapsülleme):** * *Hedef Metrik:* **DAM** ($0.8057 \rightarrow$ yükseltmek).
  * *Aksiyon:* `1.16.2` sürümünden itibaren keskinleşen DAM düşüşünü onarmak için sınıfların görünürlük (visibility) ayarlarını denetleyin. Doğrudan erişime açılmış alanları `private` yapın ve sadece gerektiğinde *getter/setter* metotları sağlayın.
* **Extract Interface / Replace Conditional with Polymorphism:**
  * *Hedef Metrik:* **ANA** ($0.7065 \rightarrow$ yükseltmek) ve **DCC** ($3.38 \rightarrow$ düşürmek).
  * *Aksiyon:* Somut sınıflara olan bağımlılıkları (DCC) kırmak için, sık iletişim kurulan bileşenlerin arasına arayüzler (Interfaces) ekleyin. Kod içindeki karmaşık `if/switch` bloklarını polimorfik yapılara taşıyarak soyutlamayı artırın.

---

## 5. MİMARİ KALİTE YORUMU (Architectural Erosion)

Sistem büyüdükçe (**DSC** $144$'ten $184$'e çıkarken) belirgin bir **mimari bozulma (architectural erosion / drift)** yaşanmaktadır. 

Yazılım geliştirmenin doğasında kod tabanının büyümesi vardır, ancak sağlıklı bir mimaride büyüme, *soyutlamaların (ANA) korunması* ve *uyumun (CAM)* stabil kalması ile yönetilir. jsoup'un bu periyodunda sistem boyutu artarken, soyutlama (ANA) ve kapsülleme (DAM) paralel olarak düşmüş, sınıflar arası bağlaşım (DCC) artmıştır.

Bu veriler; yeni özelliklerin mevcut mimari vizyona (OOD prensiplerine) uygun şekilde zarifçe entegre edilmediğini, bunun yerine mevcut sınıflara "yama yapılarak" hızlıca eklendiğini (quick-and-dirty) göstermektedir. Mimari, nesne yönelimli bir yapıdan ziyade, birbirine sıkı sıkıya bağlı prosedürel veri yığınlarına (LCOM artışı) doğru kayma tehlikesi altındadır.