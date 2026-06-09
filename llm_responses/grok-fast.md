# jsoup Kütüphanesi QMOOD Tasarım Metrikleri ve Kalite Değerlendirmesi

**Analiz Tarihi:** Haziran 2026  
**Kütüphane:** jsoup (Java HTML Parser)  
**Sürümler Aralığı:** 1.14.1 → 1.22.2  
**Uzman Rolü:** Kıdemli Yazılım Mimarı & Yazılım Kalitesi Uzmanı (QMOOD & OO Metrikler)

Bu rapor, verilen QMOOD metrikleri, kalite nitelik denklemleri ve CK metrik ortalamalarına dayalı **eleştirel ve kanıt temelli** bir analiz içermektedir. Tüm yorumlar sayısal verilere bağlıdır.

## 1. Genel Kalite Değerlendirmesi

**Genel Eğilim:** Kütüphane **büyüme** gösterirken (DSC 144 → 184, +28%), **karışık** bir kalite profili sergilemektedir.

### İyileşen Nitelikler:
- **Reusability**: 73.97 → 93.96 (+27% ham, normalized 1.000 → 1.0925).  
  Ana etkenler: DSC artışı (+28%) ve CIS/NOP'daki hafif pozitif katkı. Reusability formülündeki pozitif ağırlıklı DSC ve CIS etkisi belirgindir.
- **Functionality**: 36.70 → 45.78 (+25%).  
  NOP, CIS, DSC ve NOH'taki artışlar doğrudan katkı sağlıyor.
- **Effectiveness**: 1.518 → 1.565 (+3%).  
  ANA + DAM + MOA + MFA + NOP bileşenlerinde net pozitif hareket.

### Bozulma Gösteren Nitelikler:
- **Understandability**: -53.16 → -66.67 (önemli bozulma).  
  ANA + DCC + NOP + NOM + DSC toplamındaki artış (-0.33 katsayısı) ve DAM + CAM'deki düşüş en büyük etken. Normalized değer -0.99 → -1.19.
- **Flexibility**: 2.236 → 2.335 (hafif dalgalı, net sınırlı iyileşme).  
  DAM'deki düşüş (-0.25 etkisi) ve DCC artışı negatif etki yaratıyor.
- **Extendibility**: 1.524 → 1.576 (dalgalı, zirve 1.706 sonra gerileme).  
  DCC artışı ve ANA'daki düşüş (0.6890) negatif baskı yapıyor.

**Özet:** Büyüme odaklı **fonksiyonel** ve **yeniden kullanılabilirlik** kazanımları var ancak **anlaşılabilirlik** ciddi şekilde geriliyor. Bu, tipik "büyüme maliyeti" tablosudur.

## 2. Bakım Yapılabilirlik (Maintainability) Analizi

Bakım kolaylığı, **Understandability**, **Flexibility**, **Coupling (DCC)** ve **Cohesion (CAM)** üzerinden değerlendirilmiştir.

- **Understandability** ciddi bozuldu (-53.16 → -66.67).  
  DSC (+28%), NOM (+5.5%), DCC (+3.8%) ve NOP artışı negatif ağırlıklı terimleri şişirdi. DAM (0.876 → 0.806) ve CAM (0.363 → 0.300) düşüşü de durumu kötüleştirdi.
- **Flexibility** sınırlı iyileşti (2.236 → 2.335).  
  MOA artışı (+17%) ve NOP artışı pozitif katkı sağladı ancak DAM düşüşü ve DCC artışı (3.25 → 3.38) bu kazancı sınırladı.
- **Coupling & Cohesion**: 
  - DCC: 3.25 → 3.38 (**artış** → daha sıkı bağımlılık).
  - CAM: 0.363 → 0.300 (**düşüş** → daha düşük cohesion).

