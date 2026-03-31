"use client";

import type { Car } from "@/lib/api";

const PLACEHOLDER_IMG = "https://placehold.co/400x300/141414/737373?text=No+Photo";

function formatMileage(km: number): string {
  if (km >= 1000) {
    return `${(km / 1000).toFixed(km % 1000 === 0 ? 0 : 1)}K km`;
  }
  return `${km.toLocaleString()} km`;
}

function formatPrice(usd: number): string {
  return `$${usd.toLocaleString("en-US")}`;
}

function formatPriceKRW(krw: number): string {
  if (krw >= 10_000_000) {
    return `₩${(krw / 10_000_000).toFixed(1)}M`;
  }
  return `₩${krw.toLocaleString()}`;
}

export function CarCard({ car }: { car: Car }) {
  const imgSrc = car.image_url || PLACEHOLDER_IMG;

  return (
    <div className="card-hover group overflow-hidden rounded-2xl border border-brand-border bg-brand-card">
      {/* Фото */}
      <div className="relative aspect-[4/3] overflow-hidden bg-brand-dark">
        <img
          src={imgSrc}
          alt={`${car.brand} ${car.model} ${car.year}`}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
          loading="lazy"
          onError={(e) => {
            (e.target as HTMLImageElement).src = PLACEHOLDER_IMG;
          }}
        />
        <div className="absolute left-3 top-3">
          <span className="rounded-lg bg-brand-dark/80 px-2.5 py-1 text-xs font-medium text-white backdrop-blur-sm">
            {car.year}
          </span>
        </div>
      </div>

      {/* Контент */}
      <div className="p-4">
        <div className="mb-1 text-xs font-medium uppercase tracking-wider text-brand-accent">
          {car.brand}
        </div>
        <h3 className="mb-3 text-base font-semibold text-white line-clamp-1">
          {car.model}
        </h3>

        {/* Характеристики */}
        <div className="mb-4 flex items-center gap-4 text-xs text-brand-muted">
          <span className="flex items-center gap-1">
            <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {formatMileage(car.mileage_km)}
          </span>
          <span className="flex items-center gap-1">
            <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
            </svg>
            {car.year}
          </span>
        </div>

        {/* Цена */}
        <div className="flex items-end justify-between border-t border-brand-border pt-3">
          <div>
            <div className="text-lg font-bold text-white">
              {formatPrice(car.price_usd)}
            </div>
            <div className="text-xs text-brand-muted">
              {formatPriceKRW(car.price_krw)}
            </div>
          </div>
          <a
            href={car.detail_url}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-lg bg-brand-accent px-4 py-2 text-xs font-semibold text-brand-dark transition-colors hover:bg-brand-accent-light"
          >
            Details
          </a>
        </div>
      </div>
    </div>
  );
}
