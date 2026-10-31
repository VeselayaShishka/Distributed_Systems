# Troubleshooting: observe before changing things

Record the exact command, current directory and response/error. Change one thing at a time, then repeat the relevant check.

| Observation | Next useful check |
|---|---|
| `python3` / `py` not found | Select Python 3.12+ and reopen the terminal. |
| `No module named flask` | Was installation done with the virtual environment's Python? See [setup](setup.md). |
| `No module named app` | Run Waitress from `catalog-service/`, where `app.py` lives. |
| Local source changes do not appear | Stop/relaunch Waitress; this configuration does not reload code. |
| Address already in use | Identify the process owning the port. Preserve unrelated services; see the local fallback in [setup](setup.md). |
| Connection refused | Is the process running? Does the URL match its listening port or Docker publication? |
| 404 for a missing item | Expected application response; the service was reached. |
| 501 on a mutation route | This starter route is unfinished. Complete that checkpoint; installation and reachability may already be correct. |
| 400 on a mutation | Inspect JSON shape, field names, field types and the selected story's status values. |
| 415 on a mutation | Send `Content-Type: application/json`. |
| Docker cannot connect to its daemon | Start Docker Desktop/Engine, then run `docker version`. |
| Build cannot find a file | Run the build from the student project root with context `catalog-service`. |
| Name is already in use | Inspect the named container. Preserve another run and choose your own recorded name. |
| Container immediately stops | Inspect `docker ps -a` and `docker logs` for your container. |
| Container runs but host requests fail | Compare its published port, startup listener and your URL. Check health after startup. |
| Changed source seems ignored in Docker | Rebuild the image, then recreate your own container. Its current code was copied at build time. |
| Requests work on an unexpected port | Identify which process/container answered. Do not mix local and container state observations. |

## One diagnosis example

You recreated the container with `127.0.0.1:8086:5000`, but curl still uses 8085. Inspect `docker port` and compare it with the URL before editing the application. Correcting the host URL can repair the request without changing the inside listener.

If you need help, bring the command, directory, error/status and one relevant runtime observation. “It does not work” alone does not distinguish setup, reachability, contract and state problems.
