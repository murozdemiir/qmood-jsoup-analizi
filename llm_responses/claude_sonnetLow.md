# jsoup QMOOD Kalite Analizi (v1.14.1 → v1.22.2)

> **Rol:** Kıdemli Yazılım Mimarisi ve Kalite Uzmanı  
> **Model:** QMOOD (Bansiya & Davis, 2002)  
> **Kapsam:** 11 sürüm, sistem düzeyi ortalama metrikler

---

## 1. Genel Kalite Değerlendirmesi

### İyileşen Nitelikler

| Nitelik | v1.14.1 | v1.22.2 | Δ (ham) | Δ (normalize) |
|---|---|---|---|---|
| **Reusability** | 73.97 | 93.96 | +19.99 | **+%9.25** |
| **Flexibility** | 2.24 | 2.33 | +0.10 | **+%7.83** |
| **Effectiveness** | 1.52 | 1.57 | +0.05 | **+%5.04** |
| **Functionality** | 36.70 | 45.78 | +9.08 | **+%7.11** |
| **Extendibility** | 1.52 | 1.58 | +0.06 | **+%5.90** |

**Reusability** artışının başlıca sürücüsü `CIS` (5.38 → 5.46) ve `DSC` büyümesidir. Denklem ağırlıkları (`+0.50*CIS`, `+0.50*DSC`) bu değişkenlere büyük pay veriyor; büyüyen bir kütüphanede arayüz sayısının artması beklenir, ancak bu kalıcı bir iyileşme değil kısmen boyut etkisidir.

**Functionality** artışı ağırlıklı olarak `NOH` (12 → 13) ve `CIS`/`NOP` büyümesinden kaynaklanıyor — hiyerarşi ve polimorfizm yüzeyinin genişlemesi işlevsel zenginliğe katkı sağlıyor.

### Bozulan Nitelikler

| Nitelik | v1.14.1 | v1.22.2 | Δ (ham) | Δ (normalize) |
|---|---|---|---|---|
| **Understandability** | −53.16 | −66.67 | −13.51 | **−%19.14** |

`Understandability` tek bozulan niteliktir; ancak bozulma **en büyük mutlak değişimdir** ve tüm sürümlerde monoton olarak kötüleşmektedir. Denklem `−0.33*(ANA+DCC+NOP+NOM+DSC)` bileşenine büyük ağırlık verdiğinden `DSC` (144 → 184, +%27.8) ve `NOM` (9.08 → 9.58) artışı bu skoru aşağı çekmektedir.

---

## 2. Bakım Yapılabilirlik Analizi

### Understandability (Anlaşılabilirlik) — Kötüleşiyor

```
v1.14.1: −53.16  →  v1.22.2: −66.67   (Δ = −13.51, %19 gerileme)
```

Denklem: `−0.33*(ANA + DCC + NOP + NOM + DSC) + 0.33*(DAM + CAM)`

- `DSC`: 144 → 184 (+%27.8) — sınıf sayısı artıyor, ceza terimi büyüyor.
- `NOM`: 9.08 → 9.58 (+%5.5) — ortalama metot sayısı artıyor.
- `CAM`: 0.363 → 0.300 (−%17.4) — cohesion düşüyor, pozitif terim küçülüyor.

Sonuç: Her yeni sürümde kodu anlama maliyeti artmaktadır.

### Flexibility (Esneklik) — Sınırlı İyileşme

```
v1.14.1: 2.24  →  v1.22.2: 2.33   (+%4.2)
```

`MOA` (0.417 → 0.489, +%17.3) kompozisyon oranının artması esnekliğe katkı sağlıyor. Ancak `DCC` (3.25 → 3.38) ceza bileşeni de artıyor; iki etki birbirini kısmen götürmektedir.

### Coupling/Cohesion Dengesi — Alarm Verici

| Metrik | v1.14.1 | v1.22.2 | Yön |
|---|---|---|---|
| `DCC` (coupling) | 3.250 | 3.380 | ↑ kötü |
| `CAM` (cohesion) | 0.363 | 0.300 | ↓ kötü |
| `CBO` (CK) | 3.250 | 3.380 | ↑ kötü |
| `LCOM` (CK) | 126.2 | 148.7 | ↑ kötü |

**Coupling artar, cohesion düşer** — bu kombinasyon bakım maliyetini ikiye katlar: değişiklik yayılımı artar, sınıfların tek sorumluluğu zayıflar.

---

## 3. Teknik Borç Tahmini

Aşağıdaki metrik trendler teknik borç birikimini işaret etmektedir:

### 3.1 Artan Coupling (`DCC` / `CBO`)

```
DCC:  3.250 (v1.14.1) → 3.380 (v1.22.2)  (+%4.1)
CBO:  3.250 (v1.14.1) → 3.380 (v1.22.2)  (+%4.1)
```

Her sınıf ortalama 3.38 farklı sınıfa bağımlı. Bu oran küçük görünse de `DSC`=184 ile çarpıldığında sistemde ~620 bağımlılık kenarı oluşuyor. Değişim yayılımı ve kırılganlık artar.

### 3.2 Düşen Cohesion (`CAM` / `LCOM`)

```
CAM:   0.363 → 0.300  (−%17.4)
LCOM:  126.2 → 148.7  (+%17.8)
```

Her iki metrik aynı yönde hareket ediyor: sınıflar giderek daha az odaklı hale geliyor. `LCOM` 148.7 ile çok yüksek bir seviyededir; bu değer sınıfların birden fazla sorumluluğu taşıdığını gösterir (God Object riski).

### 3.3 Artan Karmaşıklık (`WMC` / `NOM`)

