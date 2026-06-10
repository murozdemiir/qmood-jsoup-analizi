/*
 * build_pptx.js — QMOOD + LLM projesi sunum dosyasini uretir.
 * Calistirma:  node src/build_pptx.js   (proje kokunden)
 * Cikti:       report/QMOOD_jsoup_sunum.pptx
 * Figurler:    figures/*.png (analiz pipeline'i tarafindan uretildi)
 * Not: Slayt metinleri tam Turkce karakterlidir (UTF-8).
 */
const pptxgen = require("pptxgenjs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const FIG = path.join(ROOT, "figures");

// --- Palet: Midnight Executive ---
const NAVY = "1E2761";
const ICE = "CADCFC";
const WHITE = "FFFFFF";
const INK = "1B2433";
const MUTED = "5B6678";
const GOOD = "1E8449";
const BAD = "C0392B";
const ACCENT = "3D5AAE";

const HF = "Georgia";   // baslik fontu
const BF = "Calibri";   // govde fontu

const pres = new pptxgen();
pres.defineLayout({ name: "W", width: 13.333, height: 7.5 });
pres.layout = "W";
pres.author = "QMOOD Projesi";
pres.title = "QMOOD Tabanlı Yazılım Kalitesi Analizi — jsoup";

const W = 13.333, H = 7.5;
const shadow = () => ({ type: "outer", color: "000000", blur: 7, offset: 3, angle: 135, opacity: 0.18 });

// figur en-boy oranlari (matplotlib figsize)
const AR = {
  "fig_quality_norm.png": 14 / 6,
  "fig_design_size.png": 11 / 6,
  "fig_coupling_cohesion.png": 11 / 6,
  "fig_ck_means.png": 11 / 6,
  "fig_quality_heatmap.png": 11 / 5,
  "fig_radar_first_last.png": 8 / 8,
  "fig_llm_ranking.png": 11 / 6,
  "fig_llm_qualitative.png": 12 / 8,
  "fig_llm_comparison.png": 10 / 6,
};

function fitImage(slide, file, box) {
  const ar = AR[file] || 1.6;
  let w = box.w, h = w / ar;
  if (h > box.h) { h = box.h; w = h * ar; }
  const x = box.x + (box.w - w) / 2;
  const y = box.y + (box.h - h) / 2;
  slide.addImage({ path: path.join(FIG, file), x, y, w, h, shadow: shadow() });
}

function header(slide, kicker, title) {
  slide.background = { color: WHITE };
  slide.addText(kicker.toUpperCase(), { x: 0.6, y: 0.42, w: 12, h: 0.3, fontFace: BF, fontSize: 12, color: ACCENT, bold: true, charSpacing: 2, margin: 0 });
  slide.addText(title, { x: 0.6, y: 0.72, w: 12.1, h: 0.8, fontFace: HF, fontSize: 30, color: NAVY, bold: true, margin: 0 });
}

function statCard(slide, x, y, w, value, label, color) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 1.6, fill: { color: WHITE }, line: { color: ICE, width: 1 }, rectRadius: 0.08, shadow: shadow() });
  slide.addText(value, { x, y: y + 0.18, w, h: 0.8, align: "center", fontFace: HF, fontSize: 34, color: color || NAVY, bold: true, margin: 0 });
  slide.addText(label, { x: x + 0.15, y: y + 1.0, w: w - 0.3, h: 0.5, align: "center", fontFace: BF, fontSize: 12.5, color: MUTED, margin: 0 });
}

