# jsoup QMOOD kalite değerlendirmesi (1.14.1 → 1.22.2)

## 1. Genel kalite eğilimi

### 1.1 Niteliklerin özet eğilimi

Normalize değerler (1.14.1 = 1.0):

| Nitelik           | 1.14.1 | 1.22.2 | Göreli değişim (yaklaşık) |
|-------------------|--------|--------|----------------------------|
| Reusability       | 1.0000 | 1.0925 | **+%9**                    |
| Flexibility       | 1.0000 | 1.0783 | **+%8**                    |
| Understandability | -0.9900| -1.1914| **-%20 (kötüleşme)**       |
| Functionality     | 1.0000 | 1.0711 | **+%7**                    |
| Extendibility     | 1.0000 | 1.0590 | **+%6**                    |
| Effectiveness     | 1.0000 | 1.0504 | **+%5**                    |

### 1.2 İyileşen nitelikler

**Reusability (73.97 → 93.96, ≈ +%27)**  
- Denklem:  
  

\[
  Reusability = -0.25\cdot DCC + 0.25\cdot CAM + 0.50\cdot CIS + 0.50\cdot DSC
  \]


- **DSC:** 144.0 → 184.0 (**+%28 sınıf sayısı**)  
- **CIS:** 5.3819 → 5.4565 (hafif artış)  
- **DCC:** 3.2500 → 3.3804 (**+%4 coupling**, denklemde negatif)  
- **CAM:** 0.3633 → 0.3004 (**-%17 cohesion**, denklemde pozitif)  

DCC ve CAM’deki değişim aslında Reusability’yi aşağı çekmesi gerekirken, DSC ve CIS artışı baskın geliyor. Yani yeniden kullanılabilirlik, **daha fazla sınıf ve mesajlaşma/arayüz kullanımı** üzerinden büyüyor; iç kalite (cohesion/coupling) bu artışı desteklemiyor.

---

**Functionality (36.70 → 45.78, ≈ +%25)**  
- Denklem:  
  

\[
  Functionality = 0.12\cdot CAM + 0.22\cdot (NOP + CIS + DSC + NOH)
  \]


- **DSC:** 144.0 → 184.0 (**+%28**)  
- **NOH:** 12.0 → 13.0 (hafif artış)  
- **NOP:** 5.2431 → 5.4674 (polimorfizm artışı)  
- **CIS:** 5.3819 → 5.4565 (mesajlaşma artışı)  
- **CAM:** 0.3633 → 0.3004 (düşüş, ama katsayısı düşük)

Fonksiyonellik artışı, **daha fazla sınıf, daha fazla hiyerarşi, daha fazla polimorfizm ve mesajlaşma** ile açıklanıyor. CK tarafında da **RFC_mean 18.96 → 20.42 (+%8)** artışı, daha fazla erişilebilir operasyon/method çağrısı olduğunu gösteriyor.

---

**Flexibility (2.24 → 2.33, ≈ +%4)**  
- Denklem:  
  

\[
  Flexibility = 0.25\cdot DAM - 0.25\cdot DCC + 0.50\cdot MOA + 0.50\cdot NOP
  \]


- **MOA:** 0.4167 → 0.4891 (**+%17 kompozisyon**)  
- **NOP:** 5.2431 → 5.4674 (polimorfizm artışı)  
- **DCC:** 3.2500 → 3.3804 (**+%4 coupling**, negatif etki)  
- **DAM:** 0.8760 → 0.8057 (**-%8 kapsülleme**, pozitif katsayılı metrik düşüyor)

Esneklik artışı, **kompozisyon (MOA) ve polimorfizm (NOP)** artışıyla sağlanıyor; coupling ve kapsülleme tarafındaki bozulma bu artışı frenliyor ama tamamen tersine çeviremiyor.

---

**Extendibility (1.52 → 1.58, ≈ +%4) ve Effectiveness (1.52 → 1.57, ≈ +%3)**  
- Extendibility denkleminde ANA, MFA, NOP pozitif; DCC negatif.  
  - **MFA:** 0.3048 → 0.3577 (**+%17 kalıtım kullanımı**)  
  - **NOP:** artıyor  
  - **DCC:** hafif artıyor (negatif etki)  
- Effectiveness denkleminde ANA, DAM, MOA, MFA, NOP pozitif.  
  - DAM düşse de (0.8760 → 0.8057), MOA, MFA, NOP artışıyla net etki pozitif kalıyor.

---

### 1.3 Bozulan nitelik: Understandability

**Understandability (−53.16 → −66.67, ≈ −%25 daha kötü)**  
- Denklem:  
  

