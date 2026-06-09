# jsoup QMOOD Kalite Değerlendirmesi (v1.14.1 → v1.22.2)

## 1. GENEL KALITE EĞILIMI

| Kalite Niteliği | 1.14.1 → 1.22.2 Değişim | Yön | Yorum |
|----------------|--------------------------|-----|-------|
| **Reusability** | +27.0% (74.0 → 94.0) | ✅ İyi | Sürekli ve belirgin artış |
| **Functionality** | +24.7% (36.7 → 45.8) | ✅ İyi | İstikrarlı yükseliş |
| **Understandability** | -25.4% (-53.2 → -66.7) | ❌ Kötü | Ciddi bozulma |
| **Extendibility** | +3.4% (1.52 → 1.58) | ≈ Düz | Dalgalı, net trend yok |
| **Effectiveness** | +3.1% (1.52 → 1.57) | ≈ Düz | Çok hafif artış |
| **Flexibility** | +4.4% (2.24 → 2.33) | ≈ Düz | Minimal değişim |

**Özet:** Reusability ve Functionality güçlü iyileşme gösterirken, **Understandability ciddi şekilde bozulmuştur**. Bu, kodun daha yetenekli ama daha az anlaşılır hale geldiğini gösterir.

---

## 2. BAKIM YAPILABILIRLIK (MAINTAINABILITY) ANALİZİ

### 2.1 Understandability Bileşenleri
Denklem: `-0.33*(ANA+DCC+NOP+NOM+DSC) + 0.33*(DAM+CAM)`

| Metrik | 1.14.1 | 1.22.2 | Değişim | Etki |
|--------|--------|--------|---------|------|
| ANA (soyutlama) | 0.750 | 0.707 | -5.7% | Olumsuz |
| DCC (coupling) | 3.250 | 3.380 | +4.0% | Olumsuz |
| NOP (polimorfizm) | 5.243 | 5.467 | +4.3% | Olumsuz |
| NOM (karmaşıklık) | 9.083 | 9.576 | +5.4% | Olumsuz |
| DSC (boyut) | 144 | 184 | +27.8% | Olumsuz |
| DAM (kapsülleme) | 0.876 | 0.806 | -8.0% | Olumsuz |
| CAM (cohesion) | 0.363 | 0.300 | -17.4% | **En kritik bozulma** |

**Kanıt:** CAM değerinin 0.363 → 0.300 düşüşü, sınıfların sorumluluklarının dağıldığını ve **bağlılık (cohesion) kaybı** yaşandığını gösterir. Bu, anlaşılabilirliği doğrudan düşürmüştür.

### 2.2 Flexibility Bileşenleri
Denklem: `0.25*DAM - 0.25*DCC + 0.50*MOA + 0.50*NOP`

| Metrik | Değişim | Yorum |
|--------|---------|-------|
| DAM ↓ | -8.0% | Esnekliği azaltıcı |
| DCC ↑ | +4.0% | Esnekliği azaltıcı |
| MOA ↑ | +17.4% (0.417 → 0.489) | Esnekliği artırıcı |
| NOP ↑ | +4.3% | Esnekliği artırıcı |

**Sonuç:** Esneklikteki minimal değişim (+4.4%), olumlu ve olumsuz etkilerin birbirini neredeyse tamamen nötralize ettiğini gösterir. **Sistem daha esnek hale gelmemiştir**, sadece farklı bir denge kurmuştur.

---

## 3. TEKNİK BORÇ TAHMİNİ

### 3.1 Artan Teknik Borç Göstergeleri

| Metrik | Trend | Borç Birikimi Açıklaması |
|--------|-------|---------------------------|
| **CAM** | 0.363 → 0.300 (-17%) | Sınıflar “God class” eğilimine girmeden sorumlulukları dağılıyor → **düşük cohesion** bakım zorluğu yaratır |
| **DCC** | 3.25 → 3.38 (+4%) | Artan coupling, değişikliklerin yayılma etkisini artırır → **kırılgan tasarım** |
| **LCOM_mean** | 126 → 149 (+18%) | Metodların farklı özelliklere erişmesi artmış → **düşük iç bağlılık** (CK metriklerinden) |
| **WMC_mean** | 18.0 → 19.2 (+7%) | Sınıf başına ortalama karmaşıklık artmış → test ve anlama maliyeti yükselir |

### 3.2 Borç Azaltıcı Unsurlar
- **MOA ↑ %17** → Daha fazla kompozisyon kullanılmış (kalıtım yerine)
- **ANA ↓ %5.7** → Soyutlama seviyesi düşmüş (bu bazen pragmatik olabilir, ancak borç sayılmaz)