/* ---------------- 1. KAPAK ---------------- */
let s = pres.addSlide();
s.background = { color: NAVY };
s.addShape(pres.shapes.OVAL, { x: 10.2, y: -2.0, w: 5.5, h: 5.5, fill: { color: "26306E" } });
s.addShape(pres.shapes.OVAL, { x: 11.4, y: 4.6, w: 4.2, h: 4.2, fill: { color: "26306E" } });
s.addText("YAZILIM MİMARİLERİ VE TASARIM YÖNTEMLERİ", { x: 0.8, y: 1.5, w: 11, h: 0.4, fontFace: BF, fontSize: 14, color: ICE, bold: true, charSpacing: 2, margin: 0 });
s.addText("QMOOD Tabanlı Yazılım Kalitesi Analizi\nve LLM Destekli Değerlendirme", { x: 0.8, y: 2.0, w: 11.4, h: 1.8, fontFace: HF, fontSize: 40, color: WHITE, bold: true, lineSpacingMultiple: 1.05, margin: 0 });
s.addText([
  { text: "Analiz edilen sistem:  ", options: { color: ICE } },
  { text: "jsoup (Java HTML Parser) — 11 sürüm (1.14.1 → 1.22.2)", options: { color: WHITE, bold: true } },
], { x: 0.8, y: 4.1, w: 11.4, h: 0.5, fontFace: BF, fontSize: 17, margin: 0 });
s.addText("17 LLM yapılandırması  ·  kendi yazdığımız metrik çıkarıcı  ·  6 kalite niteliği", { x: 0.8, y: 4.7, w: 11.4, h: 0.4, fontFace: BF, fontSize: 14, color: ICE, italic: true, margin: 0 });
s.addText("Grup: Murat Özdemir (255129022) · Mustafa Can Bozbuğa (255129050) · Ahmet Ateş (255129005)      Tarih: 2026-06-10", { x: 0.8, y: 6.4, w: 11.9, h: 0.4, fontFace: BF, fontSize: 12, color: ICE, margin: 0 });

/* ---------------- 2. AMAÇ & KAPSAM ---------------- */
s = pres.addSlide();
header(s, "Giriş", "Amaç ve Kapsam");
const goals = [
  ["Amaç", "jsoup'un 11 sürümünü QMOOD modeliyle analiz edip kalite evrimini ölçmek; aynı metrikleri ≥3 LLM'e verip yorum yeteneklerini kıyaslamak."],
  ["Neden jsoup?", "Tek/sürekli git geçmişi, zengin kalıtım-polimorfizm (Node→Element...), yönetilebilir boyut (~250 sınıf), düzenli sürüm yayını."],
  ["Özgünlük", "Hiçbir hazır araç yok: metrikler javalang ile kendi çözümleyicimizle çıkarıldı (yönerge: hazır sonuç kullanımı yasak)."],
];
let gy = 1.8;
goals.forEach(([h, t]) => {
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: gy, w: 0.12, h: 1.35, fill: { color: ACCENT } });
  s.addText(h, { x: 0.9, y: gy, w: 3.0, h: 1.35, fontFace: HF, fontSize: 19, color: NAVY, bold: true, valign: "middle", margin: 0 });
  s.addText(t, { x: 4.0, y: gy, w: 8.7, h: 1.35, fontFace: BF, fontSize: 15.5, color: INK, valign: "middle", margin: 0 });
  gy += 1.55;
});

/* ---------------- 3. YÖNTEM: QMOOD ---------------- */
s = pres.addSlide();
header(s, "Yöntem", "QMOOD Modeli: Metrik → Tasarım Özelliği → Kalite");
s.addText([
  { text: "Tasarım metrikleri (sistem düzeyi)\n", options: { bold: true, color: NAVY, fontSize: 16, breakLine: true } },
  { text: "DSC boyut · NOH hiyerarşi · ANA soyutlama · DAM kapsülleme · DCC coupling · CAM cohesion · MOA kompozisyon · MFA kalıtım · NOP polimorfizm · CIS mesajlaşma · NOM karmaşıklık", options: { color: INK, fontSize: 14 } },
], { x: 0.6, y: 1.75, w: 6.0, h: 2.2, fontFace: BF, valign: "top", lineSpacingMultiple: 1.15, margin: 0 });
s.addText([
  { text: "6 Kalite Niteliği\n", options: { bold: true, color: NAVY, fontSize: 16, breakLine: true } },
  { text: "Reusability · Flexibility · Understandability · Functionality · Extendibility · Effectiveness", options: { color: INK, fontSize: 14 } },
], { x: 0.6, y: 4.2, w: 6.0, h: 1.4, fontFace: BF, valign: "top", lineSpacingMultiple: 1.15, margin: 0 });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.0, y: 1.75, w: 5.7, h: 4.9, fill: { color: "F4F7FF" }, line: { color: ICE, width: 1 }, rectRadius: 0.08 });
s.addText("QMOOD Kalite Denklemleri", { x: 7.25, y: 1.95, w: 5.2, h: 0.4, fontFace: HF, fontSize: 15, color: NAVY, bold: true, margin: 0 });
s.addText([
  "Reusability   = -0.25·DCC +0.25·CAM +0.50·CIS +0.50·DSC",
  "Flexibility    =  0.25·DAM -0.25·DCC +0.50·MOA +0.50·NOP",
  "Understand.  = -0.33·(ANA+DCC+NOP+NOM+DSC)+0.33·(DAM+CAM)",
  "Functionality =  0.12·CAM +0.22·(NOP+CIS+DSC+NOH)",
  "Extendibility =  0.50·(ANA+MFA+NOP) -0.50·DCC",
  "Effectiveness =  0.20·(ANA+DAM+MOA+MFA+NOP)",
].map((t) => ({ text: t, options: { breakLine: true, paraSpaceAfter: 8 } })),
  { x: 7.25, y: 2.45, w: 5.25, h: 4.0, fontFace: "Consolas", fontSize: 11, color: INK, margin: 0 });