\[
  Understandability = -0.33\cdot(ANA + DCC + NOP + NOM + DSC) + 0.33\cdot(DAM + CAM)
  \]


- Negatif katsayılı metrikler (arttıkça kötüleşir):
  - **DSC:** 144.0 → 184.0 (**+%28**)  
  - **NOM_mean:** 9.0833 → 9.5761 (**+%5–6 metot/sınıf**)  
  - **NOP:** 5.2431 → 5.4674 (artış)  
  - **DCC:** 3.2500 → 3.3804 (artış)  
  - **ANA:** 0.7500 → 0.7065 (hafif düşüş, bu terim için olumlu ama etkisi sınırlı)
- Pozitif katsayılı metrikler (arttıkça iyileşir):
  - **DAM:** 0.8760 → 0.8057 (**-%8 kapsülleme**)  
  - **CAM:** 0.3633 → 0.3004 (**-%17 cohesion**)

Sonuç: Sistem büyüyor (DSC ↑), sınıf başına metot sayısı artıyor (NOM ↑), coupling artıyor (DCC ↑), kapsülleme ve cohesion düşüyor (DAM ↓, CAM ↓). Bu kombinasyon, QMOOD açısından anlaşılabilirliği **belirgin biçimde kötüleştiriyor**.

---

## 2. Bakım yapılabilirlik (Maintainability) analizi

Bakım yapılabilirlik için üç ana eksen: **Understandability**, **Flexibility**, **coupling/cohesion**.

### 2.1 Understandability ekseni

- **Understandability:** −53.16 → −66.67 (**≈ −%25 kötüleşme**)  
- Destekleyen metrik değişimleri:
  - **DSC:** 144.0 → 184.0 (**+%28**)  
  - **NOM_mean:** 9.0833 → 9.5761 (**+%5–6**)  
  - **DAM:** 0.8760 → 0.8057 (**-%8**)  
  - **CAM:** 0.3633 → 0.3004 (**-%17**)

Bu, bakım yapan geliştiricinin zihninde tutması gereken modelin hem **daha büyük** hem de **daha dağınık** hale geldiğini gösteriyor. Sınıflar daha fazla metot içeriyor, kapsülleme/cohesion zayıflıyor; bu da kodu anlamayı ve güvenle değiştirmeyi zorlaştırıyor.

---

### 2.2 Flexibility ekseni

- **Flexibility:** 2.2364 → 2.3346 (**≈ +%4 iyileşme**)  
- Pozitif katkılar:
  - **MOA:** 0.4167 → 0.4891 (**+%17 kompozisyon**)  
  - **NOP:** 5.2431 → 5.4674 (polimorfizm artışı)
- Negatif katkılar:
  - **DCC:** 3.2500 → 3.3804 (**+%4 coupling**)  
  - **DAM:** 0.8760 → 0.8057 (**-%8 kapsülleme**)

Esneklik artıyor; yani sistem, davranışları değiştirme/uzatma açısından daha zengin bir yapı sunuyor. Ancak bu esneklik, **daha yüksek coupling ve daha zayıf kapsülleme** ile birlikte geliyor; bu da esnekliğin bakım maliyetini artırıyor.

---

### 2.3 Coupling ve cohesion ekseni

**Coupling:**

- **DCC:** 3.2500 → 3.3804 (**+%4**)  
- **CBO_mean:** 3.2500 → 3.3804 (**+%4**)  

Coupling artışı büyük değil ama **sistem büyürken (DSC +%28)** coupling’in düşmemesi, hatta hafif artması, modülerleşmenin yeterince agresif olmadığını gösteriyor.

**Cohesion:**

- **CAM:** 0.3633 → 0.3004 (**-%17**)  
- **LCOM_mean:** 126.2014 → 148.6957 (**+%18 lack of cohesion**)  

Cohesion tarafındaki bu bozulma, sınıfların sorumluluklarının giderek daha dağınık hale geldiğini gösteriyor. Bu, bakım yapılabilirliği doğrudan olumsuz etkileyen bir sinyal.

---

### 2.4 Maintainability sonucu

- **Esneklik artıyor (Flexibility ↑)**  
- **Anlaşılabilirlik belirgin kötüleşiyor (Understandability ↓)**  
- **Coupling hafif artıyor (DCC/CBO ↑)**  
- **Cohesion belirgin düşüyor (CAM ↓, LCOM ↑)**  

Net etki: jsoup, **daha esnek ama daha zor anlaşılır ve daha dağınık** bir kod tabanına doğru evrilmiş. Bu da bakım yapılabilirliğin **genel olarak zorlaştığını** gösteriyor.

---

## 3. Teknik borç (Technical Debt) tahmini

