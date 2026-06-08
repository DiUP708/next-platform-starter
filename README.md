# ChairFill 🦷

**AI patient reactivation for dental practices (US / UK).**
We turn a practice's dormant patient list into booked appointments — done-for-you,
pay-per-result.

This repo contains both the **marketing site** (Next.js on Netlify) and the full
**business playbook** to take it from €0 to €10k/month.

---

## What's here

| Path | What it is |
|------|-----------|
| `app/` | The ChairFill landing page (Next.js 15 + Tailwind v4) |
| `components/roi-calculator.jsx` | Interactive dormant-list ROI calculator (the sales hook) |
| `playbook/` | **The whole business in a box** — read `playbook/00-START-HERE.md` first |
| `playbook/templates/` | Ready-to-use messages, onboarding checklist, DPA |
| `scripts/generate-outreach.mjs` | Claude-powered cold-email personalizer |
| `leads.sample.csv` | Example lead format (real `leads.csv` is gitignored) |

## Quick start

```bash
npm install
npm run dev      # landing page at http://localhost:3000
npm run build    # production build
```

Before deploying, edit the `CALENDLY` and `EMAIL` constants in `app/page.jsx`
(and the booking link in `components/roi-calculator.jsx`).

## The business, in one line

A practice has hundreds of patients who went quiet. ChairFill's AI re-invites them by
text + email, books them back into the calendar, and the practice pays only for patients
who show up. See `playbook/00-START-HERE.md` for the full 30-day plan.

## Generate outreach drafts

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CALENDLY_URL=https://calendly.com/your-handle/15min
export SENDER_NAME="Your Name"
node scripts/generate-outreach.mjs leads.sample.csv > outreach.json
```

> Deployed on Netlify. Built from the Next.js Platform Starter.