/* ---------------- 4. PIPELINE ---------------- */
s = pres.addSlide();
header(s, "Yöntem", "Metrik Çıkarım Pipeline'ı (kendi geliştirdiğimiz)");
const steps = [
  ["1", "fetch", "11 sürümü git archive ile indir"],
  ["2", "metrics", "javalang AST'den CK metrikleri"],
  ["3", "qmood", "Sistem düzeyi QMOOD + kalite"],
  ["4", "analyze", "CSV tabloları üret"],
  ["5", "visualize", "Grafikler (figures/)"],
  ["6", "llm", "Prompt + karşılaştırma"],
];
const sw = 1.95, gap = 0.13;
steps.forEach(([n, t, d], i) => {
  const x = 0.6 + i * (sw + gap);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.4, w: sw, h: 2.4, fill: { color: i % 2 ? "F4F7FF" : WHITE }, line: { color: ICE, width: 1 }, rectRadius: 0.08, shadow: shadow() });
  s.addShape(pres.shapes.OVAL, { x: x + sw / 2 - 0.32, y: 2.6, w: 0.64, h: 0.64, fill: { color: NAVY } });
  s.addText(n, { x: x + sw / 2 - 0.32, y: 2.6, w: 0.64, h: 0.64, align: "center", valign: "middle", fontFace: HF, fontSize: 22, color: WHITE, bold: true, margin: 0 });
  s.addText(t, { x, y: 3.4, w: sw, h: 0.5, align: "center", fontFace: BF, fontSize: 16, color: NAVY, bold: true, margin: 0 });
  s.addText(d, { x: x + 0.1, y: 3.9, w: sw - 0.2, h: 0.85, align: "center", fontFace: BF, fontSize: 11.5, color: MUTED, valign: "top", margin: 0 });
});
s.addText("144 → 184 sınıf  ·  73 → 91 dosya  ·  çözümlenemeyen dosya = 0", { x: 0.6, y: 5.6, w: 12.1, h: 0.5, align: "center", fontFace: BF, fontSize: 15, color: INK, italic: true, margin: 0 });

/* ---------------- 5. VERİ SETİ / BÜYÜME ---------------- */
s = pres.addSlide();
header(s, "Analiz Süreci", "Veri Seti: Tasarım Boyutu Büyümesi");
fitImage(s, "fig_design_size.png", { x: 0.5, y: 1.7, w: 8.3, h: 5.3 });
statCard(s, 9.1, 1.9, 3.6, "+27.8%", "DSC (sınıf sayısı) büyümesi\n144 → 184", NAVY);
statCard(s, 9.1, 3.7, 3.6, "11", "analiz edilen sürüm\n1.14.1 → 1.22.2", ACCENT);
statCard(s, 9.1, 5.5, 3.6, "+5.4%", "NOM (ort. metot/sınıf)\n9.08 → 9.58", NAVY);

