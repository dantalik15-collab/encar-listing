"use client";

export function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-brand-border bg-brand-dark">
      {/* Градиентный фон */}
      <div className="absolute inset-0 bg-gradient-to-br from-brand-accent/5 via-transparent to-transparent" />

      <div className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="max-w-2xl">
          <p className="mb-3 text-sm font-medium uppercase tracking-widest text-brand-accent">
            Korean Used Cars
          </p>
          <h1 className="mb-4 text-4xl font-bold tracking-tight text-white sm:text-5xl">
            Premium vehicles
            <br />
            <span className="text-brand-accent">from South Korea</span>
          </h1>
          <p className="mb-8 text-base leading-relaxed text-brand-muted sm:text-lg">
            Browse curated selection of quality vehicles from Encar — Korea's
            largest automotive marketplace. Updated daily.
          </p>
          <a
            href="#catalog"
            className="inline-flex items-center gap-2 rounded-xl bg-brand-accent px-6 py-3 text-sm font-semibold text-brand-dark transition-colors hover:bg-brand-accent-light"
          >
            Browse Catalog
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M19 9l-7 7-7-7" />
            </svg>
          </a>
        </div>

        {/* Декоративные числа */}
        <div className="mt-12 grid grid-cols-3 gap-6 border-t border-brand-border pt-8 sm:max-w-md">
          <div>
            <div className="text-2xl font-bold text-white">240K+</div>
            <div className="text-xs text-brand-muted">Listings on Encar</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-white">Daily</div>
            <div className="text-xs text-brand-muted">Data updates</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-white">KRW</div>
            <div className="text-xs text-brand-muted">& USD prices</div>
          </div>
        </div>
      </div>
    </section>
  );
}
