# 02 — Kā atrast klīnikas un decision-makerus (bezmaksas)

Mērķis: **200 kvalificēti leadi** pirmajā nedēļā. Tev vajag vārdu, klīniku, email un/vai
telefonu, ideālā gadījumā īpašnieka/practice manager vārdu.

---

## Kuru tieši mērķēt

- **Privātas zobārstniecības klīnikas** (ne lielas korporatīvās ķēdes — tās ir lēnas).
- 1–4 zobārsti, esoša mājaslapa, Google atsauksmes (= viņiem rūp izaugsme).
- **Decision maker:** īpašnieks-zobārsts vai *Practice Manager*.
- Tirgus: sāc ar **US** (lielākie budžeti) vai **UK** (vieglāks laika zonas pārklājums no LV).

## Avoti, kur dabūt leadus (par brīvu)

### 1. Google Maps (labākais)
- Meklē: `dentist in [city]` (piem. Austin, Manchester, Phoenix, Leeds).
- Katrai klīnikai pieraksti: nosaukums, mājaslapa, telefons, atsauksmju skaits.
- **Pro tip:** mērķē klīnikas ar 50–400 atsauksmēm — pietiekami lielas, lai būtu guļošu
  pacientu saraksts, bet pietiekami mazas, lai īpašnieks pats atbild.

### 2. Klīnikas mājaslapa
- "Meet the team" / "Contact" → dabū īpašnieka vārdu un tiešo email.
- Personalizācijai pieraksti 1 detaļu (pakalpojums, ko reklamē, jauns zobārsts, utt.).

### 3. LinkedIn
- Meklē: `"practice owner" dentist [city]` vai `"practice manager" dental`.
- Connect + personalizēta ziņa (skat. `03-outreach-scripts.md`).

### 4. Instagram / Facebook
- Daudzas klīnikas aktīvi postē. DM darbojas labi, jo maz konkurences inboxā.

## Email atrašana (bezmaksas līmeklis)

- Bieži tieši mājaslapā: `info@`, `reception@`, vai team lapā.
- Bezmaksas/freemium rīki: **Hunter.io** (25/mēn free), **Apollo.io** (free credits),
  **Anymailfinder** trial. Apollo arī dod telefonus un filtrus pēc nozares + lieluma.
- Vienmēr mēģini dabūt **personīgo** email (john@), ne tikai info@ — 3× labāka atbilžu likme.

## Lead saraksta struktūra (CSV)

Izveido `leads.csv` ar kolonnām:

```
clinic_name, owner_name, role, city, country, website, email, phone, instagram, review_count, personal_note, status
```

`status` vērtības: `new → contacted → replied → call_booked → won → lost`

> 🤖 **Automatizācija (vēlāk):** Apollo + n8n var savākt un papildināt leadus automātiski.
> Bet **pirmos 200 dari ar rokām** — tā tu iemācies, kas ir labs leads, pirms automatizē sliktu.

## Dienas mērķis nedēļā 1

- Diena 1–2: saliec 200 leadu CSV.
- Diena 3–5: sāc outreach (50/dienā) — skat. nākamo failu.

## Compliance piezīme (svarīgi US/UK)

- **UK (PECR/GDPR):** B2B cold email uz biznesa adresēm ir atļauts ar opt-out. Vienmēr iekļauj
  unsubscribe un savu identitāti.
- **US (CAN-SPAM):** cold email legāls; vajag īstu sūtītāja info + opt-out. SMS uz biznesiem — esi piesardzīgs, prioritizē email/LinkedIn outreach.
- Tas attiecas uz **tavu** outreach. Pacientu reaktivācijas ziņas (klienta vārdā) ir cita
  compliance daļa — skat. `05-delivery-automation.md`.
