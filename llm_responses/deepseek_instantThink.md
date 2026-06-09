# Jsoup Kütüphanesi QMOOD Metrikleri ile Kalite Değerlendirmesi (v1.14.1 → v1.22.2)

**Değerlendirme Tarihi:** 2026-06-10  
**Uzmanlık Alanı:** Nesne Yönelimli Tasarım Metrikleri, QMOOD Modeli (Bansiya & Davis 2002)  
**Dosya Formatı:** UTF-8 Markdown – GitHub, VS Code, Typora, Obsidian, Jupyter uyumlu

Aşağıdaki analiz, jsoup Java HTML parser’ın 11 farklı sürümüne ait ham metrikler ve QMOOD kalite niteliklerine dayanmaktadır. Her iddia, sürümler arası **sayısal değişim** ile kanıtlanmıştır.

---

## 1. GENEL KALİTE DEĞERLENDİRMESİ

### 📈 İyileşen Kalite Nitelikleri

| Nitelik | v1.14.1 | v1.22.2 | Değişim (%) | Yorum |
|---------|---------|---------|-------------|-------|
| **Reusability** | 73.97 | 93.96 | **+27.0%** | Çok güçlü artış. Daha fazla soyutlama? Hayır, ANA düştü. Asıl etken CIS ve DSC artışı (denklemde +0.5*CIS, +0.5*DSC). |
| **Functionality** | 36.70 | 45.78 | **+24.7%** | NOP, CIS, DSC, NOH hepsi arttı veya sabit. Denklemde bu dört metrik pozitif ağırlığa sahip. |
| **Effectiveness** | 1.518 | 1.565 | **+3.1%** | Hafif artış. ANA, DAM, MOA, MFA, NOP toplamı arttı. |
| **Flexibility** | 2.236 | 2.335 | **+4.4%** | Minimal artış. DAM azalmasına rağmen MOA ve NOP artışı dengeyi sağlamış. |
| **Extendibility** | 1.524 | 1.576 | **+3.4%** | Dalgalı seyir. En yüksek 1.706 (v1.16.2), son sürümde 1.576. Sürüm ortalamasına göre stabil. |

### 📉 Bozulan Kalite Nitelikleri

| Nitelik | v1.14.1 | v1.22.2 | Değişim (abs.) | Yorum |
|---------|---------|---------|----------------|-------|
| **Understandability** | -53.16 | -66.67 | **-25.4%** (daha negatif) | **Ciddi bozulma.** Denklemde negatif ağırlıklı metrikler (ANA, DCC, NOP, NOM, DSC) artarken, pozitif ağırlıklı (DAM, CAM) azalmıştır. |

> **Özet:** Jsoup, yeniden kullanılabilirlik ve işlevsellik açısından büyük ilerleme kaydetmiş, ancak **anlaşılabilirlik** (understandability) hızla kötüleşmiştir. Bu, tipik bir “büyüme – bakım zorluğu” ödünleşimidir.

---

## 2. BAKIM YAPILABİLİRLİK (MAINTAINABILITY) ANALİZİ

Bakım kolaylığını doğrudan etkileyen üç faktör: **Anlaşılabilirlik**, **Esneklik (Flexibility)** ve **bağımlılık/bağlılık (coupling/cohesion)**.

### Anlaşılabilirlik (Understandability) – Dramatik düşüş

- v1.14.1: **-53.16**  
- v1.22.2: **-66.67**  

Negatif değerin büyümesi (mutlak artış 13.51 puan) anlaşılabilirliğin **%25 oranında azaldığını** gösterir.  
**Nedenleri (denklem bazlı):**  
- Artan **DCC** (coupling): 3.25 → 3.38  
- Artan **NOM** (karmaşıklık): 9.08 → 9.58  
- Artan **NOP** (polimorfizm): 5.24 → 5.47  
- Azalan **DAM** (kapsülleme): 0.876 → 0.806  
- Azalan **CAM** (cohesion): 0.363 → 0.300  

Bu değişimlerin tümü anlaşılabilirliği düşüren yönde.

### Esneklik (Flexibility) – Durağan

Flexibility: 2.236 → 2.335 (+%4.4).  
Artışın ana kaynağı **MOA** (kompozisyon kullanımı) +%17.4 ve **NOP** +%4.4. Ancak **DCC** artışı esnekliği baskılamıştır.

### Coupling & Cohesion – Alarm veren göstergeler

| Metrik | v1.14.1 | v1.22.2 | Değişim | Etki |
|--------|---------|---------|---------|------|
| **DCC** (efferent coupling) | 3.250 | 3.380 | +4.0% | Kötü – bağımlılıklar artmış |
| **CAM** (cohesion) | 0.363 | 0.300 | **-17.3%** | Çok kötü – sınıflar daha az odaklı |
| **NOM** (metot karmaşıklığı) | 9.08 | 9.58 | +5.5% | Kötü – metotlar daha karmaşık |
| **LCOM_mean** (CK metrik) | 126.2 | 148.7 | +17.8% | Çok kötü – iç bağlılık azalmış |

> **Sonuç:** Bakım yapılabilirlik **belirgin şekilde zorlaşmıştır**. Düşük cohesion ve yüksek coupling, hata düzeltme ve yeni özellik eklemeyi yavaşlatacaktır.

---

