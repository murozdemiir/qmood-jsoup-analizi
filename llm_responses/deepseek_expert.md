# jsoup Sürümleri QMOOD Tabanlı Kalite Değerlendirme Raporu

## 1. Genel Kalite Değerlendirmesi
Sürümler boyunca kalite niteliklerinde **karma bir eğilim** gözlenmektedir.  
Bazı nitelikler belirgin biçimde iyileşirken, bazıları ciddi şekilde kötüleşmiştir.

| Nitelik | v1.14.1 | v1.22.2 | Değişim (%) | Yorum |
|---------|---------|---------|-------------|-------|
| **Reusability** | 73.9693 | 93.9583 | **+27.0** | Büyük artış; ancak kısmen DSC (boyut) büyümesinin yapay etkisi olabilir. |
| **Functionality** | 36.7011 | 45.7793 | **+24.7** | Sürekli artış, işlevsellik algısını yükseltiyor. |
| **Effectiveness** | 1.5181 | 1.5653 | **+3.1** | Ilımlı artış, genel etkinlikte yavaş iyileşme. |
| **Extendibility** | 1.5240 | 1.5756 | **+3.4** | Dalgalı seyir, son tahlilde az da olsa pozitif. |
| **Flexibility** | 2.2364 | 2.3346 | **+4.4** | Çok düşük seviyede (mutlak değer) ve neredeyse durağan. |
| **Understandability** | -53.1587 | -66.6680 | **-25.4 (düşüş)** | Negatif yönde ciddi bozulma. Kodun anlaşılması zorlaşıyor. |

**Kanıt:** Normalize edilmiş verilerde (taban sürüm 1.0) Reusability 1.0925’e ulaşırken, Understandability –1.1914’e gerilemiştir. Reusability ve Functionality artışları olumlu, fakat Understandability’deki bozulma, bakım riskini büyütmektedir.

## 2. Bakım Yapılabilirlik (Maintainability) Analizi
Bakım yapılabilirlik; Understandability, Flexibility, coupling (DCC) ve cohesion (CAM) birlikte değerlendirildiğinde **zorlaşmıştır**.

- **Understandability** sürekli kötüleşti: –53.16 → –66.67 (**%25 bozulma**).  
- **DCC (coupling)** 3.25 → 3.38 (**%4 artış**): bağımlılıklar sıkılaşıyor.  
- **CAM (cohesion)** 0.3633 → 0.3004 (**%17.3 düşüş**): sınıfların iç bütünlüğü azalıyor.  
- **Flexibility** (2.24 → 2.33) düşük mutlak değerde seyrediyor ve büyük iyileşme göstermiyor; bu da adaptasyonu zorlaştırıyor.  

**Sayısal kanıt:** LCOM ortalaması 126.2’den 148.7’ye (**%17.8**) yükselerek zayıf cohesion’ı doğruluyor. WMC (karmaşıklık) 18.03 → 19.22 (**%6.5 artış**) ve DAM (kapsülleme) 0.876 → 0.806 (**%8 düşüş**) bakım maliyetini daha da artırıyor.  
Birleşik etki: Kodun anlaşılması ve değiştirilmesi giderek zorlaşmış, bakım maliyeti büyümüştür.

## 3. Teknik Borç (Technical Debt) Tahmini
Aşağıdaki metrik eğilimleri **teknik borç birikimine** işaret etmektedir:

| Metrik | v1.14.1 | v1.22.2 | Teknik Borç Göstergesi |
|--------|---------|---------|------------------------|
| **DCC** (coupling) | 3.25 | 3.38 | Bağımlılık artışı, değişiklik yayılımını ve entegrasyon riskini büyütür. |
| **CAM** (cohesion) | 0.363 | 0.300 | Düşük cohesion, sınıfların birden çok sorumluluk taşıdığını ve ayrıştırılması gerektiğini gösterir. |
| **LCOM** | 126.2 | 148.7 | Yöntem düzeyinde uyumsuzluk arttı; sınıflar giderek dağınıklaşıyor. |
| **WMC** (ağırlıklı yöntem sayısı) | 18.03 | 19.22 | Sınıf başına karmaşıklık artıyor. |
| **DAM** (kapsülleme) | 0.876 | 0.806 | Erişim kontrolünün zayıflaması, modüller arası istemsiz bağ oluşturuyor. |
| **NOM** (yöntem sayısı) | 9.08 | 9.58 | Sınıf sorumluluklarının büyüdüğüne işaret. |

