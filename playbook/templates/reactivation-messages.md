# Reaktivācijas ziņas (klienta pacientiem)

Aizvieto `[...]` ar klīnikas datiem. Klients **apstiprina** tekstu pirms sūtīšanas.
Vienmēr iekļauj opt-out. Toņa princips: silts, īss, personīgs — kā rūpīgs zobārsts.

---

## SMS sekvence (3 touch)

### Touch 1 — Day 0 (silta atgriešanās)
```
Hi [Patient First Name], it's [Clinic Name] 🦷 We noticed it's been a while since your
last visit and wanted to check in. We'd love to see you back — and to say welcome back,
your next check-up is [offer, e.g. on us / 20% off]. Reply with a day that suits you and
we'll find a time. Reply STOP to opt out.
```

### Touch 2 — Day 4 (maigs atgādinājums + urgency)
```
Hi [First Name], just a gentle reminder from [Clinic Name] — your [offer] is still open
this month. Keeping up with check-ups now saves bigger treatment later. Want me to hold
a spot for you this week? Just reply with a day. Reply STOP to opt out.
```

### Touch 3 — Day 9 (pēdējais maigais)
```
Hi [First Name], last note from [Clinic Name] 🙂 We'd genuinely love to see you back and
your [offer] expires soon. If now's not the time, no worries at all — just reply YES and
we'll sort a convenient slot for you. Reply STOP to opt out.
```

---

## Email versija (Touch 1)

**Subject:** `We'd love to see you back at [Clinic Name], [First Name]`

```
Hi [First Name],

It's been a little while since your last visit to [Clinic Name], and we wanted to reach
out — your smile matters to us.

As a welcome back, we'd like to offer you [offer]. Regular check-ups are the easiest way
to avoid bigger (and pricier) treatments down the road.

Booking takes 30 seconds — just reply to this email with a day that works, or call us at
[phone]. We'll find a time that fits around you.

Warmly,
The team at [Clinic Name]

---
Don't want these reminders? Unsubscribe here: [link]
```

---

## AI reply-handling — sistēmas prompts (Claude)

```
You are the warm, professional front-desk assistant for [Clinic Name], a dental practice.
Your job: help this returning patient feel welcome and book an appointment.

Rules:
- Offer on the table: [offer]. Open slots: [slots/booking instructions].
- Keep replies to 1–2 short, friendly sentences.
- NEVER give clinical or medical advice. For clinical questions, say the dentist will
  confirm everything at the visit.
- If the patient proposes a time, confirm it and emit a BOOKING action.
- If they say STOP / not interested / unsubscribe, acknowledge kindly and opt them out.
- If the conversation becomes a complaint, urgent/medical, or you're unsure → hand off to
  a human staff member.
Practice voice: [voice notes, e.g. friendly, down-to-earth, British spelling].
```
