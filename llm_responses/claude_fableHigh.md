# jsoup (1.14.1 → 1.22.2) — QMOOD Temelli Kalite Değerlendirmesi

> **Kapsam:** 11 sürüm (1.14.1 – 1.22.2) · QMOOD tasarım metrikleri, QMOOD kalite nitelikleri ve CK metrik ortalamaları
> **Yöntem notu:** QMOOD ham denklemleri normalize edilmemiş metrikleri karıştırır; **DSC (boyut)** Reusability ve Functionality'de 0.50/0.22 ağırlıkla doğrudan yer aldığından, bu iki nitelikteki artışın önemli bölümü **boyut artefaktıdır**, gerçek tasarım iyileşmesi değildir. Yorumlar bu bilinçle yapılmıştır.

---

## 1. Genel Kalite Değerlendirmesi

**Eğilim: Boyuta bağlı nitelikler "iyileşiyor" görünürken, yapısal sağlık göstergeleri bozuluyor.**

| Nitelik | 1.14.1 | 1.22.2 | Değişim | Asıl sürücü |
|---|---:|---:|---:|---|
| Reusability | 73.97 | 93.96 | **+27.0 %** | DSC 144→184 (+27.8 %); CIS ~sabit, CAM **düştü** |
| Functionality | 36.70 | 45.78 | **+24.7 %** | Yine ağırlıklı DSC; CAM −17 % buna *rağmen* |
| Flexibility | 2.236 | 2.335 | +4.4 % | MOA 0.417→0.489 (+17 %), DAM düşüşünü telafi etti |
| Extendibility | 1.524 | 1.576 | +3.4 % (dalgalı) | MFA 0.305→0.358 (+17 %); DCC artışı kısmen sildi |
| Effectiveness | 1.518 | 1.565 | +3.1 % | ANA düşüşüne rağmen MOA+MFA artışı |
| Understandability | −53.16 | −66.67 | **−25.4 % (bozulma)** | DSC ve NOM artışı + CAM/DAM düşüşü |

**İyileşenler (gerçek, boyuttan bağımsız):**
- **MOA** 0.4167 → 0.4891 (+17.4 %): kompozisyon kullanımı arttı — Flexibility ve Effectiveness'taki mütevazı kazanımların asıl kaynağı.
- **MFA** 0.3048 → 0.3577 (+17.4 %): kalıtım yoluyla işlevsellik yeniden kullanımı arttı (özellikle 1.16.2 ve 1.21.2 sıçramaları).

