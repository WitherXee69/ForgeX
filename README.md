# ForgeX

ForgeX is an automated GitHub repository discovery and installation project.

## Current interface

ForgeX currently provides a Textual terminal interface for connecting to GitHub,
searching repositories, selecting a result, and inspecting repository details.
The interface is intentionally separated from the core services: `forgex.py`
creates the settings, context, exception handler, and fetcher, then injects them
into the UI.

## Run

1. Create and activate a virtual environment.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start ForgeX:

   ```bash
   python forgex.py
   ```

4. Enter your GitHub username and a personal access token when prompted.

The token is held in memory for the current session and is not saved to disk.

## Current features

- GitHub repository lookup by `owner/repository` or repository URL
- Repository search by name or GitHub search query
- Search results table
- Repository overview with description, stars, forks, language, update time,
  license, and a link to the GitHub page

Installation workflows and recipe execution are not part of the current UI yet.
