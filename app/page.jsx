import Link from 'next/link';
import { RoiCalculator } from '../components/roi-calculator';

const CALENDLY = 'https://calendly.com/your-handle/15min'; // TODO: replace with your real booking link
const EMAIL = 'hello@chairfill.co'; // TODO: replace with your real email

export default function Page() {
    return (
        <div className="min-h-screen">
            <SiteHeader />
            <Hero />
            <TrustBar />
            <Problem />
            <HowItWorks />
            <section id="roi" className="px-6 py-20 bg-slate-50">
                <div className="max-w-5xl mx-auto">
                    <SectionHeading
                        eyebrow="Free 30-second estimate"
                        title="How much revenue is sitting in your dormant patient list?"
                        subtitle="Most practices have 6 figures of unbooked treatment hiding in patients who simply went quiet. Move the sliders."
                    />
                    <RoiCalculator />
                </div>
            </section>
            <WhatYouGet />
            <Pricing />
            <Faq />
            <FinalCta />
            <SiteFooter />
        </div>
    );
}

function SiteHeader() {
    return (
        <header className="sticky top-0 z-50 border-b bg-white/80 backdrop-blur border-slate-200">
            <div className="flex items-center justify-between max-w-5xl px-6 py-4 mx-auto">
                <Link href="/" className="flex items-center gap-2 text-lg font-extrabold no-underline text-slate-900">
                    <span className="grid w-8 h-8 text-white rounded-lg place-items-center bg-teal-500">C</span>
                    ChairFill
                </Link>
                <nav className="items-center hidden gap-8 text-sm font-medium md:flex">
                    <a href="#how" className="no-underline text-slate-600 hover:text-slate-900">How it works</a>
                    <a href="#roi" className="no-underline text-slate-600 hover:text-slate-900">ROI calculator</a>
                    <a href="#pricing" className="no-underline text-slate-600 hover:text-slate-900">Pricing</a>
                    <a href="#faq" className="no-underline text-slate-600 hover:text-slate-900">FAQ</a>
                </nav>
                <Link href={CALENDLY} className="px-4 py-2 text-sm font-bold text-white no-underline transition bg-teal-500 rounded-lg hover:bg-teal-600">
                    Book a call
                </Link>
            </div>
        </header>
    );
}

function Hero() {
    return (
        <section className="px-6 py-20 sm:py-28">
            <div className="max-w-5xl mx-auto text-center">
                <div className="inline-flex items-center gap-2 px-3 py-1 mb-6 text-xs font-semibold text-teal-700 rounded-full bg-teal-50 ring-1 ring-teal-200">
                    <span className="w-2 h-2 rounded-full bg-teal-500" />
                    For dental practices in the US &amp; UK
                </div>
                <h1 className="max-w-3xl mx-auto text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl">
                    We refill your empty chairs with patients you{' '}
                    <span className="text-teal-500">already have</span>.
                </h1>
                <p className="max-w-2xl mx-auto mt-6 text-lg text-slate-600">
                    ChairFill runs AI-driven recall campaigns across your dormant patient list — the people who
                    stopped booking. We rebook them into your calendar. You pay only when they show up.
                </p>
                <div className="flex flex-col items-center justify-center gap-3 mt-8 sm:flex-row">
                    <Link href={CALENDLY} className="px-6 py-3.5 text-base font-bold text-white no-underline transition bg-teal-500 rounded-xl hover:bg-teal-600">
                        Get my free reactivation estimate
                    </Link>
                    <a href="#how" className="px-6 py-3.5 text-base font-bold no-underline transition border rounded-xl text-slate-700 border-slate-300 hover:bg-slate-50">
                        See how it works
                    </a>
                </div>
                <p className="mt-4 text-sm text-slate-500">No setup fee · No long contracts · Performance-based pricing</p>
            </div>
        </section>
    );
}

function TrustBar() {
    const stats = [
        ['$0', 'Upfront cost to start'],
        ['7 days', 'To first rebooked patient'],
        ['100%', 'Done-for-you — no work for your staff'],
        ['GDPR / HIPAA', 'Compliant messaging']
    ];
    return (
        <section className="px-6 py-10 border-y bg-slate-50 border-slate-200">
            <div className="grid max-w-5xl grid-cols-2 gap-6 mx-auto md:grid-cols-4">
                {stats.map(([big, small]) => (
                    <div key={small} className="text-center">
                        <div className="text-2xl font-extrabold text-slate-900">{big}</div>
                        <div className="mt-1 text-sm text-slate-500">{small}</div>
                    </div>
                ))}
            </div>
        </section>
    );
}