**Bozulanlar (boyuttan bağımsız):**
- **CAM** 0.3633 → 0.3004 (**−17.3 %**): sınıf içi metot-parametre uyumu zayıfladı; en sert düşüş 1.15.4→1.16.2 (0.3554→0.3234).
- **DAM** 0.8760 → 0.8057 (**−8.0 %**): kapsülleme geriledi; 1.19.1→1.20.1 arası tek adımda 0.8197→0.7945.
- **ANA** 0.7500 → 0.6824 (1.20.1'de dip), sonra 0.7207'ye (1.21.2) kısmi toparlanma — soyutlama yatırımı büyümeye ayak uyduramadı, 1.21+ sürümlerinde bilinçli düzeltme izlenimi var.
- **DCC** 3.25 → 3.38 (+4.0 %): hafif ama istikrarlı bağlaşım artışı.

> **Özet yargı:** Reusability/Functionality'deki çift haneli artışlar büyük ölçüde DSC artefaktıdır. Boyut etkisinden arındırıldığında resim: kompozisyon/kalıtım kullanımı iyileşti, **cohesion ve kapsülleme belirgin geriledi**.

---

## 2. Bakım Yapılabilirlik (Maintainability) Analizi

**Sonuç: Bakım zorlaştı.**

1. **Understandability tüm sürümlerde tekdüze bozuldu:** −53.16 → −66.67 (normalize: −0.99 → −1.19). Bozulmanın bileşenleri: DSC +40 sınıf, NOM 9.08→9.58 (+5.4 %), CAM −17.3 %, DAM −8.0 %. Yani sistem hem büyüdü hem de birim sınıf düzeyinde daha az tutarlı hale geldi.
2. **Cohesion iki bağımsız ölçümle teyitli düşüşte:** QMOOD-CAM −17.3 % ve CK-**LCOM 126.2 → 148.7 (+17.8 %)**. LCOM zirvesi 1.20.1'de (150.9). Düşük cohesion, değişikliklerin sınıf içinde öngörülemeyen yan etkiler üretme riskini artırır.
3. **Coupling hafifçe yükseldi:** DCC/CBO 3.25→3.38 (+4 %), **RFC 18.96→20.42 (+7.7 %)**. RFC artışı, bir sınıfı anlamak için izlenmesi gereken metot kümesinin büyüdüğünü gösterir.
4. **Flexibility'nin +4.4 %'lük kazanımı** (MOA sayesinde) bakım açısından olumlu tek sinyaldir; ancak CAM/DAM/LCOM'daki bozulmayı dengeleyecek büyüklükte değildir.

**Belirsizlik:** LCOM'un mutlak değeri sınıf büyüklüğüne duyarlıdır; artışın bir kısmı NOM/NOA artışından kaynaklanabilir. Yine de CAM'in eşzamanlı düşmesi, cohesion kaybının gerçek olduğuna işaret eder.

---

## 3. Teknik Borç (Technical Debt) Tahmini

Borç birikimine işaret eden eğilimler (her biri sayısal kanıtla):

| Sinyal | Kanıt | Yorum |
|---|---|---|
| **Cohesion erozyonu** | CAM −17.3 %; LCOM +17.8 % (zirve 1.20.1: 150.9) | Sınıflar çok sorumluluk biriktiriyor → "God class" riski |
| **Kapsülleme kaybı** | DAM 0.876 → 0.806; en hızlı düşüş 1.16.2–1.20.1 bandında | Public/erişilebilir durum artışı → değişiklik dalgalanma (ripple) maliyeti |
| **Bağlaşım sürünmesi** | DCC 3.25→3.38; RFC +7.7 %; MPC 17.34→18.23 (+5.1 %) | Yavaş ama 11 sürümde kesintisiz; faiz birikiyor |
| **Soyutlama açığı (kısmen ödendi)** | ANA 0.750→0.682 (1.20.1), sonra 0.721 (1.21.2); NOH 12→9→13 | 1.21–1.22'de hiyerarşi yeniden yapılandırması borcun bir kısmını kapatmış görünüyor |
| **Karmaşıklık artışı** | WMC 18.03→19.22 (+6.6 %); NOM +5.4 % | Sınıf başına yük büyüyor, boyut artışıyla bileşik etki |

**Tahmin:** Borç **orta düzeyde ve birikmekte**; kriz seviyesinde değil (DCC artışı %4 ile sınırlı, DIT/NOC sığ ve stabil), ancak cohesion–kapsülleme eksenindeki bozulma düzeltilmezse 1.2x sürümlerinde değişiklik maliyeti doğrusal değil, bileşik artacaktır. 1.21.2'deki ANA/NOH toparlanması, ekibin borcu kısmen fark edip ödemeye başladığının olumlu işaretidir.

---

## 4. Refactoring Önerileri (metrik temelli)

1. **Extract Class / Move Method — düşük cohesion'lı sınıfları böl.**
   Gerekçe: LCOM +17.8 % (126→149), CAM −17.3 %. Hedef: LCOM'u 1.14.x bandına (≈126–135) geri çekmek. Önce LCOM'u sistem ortalamasının çok üzerinde olan sınıflardan başlanmalı.

2. **Encapsulate Field — kapsüllemeyi onar.**
   Gerekçe: DAM 0.876→0.806; özellikle 1.19.1→1.20.1 düşüşü (0.820→0.795). Public/paket-görünür alanları private yapıp erişimciler ardına alın. DAM, Flexibility (0.25 ağırlık) ve Understandability'yi (0.33) doğrudan iyileştirir.

3. **Introduce Interface / Facade — bağlaşımı kes.**
   Gerekçe: DCC +4 %, RFC +7.7 %, MPC +5.1 %. Yüksek CBO'lu sınıflar arasına arayüz katmanı koymak DCC'yi düşürür; DCC dört QMOOD niteliğinde negatif ağırlık taşıdığından kaldıraç etkisi yüksektir.

4. **Soyutlama katmanını büyümeyle ölçekle (Extract Superclass/Interface).**
   Gerekçe: DSC +27.8 % büyürken ANA 0.750→0.682'ye gerilemişti; 1.21.2'deki kısmi düzeltme (ANA 0.721, NOH 9→11→13) sürdürülmeli. Yeni eklenen somut sınıflar ortak soyutlamalar altında toplanmalı — Extendibility'de ANA ve MFA 0.50 ağırlıklıdır.

5. **Kompozisyon stratejisini koru, kalıtımı derinleştirme.**
   Gerekçe: MOA +17.4 % bu dönemin en sağlıklı eğilimi; DIT ortalaması 0.71 ile sığ kalmış (iyi). Yeni işlevsellikte composition-over-inheritance sürdürülmeli; MFA artışı izlenmeli ki derin/kırılgan hiyerarşilere dönüşmesin.

---

## 5. Mimari Kalite Yorumu — Architectural Erosion Var mı?

**Yanıt: Hafif–orta düzeyde erozyon belirtisi var; çökme yok, ama yönelim olumsuz.**

**Erozyon lehine kanıt:**
- Boyut +27.8 % (DSC 144→184) büyürken **cohesion −17.3 %** (CAM) ve **kapsülleme −8 %** (DAM): büyüme, modüler disiplinden taviz verilerek gerçekleşmiş.
- 1.14.1–1.20.1 arasında **NOH 12→9 ve ANA 0.750→0.682**: sistem büyürken hiyerarşi/soyutlama küçüldü — yeni kodun mevcut somut sınıflara "yığıldığının" klasik işareti.
- Understandability'nin **her sürümde istisnasız** kötüleşmesi (−53.2 → −66.7) erozyonun bileşik etkisini gösterir.

**Erozyon aleyhine (dengeleyici) kanıt:**
- **DCC yalnızca +4 %**: bağlaşım patlaması yok; modül sınırları büyük ölçüde korunuyor. Gerçek erozyonda CBO/DCC tipik olarak boyutla birlikte hızlanır — burada hızlanmıyor.
- **MOA +17 %**: kompozisyona kayış bilinçli bir mimari tercihtir, bozulma değil.
- **1.21.2–1.22.2 düzeltici hamlesi:** NOH 9→11→13, ANA 0.682→0.721, MFA 0.323→0.366. Bu, mimarinin pasif çürümeye bırakılmadığını, periyodik restorasyon yapıldığını gösterir.

**Nihai değerlendirme:** jsoup'ta gözlenen tablo "kontrollü büyüme altında yerel erozyon"dur: makro mimari (bağlaşım, hiyerarşi sığlığı) ayakta, ancak **sınıf-içi kalite (cohesion, kapsülleme) sistematik aşınıyor**. Öncelik, 4. bölümdeki 1. ve 2. önerilerdir; bunlar yapılmadan Reusability/Functionality'deki sayısal artışlar yanıltıcı bir iyimserlik yaratmaya devam edecektir.

---

*Not: Tüm yüzdeler 1.14.1 tabanına göredir. QMOOD ham puanları nitelikler arası karşılaştırma için uygun değildir (farklı ölçekler); yalnızca sürümler arası eğilim okunmalıdır.*
