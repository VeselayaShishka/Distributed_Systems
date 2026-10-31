# Lab 1 — Your First Service

**Can you explain what happens when someone uses your service—and when it restarts?**

Start with the [activity guide](DSA-LAB-01-docker-rest.pdf). This folder is the opening milestone of your semester project; keep your code and observations for the next milestone. AI assistance is welcome. Make a personal prediction before each experiment, then use the observed behavior to check and correct it.

## Your route

1. Choose `campus`, `greenhouse` or `library` and complete [your short story](docs/story.md).
2. [Run the supplied service](support/setup.md) and meet its health/read routes.
3. Implement creation/validation, then replacement and deletion using the [shared contract](support/contract.md).
4. [Build, operate and restart the Docker container](support/docker.md); recreate it with a changed host publication.
5. Complete [four short observations](docs/observations.md) and the activity guide's single acceptance checklist. Be ready to operate and explain your service in the interview.

The guide explains the activity; [support](support/README.md) helps when you need a command or a diagnosis. There is no additional long report or screenshot dossier.

## Folder map

```text
catalog-service/     app.py, story profiles, pinned dependencies, Dockerfile
checks/              staged HTTP checks
docs/                your story and four observations
support/             setup, contract, Docker and troubleshooting
DSA-LAB-01-docker-rest.pdf
```

The starter supplies health/read routes and transport/error helpers. POST, PUT and DELETE return **501** until you implement them. Complete domain validation yourself; the JSON parsing helper is supplied. The Dockerfile is supplied and annotated; you build, run and inspect the resulting container.

The reference runtime is Python `3.13.13-slim`, Flask `3.1.3`, Waitress `3.0.2`, one process and one application-processing thread. Local development uses Python 3.12+. This milestone stores items in memory only.

## Staged checks

Keep the service running in terminal A. Run checks from the **project root** in terminal B. Use `python3` on macOS/Linux, or replace it with `py -3` on Windows:

```sh
python3 checks/check_service.py --stage starter --base-url http://127.0.0.1:5000
python3 checks/check_service.py --stage create --base-url http://127.0.0.1:5000
python3 checks/check_service.py --stage crud --base-url http://127.0.0.1:5000
```

Choose the stage matching your progress:

- **starter:** fresh starter process; supplied health/list/missing responses and expected 501 TODOs. Passing this stage is not final acceptance. Stop using it once you implement the mutations.
- **create:** creation and validation; the script creates its own test items and leaves them available because deletion may still be unfinished.
- **crud:** the completed contract; test items are created, updated and deleted. Cleanup is limited to the items created by this check run.

The program reads the story profile from `/health`; choose the story when launching the service, not in the check command. These checks actively mutate the service: use your own lab process, never a shared or important service. Passing checks does not replace explaining a response and its state change.

For Docker, change only the base URL:

```sh
python3 checks/check_service.py --stage crud --base-url http://127.0.0.1:8085
```

After changing publication, use port 8086. A recorded local-port fallback also needs a matching base URL. For available command options, run `python3 checks/check_service.py --help`.

## Class and home work

Session 1 covers story choice, meeting the service and valid/rejected creation. Between sessions finish creation and implement replacement/deletion. Session 2 begins with a request-path recall, follows an item through CRUD and then runs the Docker experiments. Afterward resolve remaining failures and finish the short observation record. The two 90-minute sessions are supervised learning time; the semester project also includes home work.

Three ideas to carry forward:

- A response and the resulting state should agree with the HTTP contract.
- The client address, published host port and process listener have different roles.
- A new process starts with new memory; packaging code does not persist its dictionary.
