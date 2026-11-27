# ForgeX

ForgeX is a GitHub-powered repository discovery and installation project from Withering Studios. It aims to make installing GitHub-hosted projects approachable for everyone, not only developers.

**ForgeX is currently under active development.** The desktop interface and repository-discovery workflow are in place, while the `.forgeman` manifest pipeline and actual installation process are still being developed.

## Current interface

ForgeX uses a **PySide6 desktop GUI**.

The application is organized into separate layers:

- **GUI** — desktop pages and widgets for login, discovery, repository details, installation, and settings.
- **Controller** — connects UI actions to the application engine and exposes Qt signals for UI updates.
- **Engine** — coordinates repository lookup, search, and repository-detail operations.
- **Fetcher** — communicates with the GitHub REST API and retrieves repository data, README content, releases, and release-asset content.
- **Context and supporting handlers** — hold shared application state and handle GitHub/API errors.

The entry point, `forgex.py`, creates the core dependencies and injects the controller into the main window.

## Current features

- Search public GitHub repositories by name or GitHub search query.
- Look up a repository using an `owner/repository` identifier or GitHub repository URL.
- Continue anonymously without entering GitHub credentials.
- Optionally provide a GitHub username and personal access token to make authenticated API requests.
- Inspect repository descriptions and metadata, including stars, forks, language, license, and last update.
- View a selected repository's README inside ForgeX.
- Retrieve latest-release information and release-asset content through the Fetcher layer (the complete installation flow is not connected yet).
- Display GitHub/API errors through custom exception handling.

Anonymous requests are subject to GitHub's stricter unauthenticated API rate limits. Credentials are used for the current application session; ForgeX does not currently provide a completed persistent credential-storage workflow.

## Installation

1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Launch ForgeX:

   ```bash
   python forgex.py
   ```

## Installation workflow status

The installation interface is present, but the actual installer is **not implemented yet**. ForgeX is being developed around a repository manifest format named `.forgeman`.

The planned workflow is:

```text
Repository
    ↓
Release discovery
    ↓
.forgeman retrieval
    ↓
Manifest parsing and validation
    ↓
Resolved installation description
    ↓
Installer
```

The current sample manifest is available at `models/example.forgeman`. Its format is still being defined, so it should be treated as an early example rather than a finalized specification.

## Project structure

```text
ForgeX/
├── config/                 # Application settings
├── core/
│   ├── context.py          # Shared application context
│   ├── engine.py           # Core application logic
│   ├── parser.py           # Repository input parsing
│   └── handlers/
│       ├── exceptions/     # GitHub/API exception handling
│       └── repo/
│           ├── fetcher.py  # GitHub API requests
│           ├── resolver.py # Release and manifest resolution (in progress)
│           ├── validator.py# Manifest validation (in progress)
│           └── installer.py# Installation implementation (planned)
├── models/
│   └── example.forgeman    # Early manifest example
├── ui/
│   └── desktop/            # PySide6 interface, controller, pages and styles
├── forgex.py               # Application entry point
└── requirements.txt
```

## Development direction

The next development priorities are:

1. Finalize the `.forgeman` manifest specification.
2. Implement manifest parsing and validation.
3. Align the Resolver and Fetcher interfaces.
4. Resolve repository releases and their manifests.
5. Define the resolved installation object.
6. Implement and connect the installer.
7. Add background execution, progress reporting, cancellation, and end-to-end tests.

ForgeX is not ready for a production release yet. Features and the manifest format may change as development progresses.

---

Built by **Withering Studios**.