**Sonuç:** Bakım yapılabilirlik **zorlaştı**. Özellikle büyük sürümlerde (1.17+), artan sınıf sayısı ve karmaşıklık, kodun anlaşılmasını ve değiştirilmesini güçleştiriyor. CK metriklerinden LCOM artışı (126 → 148) da bu görüşü destekliyor.

## 3. Teknik Borç (Technical Debt) Tahmini

Aşağıdaki metrik eğilimleri **teknik borç birikimine** işaret ediyor:

1. **CAM düşüşü** (0.3633 → 0.3004): Sınıflar arası cohesion azalıyor → metotlar daha az ilgili görev yapıyor.
2. **DAM düşüşü** (0.876 → 0.806): Kapsülleme zayıflıyor → daha fazla public/internal erişim.
3. **DCC hafif artışı** (3.25 → 3.38) + CK CBO (3.25 → 3.38): Sınıflar arası bağımlılık artıyor.
4. **WMC artışı** (18.03 → 19.22) ve **LCOM artışı** (126 → 148): Sınıf karmaşıklığı ve düşük cohesion artıyor.
5. **ANA düşüşü** (0.75 → 0.7065): Soyutlama seviyesi geriliyor → daha somut, az esnek sınıflar.

**Tahmin:** Orta-yüksek teknik borç birikimi var. Özellikle 1.16.2 sonrası ivme kazanıyor. Büyüme (DSC) ile birlikte "architectural erosion" riski artıyor.

## 4. Refactoring Önerileri (Metrik Temelli)

1. **Cohesion Odaklı Refactoring (CAM & LCOM)**:  
   Düşük CAM'li sınıfları tespit edip, sorumlulukları ayırın veya Extract Class/Extract Interface uygulayın. Hedef: CAM > 0.35 seviyesine çıkarmak.

2. **Kapsülleme İyileştirmesi (DAM)**:  
   Erişim belirleyicileri gözden geçirin. Özellikle veri taşıyıcı sınıflarda private/protected kullanımı artırın. Hedef: DAM > 0.85.

3. **Coupling Azaltma (DCC & CBO)**:  
   Yüksek DCC'li sınıflarda Dependency Inversion Principle ve Interface Segregation uygulayın. Facade veya Mediator pattern'leri değerlendirin.

4. **Soyutlama ve Hiyerarşi Temizliği (ANA & MFA)**:  
   Gereksiz kalıtım zincirlerini (MFA artarken ANA düşüyor) düzeltin. Composition over Inheritance prensibini daha agresif uygulayın (MOA zaten artıyor, bunu destekleyin).

5. **Modülerlik Artırma**:  
   Büyük paket/sınıf gruplarını (DSC 184) alt-modüllere ayırın. Bu, Understandability ve Flexibility'yi doğrudan iyileştirecektir.

## 5. Mimari Kalite Yorumu (Architectural Erosion)

DSC'nin istikrarlı artışı (144 → 184) ile birlikte:
- ANA düşüşü ve DAM düşüşü → mimari bozulma (erosion) belirtileri mevcut.
- NOH'un 12 → 13'e çıkması hiyerarşide kontrollü büyüme gösterse de, CAM ve Understandability'deki gerileme "organik büyüme" yerine "rastgele genişleme" izlenimi veriyor.
- Pozitif taraf: MOA ve Reusability artışı, bazı kompozisyon iyileştirmelerinin yapıldığını gösteriyor.

**Genel Mimari Durum:** jsoup hala sağlam bir kütüphane ancak **sürdürülebilir büyüme** için proaktif refactoring şart. Mevcut eğilim devam ederse 1.25+ sürümlerde bakım maliyeti belirgin şekilde artacaktır.

---

**Sonuç ve Tavsiye:**  
jsoup'un **fonksiyonel** gücü artıyor ancak **iç kalite** (maintainability, understandability) geriliyor. Düzenli metrik odaklı refactoring döngüleri (örneğin her 3-4 minor sürümde) önerilir.

**Referans:** QMOOD (Bansiya & Davis, 2002) ve CK Metrikleri.