import '../styles/globals.css';

export const metadata = {
    title: {
        template: '%s | ChairFill',
        default: 'ChairFill — We refill your empty chairs with patients you already have'
    },
    description:
        'ChairFill reactivates your dormant patient list with AI-driven recall campaigns. Pay only for the patients we bring back. Built for dental practices in the US & UK.'
};

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <head>
                <link rel="icon" href="/favicon.svg" sizes="any" />
            </head>
            <body className="antialiased text-slate-800 bg-white">{children}</body>
        </html>
    );
}
