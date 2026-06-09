# jsoup QMOOD Kalite Değerlendirmesi

**Kapsam:** 1.14.1 → 1.22.2 sürümleri  
**Not:** QMOOD ham değerleri sistem içi karşılaştırma için yorumlanmıştır. Özellikle **Understandability** değerinin negatif çıkması, formül yapısından kaynaklıdır; burada önemli olan **göreli değişim** yönüdür.

---

## 1) Genel kalite değerlendirmesi

Genel eğilim **karma ama kısmen iyileşen dış kalite / zayıflayan iç bakım kalitesi** şeklindedir.

### QMOOD kalite nitelikleri: ilk sürümden son sürüme değişim

| Nitelik | 1.14.1 | 1.22.2 | Değişim |
|---|---:|---:|---:|
| Reusability | 73.9693 | 93.9583 | **+27.02%** |
| Flexibility | 2.2364 | 2.3346 | **+4.39%** |
| Understandability | -53.1587 | -66.6680 | **daha kötü** (≈ **25.41%** daha negatif) |
| Functionality | 36.7011 | 45.7793 | **+24.74%** |
| Extendibility | 1.5240 | 1.5756 | **+3.39%** |
| Effectiveness | 1.5181 | 1.5653 | **+3.11%** |

### Sayısal yorum

- **Reusability artmış**: 73.9693 → 93.9583. Bu, yeni sürümlerde kodun yeniden kullanılabilirliğinin yükseldiğini gösterir.
- **Functionality artmış**: 36.7011 → 45.7793. Sistem daha fazla işlevsel kapasite taşıyor.
- **Flexibility hafif artmış**: 2.2364 → 2.3346, ancak artış düzensiz; örneğin 1.16.2’de 2.4146 ile tepe yapıp son sürümde geriliyor.
- **Extendibility ve Effectiveness sınırlı ama pozitif artmış**: sırasıyla +3.39% ve +3.11%.
- **Understandability bozulmuş**: -53.1587 → -66.6680. Bu, son sürümün daha zor anlaşılır olduğuna işaret eder.

### Neden böyle olmuş olabilir?

- Reusability artışının ana destekçisi **DSC**’deki büyüme: 144 → 184 (**+27.78%**).
- Functionality artışı da yine ölçek büyümesiyle uyumlu: daha fazla sınıf ve daha fazla mesajlaşma/arayüz kullanımı.
- Buna karşılık **CAM** düşmüş: 0.3633 → 0.3004 (**-17.31%**). Cohesion zayıfladığı için anlaşılabilirlik ve bakım kolaylığı baskılanmış olabilir.
- **DCC** artmış: 3.2500 → 3.3804 (**+4.01%**). Coupling artışı, kalite kazanımlarının bir kısmını geri götürüyor.

---

## 2) Bakım yapılabilirlik (Maintainability) analizi

Bakım yapılabilirlik açısından tablo **zayıflama yönünde**.

### Gerekçeler

- **Understandability kötüleşmiş**: -53.1587 → -66.6680.  
  Bu, kodun zihinsel olarak daha zor takip edildiğini gösterir.
- **Flexibility hafif iyileşmiş**: 2.2364 → 2.3346.  
  Ancak artış küçük ve dalgalı; tek başına bakım kolaylığını güçlü biçimde iyileştirmiyor.
- **Coupling artmış**: DCC 3.25 → 3.3804.  
  Ayrıca CK tarafında **CBO_mean** de 3.25 → 3.3804.
- **Cohesion düşmüş**: CAM 0.3633 → 0.3004.  
  Düşük cohesion, sınıfların daha az odaklı hale geldiğini gösterir.
- **Karmaşıklık artmış**: WMC_mean 18.0347 → 19.2174 ve NOM_mean 9.0833 → 9.5761.
- **LCOM artmış**: 126.2014 → 148.6957.  
  Bu da sınıfların iç uyumunun bozulduğunu destekler.

### Sonuç

Bakım yapılabilirlik, **flexibility’deki küçük artışa rağmen** genel olarak **zorlaşmış** görünüyor.  
Bunu belirleyen ana sinyaller: **düşen CAM**, **artan DCC/CBO**, **artan WMC/LCOM** ve **kötüleşen Understandability**.

---

## 3) Teknik borç (Technical Debt) tahmini

Teknik borç birikimine en çok işaret eden eğilimler şunlar:

### Güçlü borç sinyalleri

- **LCOM artışı:** 126.2014 → 148.6957 (**+17.82%**)  
  Sınıflar daha az tutarlı hale geliyor.
- **WMC artışı:** 18.0347 → 19.2174 (**+6.56%**)  
  Sınıf başına davranış yükü artıyor; değişiklik riski yükselir.
- **RFC artışı:** 18.9583 → 20.4239 (**+7.73%**)  
  Bir sınıfı anlamak ve test etmek için tetiklenebilecek davranış sayısı artıyor.
