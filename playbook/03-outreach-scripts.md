# 03 — Outreach skripti (gatavi, angliski)

Mērķis: dabūt **zvanu kalendārā**, ne pārdot emailā. Katra ziņa = viens skaidrs CTA: "book a 15-min call".

> Sūti **50–80 kontaktu dienā** pa vairākiem kanāliem. Sagaidi 1–5% atbilžu likmi → seko līdzi.

---

## KANĀLS 1 — Cold email (galvenais)

### Email #1 (pirmais kontakts)
**Subject:** `quick question about [Clinic Name]'s past patients`

```
Hi [First Name],

Most dental practices are sitting on hundreds of patients who came once or twice,
then quietly went silent — never angry, just busy.

We help practices like [Clinic Name] win those patients back. Our AI gently re-invites
your lapsed patients by text and email, answers their questions, and books them straight
into your calendar. Your team does nothing.

You only pay for patients who actually show up. No setup fee, no contract.

Worth a quick 15-minute look? Here's my calendar: [Calendly link]

Best,
[Your Name]
ChairFill
```

### Email #2 (follow-up, +3 dienas) — ROI angle
**Subject:** `re: [Clinic Name]'s past patients`

```
Hi [First Name],

Quick math: if [Clinic Name] has ~1,500 lapsed patients and we rebook even 8% of them
at an average visit value of ~$280, that's roughly $33,000 in recovered revenue —
from people already in your system.

We do the whole thing for you and you only pay per patient who shows up.

15 minutes this week? [Calendly link]

[Your Name]
```

### Email #3 (break-up, +4 dienas) — vislabākā atbilžu likme
**Subject:** `should I close your file?`

```
Hi [First Name],

I haven't heard back, so I'll assume reactivating past patients isn't a priority
right now and I'll stop reaching out.

If that changes, my door's open — we only get paid when your chairs get filled.

Wishing [Clinic Name] a fully-booked month,
[Your Name]
```

---

## KANĀLS 2 — LinkedIn

### Connection request (≤300 chars)
```
Hi [First Name] — I help dental practices rebook lapsed patients with AI recall campaigns
(you only pay when patients show up). Would love to connect.
```

### Pēc pieņemšanas (DM)
```
Thanks for connecting, [First Name]! Genuinely — does [Clinic Name] do much to win back
patients who stopped booking? We turn that dormant list into booked appointments,
done-for-you, pay-per-result. Happy to show you a 2-min example if useful.
```

---

## KANĀLS 3 — Instagram / Facebook DM

```
Hey [Clinic Name] team! Love what you're doing 🙌 Quick one — we help practices rebook
past patients who went quiet (AI texts + emails, books them right into your calendar,
you only pay per show-up). Want me to send a quick example?
```

---

## KANĀLS 4 — Cold call (visātrākais ceļš uz pirmo klientu)

**Mērķis zvanā:** nevis pārdot, bet sarunāt 15-min zvanu vai dabūt īpašnieka email.

```
"Hi, this is [Your Name] — I'll be quick. Do you help patients who came in once
and then never rebooked come back? ... Right, most practices don't have time.

We run AI campaigns that re-invite your lapsed patients and book them straight into
your calendar — and you only pay when they actually show up. No upfront cost.

Who'd be the best person to send a 2-minute example to — is that you or the practice owner?"
```

Ja vārtu sargs (receptionist): dabū īpašnieka vārdu + email, sūti Email #1 ar "as discussed".

---

## Sekošanas sistēma (kritiski)

- 80% deals nāk no **follow-up #2–#4**, ne pirmā kontakta.
- Izmanto `leads.csv` `status` kolonnu + atgādinājumus.
- Sekvence vienam leadam: Email#1 → +3d Email#2 → +4d Email#3 → paralēli LinkedIn.
- **Cilvēks atbild → nekavējoties piedāvā konkrētu zvana laiku** (skat. `04`).

> 🤖 **Automatizācija (vēlāk):** visu šo sekvenci var palaist ar n8n + Claude API, kas
> personalizē katru emailu pēc `personal_note`. Skripts: `scripts/generate-outreach.mjs`.
