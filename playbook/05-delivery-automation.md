# 05 — Piegādes automatizācija (reaktivācijas mašīna)

Šis ir kodola produkts: sistēma, kas paņem guļošo pacientu sarakstu un pārvērš to
pierakstos — pati. Būvē to **lēti** un tā, lai vēlāk darbojas autonomi.

---

## Tehnoloģiju steks (viss bezmaksas / pay-as-you-go)

| Funkcija | Rīks | Izmaksas |
|----------|------|----------|
| Workflow orchestration | **n8n** (self-host Docker / n8n.cloud free trial) | 0€ self-host |
| AI ziņu rakstīšana + atbildes | **Claude API** (`claude-haiku-4-5` lētām, `claude-sonnet-4-6` sarunām) | centi par pacientu |
| SMS sūtīšana | **Twilio** (pay per SMS) vai klienta esošā sistēma | klients sedz / ietur izmaksās |
| Email sūtīšana | **Resend** / **SendGrid** (free tier) | 0€ sākumā |
| Dati / status | **Airtable** (free) vai **Netlify Blobs** | 0€ |
| Dashboard klientam | Šis Next.js projekts (Netlify) | 0€ |

> 💡 **Lētums ir tava peļņas marža.** Viena pacienta apstrāde (daži AI izsaukumi + 1–3 SMS)
> maksā tev centus, bet tu paņem 50–80$ par atvestu pacientu. Marža ir milzīga.

---

## Plūsma (end-to-end)

```
Patient CSV
   │
   ▼
[1] Import & clean  ──►  normalize phone/email, dedupe, filter opt-outs
   │
   ▼
[2] Segment         ──►  by recency (12–24m, 24–36m, 36m+), treatment type
   │
   ▼
[3] AI personalize  ──►  Claude writes message in clinic's voice + offer
   │
   ▼
[4] Send sequence   ──►  SMS/email day 0 → no reply day 4 → day 9 (3 touches)
   │
   ▼
[5] Handle replies  ──►  Claude reads reply, answers Q, proposes booking slots
   │
   ▼
[6] Book            ──►  push appointment to calendar / hand off to front desk
   │
   ▼
[7] Track + bill    ──►  log "showed up" → dashboard → invoice client
```

## Reaktivācijas ziņas (3-touch sekvence)

Gatavie templeiti: `templates/reactivation-messages.md`. Principi:
- **Silti, īsi, personīgi.** Sajūta = rūpīgs zobārsts, ne robots.
- **Viegls opt-out** katrā ziņā ("Reply STOP to opt out").
- **Skaidrs piedāvājums** (free check-up / cleaning discount) + **viegls booking** ("Reply with a day that works").
- Touch 1 (day 0): silta atgriešanās + piedāvājums. Touch 2 (day 4): atgādinājums + urgency. Touch 3 (day 9): pēdējais maigs aicinājums.

## AI atbilžu apstrāde (kā tas paliek autonoms)

n8n webhook saņem pacienta atbildi → padod Claude ar šādu sistēmas promptu:

```
You are the friendly front-desk assistant for [Clinic Name], a dental practice.
Goal: warmly help this returning patient book an appointment.
- Offer: [clinic's offer]. Available slots: [from calendar].
- Answer questions briefly and kindly. Never give clinical/medical advice — for clinical
  questions say the dentist will confirm at the visit.
- If they pick a time, confirm it and output a BOOKING action with the details.
- If they say STOP / not interested, politely acknowledge and opt them out.
Keep replies under 2 sentences, human and warm. Practice voice: [voice notes].
```

Claude atgriež strukturētu atbildi (text + optional `booking` objektu), ko n8n izpilda:
ieliek kalendārā vai paziņo front desk. **Eskalē uz cilvēku**, ja saruna kļūst klīniska,
sūdzas, vai AI nav pārliecināts → vienmēr atstāj drošu cilvēka rezerves variantu.

## Compliance (dari pareizi — tas aizsargā tevi un klientu)

- **Klients = data controller, tu = data processor.** Paraksti DPA (`templates/dpa-short.md`).
- Sūti tikai esošajiem pacientiem ar likumīgu pamatu (existing relationship). Nepērc sarakstus.
- **Katrā ziņā opt-out** (STOP / unsubscribe). Ievēro tos nekavējoties.
- **US:** SMS — ievēro TCPA (esoša attiecība + opt-out); zobu/veselības dati → uzvedies HIPAA-aware,
  glabā datus minimāli un šifrēti.
- **UK:** GDPR + PECR; legitimate interest / esoša attiecība; viegls opt-out.
- Glabā pacientu datus tikai cik nepieciešams, dzēs pēc kampaņas, šifrē at-rest.
- ⚖️ Pirms pirmā live klienta izlasi compliance basics un, ja deals lieli, paņem vienkāršu
  juridisku review. Tas ir tavs uzticības/reputācijas pamats.

## MVP būvēšanas secība (tev)

1. **Manuāli pirmajam klientam.** Eksports → tu pats palaid Claude, lai uzraksta ziņas →
   sūti caur Twilio/email → atbildi pats vai ar Claude palīdzību. Pierādi, ka pacienti atnāk.
2. **Daļēja automatizācija.** Saliec n8n plūsmu soļiem 1–4 (import → send).
3. **Pilna automatizācija.** Pievieno AI reply handling (5) + booking (6) + dashboard (7).

> ⚠️ Neautomatizē, pirms neesi izdarījis manuāli reizi. Pirmais klients = tava mācība
> un tavs case study vienlaikus.

## Dashboard (jau šajā repo)

Šis Next.js projekts kļūs par klienta rezultātu dashboard: pacienti aizsniegti / atbildējuši /
pierakstīti / atnākuši / ieņēmumi atjaunoti. Skat. `06-scaling-to-10k.md` par to, kā to
pārvērst self-serve produktā (= autonomais finiša posms).