function Problem() {
    return (
        <section className="px-6 py-20">
            <div className="max-w-3xl mx-auto">
                <SectionHeading
                    eyebrow="The hidden leak"
                    title="The most expensive patients are the ones who never came back"
                    subtitle=""
                />
                <div className="space-y-4 text-lg text-slate-600">
                    <p>
                        Every practice has them: hundreds — sometimes thousands — of patients who came once or twice
                        and then quietly disappeared. They didn&apos;t leave angry. Life just got busy.
                    </p>
                    <p>
                        Your front desk is already buried answering phones and checking in today&apos;s patients.
                        Nobody has time to manually call 1,800 lapsed patients and gently invite them back. So that
                        list just sits there — a six-figure asset gathering dust.
                    </p>
                    <p className="font-semibold text-slate-900">
                        ChairFill turns that dormant list into booked appointments — automatically, on autopilot,
                        without adding a single task to your team&apos;s day.
                    </p>
                </div>
            </div>
        </section>
    );
}

function HowItWorks() {
    const steps = [
        {
            n: '01',
            t: 'You hand us your dormant list (securely)',
            d: 'We export inactive patients from your practice software — no manual work for you. Data is handled under a signed processing agreement and never leaves compliant infrastructure.'
        },
        {
            n: '02',
            t: 'Our AI runs personalized recall campaigns',
            d: 'Warm, human-sounding SMS and email sequences invite each patient back at the right time. The AI handles replies, answers questions, and offers booking slots 24/7 — in your practice’s voice.'
        },
        {
            n: '03',
            t: 'Patients land in your calendar',
            d: 'Confirmed appointments drop straight into your existing scheduling system. Your front desk just sees a fuller calendar. You pay per booked, attended patient.'
        }
    ];
    return (
        <section id="how" className="px-6 py-20 bg-slate-900">
            <div className="max-w-5xl mx-auto">
                <SectionHeading
                    dark
                    eyebrow="How it works"
                    title="Three steps. Zero extra work for your team."
                    subtitle="We do the whole thing for you. You approve the message, we run the machine."
                />
                <div className="grid gap-6 md:grid-cols-3">
                    {steps.map((s) => (
                        <div key={s.n} className="p-6 border bg-slate-800/50 rounded-2xl border-slate-700">
                            <div className="text-sm font-extrabold tracking-widest text-teal-400">{s.n}</div>
                            <h3 className="mt-3 text-lg font-bold text-white">{s.t}</h3>
                            <p className="mt-2 text-sm leading-relaxed text-slate-300">{s.d}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

function WhatYouGet() {
    const items = [
        ['Done-for-you setup', 'We build, write, and launch everything. Go-live in under 7 days.'],
        ['AI reply handling', 'The system answers patient questions and books slots around the clock.'],
        ['Your brand voice', 'Every message sounds like it came from your practice, not a robot.'],
        ['Live results dashboard', 'See exactly how many patients were reactivated and the revenue booked.'],
        ['Compliance built in', 'Opt-outs, consent, and data handling done by the book (GDPR / HIPAA-aware).'],
        ['No lock-in', 'Month-to-month. We earn your business with results, not contracts.']
    ];
    return (
        <section className="px-6 py-20">
            <div className="max-w-5xl mx-auto">
                <SectionHeading eyebrow="What's included" title="Everything done for you" subtitle="" />
                <div className="grid gap-5 md:grid-cols-2">
                    {items.map(([t, d]) => (
                        <div key={t} className="flex gap-4 p-5 border rounded-xl border-slate-200">
                            <svg className="flex-shrink-0 w-6 h-6 text-teal-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                            </svg>
                            <div>
                                <h3 className="text-base font-bold text-slate-900">{t}</h3>
                                <p className="mt-1 text-sm text-slate-600">{d}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

function Pricing() {
    return (
        <section id="pricing" className="px-6 py-20 bg-slate-50">
            <div className="max-w-3xl mx-auto">
                <SectionHeading
                    eyebrow="Pricing"
                    title="You only win if we win"
                    subtitle="We remove all the risk. If we don't rebook patients, you don't pay."
                />
                <div className="p-8 bg-white border-2 shadow-sm rounded-3xl border-teal-200 sm:p-10">
                    <div className="inline-block px-3 py-1 text-xs font-bold text-teal-700 rounded-full bg-teal-50">
                        MOST POPULAR · PERFORMANCE PLAN
                    </div>
                    <div className="mt-6">
                        <span className="text-5xl font-extrabold text-slate-900">$0</span>
                        <span className="ml-2 text-slate-500">to start — then a flat fee per attended patient we rebook</span>
                    </div>
                    <ul className="mt-8 space-y-3 text-slate-700">
                        {[
                            'No setup fee, no monthly retainer to begin',
                            'We build and run the entire campaign for you',
                            'You approve the messaging before anything goes out',
                            'Pay only for patients who book AND show up',
                            'Cancel anytime — month-to-month'
                        ].map((li) => (
                            <li key={li} className="flex gap-3">
                                <svg className="flex-shrink-0 w-5 h-5 mt-0.5 text-teal-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                <span>{li}</span>
                            </li>
                        ))}
                    </ul>
                    <Link href={CALENDLY} className="block w-full px-6 py-4 mt-8 text-base font-bold text-center text-white no-underline transition bg-teal-500 rounded-xl hover:bg-teal-600">
                        Book my free strategy call
                    </Link>
                    <p className="mt-4 text-sm text-center text-slate-500">
                        On the call we&apos;ll estimate your dormant-list revenue live. No obligation.
                    </p>
                </div>
            </div>
        </section>
    );
}

function Faq() {
    const faqs = [
        ['Do I need to change my scheduling software?', 'No. We work alongside whatever you already use. Appointments land in your existing calendar.'],
        ['Is this compliant with patient data rules?', 'Yes. We operate under a signed data processing agreement, honor opt-outs, and follow GDPR/HIPAA-aware messaging practices. You stay the data controller; we are the processor.'],
        ['Will this annoy my patients?', 'No. Messages are warm, infrequent, and easy to opt out of. They sound like a caring nudge from your practice, not spam. You approve the wording first.'],
        ['How fast will I see results?', 'Most practices see their first rebooked patients within 7 days of launch.'],
        ['What does it actually cost?', 'There is no upfront cost. You pay a flat fee only for patients who book and attend. On our call we agree the exact number so it always stays profitable for you.'],
        ['How much of my staff’s time does this take?', 'Almost none. Setup is a short onboarding call plus a secure data export. After that it runs on autopilot.']
    ];
    return (
        <section id="faq" className="px-6 py-20">
            <div className="max-w-3xl mx-auto">
                <SectionHeading eyebrow="FAQ" title="Questions practices ask us" subtitle="" />
                <div className="divide-y divide-slate-200">
                    {faqs.map(([q, a]) => (
                        <details key={q} className="py-5 group">
                            <summary className="flex items-center justify-between font-semibold list-none cursor-pointer text-slate-900">
                                {q}
                                <span className="ml-4 text-teal-500 transition group-open:rotate-45">+</span>
                            </summary>
                            <p className="mt-3 text-slate-600">{a}</p>
                        </details>
                    ))}
                </div>
            </div>
        </section>
    );
}

function FinalCta() {
    return (
        <section className="px-6 py-20 bg-teal-500">
            <div className="max-w-3xl mx-auto text-center">
                <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
                    Your next 50 patients are already in your database.
                </h2>
                <p className="mt-4 text-lg text-teal-50">
                    Let&apos;s go get them. Book a free 15-minute call and we&apos;ll show you exactly how much
                    revenue is sitting in your dormant list.
                </p>
                <Link href={CALENDLY} className="inline-block px-8 py-4 mt-8 text-base font-bold text-teal-600 no-underline transition bg-white rounded-xl hover:bg-teal-50">
                    Book my free call
                </Link>
            </div>
        </section>
    );
}

function SiteFooter() {
    return (
        <footer className="px-6 py-12 text-sm bg-slate-900 text-slate-400">
            <div className="flex flex-col items-center justify-between max-w-5xl gap-4 mx-auto sm:flex-row">
                <div className="flex items-center gap-2 font-extrabold text-white">
                    <span className="grid w-7 h-7 text-white rounded-lg place-items-center bg-teal-500">C</span>
                    ChairFill
                </div>
                <p>© {new Date().getFullYear()} ChairFill. Patient reactivation for modern dental practices.</p>
                <a href={`mailto:${EMAIL}`} className="no-underline text-slate-400 hover:text-white">{EMAIL}</a>
            </div>
        </footer>
    );
}

function SectionHeading({ eyebrow, title, subtitle, dark }) {
    return (
        <div className="max-w-2xl mx-auto mb-12 text-center">
            {eyebrow && <div className="mb-3 text-sm font-bold tracking-widest text-teal-500 uppercase">{eyebrow}</div>}
            <h2 className={`text-3xl font-extrabold sm:text-4xl ${dark ? 'text-white' : 'text-slate-900'}`}>{title}</h2>
            {subtitle && <p className={`mt-4 text-lg ${dark ? 'text-slate-300' : 'text-slate-600'}`}>{subtitle}</p>}
        </div>
    );
}
