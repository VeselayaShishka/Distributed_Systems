# Setup: run the supplied service

These instructions begin in the **extracted student project root**: the directory containing `README.md`, `catalog-service/`, `checks/`, `docs/` and `support/`. Keep that directory as your semester-project working directory.

You need Python 3.12 or newer, Docker Engine or Docker Desktop, and a terminal. The container is the reference runtime. Docker must be running before checkpoint 4; you can complete the local checkpoints first.

## macOS / Linux

In terminal A, from the project root:

```sh
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r catalog-service/requirements.txt
export PROJECT_STORY=greenhouse
cd catalog-service
waitress-serve --host=127.0.0.1 --port=5000 --threads=1 app:app
```

Choose `campus`, `greenhouse` or `library` before starting. An omitted `PROJECT_STORY` selects `greenhouse`. Keep terminal A open: Waitress is running in the foreground. Stop it with **Ctrl+C** before rebuilding the container or changing local runtime settings.

After changing `app.py`, stop and relaunch Waitress; this command does not reload changed source automatically. Relaunching also resets the in-memory items.

Open terminal B at the project root for requests and checks. The check program uses Python's standard library; it does not need the virtual environment.

## Windows PowerShell

In terminal A, from the project root:

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r catalog-service\requirements.txt
$env:PROJECT_STORY = "greenhouse"
cd catalog-service
..\.venv\Scripts\waitress-serve.exe --host=127.0.0.1 --port=5000 --threads=1 app:app
```

These commands call the virtual environment directly, so activating a PowerShell script is unnecessary. Keep terminal A open and use terminal B at the project root for requests/checks. In PowerShell, write **`curl.exe`**, because `curl` can refer to a different command.

## First requests

From terminal B, use `curl` on macOS/Linux or `curl.exe` on Windows:

```sh
curl -i http://127.0.0.1:5000/health
curl -i http://127.0.0.1:5000/items
curl -i http://127.0.0.1:5000/items/999
```

The starter provides health/read routes. Creation, replacement and deletion deliberately return **501**, until you implement them. A 501 response is expected incompleteness, rather than a broken installation.

## If a command fails

Use [troubleshooting](troubleshooting.md) to connect an observation to the next useful check.

If local port 5000 is occupied, use `--port=5001` for local Waitress and `http://127.0.0.1:5001` for local requests/checks. Record the change. This does not change the container's port 5000 or its later host publication. Ask the lecturer if you cannot identify a collision safely.

## Keep your work

Save code and `docs/` in your semester-project repository. Exclude `.venv/`, Python caches and generated build files. Commit useful milestones according to your usual Git workflow. If Git is new, ask for help after getting the first request working; do not let repository setup prevent checkpoint 1.
