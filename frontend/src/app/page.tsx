"use client";

import { useCallback, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchBrands, fetchCars } from "@/lib/api";
import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { FilterBar } from "@/components/FilterBar";
import { CarCard } from "@/components/CarCard";
import { Footer } from "@/components/Footer";

const PAGE_SIZE = 20;

export default function Home() {
  const [brand, setBrand] = useState("");
  const [yearMin, setYearMin] = useState("");
  const [yearMax, setYearMax] = useState("");
  const [priceMax, setPriceMax] = useState("");
  const [sortBy, setSortBy] = useState("created_at");
  const [page, setPage] = useState(0);

  const { data: brandsData } = useQuery({
    queryKey: ["brands"],
    queryFn: fetchBrands,
  });

  const { data, isLoading, isError } = useQuery({
    queryKey: ["cars", brand, yearMin, yearMax, priceMax, sortBy, page],
    queryFn: () =>
      fetchCars({
        brand: brand || undefined,
        year_min: yearMin ? Number(yearMin) : undefined,
        year_max: yearMax ? Number(yearMax) : undefined,
        price_max_usd: priceMax ? Number(priceMax) : undefined,
        sort_by: sortBy,
        offset: page * PAGE_SIZE,
        limit: PAGE_SIZE,
      }),
  });

  const handleReset = useCallback(() => {
    setBrand("");
    setYearMin("");
    setYearMax("");
    setPriceMax("");
    setSortBy("created_at");
    setPage(0);
  }, []);

  const totalPages = data ? Math.ceil(data.total / PAGE_SIZE) : 0;

  return (
    <>
      <Header />
      <Hero />

      <main
        id="catalog"
        className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-12 lg:px-8"
      >
        {/* Фильтры */}
        <FilterBar
          brands={brandsData?.brands || []}
          selectedBrand={brand}
          yearMin={yearMin}
          yearMax={yearMax}
          priceMax={priceMax}
          sortBy={sortBy}
          onBrandChange={(v) => { setBrand(v); setPage(0); }}
          onYearMinChange={(v) => { setYearMin(v); setPage(0); }}
          onYearMaxChange={(v) => { setYearMax(v); setPage(0); }}
          onPriceMaxChange={(v) => { setPriceMax(v); setPage(0); }}
          onSortChange={(v) => { setSortBy(v); setPage(0); }}
          onReset={handleReset}
          total={data?.total || 0}
        />

        {/* Контент */}
        <div className="mt-8">
          {isLoading && (
            <div className="flex items-center justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-brand-border border-t-brand-accent" />
            </div>
          )}

          {isError && (
            <div className="flex flex-col items-center justify-center py-20 text-center">
              <p className="mb-2 text-lg font-semibold text-white">
                Failed to load cars
              </p>
              <p className="text-sm text-brand-muted">
                Please make sure the backend API is running and try again.
              </p>
            </div>
          )}

          {data && data.items.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 text-center">
              <p className="mb-2 text-lg font-semibold text-white">
                No cars found
              </p>
              <p className="text-sm text-brand-muted">
                Try adjusting your filters or run the scraper first.
              </p>
            </div>
          )}

          {data && data.items.length > 0 && (
            <>
              {/* Сетка карточек */}
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {data.items.map((car) => (
                  <CarCard key={car.id} car={car} />
                ))}
              </div>

              {/* Пагинация */}
              {totalPages > 1 && (
                <div className="mt-10 flex items-center justify-center gap-2">
                  <button
                    onClick={() => setPage((p) => Math.max(0, p - 1))}
                    disabled={page === 0}
                    className="rounded-lg border border-brand-border px-4 py-2 text-sm text-brand-muted transition-colors hover:border-brand-accent hover:text-white disabled:opacity-30 disabled:hover:border-brand-border disabled:hover:text-brand-muted"
                  >
                    Previous
                  </button>
                  <span className="px-4 text-sm text-brand-muted">
                    {page + 1} / {totalPages}
                  </span>
                  <button
                    onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                    disabled={page >= totalPages - 1}
                    className="rounded-lg border border-brand-border px-4 py-2 text-sm text-brand-muted transition-colors hover:border-brand-accent hover:text-white disabled:opacity-30 disabled:hover:border-brand-border disabled:hover:text-brand-muted"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </main>

      <Footer />
    </>
  );
}
