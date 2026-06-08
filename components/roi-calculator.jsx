'use client';

import { useState } from 'react';

export function RoiCalculator() {
    const [dormant, setDormant] = useState(1500);
    const [value, setValue] = useState(280);
    const [reactivationRate, setReactivationRate] = useState(8); // % of dormant patients we rebook

    const rebooked = Math.round((dormant * reactivationRate) / 100);
    const revenue = rebooked * value;

    const fmt = (n) => '$' + n.toLocaleString('en-US');

    return (
        <div className="grid gap-8 p-6 bg-white border shadow-sm rounded-3xl border-slate-200 sm:p-10 md:grid-cols-2">
            <div className="space-y-8">
                <Slider
                    label="Dormant / lapsed patients in your database"
                    value={dormant}
                    min={200}
                    max={6000}
                    step={100}
                    onChange={setDormant}
                    display={dormant.toLocaleString('en-US')}
                />
                <Slider
                    label="Average value of one patient visit"
                    value={value}
                    min={80}
                    max={1200}
                    step={10}
                    onChange={setValue}
                    display={fmt(value)}
                />
                <Slider
                    label="Reactivation rate (conservative: 5–10%)"
                    value={reactivationRate}
                    min={3}
                    max={15}
                    step={1}
                    onChange={setReactivationRate}
                    display={reactivationRate + '%'}
                />
            </div>

            <div className="flex flex-col justify-center p-8 text-center bg-teal-50 rounded-2xl ring-1 ring-teal-100">
                <div className="text-sm font-semibold tracking-wide text-teal-700 uppercase">
                    Estimated revenue we can recover
                </div>
                <div className="my-3 text-5xl font-extrabold text-teal-600">{fmt(revenue)}</div>
                <p className="text-slate-600">
                    from rebooking <span className="font-bold text-slate-900">{rebooked.toLocaleString('en-US')}</span> dormant
                    patients
                </p>
                <div className="pt-6 mt-6 text-sm border-t text-slate-500 border-teal-200">
                    That&apos;s revenue you already earned the right to — it just needs the right nudge. ChairFill
                    delivers that nudge automatically.
                </div>
                <a
                    href="https://calendly.com/your-handle/15min"
                    className="px-6 py-3 mt-6 text-sm font-bold text-white no-underline transition bg-teal-500 rounded-xl hover:bg-teal-600"
                >
                    Claim this revenue — book a call
                </a>
            </div>
        </div>
    );
}

function Slider({ label, value, min, max, step, onChange, display }) {
    return (
        <div>
            <div className="flex items-baseline justify-between mb-2">
                <label className="text-sm font-medium text-slate-700">{label}</label>
                <span className="text-lg font-extrabold text-slate-900">{display}</span>
            </div>
            <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={value}
                onChange={(e) => onChange(Number(e.target.value))}
                className="w-full accent-teal-500 cursor-pointer"
            />
        </div>
    );
}
