# Docker: build, operate and change the address

Run all commands here from the **student project root**. Finish your API first and stop the local Waitress process with Ctrl+C. Keep Docker running. Use your own selected story in both `docker run` commands below.

## Prepare without disturbing other work

```sh
docker version
docker ps -a --filter "name=^/dsa26-lab1-student$"
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

If the name `dsa26-lab1-student` already belongs to another run, preserve it and choose a unique name for your run. Replace that name consistently below. If 8085 or 8086 is occupied, identify the owner and ask the lecturer for an available pair; record any agreed change. A host process outside Docker can also occupy a port. Do not use a blanket cleanup or Docker prune.

## Build and run

```sh
docker build -t dsa26-lab1:1.0 catalog-service
docker run -d --name dsa26-lab1-student -p 127.0.0.1:8085:5000 -e PROJECT_STORY=greenhouse dsa26-lab1:1.0
docker port dsa26-lab1-student
docker logs dsa26-lab1-student
docker exec dsa26-lab1-student id
docker inspect --format '{{json .Config.Cmd}}' dsa26-lab1-student
```

The Dockerfile installs dependencies, copies the application, selects a non-root user and starts Waitress. Read its comments. Explain which instruction sets the process's command and why its listener uses `0.0.0.0:5000` inside the container. `EXPOSE 5000` describes the intended container port; **`-p` publishes it** to the host.

The container starts in the background. After each start/run, check `/health` before the next experiment; if it is not ready yet, wait briefly and retry the health request. Inspect your container's logs if it remains unavailable. A successful `docker start` reports process startup, not completion of every application initialization step.

Make requests to `http://127.0.0.1:8085`. This host address reaches the container's port 5000. It does not make `127.0.0.1:5000` the same host endpoint.

```sh
curl -i http://127.0.0.1:8085/health
curl -i -H "Content-Type: application/json" --data-binary "@item.json" http://127.0.0.1:8085/items
curl -i http://127.0.0.1:8085/items
```

On Windows use `curl.exe`. Use the ID returned by your successful creation when reading one item.

## Experiment A: stop/start the same container

First predict whether the item will remain. Record the container identity and the collection before the stop:

```sh
docker inspect --format '{{.Id}}' dsa26-lab1-student
docker stop dsa26-lab1-student
docker start dsa26-lab1-student
docker inspect --format '{{.Id}}' dsa26-lab1-student
curl -i http://127.0.0.1:8085/items
```

Allow startup to finish; inspect `docker logs` if the first request arrives too early. The container identity and publication remain. Waitress starts a new process, so its dictionary and ID counter are new. Building the code into an image did not store the changing dictionary.

This experiment concerns **application memory**. It does not establish what happens to files written into a container's filesystem or into a mounted volume.

## Experiment B: change host publication

Predict the new host address and the unchanged container port. Replace only the container you created:

```sh
docker stop dsa26-lab1-student
docker rm dsa26-lab1-student
docker run -d --name dsa26-lab1-student -p 127.0.0.1:8086:5000 -e PROJECT_STORY=greenhouse dsa26-lab1:1.0
docker port dsa26-lab1-student
curl -i http://127.0.0.1:8086/health
curl -i http://127.0.0.1:8085/health
```

An old-address failure is useful evidence only if no unrelated service now owns 8085. Compare `docker port`, the running process and your actual URL. The image and container listener still use port 5000. Docker cannot change an existing container's publication through `docker start`; here you recreated it with a different `-p` setting.

## Finish this run

```sh
docker stop dsa26-lab1-student
docker rm dsa26-lab1-student
```

Clean up only the name you recorded for your run. Keep your source, observations and built image for later use. No volumes or networks are created by this milestone.

## Useful diagnosis questions

Use [troubleshooting](troubleshooting.md) for symptom-based checks. Record the observation before trying a repair.

Further reading: [Docker build overview](https://docs.docker.com/build/concepts/overview/) and [published ports](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/).