/* ---------------- 6. SONUÇ: KALİTE EVRİMİ ---------------- */
s = pres.addSlide();
header(s, "Sonuçlar", "QMOOD Kalite Niteliklerinin Evrimi");
fitImage(s, "fig_quality_norm.png", { x: 0.5, y: 1.7, w: 12.3, h: 4.6 });
s.addText([
  { text: "Pozitif nitelikler artıyor (Reusability +%9, Flexibility +%8); ", options: { color: GOOD, bold: true } },
  { text: "Understandability tek yönlü kötüleşiyor (-%20). ", options: { color: BAD, bold: true } },
  { text: "Çift yönlü evrim.", options: { color: INK } },
], { x: 0.6, y: 6.45, w: 12.1, h: 0.6, fontFace: BF, fontSize: 14.5, align: "center", margin: 0 });

/* ---------------- 7. COUPLING vs COHESION ---------------- */
s = pres.addSlide();
header(s, "Sonuçlar", "Coupling ↑ vs Cohesion ↓ — Teknik Borç Makası");
fitImage(s, "fig_coupling_cohesion.png", { x: 0.4, y: 1.7, w: 8.2, h: 5.3 });
statCard(s, 9.0, 2.0, 3.7, "-17.3%", "CAM (cohesion) düşüşü", BAD);
statCard(s, 9.0, 3.8, 3.7, "+17.8%", "LCOM (CK) artışı — çapraz doğrulama", BAD);
statCard(s, 9.0, 5.6, 3.7, "+4.0%", "DCC/CBO (coupling) artışı", BAD);

/* ---------------- 8. TEKNİK BORÇ ---------------- */
s = pres.addSlide();
header(s, "Tartışma", "Teknik Borç: Kontrollü Birikim");
statCard(s, 0.6, 1.9, 2.85, "-17.3%", "CAM cohesion", BAD);
statCard(s, 3.65, 1.9, 2.85, "-8.0%", "DAM kapsülleme", BAD);
statCard(s, 6.7, 1.9, 2.85, "+6.5%", "WMC karmaşıklık", BAD);
statCard(s, 9.75, 1.9, 2.95, "+17.4%", "MOA + MFA (olumlu)", GOOD);
s.addText([
  { text: "Cohesion erozyonu en güçlü sinyal:  ", options: { bold: true, color: NAVY } },
  { text: "CAM ve LCOM iki bağımsız metrik aynı yöne işaret ediyor.  ", options: { color: INK } },
  { text: "Ancak ", options: { color: INK } },
  { text: "MOA/MFA artışı (+%17) bilinçli kompozisyon/kalıtım iyileştirmesi", options: { bold: true, color: GOOD } },
  { text: " — yıkıcı değil, kontrollü bir borç tablosu.", options: { color: INK } },
], { x: 0.7, y: 4.0, w: 12.0, h: 1.2, fontFace: BF, fontSize: 16, valign: "top", lineSpacingMultiple: 1.2, margin: 0 });
s.addText([
  { text: "Kırılma noktası ≈ 1.20.1 ", options: { bold: true, color: NAVY } },
  { text: "(ANA/DAM dip, LCOM zirve) → ", options: { color: INK } },
  { text: "1.21.2+ kısmi toparlanma", options: { bold: true, color: GOOD } },
  { text: " (ANA, MFA, NOH yukarı): ekip borcu fark edip ödemeye başlamış.", options: { color: INK } },
], { x: 0.7, y: 5.3, w: 12.0, h: 1.2, fontFace: BF, fontSize: 16, valign: "top", lineSpacingMultiple: 1.2, margin: 0 });

/* ---------------- 9. CK METRİK EVRİMİ ---------------- */
s = pres.addSlide();
header(s, "Sonuçlar", "CK Metrik Ortalamalarının Evrimi");
fitImage(s, "fig_ck_means.png", { x: 0.5, y: 1.7, w: 8.3, h: 5.3 });
s.addText("CK metrik değişimi (1.14.1 → 1.22.2)", { x: 9.0, y: 1.85, w: 3.8, h: 0.4, fontFace: HF, fontSize: 15, color: NAVY, bold: true, margin: 0 });
s.addTable([
  [{ text: "Metrik", options: { bold: true, color: WHITE, fill: { color: NAVY } } }, { text: "Δ%", options: { bold: true, color: WHITE, fill: { color: NAVY } } }],
  ["WMC", "+6.5"], ["CBO", "+4.0"], ["RFC", "+7.7"], ["LCOM", "+17.8"], ["NOM", "+5.4"], ["NOA", "+9.3"],
], { x: 9.0, y: 2.35, w: 3.8, colW: [2.2, 1.6], rowH: 0.42, fontFace: BF, fontSize: 14, color: INK, border: { pt: 0.5, color: ICE }, align: "left", valign: "middle" });

