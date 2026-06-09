# Prompt Muhendisligi Sureci

Bu klasordeki promptlar, QMOOD metrik verilerini farkli LLM modellerine ayni
kosullar altinda vermek icin tasarlanmistir. Amac, modellerin yazilim kalite
degerlendirme yeteneklerini KARSILASTIRMAKTIR.

## Tasarim ilkeleri
1. **Rol atama (persona):** Her prompt, modele "kidemli yazilim kalite uzmani"
   rolu verir. Bu, daha tutarli ve teknik yanitlar uretir.
2. **Baglam saglama:** QMOOD denklemleri ve metrik tanimlari prompt icine
   gomulur; model harici bilgiye guvenmek zorunda kalmaz.
3. **Kanit zorunlulugu:** Model her iddiayi bir metrik degisimine baglamak
   zorundadir ("sayisal kanit goster"). Bu, halusinasyonu azaltir.
4. **Yapilandirilmis cikti:** 5 sabit baslik istenir; boylece modeller arasi
   karsilastirma kolaylasir.
5. **Esit kosul:** Tum modellere AYNI prompt verilir (00 + 01). Farkliliklar
   yalnizca modelden kaynaklanir.

## Kullanim
- `01_full_evolution_prompt.txt`: ANA PROMPT. Tum modellere bunu verin.
- `02_version_*`: Tek surum derinlemesine inceleme (opsiyonel ek sorgu).
- `03_diff_*`: Ardisik surum farki yorumu (opsiyonel ek sorgu).

## Onerilen modeller (>=3)
ChatGPT (GPT-4o/5), Claude, Gemini, DeepSeek, Grok, Llama.
Her modelin yanitini `llm_responses/<model>.md` altina kaydedin; sonra
`compare_llm.py` (veya manuel) ile karsilastirin.

## Eklestirel degerlendirme
Her LLM yaniti icin not edin:
- Sayisal kanit kullandi mi? (evet/kismi/hayir)
- QMOOD denklemlerini dogru yorumladi mi?
- Halusinasyon/uydurma metrik var mi?
- Refactoring onerileri somut mu?
