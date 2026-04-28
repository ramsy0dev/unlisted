# v0.1.4

## performance
- switched from pytube's `check_availability()` to the YouTube oEmbed API for per-video checks — one lightweight HTTP request instead of a full page parse, roughly 10x faster per check
- deduplication is now O(1) using sets instead of linear scans over concatenated lists — no more slowdown as checked IDs accumulate

## reliability
- all shared state across threads is now properly locked — race conditions on counters and ID lists are fixed
- worker threads are now daemon threads, so Ctrl+C exits immediately instead of waiting up to 8 seconds for in-flight requests to finish
- 429 rate-limit responses are handled with exponential backoff (1s → 2s → 4s … capped at 60s) instead of counting as failed attempts

## new
- `--delay` flag: configurable delay between requests per thread in milliseconds (default 500ms) to reduce the chance of getting IP blocked
- live dashboard replacing the plain status spinner — shows found / checked / failed / blocked counters, elapsed time, and thread count, updating in real time
- results are auto-saved every 30 seconds while running, so a crash doesn't lose everything

## fixes
- proxies now correctly include an `https` key, fixing requests to the oEmbed endpoint
- `_initiate_file_output` was mutating a module-level constant dict, corrupting state across calls