Bu göstergelerin tamamı **birikimli olarak negatif yönlüdür**; yazılım büyüdükçe yapısal kalite gerilemektedir. Özellikle CAM’daki %17’lik düşüş ve LCOM’daki %18’lik artış, acil refactoring ihtiyacını ortaya koyar.

## 4. Refactoring Önerileri
Sayısal metriklerin hedef değerlere çekilmesi için somut, metrik-temelli öneriler:

1. **Cohesion’ı Artırmak (CAM ↑, LCOM ↓)**  
   - Mevcut: CAM 0.30 (çok düşük), LCOM 148.7.  
   - Eylem: Büyük LCOM’lu sınıfları belirleyip (*LCOM > 200 olanlar*) “Extract Class” ile ayrıştırın.  
   - Hedef: CAM’ı 0.40’ın, LCOM ortalamasını 100’ün altına çekmek.

2. **Coupling’i Azaltmak (DCC ↓, CBO ↓)**  
   - Mevcut: DCC 3.38, CBO_mean 3.38.  
   - Eylem: Yoğun bağımlılık gösteren sınıflara “Dependency Inversion” uygulayın; arayüzler üzerinden haberleşmeyi yaygınlaştırın.  
   - Hedef: DCC < 3.0, CBO < 2.5.

3. **Kapsüllemeyi Güçlendirmek (DAM ↑)**  
   - Mevcut: DAM 0.806 (yaklaşık %20’lik erişim zaafı).  
   - Eylem: Genel (public) alan/erişimcileri minimize edin; mümkünse `private`/`protected` yapın.  
   - Hedef: DAM ≥ 0.90.

4. **Karmaşıklığı Sadeleştirmek (WMC ↓, NOM ↓)**  
   - Mevcut: WMC 19.22, NOM 9.58.  
   - Eylem: Yüksek WMC’li sınıflarda uzun metotları bölün, “Extract Method” ve “Replace Conditional with Polymorphism” uygulayın.  
   - Hedef: WMC < 15, NOM < 8.

5. **Soyutlamayı Güçlendirmek (ANA ↑)**  
   - Mevcut: ANA 0.7065 (düşüş eğiliminde).  
   - Eylem: Alt sınıfların ortak davranışlarını arayüz/soyut sınıflara taşıyın; somut bağımlılıkları soyuta çevirin.  
   - Hedef: ANA ≥ 0.75.

## 5. Mimari Kalite Yorumu (Architectural Erosion)
Sistem büyüdükçe (DSC 144 → 184, **%27.8 artış**) mimari bozulma belirtileri belirgindir:

- **DSC artışı ile birlikte DCC yükselmiş**, CAM düşmüştür. Bu, büyümenin zayıf bağlaşımla (loose coupling) sağlanamadığını, aksine bağımlılıkların arttığını gösterir.  
- **ANA (soyutlama)** 0.75’ten 0.7065’e **%5.8 azalmıştır**. Daha çok sınıf eklenmesine rağmen soyutlama seviyesi gerilemiş; bu, somut bağımlılıkların çoğaldığının işaretidir.  
- **Reusability’deki artış**, denklemdeki (+0.50*DSC) terimi nedeniyle boyuttan bağımsız düşünüldüğünde tamamen pozitif bir kazanç olmayabilir. Gerçek yeniden kullanılabilirlik iyileşmesi, DCC ve CAM’daki olumsuz tablo ile sorgulanabilir.  
- **Etkinlik ve genişletilebilirlikteki ılımlı artışlar**, mimari çöküşü maskeleyebilir. Asıl yapısal göstergeler (cohesion, coupling, encapsulation) bozulmuştur.  

**Sonuç:** Proje büyüdükçe mimari erozyon başlamıştır. Anlık işlevsellik kazançları elde edilse de, teknik borç birikmekte ve gelecekteki değişikliklerin maliyeti artmaktadır. Büyümeye koşut olarak periyodik mimari temizlik ve cohesion/coupling odaklı refactoring’ler şarttır.