```
WMC_mean:  18.03 → 19.22  (+%6.6)
NOM_mean:   9.08 →  9.58  (+%5.5)
RFC_mean:  18.96 → 20.42  (+%7.7)
```

Sınıf başına düşen metot ağırlıklı karmaşıklığı (%6.6) ve yanıt kümesi (%7.7) artıyor. Test edilebilirlik ve hata ayıklama maliyeti yükseliyor.

### 3.4 Düşen Soyutlama (`ANA`)

```
ANA:  0.750 (v1.14.1) → 0.707 (v1.22.2)  (−%5.7)
```

Soyut sınıf oranı azalıyor. Somutlaşma, miras hiyerarşisinin düzleştiğine veya yeni sınıfların soyut tasarım olmadan eklendiğine işaret eder.

### 3.5 Düşen Kalıtım Kullanımı (`DIT_mean`)

```
DIT_mean:  0.750 → 0.707  (−%5.7)
NOC_mean:  0.556 → 0.533  (−%4.1)
```

Ortalama kalıtım derinliği düşüyor; yeni sınıflar hiyerarşiye entegre edilmek yerine bağımsız ekleniyor olabilir.

---

## 4. Refactoring Önerileri

### Öneri 1 — God Object Bölünmesi (`LCOM` → 148.7)

**Kanıt:** `LCOM_mean` 126.2'den 148.7'ye çıktı (+%17.8). `CAM` 0.363'ten 0.300'e düştü.  
**Eylem:** `LCOM > 200` olan sınıfları tespit edip sorumluluk ekseninde böl (Single Responsibility). Öncelikli adaylar parser, cleaner ve selector modülleridir.

### Öneri 2 — Coupling Azaltma: Arayüz Katmanı (`DCC` → 3.38)

**Kanıt:** `DCC` 3.25 → 3.38; `CBO` aynı oranda arttı.  
**Eylem:** Somut bağımlılıkları interface/abstract class arkasına çek. Özellikle `TreeBuilder` ve `Parser` bileşenleri arasındaki doğrudan bağları Facade veya Strategy örüntüsü ile kır.

### Öneri 3 — Soyut Katman Güçlendirme (`ANA` → 0.707)

**Kanıt:** `ANA` 0.750'den 0.707'ye düştü (−%5.7); yeni eklenen sınıflar soyutlama hiyerarşisi dışında.  
**Eylem:** Yeni eklenen somut sınıflar için üst soyut sınıf veya interface tanımla. `NOH` 12 → 13 olumlu ama yeterli değil; `ANA` artışı hedeflenmeli.

### Öneri 4 — Metot Karmaşıklığı Azaltma (`WMC` → 19.22)

**Kanıt:** `WMC_mean` 18.03 → 19.22 (+%6.6); `RFC_mean` 18.96 → 20.42 (+%7.7).  
**Eylem:** `WMC > 30` olan sınıflarda Extract Method refactoring uygula. Özellikle `Jsoup`, `Parser` ve `Cleaner` sınıfları potansiyel hedeflerdir. Her metot tek bir işi yapmalı.

### Öneri 5 — Composition over Inheritance Dengesini Koru (`MOA` / `MFA`)

**Kanıt:** `MOA` 0.417 → 0.489 (+%17.3) — kompozisyon artıyor; `MFA` 0.305 → 0.358 (+%17.4) — kalıtım da artıyor; ikisi paralel büyüyor.  
**Eylem:** Yeni özellikler için miras yerine composition tercih edilip edilmediğini gözden geçir. `MFA` artışı derinleşen hiyerarşiyi ve potansiyel fragile base class riskini işaret edebilir.

---

## 5. Mimari Kalite Yorumu

### Boyut Büyümesi ve Erozyon Belirtileri

```
DSC:  144 → 184  (+%27.8)   — 11 sürümde 40 yeni sınıf
NOH:  12  → 13   (+%8.3)    — hiyerarşi hafif genişledi
```

Sistem %27.8 büyürken hiyerarşi yalnızca %8.3 büyüdü. Bu makas, yeni sınıfların mimari yapıya **entegre edilmeden** eklendiğine işaret eder. Mimari erozyon için üç somut kanıt:

| Belirti | Metrik | Trend |
|---|---|---|
| Cohesion bozulması | `CAM`: 0.363 → 0.300 | ↓ %17.4 |
| Coupling artışı | `DCC`: 3.25 → 3.38 | ↑ %4.1 |
| Soyutlama seyrelmesi | `ANA`: 0.750 → 0.707 | ↓ %5.7 |

### Olumlu Mimari Sinyaller

- `MOA` (0.417 → 0.489): Kompozisyon kullanımı artıyor — doğru yön.
- `MFA` (0.305 → 0.358): Kalıtımdan yararlanma artıyor — ölçülü kabul edilebilir.
- `NOP` (5.24 → 5.47): Polimorfizm kullanımı artıyor — genişletilebilirliği destekler.

### Sonuç

jsoup, açık kaynak bir kütüphane olarak **kabul edilebilir bir teknik borç düzeyinde** gelişmektedir. Reusability ve Functionality iyileşmeleri gerçek işlevsel genişlemeyi yansıtırken, `Understandability`'nin monoton kötüleşmesi (%19) ve `CAM`/`LCOM` çiftinin olumsuz trendi **uzun vadeli bakım riskini** artırmaktadır. Mimari erozyon henüz kritik değil, ancak `DSC` büyümesi mevcut hızda devam ederse `Understandability` skoru v1.25+ bandında ciddi bir eşiği aşabilir.

---

*Analiz: QMOOD (Bansiya & Davis, 2002) denklemleri ve verilen ham metrikler esas alınarak üretilmiştir.*
