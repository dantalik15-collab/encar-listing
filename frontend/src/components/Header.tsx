"use client";

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-brand-border bg-brand-dark/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <a href="/" className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-accent">
            <span className="text-lg font-bold text-brand-dark">E</span>
          </div>
          <div>
            <span className="text-lg font-semibold tracking-tight text-white">
              Encar
            </span>
            <span className="text-lg font-light text-brand-accent">
              {" "}
              Listing
            </span>
          </div>
        </a>

        <nav className="hidden items-center gap-8 sm:flex">
          <a
            href="#catalog"
            className="text-sm text-brand-muted transition-colors hover:text-white"
          >
            Catalog
          </a>
          <a
            href="https://www.encar.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-brand-muted transition-colors hover:text-white"
          >
            Encar.com
          </a>
        </nav>

        <div className="flex items-center gap-3">
          <span className="hidden text-xs text-brand-muted sm:inline">
            Korean Used Cars
          </span>
          <span className="inline-flex items-center rounded-full bg-brand-accent/10 px-3 py-1 text-xs font-medium text-brand-accent">
            LIVE
          </span>
        </div>
      </div>
    </header>
  );
}
