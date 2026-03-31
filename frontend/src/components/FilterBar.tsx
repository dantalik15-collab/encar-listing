"use client";

interface FilterBarProps {
  brands: string[];
  selectedBrand: string;
  yearMin: string;
  yearMax: string;
  priceMax: string;
  sortBy: string;
  onBrandChange: (brand: string) => void;
  onYearMinChange: (year: string) => void;
  onYearMaxChange: (year: string) => void;
  onPriceMaxChange: (price: string) => void;
  onSortChange: (sort: string) => void;
  onReset: () => void;
  total: number;
}

export function FilterBar({
  brands,
  selectedBrand,
  yearMin,
  yearMax,
  priceMax,
  sortBy,
  onBrandChange,
  onYearMinChange,
  onYearMaxChange,
  onPriceMaxChange,
  onSortChange,
  onReset,
  total,
}: FilterBarProps) {
  const selectClass =
    "w-full rounded-lg border border-brand-border bg-brand-card px-3 py-2.5 text-sm text-white outline-none transition-colors focus:border-brand-accent";
  const inputClass =
    "w-full rounded-lg border border-brand-border bg-brand-card px-3 py-2.5 text-sm text-white outline-none transition-colors focus:border-brand-accent placeholder:text-brand-muted";

  const hasFilters = selectedBrand || yearMin || yearMax || priceMax;

  return (
    <div className="rounded-2xl border border-brand-border bg-brand-card p-4 sm:p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-brand-muted">
          Filters
        </h2>
        <span className="text-sm text-brand-muted">
          {total} {total === 1 ? "car" : "cars"} found
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        {/* Brand */}
        <select
          value={selectedBrand}
          onChange={(e) => onBrandChange(e.target.value)}
          className={selectClass}
        >
          <option value="">All Brands</option>
          {brands.map((b) => (
            <option key={b} value={b}>
              {b}
            </option>
          ))}
        </select>

        {/* Year min */}
        <input
          type="number"
          placeholder="Year from"
          value={yearMin}
          onChange={(e) => onYearMinChange(e.target.value)}
          min={1990}
          max={2030}
          className={inputClass}
        />

        {/* Year max */}
        <input
          type="number"
          placeholder="Year to"
          value={yearMax}
          onChange={(e) => onYearMaxChange(e.target.value)}
          min={1990}
          max={2030}
          className={inputClass}
        />

        {/* Price max */}
        <input
          type="number"
          placeholder="Max price $"
          value={priceMax}
          onChange={(e) => onPriceMaxChange(e.target.value)}
          min={0}
          className={inputClass}
        />

        {/* Sort */}
        <select
          value={sortBy}
          onChange={(e) => onSortChange(e.target.value)}
          className={selectClass}
        >
          <option value="created_at">Newest</option>
          <option value="price_usd">Price</option>
          <option value="year">Year</option>
          <option value="mileage_km">Mileage</option>
        </select>

        {/* Reset */}
        {hasFilters && (
          <button
            onClick={onReset}
            className="rounded-lg border border-brand-border px-3 py-2.5 text-sm text-brand-muted transition-colors hover:border-brand-accent hover:text-brand-accent"
          >
            Reset
          </button>
        )}
      </div>
    </div>
  );
}
