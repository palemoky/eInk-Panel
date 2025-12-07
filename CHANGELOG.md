# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-07

### Added
- Xiaomi speaker notification support for audio alerts
- Comprehensive test suite with 66% coverage
- Mock image generation CLI tool for debugging without hardware
- 4-level grayscale support for enhanced visual quality
- Strikethrough effect for completed TODO items
- Year-end GitHub contribution summary (auto-triggered on Dec 31st)
- Valentine's Day special greeting layout
- Holiday icon rendering system
- Language and technology icons for GitHub stats
- Octicons integration for UI elements
- System architecture diagram in documentation

### Changed
- Renamed project from `eink-dashboard` to `paper-pi`
- Refactored layout system with `LayoutHelper` for unified coordinate management
- Improved header rendering to prevent fading on partial refresh
- Optimized font loading with lazy loading to reduce Docker image size
- Refactored year-end layout with modular components
- Removed HackerNews time slots in favor of TODO time slots
- Updated TODO list management with better data source support
- Enhanced HackerNews lazy loading and pagination

### Fixed
- Header fading issue on partial refresh (now uses 4-level COLOR_BLACK)
- HackerNews pagination reset bug
- Type checking errors in layout components
- Concurrent display refresh conflicts

### Removed
- Deprecated functions from core modules
- Unnecessary GCC dependency from Dockerfile
- README.md and LICENSE files from Docker image (reduced size)
- 30-second waiting period in CI workflow

## [0.1.0] - 2025-11-30

### Added
- Initial release of Paper Pi
- Multi-mode E-Ink dashboard (Dashboard, Quote, Poetry, Wallpaper)
- Real-time weather integration (OpenWeatherMap)
- GitHub contribution statistics with visual rings
- Bitcoin price tracking with 24h change
- VPS data usage monitoring
- Customizable TODO lists with multiple data sources (Config, Gist, Notion, Sheets)
- HackerNews top stories with auto-pagination
- Holiday detection and greeting system:
  - Birthdays & Anniversaries
  - Lunar New Year (Spring Festival)
  - Mid-Autumn Festival
  - New Year's Day & Christmas
- Time-based content switching (TODO lists vs HackerNews)
- Quiet hours configuration (no refresh during sleep time)
- Async/await architecture with `asyncio` and `httpx`
- Modular design with 23+ focused modules
- Full type safety with mypy validation
- Plugin system for extensible display modes
- Event bus for decoupled component communication
- Smart caching with TTL and LRU eviction
- Unified retry mechanism with exponential backoff
- Config hot reload with `watchdog`
- Graceful shutdown handling (SIGTERM/SIGINT)
- Docker support with multi-architecture builds (arm64)
- GitHub Actions CI/CD pipeline
- Pre-commit hooks for code quality
- Commitizen for conventional commits
- Comprehensive documentation

### Infrastructure
- Python 3.14 support
- UV package manager integration (10-100x faster than pip)
- Ruff for linting and formatting
- MyPy for type checking
- Pytest with 90+ tests
- Docker Hub automated builds
- Mock driver for development without hardware

[Unreleased]: https://github.com/palemoky/paper-pi/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/palemoky/paper-pi/releases/tag/v0.1.0

## v0.2.0 (2025-12-07)

### Feat

- implement done todo display with strikethrough effect
- implement Valentine's Day
- implement year end summary
- add octicons icons
- update 12.31 layout
- update github year summary
- add draw image icon
- add language icons
- add holiday icons

### Fix

- fix partical refresh header fade
- hacker news lazy load
- fix type
- fix hn_slots
- fix mypy error

### Refactor

- remove deprecation func
- hacker news lazy load
- remove hacker news time slots
- refactor todo
- refactor year end layout
- refactor year end
- font lazy load for docker image size
- refactor header
- refactor layout

## v0.1.0 (2025-11-30)

### Feat

