export interface Car {
  id: string;
  encar_id: string;
  brand: string;
  model: string;
  year: number;
  mileage_km: number;
  price_krw: number;
  price_usd: number;
  image_url: string | null;
  detail_url: string;
  created_at: string;
  updated_at: string;
}

export interface CarsListResponse {
  items: Car[];
  total: number;
  offset: number;
  limit: number;
}

export interface BrandsResponse {
  brands: string[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

export async function fetchCars(params: {
  brand?: string;
  year_min?: number;
  year_max?: number;
  price_max_usd?: number;
  sort_by?: string;
  offset?: number;
  limit?: number;
}): Promise<CarsListResponse> {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });

  const res = await fetch(`${API_BASE}/cars?${searchParams.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch cars");
  return res.json();
}

export async function fetchBrands(): Promise<BrandsResponse> {
  const res = await fetch(`${API_BASE}/brands`);
  if (!res.ok) throw new Error("Failed to fetch brands");
  return res.json();
}
