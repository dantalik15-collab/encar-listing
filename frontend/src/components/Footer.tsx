export function Footer() {
  return (
    <footer className="mt-auto border-t border-brand-border bg-brand-dark">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-brand-accent">
              <span className="text-sm font-bold text-brand-dark">E</span>
            </div>
            <span className="text-sm text-brand-muted">
              Encar Listing — Korean Used Cars
            </span>
          </div>
          <div className="flex items-center gap-6 text-xs text-brand-muted">
            <span>
              Data sourced from{" "}
              <a
                href="https://www.encar.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-brand-accent transition-colors hover:text-brand-accent-light"
              >
                Encar.com
              </a>
            </span>
            <span>Test assignment project</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