- correctly scales down the font for long quotes
- implement partical refresh quiet
- implement mock screenshots
- implement mutex refresh display
- support for 4 levels of grayscale
- Support for cross-day settings for HACKERNEWS_TIME_SLOTS
- implement hacker news best stories
- implement hacker news best stories
- feat: implement partial refresh
- implement github commits cross show
- implement github commit day/month/year show
- implement Christmas Tree
- implement the hacker news on the dashboard
- implement fast refresh
- refine poetry layout
- multi mode support refresh interval time
- add next refresh time
- support multi mode
- update config
- generate screenshot for test
- implement poetry, quote and movie
- Implement cleanup for old pre-release Docker images and refine release tag matching.
- weather icon replace draw
- add thunder icon
- added weather icons
- Adopt uv for dependency management, reproducible builds, and script execution.
- greating can config
- Add asynchronous year-end summary check and update its invocation to pass client.
- Implement external TODO list providers (Gist, Notion, Google Sheets) with dynamic fetching and display, including new configuration, data fetching, and layout integration.
- Implement async context manager for DataManager and update black development dependency.
- Adjust GitHub stats end time to current time and add debug logging
- Organize generated screenshots and wallpapers into category and theme-based subdirectories.
- Add pytest-xdist for concurrent testing and update development environment configurations.
- generate wallpapers with a README snippet and consolidate all image outputs to the `screenshots` directory.
- Add wallpaper mode with new configuration options and drawing functions for various themes.
- implement holidays only refresh once
- Add script to generate E-Ink panel screenshots.
- Add combined celebration for birthday and anniversary and reorder holiday detection logic.
- update Python version from 3.11 to 3.14
- Query GitHub contributions using a `to` parameter for a specific time range and enhance logging with a detailed breakdown.
- Add Git pre-commit and pre-push hooks with documentation.
- Add Douban stats, year-end summary, graceful shutdown, implement code quality checks in CI, and enhance configuration and documentation.
- Add Waveshare e-paper display hardware configuration and interface module.
- improve BTC display formatting with comma separators and explicit sign, and increase weather icon size
- add Xiaomi Box notifications for CI and release workflow failures
- implement dynamic header layout with weather icons and structured multi-column list rendering.
- Add year-end summary display, Douban stats, and an extra-large font for new content.
- Add explicit stdout logging handler and extensive debug output for GPIO environment.
- Remove `data_cache.json` and add it and `data/` to `.gitignore`.
- Centralize persistent data into a dedicated `data` directory and update Docker volumes accordingly.
- add .dockerignore for optimized builds and populate data cache with initial values.
- Introduce configurable timezone setting and apply it for consistent time calculations.
- add empty data cache file
- Add `image` declaration to eink-panel service in docker-compose.
- add manual workflow dispatch trigger and restrict Docker image builds to tag pushes.
- Add CI tests, multi-platform Docker builds to Docker Hub and GHCR, and update README with detailed Docker instructions and badges.
- Add pytest configuration for asynchronous testing and update dependencies
- Add EPD model and mock driver configuration, user info for holiday greetings, and update README for new features and Docker deployment.
- Add GitHub Actions workflow for running tests and an initial test for the dashboard layout.
- Implement EPD driver architecture with base interface, mock, and Waveshare drivers, replacing old hardware libraries.
- Introduce holiday and special date detection with dedicated full-screen UI and icons.
- add GitHub Actions workflow for multi-architecture Docker image build and push
- Introduce asynchronous data fetching, caching, and Docker containerization.
- refactor configuration, and enhance API calls with retry logic and timezone awareness.
- refactor GitHub commit fetching to GraphQL
- Implement initial e-ink dashboard application including rendering, configuration, data providers.

### Fix

- fix screenshot save path
- fix screenshot
- fix IS_SCREENSHOT_MODE=true not effect
- fix vps test
- fix vps data url error
- fix start todo
- fix vps data
- fix start error
- fix display ghosting
- fix ring and poetry layout
- fix todo blank
- fix hacker news reset page
- fix layouts
- fix layout error
- fix driver
- fix driver
- fix partial refresh getbuffer
- fix hacker news partial refresh
- fix hacker news and btc price blank
- fix Dockerfile
- fix lgpio
- fix lgpio
- fix lgpio
- fix docker run
- refine poetry layout
- fix poetry data error
- fix poetry get data error
- fix get poetry data error
- fix poetry data error
- fix bug
- fix bug
- fix bug
- fix docker hub overview picture
- fix ci
- fix import error
- fix bug
- fix bug
- fix bug
- fix test
- fix github commit count bug
- fix goals dot
- fix main import config bug
- fix github commit timezone
- fix config
- fix mode
- fix screenshot bug
- fix draw_text() bug
- fix ssl error
- fix get_todo_lists bug
- fix github cleanup package
- fix release latest bug
- fix import config error
- clean github sha256 package
- fix release env err
- fix github stale package delete
- fix warning
- fix ui
- fix github clean up old images
- fix weather icon
- fix alpha icon
- github commit date range
- fix date ui
- fix layout
- fix ui
- fix layout test
- fix ui
- add RPi.GPIO dependency
- add gpiozero dependency
- add spidev dependency
- fix pytest miss on release
- fix `get_vps_info()` call error
- Fix `import HolidayManager` error.
- Use RPi.GPIO directly for the BUSY pin to prevent gpiozero edge detection failures in Docker.
- Use `gpiozero.InputDevice` for busy pin to prevent Docker edge detection failures and update `docker-compose.yml`.
- correct Docker Hub link capitalization in README
- Corrected the casing of the Docker Hub repository name in README badges.
- correct Docker Hub repository name capitalization in README links

### Refactor

- boost startup
- refactor dashboard layout
- refactor
- refactor `main.py`
- refine poetry layout
- update drive from repo clone to git version
- refactor env
- dashboard
- dashboard
- rename dashboard_renderer.py to renderer/dashboard.py
- `main.py`
- refactor providers and layouts
- update dashboard date
- refactor holidays
- Switch Bitcoin data fetching from price to general data provider.
- remove Douban integration because need to login.
- standardize vertical alignment of layout items by introducing unified line baselines.
- remove unused loop variable `i` and `center_y` variable
- replace "BTC" text with Bitcoin symbol "₿TC" in BTC label
- rename Xiaomi notification script and device ID environment variable
- lazily initialize RPi.GPIO for BUSY pin with error handling and fallback.
- Standardize project title and image naming to kebab-case.
- directly import and use BASE_DIR from config for cache file path.
- Update provider tests to use `pytest.mark.asyncio` and mock `httpx.AsyncClient` for asynchronous operations.
- add return type hint to `get_holiday` method
- Replace if/elif/else statements with match/case for conditional logic.