**Değerlendirme:** Teknik borç **artmıştır**. Özellikle düşen CAM ve artan LCOM, gelecekteki değişikliklerin **beklenenden daha maliyetli** olacağını işaret eder.

---

## 4. REFACTORING ÖNERİLERİ (Metrik-Temelli)

### Öneri 1: Düşük CAM’ı İyileştir (Cohesion Artırımı)
- **Metrik hedefi:** CAM’ı 0.321 → 0.350+
- **Aksiyon:** Tek sorumluluk prensibini ihlal eden sınıfları tespit edin. Özellikle `WMC > 25` ve `CAM < 0.30` olan sınıflar hedef alınmalı.
- **Teknik:** Extract Class, Move Method

### Öneri 2: DCC’yi Azalt (Coupling Düşürme)
- **Metrik hedefi:** DCC’yi 3.38 → 3.10 altına çekin
- **Aksiyon:** `CBO_mean` (CK metrik) ile DCC paralel gidiyor. `RFC > 25` ve `CBO > 6` olan sınıfları inceleyin.
- **Teknik:** Introduce Facade, Dependency Inversion

### Öneri 3: Understandability’yi Düzelt (DAM ve CAM Odağı)
- **Metrik hedefi:** Understandability ≥ -58 seviyesine çıkarın (mevcut: -66.7)
- **Aksiyon:** DAM düşüşünü durdurun. Kapsüllemeyi güçlendirin (`private` alan oranını artırın).
- **Teknik:** Encapsulate Field, Hide Delegate

### Öneri 4: LCOM’u Azalt (Metod-Alan İlişkisi)
- **Metrik hedefi:** LCOM_mean’i 149 → 130 altına indirin
- **Aksiyon:** LCOM > 200 olan sınıfları parçalayın.
- **Teknik:** Split Class, Extract Delegate

### Öneri 5: NOP Artışını Kontrollü Yapın
- **Metrik hedefi:** NOP’u 5.47 → 5.20 (eski seviye)
- **Aksiyon:** Gerçek polimorfizm mi yoksa gereksiz kalıtım mı kontrol edin. NOP artarken MFA da artmış (0.30 → 0.36) – bu iyi, ancak anlaşılabilirliği düşürmemeli.
- **Teknik:** Replace Inheritance with Delegation (gereksizse)

---

## 5. MİMARİ KALİTE YORUMU – Architectural Erosion?

**Erosion belirtileri:**

| Belirti | Veri | Erosion var mı? |
|---------|------|------------------|
| DSC artarken CAM düşüyor | 144→184 sınıf, CAM 0.363→0.300 | ✅ Evet – boyut artışı cohesion kaybıyla birlikte |
| DSC artarken DCC artıyor | 144→184, DCC 3.25→3.38 | ✅ Evet – daha büyük sistem daha bağımlı hale gelmiş |
| Soyutlama seviyesi düşüyor | ANA 0.75→0.68 | ✅ Evet – mimari soyutlama zayıflamış |
| Derinlik (DIT_mean) azalıyor | 0.75→0.71 | ≈ Nötr – kalıtım derinliği azalmış (bazen iyi) |

**Kesin yargı:** **Hafif-orta düzeyde mimari erozyon mevcuttur.** Sistem 40 sınıf büyümüş ancak cohesion kaybetmiş, coupling artmış, anlaşılabilirlik ciddi düşmüştür. Bu, “big ball of mud” eğiliminin erken uyarı işaretleridir.

**Olumlu not:** Reusability ve Functionality artmıştır – bu, erozyonun işlevselliği engellemediğini ama gelecekte bakım maliyetlerini artıracağını gösterir.

---

## ÖZET TABLO

| Boyut | Trend 1.14→1.22 | Kritik Uyarı |
|-------|----------------|--------------|
| Reusability | +27% | – |
| Functionality | +25% | – |
| Understandability | -25% | 🔴 CAM, DAM düşüşü |
| Coupling (DCC) | +4% | 🟡 Yavaş ama istikrarlı artış |
| Cohesion (CAM) | -17% | 🔴 En kritik metrik |
| Architectural Erosion | Var (hafif-orta) | 🔴 Boyut/CAM/ANA uyumsuzluğu |

**Sonuç:** jsoup daha yetenekli ve yeniden kullanılabilir hale gelmiş, ancak **anlaşılabilirlik ve iç yapı kalitesi önemli ölçüde bozulmuştur**. Teknik borç birikmektedir. Önerilen refactoring adımları uygulanmazsa, gelecek sürümlerde bakım maliyetleri beklenenden hızlı artacaktır.