#!/usr/bin/env node
/**
 * generate-outreach.mjs
 * -------------------------------------------------------------
 * Reads leads from a CSV and uses the Claude API to write a
 * personalized cold outreach email for each one.
 *
 * This is the "automation" layer for playbook/03-outreach-scripts.md.
 * Start by running it on 10–20 leads, review the output by hand, then scale.
 *
 * Usage:
 *   export ANTHROPIC_API_KEY=sk-ant-...
 *   node scripts/generate-outreach.mjs leads.csv > outreach.json
 *
 * CSV columns expected (header row required):
 *   clinic_name, owner_name, role, city, country, website, email, personal_note
 *
 * Cost: pennies. Uses claude-haiku-4-5 (fast + cheap) for drafting.
 * -------------------------------------------------------------
 */

import fs from 'node:fs';
import process from 'node:process';

const MODEL = 'claude-haiku-4-5'; // cheap + fast for high-volume drafting
const CALENDLY = process.env.CALENDLY_URL || 'https://calendly.com/your-handle/15min';
const SENDER = process.env.SENDER_NAME || 'Your Name';

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
    console.error('Missing ANTHROPIC_API_KEY. Run: export ANTHROPIC_API_KEY=sk-ant-...');
    process.exit(1);
}

const csvPath = process.argv[2] || 'leads.csv';
if (!fs.existsSync(csvPath)) {
    console.error(`CSV not found: ${csvPath}`);
    process.exit(1);
}

/** Minimal CSV parser (handles quoted fields and commas inside quotes). */
function parseCsv(text) {
    const rows = [];
    let row = [];
    let field = '';
    let inQuotes = false;
    for (let i = 0; i < text.length; i++) {
        const c = text[i];
        if (inQuotes) {
            if (c === '"' && text[i + 1] === '"') {
                field += '"';
                i++;
            } else if (c === '"') {
                inQuotes = false;
            } else {
                field += c;
            }
        } else if (c === '"') {
            inQuotes = true;
        } else if (c === ',') {
            row.push(field);
            field = '';
        } else if (c === '\n' || c === '\r') {
            if (field !== '' || row.length) {
                row.push(field);
                rows.push(row);
                row = [];
                field = '';
            }
            if (c === '\r' && text[i + 1] === '\n') i++;
        } else {
            field += c;
        }
    }
    if (field !== '' || row.length) {
        row.push(field);
        rows.push(row);
    }
    return rows;
}

const raw = fs.readFileSync(csvPath, 'utf8');
const rows = parseCsv(raw).filter((r) => r.some((c) => c.trim() !== ''));
const header = rows.shift().map((h) => h.trim());
const leads = rows.map((r) => Object.fromEntries(header.map((h, i) => [h, (r[i] || '').trim()])));

const SYSTEM = `You write short, warm, high-converting B2B cold emails for ChairFill, a service
that reactivates dental practices' dormant patients with AI recall campaigns (SMS + email),
booking lapsed patients back into the calendar. Key selling points: done-for-you, no setup
fee, no contract, pay only per patient who shows up.

Rules:
- 70–110 words, plain text, no markdown, no emojis.
- One clear CTA: book a 15-minute call at the provided link.
- Personalize naturally using the lead's clinic name, city, and personal note.
- Sound like a real human, not marketing. No hype, no "I hope this finds you well".
- Lead with the dormant-patient insight, then the no-risk offer, then the CTA.
Return ONLY a JSON object: {"subject": "...", "body": "..."} and nothing else.`;

async function draftFor(lead) {
    const userPrompt = `Lead:
- Clinic: ${lead.clinic_name || '(unknown)'}
- Contact: ${lead.owner_name || '(unknown)'} (${lead.role || 'practice owner'})
- City/Country: ${lead.city || ''} ${lead.country || ''}
- Website: ${lead.website || ''}
- Personal note: ${lead.personal_note || '(none)'}

Sender name: ${SENDER}
Booking link to include in the CTA: ${CALENDLY}

Write the email now.`;

    const res = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        body: JSON.stringify({
            model: MODEL,
            max_tokens: 600,
            system: SYSTEM,
            messages: [{ role: 'user', content: userPrompt }]
        })
    });

    if (!res.ok) {
        throw new Error(`API ${res.status}: ${await res.text()}`);
    }
    const data = await res.json();
    const text = data.content?.[0]?.text?.trim() ?? '';
    try {
        return JSON.parse(text);
    } catch {
        return { subject: '(parse failed)', body: text };
    }
}

const out = [];
for (const lead of leads) {
    if (!lead.email) {
        console.error(`Skipping ${lead.clinic_name || 'unknown'} — no email`);
        continue;
    }
    try {
        const draft = await draftFor(lead);
        out.push({ to: lead.email, clinic: lead.clinic_name, ...draft });
        console.error(`✓ drafted: ${lead.clinic_name}`);
    } catch (e) {
        console.error(`✗ ${lead.clinic_name}: ${e.message}`);
    }
}

process.stdout.write(JSON.stringify(out, null, 2) + '\n');
console.error(`\nDone. ${out.length} emails drafted. Review before sending!`);