/* ---------------- 10. LLM KURULUM ---------------- */
s = pres.addSlide();
s.background = { color: NAVY };
s.addText("LLM DESTEKLİ DEĞERLENDİRME", { x: 0.8, y: 1.3, w: 11, h: 0.4, fontFace: BF, fontSize: 14, color: ICE, bold: true, charSpacing: 2, margin: 0 });
s.addText("17 LLM Yapılandırması, Tek Ortak Prompt", { x: 0.8, y: 1.75, w: 11.7, h: 0.9, fontFace: HF, fontSize: 32, color: WHITE, bold: true, margin: 0 });
const prov = [["ChatGPT", "Ask, Think"], ["Claude", "Opus, Fable, Sonnet"], ["Copilot", "Smart, Think"], ["DeepSeek", "Expert, Inst-Std, Inst-Think"], ["Gemini", "Pro x2, Flash x3"], ["Grok", "Fast"]];
prov.forEach((p, i) => {
  const x = 0.8 + (i % 3) * 4.0, y = 3.0 + Math.floor(i / 3) * 1.7;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 3.7, h: 1.45, fill: { color: "26306E" }, line: { color: ACCENT, width: 1 }, rectRadius: 0.08 });
  s.addText(p[0], { x: x + 0.25, y: y + 0.18, w: 3.2, h: 0.5, fontFace: HF, fontSize: 19, color: WHITE, bold: true, margin: 0 });
  s.addText(p[1], { x: x + 0.25, y: y + 0.72, w: 3.2, h: 0.6, fontFace: BF, fontSize: 13, color: ICE, margin: 0 });
});
s.addText("Aynı prompt (01_full_evolution_prompt.txt) — rol atama, denklem gömme, sayısal-kanıt zorunluluğu, yapılandırılmış 5 başlık.", { x: 0.8, y: 6.6, w: 11.7, h: 0.5, fontFace: BF, fontSize: 13.5, color: ICE, italic: true, margin: 0 });

/* ---------------- 11. LLM SIRALAMA ---------------- */
s = pres.addSlide();
header(s, "LLM Karşılaştırma", "Eleştirel Puanlama — Sıralama (40 üzerinden)");
fitImage(s, "fig_llm_ranking.png", { x: 0.4, y: 1.7, w: 8.0, h: 5.3 });
s.addText("8 kriter × 5 puan", { x: 8.8, y: 1.9, w: 4.0, h: 0.4, fontFace: HF, fontSize: 14, color: NAVY, bold: true, margin: 0 });
s.addText([
  { text: "Sayısal kanıt · Denklem doğruluğu · DSC-artefakt farkındalığı · zamansal granülerlik · halüsinasyon direnci · refactoring somutluğu · sınırlama farkındalığı · analitik derinlik", options: { color: INK } },
], { x: 8.8, y: 2.3, w: 4.0, h: 2.4, fontFace: BF, fontSize: 12.5, valign: "top", lineSpacingMultiple: 1.15, margin: 0 });
s.addText([
  { text: "Lider: claude_opusHigh (40/40)\n", options: { bold: true, color: GOOD, breakLine: true } },
  { text: "En zayıf grup: Gemini Flash kademesi", options: { bold: true, color: BAD } },
], { x: 8.8, y: 5.1, w: 4.0, h: 1.0, fontFace: BF, fontSize: 14, valign: "top", margin: 0 });

