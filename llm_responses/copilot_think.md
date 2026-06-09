### Genel Notlar
**ROL:** Kıdemli yazılım mimarı / yazılım kalitesi uzmanı.  
Aşağıdaki değerlendirme yalnızca sağladığınız sayısal verilere dayanır; dış kaynak veya ek analiz kullanılmadı. Her iddia ilgili metrik değişimiyle **sayısal kanıt** içerir.

---

### 1. Genel kalite eğilimi (sürümler boyunca)
**Kısa özet:** Bazı kalite nitelikleri (Reusability, Functionality, Extendibility, Effectiveness) **artış** gösterirken; **Understandability** belirgin şekilde **bozulmuş**, **Flexibility** ise hafif dalgalanma/ılımlı artış gösteriyor.

**Sayısal kanıt (başlangıç → son):**
- **Reusability:** 73.9693 → 93.9583 (**+19.99**, ≈**+27.0%**).  
  *Kaynak:* Veri2.
- **Functionality:** 36.7011 → 45.7793 (**+9.0782**, ≈**+24.7%**).  
- **Understandability:** -53.1587 → -66.6680 (**-13.5093**, ≈**-25.4%** kötüleşme).  
- **Flexibility:** 2.2364 → 2.3346 (**+0.0982**, ≈**+4.4%**).  
- **Extendibility:** 1.5240 → 1.5756 (**+0.0516**, ≈**+3.4%**).  
- **Effectiveness:** 1.5181 → 1.5653 (**+0.0472**, ≈**+3.1%**).

**Nedenler (formüller ve metrik değişimleriyle):**
- **Reusability** formülünde *+0.50·DSC* ve *-0.25·DCC* ve *+0.25·CAM* ve *+0.50·CIS* var.  
  - **DSC** (boyut) **144 → 184** (+40) büyük artış; bu, Reusability’ye pozitif katkı sağlar (0.5 katsayıyla).  
  - **CAM** (cohesion) **0.3633 → 0.3004** (azalma) olumsuz etki yapmış olsa da DSC artışı baskın olmuş; ayrıca **CIS** (mesajlaşma) **5.3819 → 5.4565** hafif artış katkı sağlamış.  
  - Sonuç: Reusability arttı ama **nedeninin büyük ölçüde kod tabanının büyümesi (DSC)** olduğunu gösterir; bu artış “gerçek kalite” artışı değil, boyut kaynaklı etki olabilir.
- **Understandability** formülü: \(-0.33*(ANA+DCC+NOP+NOM+DSC) + 0.33*(DAM+CAM)\).  
  - **DSC** ve **DCC** ve **NOM** artışı baskın: **DSC +40**, **DCC 3.25 → 3.3804 (+0.1304)**, **NOM 9.0833 → 9.5761 (+0.4928)**.  
  - **CAM** düştü (0.3633 → 0.3004) ve **DAM** hafif düştü (0.8760 → 0.8057); pozitif terimler zayıfladı.  
  - Net etki: Understandability ciddi şekilde düştü; yani kodun **anlaşılması zorlaştı**.
- **Functionality** artışı (≈+24.7%) büyük ölçüde **NOP, CIS, DSC, NOH** gibi pozitif katkı yapan metriklerin artışından kaynaklanıyor (ör. **NOP** 5.2431 → 5.4674; **CIS** 5.3819 → 5.4565; **DSC** artışı).
- **Flexibility** formülünde *+0.25·DAM -0.25·DCC +0.50·MOA +0.50·NOP*.  
  - **DAM** azaldı (0.8760 → 0.8057) olumsuz; **DCC** hafif arttı (olumsuz); ama **MOA** (kompozisyon) **0.4167 → 0.4891** ve **NOP** arttı; net küçük pozitif değişim görüldü.

---

### 2. Bakım yapılabilirlik (Maintainability) analizi
**Kısa sonuç:** **Bakım zorluğu artıyor.** Özellikle *Understandability* düşüşü, artan coupling ve artan sınıf/metot karmaşıklıkları bakım maliyetini yükseltir.