## 3. TEKNİK BORÇ (TECHNICAL DEBT) TAHMİNİ

Aşağıdaki metrik eğilimleri, biriken teknik borca işaret eder:

| Gösterge | v1.14.1 | v1.22.2 | Değişim | Borç Türü |
|----------|---------|---------|---------|------------|
| **CAM** (cohesion) | 0.363 | 0.300 | -17.3% | **Sınıflar çok fazla sorumluluk alıyor** → “God Class” riski |
| **DCC** (coupling) | 3.250 | 3.380 | +4.0% | **Ripple effect** – bir değişiklik birçok sınıfı etkiler |
| **NOM** (karmaşıklık) | 9.08 | 9.58 | +5.5% | Metotlar şişiyor, test edilebilirlik düşüyor |
| **WMC_mean** (CK) | 18.03 | 19.22 | +6.6% | Sınıf başına ortalama iş yükü artmış |
| **LCOM_mean** (CK) | 126.2 | 148.7 | +17.8% | Yüksek lack of cohesion – sınıflar bölünmeli |

Özellikle **CAM**’daki %17’lik düşüş, jsoup’un son sürümlerinde **tek sorumluluk ilkesinin (SRP) ihlal edildiğini** gösterir. Teknik borç, özellikle yeni geliştiricilerin koda adaptasyon süresini uzatacak düzeydedir.

---

## 4. REFACTORING ÖNERİLERİ (METRİK-TEMELLİ)

### 4.1 Cohesion’u artır – Sınıfları böl

**Kanıt:** CAM 0.363 → 0.300, LCOM_mean 126 → 149.  
**Öneri:** En yüksek WMC ve LCOM değerine sahip sınıfları tespit edin (ör. `HtmlTreeBuilder`, `TokenQueue`). Her sınıfı **tek bir sorumluluğa** indirgeyin. Büyük sınıfları 3-5 küçük yardımcı sınıfa ayırın.

### 4.2 Coupling’i azalt – Arayüzler ekleyin

**Kanıt:** DCC 3.25 → 3.38 (+%4). CIS (mesajlaşma/arayüz) sadece +%1.5 artmış – yetersiz.  
**Öneri:** Doğrudan sınıf bağımlılıklarını soyut arayüzlerle değiştirin. Özellikle `Element` ve `Node` arasındaki karşılıklı bağımlılıkları gevşetin.

### 4.3 Karmaşıklığı düşür – Metotları parçala

**Kanıt:** NOM 9.08 → 9.58. Ortalama metot sayısı artmış ve muhtemelen metot uzunlukları da artmıştır.  
**Öneri:** Metrik analizi ile **en uzun metotları** (örn. `Parser.parse()`, `HtmlTreeBuilder.process()`) belirleyin. Her metot 20 satırı geçmemeli.

### 4.4 Kalıtım yerine kompozisyonu güçlendirin

**Kanıt:** MFA (inheritance) artmış (+17.4%), MOA (composition) da artmış (+17.4%). Kalıtım derinliği (DIT_mean) azalmış (0.75 → 0.706).  
**Öneri:** Halen kalıtım ağırlıklı olan yerleri (örn. `Node` → `Element` → `Document`) kompozisyon ile değiştirin. `MFA`’nın daha fazla artmasını engelleyin.

### 4.5 Dokümantasyonu ve isimlendirmeyi iyileştirin

Metriklerle ölçülemez ama **understandability**’nin düşüşü bunu zorunlu kılar. Javadoc ekleyin, değişken/metot adlarını anlamlı hale getirin.

---

## 5. MİMARİ KALİTE YORUMU (Architectural Erosion)

**DSC (sistem büyüklüğü) 144 → 184 (+%27.8) artarken aşağıdaki mimari kalite göstergeleri bozulmuştur:**

| Mimari Gösterge | v1.14.1 | v1.22.2 | Değişim | Erosion Belirtisi |
|----------------|---------|---------|---------|-------------------|
| **ANA** (abstraction) | 0.750 | 0.706 | -5.8% | Soyutlama seviyesi düştü → daha az arayüz, daha çok somut sınıf |
| **DAM** (encapsulation) | 0.876 | 0.806 | -8.0% | Veri saklama zayıfladı → doğrudan erişim artmış olabilir |
| **CAM** (cohesion) | 0.363 | 0.300 | -17.3% | Modüller arası sorumluluk dağılımı bozuldu |

Ayrıca **DCC artışı** ve **NOM artışı** da mimari erozyonu destekler.

> **Ancak:** MOA (kompozisyon) ve MFA (kalıtım) artışları, bazı iyileştirmelerin de yapıldığını gösterir. Dolayısıyla **kısmi fakat belirgin bir mimari bozulma vardır**.

---

## SONUÇ

Jsoup, işlevsellik ve yeniden kullanılabilirlik gibi dışsal kalite niteliklerini başarıyla artırmıştır. Ancak **içsel kalite** (anlaşılabilirlik, cohesion, coupling) giderek kötüleşmiştir. Sürüm 1.22.2 itibarıyla teknik borç birikimi dikkat çekicidir. Önerilen refactoring adımları uygulanmazsa, önümüzdeki sürümlerde bakım maliyetleri katlanarak artacaktır.

**Değerlendirme:** *Kalite iyileştirmeleri devam etmekte, ancak sürdürülebilirlik için mimari revizyon acildir.*