/* ---------------- 12. LLM BULGULAR ---------------- */
s = pres.addSlide();
header(s, "LLM Karşılaştırma", "Eleştirel Bulgular");
const finds = [
  ["Uzlaşı yüksek", "17 modelin tamamı 'dış kalite artıyor, iç kalite geriliyor' anlatısında birleşti — bizim analizimizle örtüşüyor.", GOOD],
  ["Metrik halüsinasyonu YOK", "Hiçbir model sayısal değer uydurmadı (sayısal-kanıt kuralının başarısı).", GOOD],
  ["Sınıf adı halüsinasyonu", "Bazı modeller toplu veriden türetilemeyecek sınıf adlarını (Parser, Element...) refactoring hedefi gösterdi.", BAD],
  ["Ayırt edici: DSC-artefakt", "En güçlü yanıt, Reusability +%27'nin tamamının boyut kaynaklı olduğunu sayısal ayrıştırdı (kalite bileşeni 1.969→1.958).", NAVY],
  ["Kademe > sağlayıcı", "Üst kademe reasoning modları belirgin derin; aynı ailede Flash << Pro.", NAVY],
];
let fy = 1.75;
finds.forEach(([h, t, c]) => {
  s.addShape(pres.shapes.OVAL, { x: 0.6, y: fy + 0.05, w: 0.22, h: 0.22, fill: { color: c } });
  s.addText([
    { text: h + ".  ", options: { bold: true, color: c } },
    { text: t, options: { color: INK } },
  ], { x: 1.0, y: fy - 0.05, w: 11.7, h: 0.95, fontFace: BF, fontSize: 15, valign: "top", lineSpacingMultiple: 1.1, margin: 0 });
  fy += 1.02;
});

/* ---------------- 13. SONUÇ ---------------- */
s = pres.addSlide();
s.background = { color: NAVY };
s.addShape(pres.shapes.OVAL, { x: -1.8, y: 4.6, w: 5.0, h: 5.0, fill: { color: "26306E" } });
s.addText("SONUÇ VE GELECEK ÇALIŞMALAR", { x: 0.8, y: 0.9, w: 11, h: 0.4, fontFace: BF, fontSize: 14, color: ICE, bold: true, charSpacing: 2, margin: 0 });
s.addText("Sonuç", { x: 0.8, y: 1.35, w: 11, h: 0.8, fontFace: HF, fontSize: 34, color: WHITE, bold: true, margin: 0 });
s.addText([
  { text: "jsoup, 1.14→1.22 boyunca olgun ve kontrollü yönetilen bir kütüphane: yeniden kullanılabilirlik ve esneklik artarken anlaşılabilirlik kademeli azaldı; cohesion en belirgin teknik borç eğilimi. QMOOD bu çift yönlü evrimi nicel olarak yakalayabildi.", options: { color: ICE, breakLine: true, paraSpaceAfter: 10 } },
  { text: "LLM'ler nitelikte uzlaştı; ayrışma derinlikte oldu — üst kademe reasoning modları, çıktıyı sınıf düzeyi veriyle çapraz doğrulama koşuluyla güvenilir yorum üretti.", options: { color: ICE } },
], { x: 0.8, y: 2.3, w: 11.8, h: 2.2, fontFace: BF, fontSize: 16.5, valign: "top", lineSpacingMultiple: 1.18, margin: 0 });
s.addText("Gelecek çalışmalar", { x: 0.8, y: 4.7, w: 11, h: 0.5, fontFace: HF, fontSize: 19, color: WHITE, bold: true, margin: 0 });
s.addText([
  { text: "Çoklu proje karşılaştırması (C# + Java)", options: { bullet: true, color: ICE, breakLine: true } },
  { text: "LLM yanıtlarının API ile otomatik, çok-tekrarlı toplanması + istatistik anlamlılık testi", options: { bullet: true, color: ICE, breakLine: true } },
  { text: "Metrik eğilimleri ile gerçek hata/commit kayıtları arasındaki korelasyon", options: { bullet: true, color: ICE } },
], { x: 1.0, y: 5.2, w: 11.6, h: 1.6, fontFace: BF, fontSize: 15, valign: "top", margin: 0 });

pres.writeFile({ fileName: path.join(ROOT, "report", "QMOOD_jsoup_sunum.pptx") })
  .then(f => console.log("[OK] Sunum uretildi:", f))
  .catch(e => { console.error(e); process.exit(1); });