- **DCC/CBO artışı:** 3.25 → 3.3804 (**+4.01%**)  
  Bağımlılık yükü yükseliyor.
- **CAM düşüşü:** 0.3633 → 0.3004 (**-17.31%**)  
  Cohesion zayıfladığı için bakım maliyeti artar.
- **ANA ve DAM düşüşü:**  
  - ANA: 0.75 → 0.7065 (**-5.80%**)  
  - DAM: 0.8760 → 0.8057 (**-8.03%**)  
  Soyutlama ve kapsülleme zayıflaması teknik borç belirtisidir.

### Daha karışık sinyaller

- **MFA artmış:** 0.3048 → 0.3577 (**+17.36%**)  
  Kalıtım/soyut sınıf kullanımı artmış; bu extendibility’yi destekleyebilir.
- **NOP artmış:** 5.2431 → 5.4674 (**+4.28%**)  
  Polimorfizm artışı esneklik sağlar; ancak fazla artış karmaşıklığı da büyütebilir.
- **MOA artmış:** 0.4167 → 0.4891 (**+17.37%**)  
  Kompozisyon kullanımı artmış; bu olumlu olabilir.

### Sonuç

Teknik borç birikimi sinyali **güçlüdür**, çünkü kazanılan esneklik ve genişleyebilirlik; **cohesion kaybı, coupling artışı ve sınıf karmaşıklığı** ile dengelenmemiştir.

---

## 4) Refactoring önerileri

### 1. Düşük cohesion gösteren sınıfları böl
- Gerekçe: **CAM 0.3633 → 0.3004**, **LCOM 126.2 → 148.7**
- Hedef: tek sorumlulukları ayrıştırmak, sınıf içi tutarlılığı artırmak.

### 2. Yüksek bağımlılık oluşturan ilişkileri arayüz / adaptör ile gevşet
- Gerekçe: **DCC 3.25 → 3.3804**, **CBO 3.25 → 3.3804**
- Hedef: doğrudan sınıf bağımlılıklarını azaltmak, değişiklik etkisini sınırlandırmak.

### 3. Büyük sınıfları parçala, davranışı servis / yardımcı sınıflara taşı
- Gerekçe: **WMC 18.0347 → 19.2174**, **RFC 18.9583 → 20.4239**
- Hedef: sınıf başına davranış yoğunluğunu düşürmek, test edilebilirliği artırmak.

### 4. Soyutlama ve kapsüllemeyi güçlendir
- Gerekçe: **ANA 0.75 → 0.7065**, **DAM 0.8760 → 0.8057**
- Hedef: implementasyon detaylarını gizlemek, genişleme noktalarını artırmak.

### 5. Kalıtım artışını kontrollü tut, kompozisyonu tercih et
- Gerekçe: **MFA 0.3048 → 0.3577**, **NOH 12 → 13**, **DSC 144 → 184**
- Hedef: derin/karmaşık hiyerarşiler yerine daha yönetilebilir bileşim yapıları kurmak.

---

## 5) Mimari kalite yorumu: architectural erosion var mı?

**Kısmi architectural erosion belirtisi var.** Tam bir çöküş yok, ama mimari sağlık karışık.

### Erozyon lehine kanıtlar

- Sistem büyümüş: **DSC 144 → 184 (+27.78%)**
- Buna rağmen:
  - **CAM düşmüş**: 0.3633 → 0.3004
  - **DCC artmış**: 3.25 → 3.3804
  - **WMC artmış**: 18.0347 → 19.2174
  - **LCOM artmış**: 126.2014 → 148.6957
  - **Understandability bozulmuş**: -53.1587 → -66.6680

Bu kombinasyon, büyüme ile birlikte mimarinin daha az anlaşılır, daha az tutarlı ve daha bağımlı hale geldiğini düşündürür.

### Erozyon aleyhine kanıtlar

- **Reusability**, **Functionality**, **Extendibility** ve **Effectiveness** artmış.
- **MOA** ve **NOP** yükselmiş; bu, bazı yerlerde daha esnek tasarım tercihleri olduğunu gösterir.

### Nihai yorum

Mimari, büyürken tamamen kötüleşmemiş; fakat **iç yapısal kalite, dış kalite kazanımlarına göre daha zayıf ilerlemiş**.  
Dolayısıyla tablo, **ölçek büyümesiyle birlikte kademeli mimari erozyon** işaretleri veriyor.

---

## Kısa sonuç

- **İyileşenler:** Reusability, Functionality, Extendibility, Effectiveness
- **Bozulanlar:** Understandability, CAM, ANA, DAM
- **Riskli eğilimler:** DCC/CBO, WMC, LCOM, RFC artışı
- **Genel hüküm:** jsoup büyürken işlevsel ve yeniden kullanılabilir tarafı güçlenmiş; ancak bakım kolaylığı ve mimari saflık zayıflamış.