Teknik borç sinyallerini özellikle karmaşıklık, cohesion, coupling ve anlaşılabilirlik trendlerinden okuyabiliriz.

### 3.1 Artan karmaşıklık

- **WMC_mean:** 18.0347 → 19.2174 (**≈ +%6**)  
- **RFC_mean:** 18.9583 → 20.4239 (**≈ +%8**)  
- **NOM_mean:** 9.0833 → 9.5761 (**≈ +%5–6**)  

Bu artışlar, sınıfların daha fazla metot içerdiğini ve daha fazla mesaj/çağrı yaptığını gösteriyor. Refactoring yapılmadan büyüyen sınıflar, tipik bir **tasarım borcu** göstergesi.

---

### 3.2 Artan lack of cohesion

- **LCOM_mean:** 126.2014 → 148.6957 (**≈ +%18**)  
- **CAM:** 0.3633 → 0.3004 (**-%17**)  

LCOM artışı ve CAM düşüşü, sınıfların içsel tutarlılığının azaldığını gösteriyor. Bu, “çok iş yapan” veya “konu olarak dağılmış” sınıfların arttığına işaret ediyor; bu da ileride **God Class**, **Feature Envy** gibi kokulara dönüşebilecek teknik borç birikimi.

---

### 3.3 Coupling artışı

- **DCC:** 3.2500 → 3.3804 (**+%4**)  
- **CBO_mean:** 3.2500 → 3.3804 (**+%4**)  

Sistem büyürken coupling’in düşmemesi, aksine hafif artması, bağımlılıkların **kontrollü soyutlanmadığını** düşündürüyor. Bu, modüller arası sınırların net olmaması ve ileride değişikliklerin daha fazla yeri etkilemesi anlamına gelebilir.

---

### 3.4 Understandability düşüşü

- **Understandability:** −53.1587 → −66.6680 (**≈ −%25**)  

Bu, teknik borcun “görünmeyen” ama en kritik kısmı: kod çalışıyor ve fonksiyonellik artıyor, ancak kodu anlamak ve güvenle değiştirmek giderek daha pahalı hale geliyor.

---

### 3.5 Teknik borç sonucu

- **Artan WMC, RFC, LCOM ve düşen CAM**, tasarım borcunun biriktiğini gösteriyor.  
- **Coupling’in hafif artışı** ve **anlaşılabilirliğin ciddi düşüşü**, bu borcun ileride büyük refactoring dalgaları gerektirebileceğini işaret ediyor.  
- Borç şu anda “kritik patlama” seviyesinde görünmüyor, ancak trend **borç birikimi yönünde**.

---

## 4. Refactoring önerileri (metrik-temelli)

### 4.1 Yüksek WMC/LCOM sınıflarını parçalama

- Hedef metrikler:  
  - **WMC_mean:** 18.03 → 19.22  
  - **LCOM_mean:** 126.20 → 148.70  
  - **NOM_mean:** 9.08 → 9.58  
- Öneri:  
  - WMC ve LCOM değeri ortalamanın belirgin üzerinde olan sınıfları tespit et.  
  - Bu sınıfları **tek sorumluluk ilkesine** göre alt sınıflara böl.  
  - İlgili metot kümelerini yeni sınıflara/servislere taşı.  
- Beklenen etki:  
  - WMC ve LCOM düşer, CAM yükselir.  
  - QMOOD’da Understandability ve Reusability iyileşir.

---

### 4.2 Cohesion artırıcı yeniden düzenleme

- Hedef metrikler:  
  - **CAM:** 0.3633 → 0.3004 (yükseltilmeli)  
  - **LCOM_mean:** 126.20 → 148.70 (düşürülmeli)  
- Öneri:  
  - Sınıf içindeki metot–alan kullanım matrisini çıkar.  
  - Aynı alanları kullanan metotları aynı sınıfta grupla, ilgisiz metotları başka sınıflara taşı.  
  - Gerektiğinde “helper” veya “service” sınıflar oluştur.  
- Beklenen etki:  
  - CAM artar, LCOM düşer.  
  - Understandability ve Maintainability artar.

---

### 4.3 Coupling azaltma (DCC/CBO düşürme)

- Hedef metrikler:  
  - **DCC:** 3.25 → 3.38 (trend tersine çevrilmeli)  
  - **CBO_mean:** 3.25 → 3.38  
- Öneri:  
  - Sınıflar arası doğrudan bağımlılıkları arayüzler veya adapter’lar üzerinden soyutla.  
  - Modüller/packageler arası sınırları netleştir; dışa sadece dar, iyi tanımlı API’ler sun.  
  - “Utility” sınıflara aşırı bağımlılığı azalt.  