**Kanıt ve açıklama:**
- **Understandability** ciddi düşüş: -53.16 → -66.67 (bkz. üst). Bu doğrudan bakım maliyetini artırır (daha uzun öğrenme süresi, hata bulma zorlaşması).
- **Coupling (DCC)**: 3.2500 → 3.3804 (**+0.1304**, ≈**+4.0%**). Artan coupling, değişikliklerin yayılma riskini yükseltir; bakım sırasında regresyon olasılığı artar.
- **Cohesion (CAM)**: 0.3633 → 0.3004 (**-0.0629**, ≈**-17.3%**). Azalan cohesion, sınıfların tek sorumluluk ilkesinden uzaklaştığını gösterir; bu da refactor/bugfix sırasında daha fazla yan etki demektir.
- **Complexity göstergeleri:**  
  - **WMC_mean** 18.03 → 19.22 (**+1.19**, ≈**+6.6%**) — metot karmaşıklığı arttı.  
  - **LCOM_mean** 126.20 → 148.70 (**+22.49**, ≈**+17.8%**) — sınıf içi bağlılık bozulmuş; sınıflar daha parçalanmış/uyumsuz hale gelmiş.  
  - **NOM_mean** 9.0833 → 9.5761 (**+0.4928**, ≈**+5.4%**) — sınıf başına metot sayısı arttı; daha fazla yüzey alan, daha fazla test/inceleme gerektirir.
- **Sonuç:** Understandability ve cohesion/coupling trendleri bakımın zorlaştığını, hata düzeltme ve yeni özellik eklemenin maliyetinin arttığını gösteriyor.

---

### 3. Teknik borç (Technical debt) göstergeleri
**Öne çıkan riskler ve nedenleri:**

1. **Artan coupling (DCC)** — değişiklik yayılımı riski: DCC 3.25 → 3.3804. Küçük ama sürekli artış, modüller arası sıkı bağların arttığını gösterir; bu, kodun yeniden düzenlenmesini ve güvenli değişiklik yapmayı zorlaştırır.
2. **Artan sınıf karmaşıklığı ve düşük cohesion:**  
   - **LCOM_mean** +17.8% ve **CAM** -17.3%: sınıflar daha az uyumlu, tek sorumluluk ihlali olasılığı artmış. Bu tip sorunlar teknik borcun klasik kaynağıdır (anlaşılması zor, yeniden kullanılabilir olmayan sınıflar).
3. **Büyüyen kod tabanı (DSC)**: 144 → 184 (+27.8%). Kod büyümesi tek başına borç değil ama **DSC** artışıyla birlikte **WMC**, **LCOM**, **DCC** artıyorsa bu büyüme kontrolsüzdür ve bakım yükü getirir.
4. **Artan RFC ve LCOM** (RFC_mean 18.96 → 20.42; LCOM yukarıda): daha fazla davranış yüzeyi ve düşük içsel bağlılık, test kapsamı ve regresyon riskini artırır.
5. **Azalan CAM ve hafif azalan DAM**: kapsülleme ve cohesion zayıflaması, kodun modülerliğini bozar; bu da gelecekteki değişiklikleri pahalı hale getirir.

**Tahmin:** Mevcut eğilimler devam ederse orta vadede (birkaç sürüm) teknik borç birikimi belirgin şekilde artacaktır; özellikle refactor yapılmazsa hata oranı ve geliştirme süresi artar.

---

### 4. Metrik-temelli refactoring önerileri (3–5 somut öneri)
Her öneri **hangi metrikleri** hedefler ve **beklenen etkisi** belirtilmiştir.

1. **Sınıf parçalama (Extract Class / SRP uygulama)**  
   - **Hedef metrikler:** LCOM (düşürme), CAM (yükseltme), WMC (düşürme), NOM (düşme)  
   - **Neden:** LCOM_mean 126.2 → 148.7 ve CAM 0.3633 → 0.3004 gösteriyor ki sınıflar birden fazla sorumluluk taşıyor.  
   - **Beklenen etki:** LCOM azalır, CAM artar; Understandability ve Maintainability iyileşir.

2. **Bağımlılıkların gevşetilmesi (Introduce Interfaces / Dependency Injection)**  
   - **Hedef metrikler:** DCC (düşürme), RFC (düşürme), Effectiveness/Extendibility pozitif etki  
   - **Neden:** DCC artışı (3.25 → 3.38) coupling sorununu işaret ediyor.  
   - **Beklenen etki:** Modüller arası bağımlılık azalır; değişikliklerin yayılma riski düşer; Extendibility artar.

