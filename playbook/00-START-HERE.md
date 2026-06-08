# ChairFill — Bizness kastē 🦷

**Modelis:** AI pacientu reaktivācija zobārstniecības klīnikām (US / UK tirgus)
**Tavs profils:** pilna slodze · vari kodēt + pārdot + mārketēt · budžets ≤50€
**Mērķis:** 0€ → 10 000€/mēn uz ~3. mēnesi (reālistiski, nevis hype)

---

## Kāpēc tieši šis bizness

1. **Augsta vērtība uz klientu.** Viens atvests zobārsta pacients = 200–3000$. Tāpēc klīnika
   labprāt maksā par rezultātu, un tev nav jācīnās par katru centu.
2. **Nulles riska piedāvājums.** "Maksā tikai par pacientiem, kas atnāk" → viegli pārdot bez
   reputācijas un bez case study.
3. **Zemas izmaksas.** Automatizāciju būvē ar bezmaksas/lētiem rīkiem (n8n, Claude API, Netlify).
4. **Tu vari to izpildīt viens** pirmajos mēnešos, tad automatizēt.

## Reālistiskā matemātika līdz 10k€

| Klienti | Vidējais retainer/klients | Mēneša ieņēmumi |
|--------:|--------------------------:|----------------:|
| 2       | ~700€                     | ~1 400€         |
| 5       | ~900€                     | ~4 500€         |
| 8       | ~1 100€                   | ~8 800€         |
| 10      | ~1 200€                   | ~12 000€ ✅      |

Tev vajag **~10 maksājošus klientus**. Tas ir sasniedzams pilnā slodzē 8–12 nedēļās.

## 30 dienu kalendārs (high-level)

| Nedēļa | Fokuss | Galvenais rezultāts |
|-------|--------|---------------------|
| **1** | Setup + offer | Vietne live, booking links, 200 leadu saraksts, outreach sākts |
| **2** | Outreach masē | 300+ kontakti aizsniegti, pirmie zvani sarunāti |
| **3** | Pirmais klients | 1.–2. klients parakstīts, piegādes sistēma uzbūvēta |
| **4** | Piegāde + pierādījums | Pirmie pacienti atvesti → tavs pirmais case study |

Pēc tam: atkārto outreach + ej augšup cenā + automatizē piegādi (skat. `06-scaling-to-10k.md`).

## Failu ceļvedis (lasi šādā secībā)

1. **`01-offer-and-pricing.md`** — precīzs piedāvājums, cenas, garantija, kā strukturēt deal
2. **`02-finding-leads.md`** — kā atrast klīnikas un decision-makerus (bezmaksas)
3. **`03-outreach-scripts.md`** — email / LinkedIn / cold call skripti (gatavi, angliski)
4. **`04-sales-call-script.md`** — discovery + close skripts zvanam
5. **`05-delivery-automation.md`** — tehniskā piegāde: n8n + Claude reaktivācijas mašīna
6. **`06-scaling-to-10k.md`** — kā no 1 klienta tikt līdz 10k un padarīt autonomu
7. **`templates/`** — gatavie SMS/email reaktivācijas teksti + DPA + onboarding

## Šodien (tavs pirmais solis)

1. Reģistrē domēnu (`chairfill.co` vai līdzīgu) — ~10€. Tas ir tavs vienīgais obligātais tēriņš.
2. Izveido bezmaksas Calendly + business email.
3. Atver `app/page.jsx` un nomaini `CALENDLY` un `EMAIL` konstantes uz savām.
4. Deploy uz Netlify (bezmaksas). Vietne live.
5. Sāc ar `02-finding-leads.md` — saliec pirmos 50 leadus.

> ⚠️ **Godīgi par "autonomu un bez darba":** pirmais mēnesis NAV pasīvs. Tu pārdod ar rokām.
> Autonomija nāk 2.–3. mēnesī, kad process atkārtojas un tu to automatizē. Tā ir vienīgā
> reālā ceļa versija — visi, kas sola pasīvus 10k pirmajā nedēļā, melo.