- Beklenen etki:  
  - DCC ve CBO düşer.  
  - Flexibility ve Maintainability artar, architectural erosion yavaşlar.

---

### 4.4 Kapsüllemeyi güçlendirme (DAM yükseltme)

- Hedef metrik:  
  - **DAM:** 0.8760 → 0.8057 (tekrar yukarı çekilmeli)  
- Öneri:  
  - Gereksiz public/protected alanları private yap.  
  - Alanlara doğrudan erişim yerine davranış odaklı metotlar tasarla.  
  - Gereksiz getter/setter’ları azalt; domain odaklı API’ler tasarla.  
- Beklenen etki:  
  - DAM artar.  
  - Understandability ve Flexibility denkleminde pozitif katkı sağlar.

---

### 4.5 Karmaşık mesajlaşmayı sadeleştirme (RFC düşürme)

- Hedef metrik:  
  - **RFC_mean:** 18.9583 → 20.4239 (artış trendi kırılmalı)  
- Öneri:  
  - Çok sayıda farklı metot çağrısı yapan metotları tespit et.  
  - Bu metotları daha küçük, iyi adlandırılmış yardımcı metotlara böl.  
  - Gereksiz zincir çağrıları ve “orchestrator” metotları sadeleştir.  
- Beklenen etki:  
  - RFC düşer, test edilebilirlik ve anlaşılabilirlik artar.

---

## 5. Mimari kalite ve architectural erosion

### 5.1 Sistem büyümesi ve hiyerarşi

- **DSC (sınıf sayısı):** 144 → 184 (**+%28**)  
- **NOH:** 12 → 13 (hafif artış)  
- **DIT_mean:** 0.7500 → 0.7065 (biraz daha sığ kalıtım)  
- **NOC_mean:** 0.5556 → 0.5326 (alt sınıf sayısı ortalaması hafif düşüş)  
- **MFA:** 0.3048 → 0.3577 (**+%17 kalıtım kullanımı**)  
- **MOA:** 0.4167 → 0.4891 (**+%17 kompozisyon**)  
- **NOP:** 5.2431 → 5.4674 (polimorfizm artışı)

Sistem, **sınıf sayısını artırarak** büyüyor; kalıtım hiyerarşisi çok derinleşmiyor (DIT hafif düşüyor), ancak kalıtım ve polimorfizm kullanımı (MFA, NOP) artıyor. Kompozisyonun da artması (MOA ↑), mimarinin prensipte doğru yönde (composition over inheritance) evrildiğini gösteriyor.

---

### 5.2 Mimari bütünlük ve erozyon sinyalleri

Büyüme ile birlikte şu trendler var:

- **Coupling:**  
  - DCC: 3.25 → 3.38 (**+%4**)  
  - CBO_mean: 3.25 → 3.38 (**+%4**)  
- **Cohesion:**  
  - CAM: 0.3633 → 0.3004 (**-%17**)  
  - LCOM_mean: 126.20 → 148.70 (**+%18**)  
- **Understandability:**  
  - −53.16 → −66.67 (**≈ −%25**)  

Bu kombinasyon, mimarinin **net modüler sınırlarla** büyümesinden çok, mevcut sınıflara ve modüllere yeni sorumluluklar eklenerek genişlediğini düşündürüyor:

- Sınıf sayısı artıyor (DSC ↑),  
- Sınıflar daha dağınık sorumluluklar alıyor (CAM ↓, LCOM ↑),  
- Bağımlılıklar hafif artıyor (DCC/CBO ↑),  
- Anlaşılabilirlik düşüyor (Understandability ↓).

Bu, **erken düzeyde bir architectural erosion** sinyali:

- Mimarinin tamamen çöktüğünü söylemek için metrikler yeterince dramatik değil (coupling artışı sınırlı).  
- Ancak cohesion’daki belirgin düşüş ve anlaşılabilirlikteki ciddi bozulma, mimarinin “temiz sınırlar” yerine “organik büyüme” ile genişlediğini gösteriyor.

---

### 5.3 Mimari kalite sonucu

- **Fonksiyonellik, yeniden kullanılabilirlik ve esneklik artıyor**: jsoup, daha fazla özellik ve kullanım senaryosunu destekler hale gelmiş.  
- **Anlaşılabilirlik, cohesion ve kısmen coupling kötüleşiyor**: mimari sınırlar ve sorumluluk ayrımı zayıflamış.  

Bu tablo, “özellik odaklı büyüme”nin “mimari temizlik”ten biraz daha fazla önceliklendirildiğini gösteriyor. Trend devam ederse, ileride **büyük ölçekli mimari refactoring** ihtiyacı doğabilir; şu anki metrikler, bunun **erken uyarı** aşamasında olduğunu gösteriyor.
