# Onboarding checklist (jaunam klientam)

Mērķis: no parakstīta "jā" līdz go-live ≤7 dienās. Sūti šo klientam pēc close.

## 1. Paraksti (diena 0–1)
- [ ] Service agreement (pakalpojuma apraksts, cena, no-lock-in, garantija)
- [ ] DPA — data processing agreement (`dpa-short.md`)

## 2. Dati (diena 1–2)
- [ ] Guļošo pacientu eksports CSV formātā ar kolonnām:
      `first_name, last_name, phone, email, last_visit_date, last_treatment`
- [ ] Filtrs: pacienti bez vizīta 12+ mēnešus, ar derīgu telefonu vai email
- [ ] Drošs nodošanas veids (šifrēts upload, ne parasts email)

## 3. Balss un piedāvājums (diena 2–3, 20-min zvans)
- [ ] Klīnikas "balss" (toņa piezīmes, brand, spelling US/UK)
- [ ] Reaktivācijas piedāvājums (free check-up / cleaning discount / whitening offer)
- [ ] Sūtītāja vārds/numurs (klīnikas vai dedicated)
- [ ] Booking plūsma: tieši kalendārā / "reply with a day" / front desk handoff

## 4. Tehniskais setup (diena 3–5)
- [ ] SMS kanāls (Twilio numurs vai klienta esošā sistēma)
- [ ] Email kanāls (verificēts domēns, SPF/DKIM)
- [ ] n8n plūsma konfigurēta ar klienta datiem
- [ ] Opt-out un compliance pārbaudīts

## 5. Apstiprināšana un go-live (diena 5–7)
- [ ] Klients apstiprina ziņu tekstus (touch 1–3)
- [ ] Tests uz 5–10 pacientiem (soft launch)
- [ ] Pilns palaišana
- [ ] Dashboard links nodots klientam

## 6. Pēc launch
- [ ] Dienas/nedēļas rezultātu update klientam
- [ ] Pirmā invoice pēc pirmajiem atvestajiem pacientiem
- [ ] Lūdz testimonial pēc pirmajiem rezultātiem (tavs nākamais case study!)