3. **Büyük sınıfların modülerleştirilmesi (Modularization / Package refactor)**  
   - **Hedef metrikler:** DSC (kontrollü yönetim), NOH/NOA, DCC (azalma), CAM (artış)  
   - **Neden:** DSC 144 → 184; kod tabanı büyüyor. Büyüme paket sınırlarıyla kontrol altına alınmalı.  
   - **Beklenen etki:** Daha küçük, daha odaklı modüller; bağımlılıklar daha görünür; mimari sınırlar netleşir.

4. **Metot karmaşıklığını azaltma (Extract Method, limit WMC)**  
   - **Hedef metrikler:** WMC_mean (düşürme), NOM_mean (düşürme), Understandability iyileşmesi  
   - **Neden:** WMC 18.03 → 19.22 ve NOM artışı, metotların karmaşıklaştığını gösterir.  
   - **Beklenen etki:** Daha küçük metotlar, daha kolay test edilebilirlik, daha düşük hata riski.

5. **Cohesion artırıcı düzenlemeler (cohesion-driven refactor: move method/field)**  
   - **Hedef metrikler:** CAM (yükseltme), LCOM (düşürme)  
   - **Neden:** CAM düşüşü ve LCOM artışı sınıf içi uyumsuzluğu gösteriyor.  
   - **Beklenen etki:** Sınıfların tek bir sorumluluğa odaklanması, daha iyi yeniden kullanılabilirlik ve anlaşılabilirlik.

---

### 5. Mimari kalite yorumu (architectural erosion riski)
**Durum:** **Orta düzeyde mimari erozyon riski** var; şu işaretler bunu destekliyor:

- **Kod tabanı büyüyor (DSC +27.8%)** ve aynı zamanda **DCC** artıyor: büyüme paket sınırları ve bağımlılık yönetimi olmadan gerçekleşmiş. Bu, zamanla modüller arası çapraz bağımlılıkların artmasına yol açar (mimari sınırların bulanıklaşması).
- **RFC_mean** ve **WMC_mean** artışı (RFC 18.96 → 20.42; WMC 18.03 → 19.22) uygulama davranış yüzeyinin genişlediğini gösterir; bu da bileşenlerin daha fazla sorumluluk alması ve sınırların aşınmasıyla ilişkilidir.
- **LCOM_mean** artışı (126.2 → 148.7) sınıfların iç tutarlılığının bozulduğunu gösterir; mimari katmanlarda tek sorumluluk ilkesinin ihlal edildiğine işaret edebilir.

**Yorum:** Mevcut eğilimler mimari erozyonun erken belirtilerini gösteriyor — henüz çöküntü değil, fakat **kontrolsüz büyüme + artan coupling + azalan cohesion** devam ederse mimari borç hızla artar. Erken müdahale (modülerleştirme, bağımlılık yönetimi, sınırların netleştirilmesi) önerilir.

---

### Kapanış — Özet (özlü)
- **Olumlu:** Reusability ve Functionality sayısal olarak arttı; bazı yetenekler (özellikle yeniden kullanım ve fonksiyonel kapsam) genişliyor.  
- **Olumsuz:** **Understandability** belirgin şekilde bozuldu; bu, bakım maliyetini ve hata riskini artırır. **Cohesion** düşüyor, **coupling** ve **complexity** artıyor — bunlar teknik borç sinyalleri.  
- **Eylem önerisi (önceliklendirme):** 1) LCOM/CAM odaklı sınıf parçalama; 2) DCC azaltma için arayüzler/DI; 3) WMC azaltma (extract method); 4) modülerleştirme ile DSC büyümesini kontrol altına alma. Her biri yukarıda belirtilen metriklerde doğrudan iyileşme hedefler.

---

**Not:** Bazı metrik değişimleri (ör. Reusability artışı) **DSC gibi boyut etkilerinden** kaynaklanıyor olabilir; yani sayısal artış her zaman gerçek kalite artışı anlamına gelmez. Belirsizlikler varsa (ör. metriklerin nasıl hesaplandığı, ölçüm aralığı, outlier sınıflar) daha derin sınıf/ paket düzeyi analiz (hotspot listesi, en yüksek LCOM/WMC sınıfları) ile kanıt-temelli önceliklendirme yapılmasını öneririm.
