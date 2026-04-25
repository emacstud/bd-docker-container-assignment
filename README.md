# Portugal SAF-T XML Validator API - Dockerized Python Application

## Table of Contents

- [Introduction](#introduction)
- [Sample XML files for testing](#sample-xml-files-for-testing)
- [Project Overview](#project-overview)
- [How to run and test the published Docker image](#how-to-run-and-test-the-published-docker-image)
  - [XML samples](#xml-samples)
    - [Test the `/validate` endpoint with the valid XML file](#test-the-validate-endpoint-with-the-valid-xml-file)
    - [Test the `/validate` endpoint with the invalid XML file](#test-the-validate-endpoint-with-the-invalid-xml-file)
  - [Stop and remove the container after testing](#stop-and-remove-the-container-after-testing)
  - [Notes](#notes)
- [Setting up a Docker environment](#setting-up-a-docker-environment)
- [Dockerfile](#dockerfile)
  - [Dockerfile used in this project](#dockerfile-used-in-this-project)
  - [Explanation of the Dockerfile](#explanation-of-the-dockerfile)
    - [1. Select the base image](#1-select-the-base-image)
    - [2. Define the working directory](#2-define-the-working-directory)
    - [3. Define environment variables](#3-define-environment-variables)
    - [4. Copy the dependency file first](#4-copy-the-dependency-file-first)
    - [5. Install the Python dependencies](#5-install-the-python-dependencies)
    - [6. Copy the application source files](#6-copy-the-application-source-files)
    - [7. Document the application port](#7-document-the-application-port)
    - [8. Define the container startup command](#8-define-the-container-startup-command)
  - [Result of writing a Dockerfile](#result-of-writing-a-dockerfile)
- [Build the Docker image](#build-the-docker-image)
  - [Build command used](#build-command-used)
  - [What happened during the build](#what-happened-during-the-build)
  - [Verify that the image was created](#verify-that-the-image-was-created)
  - [Result of building the Docker image](#result-of-building-the-docker-image)
- [Test the Docker image](#test-the-docker-image)
  - [Start a container from the image](#start-a-container-from-the-image)
  - [Check whether the container is running](#check-whether-the-container-is-running)
  - [Inspect application logs](#inspect-application-logs)
  - [Test the health endpoint](#test-the-health-endpoint)
  - [Test the validation endpoint with XML content](#test-the-validation-endpoint-with-xml-content)
  - [Stop the container after testing](#stop-the-container-after-testing)
  - [Result of testing the Docker image](#result-of-testing-the-docker-image)
- [Push the Docker image to a container registry](#push-the-docker-image-to-a-container-registry)
  - [Create access to the container registry](#create-access-to-the-container-registry)
  - [Log in to Docker Hub](#log-in-to-docker-hub)
  - [Building and pushing the image to Docker Hub](#building-and-pushing-the-image-to-docker-hub)
  - [Result of pushing the Docker image to a container registry](#result-of-pushing-the-docker-image-to-a-container-registry)

## Introduction

This project was developed as part of the task **"Creating a Python Code and Packaging it into a Docker Container."**

For this task, I implemented a **Python web API built with FastAPI** that validates XML files against a **Portugal SAF-T XSD schema**. The application receives XML content through an HTTP request, validates it using the provided schema file, and returns a structured JSON response indicating whether the XML is valid and, if not, which validation errors were found.

> **What is SAF-T?**  
> The Standard Audit File for Tax (SAF-T) is an electronic reporting format designed to standardize the exchange of accounting and tax data between businesses and tax authorities. In Portugal, SAF-T is a mandatory XML-based file format used to report accounting, invoicing, and transport document data to the Autoridade Tributária e Aduaneira (AT).

This project is a good candidate for containerization because it:

- is a self-contained Python application,
- uses external dependencies,
- includes static resources required at runtime,
- exposes HTTP endpoints,
- and can be easily deployed and executed in a Docker container.

---

## Sample XML files for testing

Two sample XML files are included in the `samples/` directory for testing the API:

- `samples/valid.xml` - an example expected to return `"valid": true`
- `samples/invalid.xml` - an example expected to return `"valid": false`

They can be tested with the following commands:

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/xml" \
  --data-binary @samples/valid.xml

curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/xml" \
  --data-binary @samples/invalid.xml
```

---

## Project Overview

The API exposes two endpoints:

- `GET /health`  
  Returns a simple health status response to confirm that the service is running.

- `POST /validate`  
  Accepts XML content in the request body, validates it against the XSD schema, and returns a JSON response containing:
  - whether the XML is valid,
  - a list of validation errors,
  - and the total number of detected errors.

The project is organized into separate Python modules to keep the code structured and maintainable:

- `app.py` - defines the FastAPI application and HTTP endpoints
- `validator.py` - contains the XML validation logic
- `models.py` - defines typed response models using `TypedDict`
- `resources/saftpt1.04_01.xsd` - the XSD schema used for validation

---

## How to run and test the published Docker image

The published Docker image for this project is:

```text
emacstud/saft-validator:1.0
```

To download the image from Docker Hub, run:

```bash
docker pull emacstud/saft-validator:1.0
```

Start the container with the following command:

```bash
docker run -d --name saft-validator-container -p 8000:8000 emacstud/saft-validator:1.0
```

This command:

- starts the container in detached mode,
- names it `saft-validator-container`,
- and publishes port `8000` from the container to port `8000` on the host machine.

Once started, the API will be available at:

```text
http://localhost:8000
```

To confirm that the API is running correctly, test the `/health` endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

### XML samples

Two sample XML files are included in the `samples/` directory of this repository for testing the API:

- `samples/valid.xml` - an example expected to return `"valid": true`
- `samples/invalid.xml` - an example expected to return `"valid": false`

The sample files are not added to the Docker image, as image is intended to be a standalone and produciton ready application, thus, the sample files are included only in the repository and must be saved locally in order to test the application.

#### Test the `/validate` endpoint with the valid XML file

Run the following command from the root of the repository:

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/xml" \
  --data-binary "@samples/valid.xml"
```

Expected result:

```json
{
  "valid": true,
  "errors": [],
  "number_errors": 0
}
```

#### Test the `/validate` endpoint with the invalid XML file

Run the following command:

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/xml" \
  --data-binary "@samples/invalid.xml"
```

Expected result:

```json
{
  "valid": false,
  "errors": [
    {
      "path": "...",
      "reason": "...",
      "message": "..."
    }
  ],
  "number_errors": 1
}
```

### Stop and remove the container after testing

When testing is complete, stop the container with:

```bash
docker stop saft-validator-container
```

Then remove it:

```bash
docker rm saft-validator-container
```

### Notes

- If port `8000` is already in use on the local machine, the container can be started on a different host port, for example:

```bash
docker run -d --name saft-validator-container -p 8080:8000 emacstud/saft-validator:1.0
```

In that case, all test requests should use `http://localhost:8080` instead of `http://localhost:8000`.

## Setting up a Docker environment

Docker Desktop was installed on the local machine to provide a containerization environment for the Python application. After installation, the setup was verified using the following commands:

```bash
docker --version
docker compose version
docker run hello-world
```

The `hello-world` container confirmed that Docker was installed and functioning correctly.

---

## Dockerfile

A `Dockerfile` is a text file that contains the instructions Docker uses to build an image. It defines the runtime environment of the application, including:

- the base operating system and Python runtime,
- the working directory inside the container,
- the application dependencies,
- the project files that need to be copied,
- environment variables,
- the port used by the application,
- and the command that should be executed when the container starts.

For this project, the Dockerfile had to be designed specifically for a **FastAPI web API** that validates XML content using an external schema. This meant that the final image needed to include not only the Python source code, but also the `requirements.txt` file and the `resources` directory containing the XSD schema used at runtime.

### Dockerfile used in this project

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY validator.py .
COPY models.py .
COPY resources ./resources

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Explanation of the Dockerfile

#### 1. Select the base image

```dockerfile
FROM python:3.12-slim
```

The first instruction defines the base image used to build the container.

In this case, the official Docker image `python:3.12-slim` was selected. This image was chosen because:

- it already includes a working Python 3.12 runtime,
- it is lightweight compared to the full Python image,
- it is suitable for API applications such as FastAPI,
- and it supports the language features used in the project.

Using an official Python base image avoids the need to install Python manually inside the container and provides a reliable starting point for the application environment.

The `slim` variant was selected to keep the image smaller and more efficient while still providing the required functionality.

#### 2. Define the working directory

```dockerfile
WORKDIR /app
```

The `WORKDIR` instruction sets the working directory inside the container to `/app`.

This means that all following instructions are executed relative to this directory. It also helps organize the contents of the container and keeps the project files in a predictable location.

Once this instruction is applied:

- copied files are placed into `/app`,
- dependency installation commands run from `/app`,
- and the FastAPI application starts from this directory.

#### 3. Define environment variables

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

Two environment variables were added to improve the behavior of Python inside the container.

##### `PYTHONDONTWRITEBYTECODE=1`

This tells Python not to generate `.pyc` bytecode files.

This is useful in a containerized environment because:

- bytecode cache files are not necessary for this project,
- it keeps the container filesystem cleaner,
- and it avoids generating extra files that do not need to be stored in the image.

##### `PYTHONUNBUFFERED=1`

This makes Python output logs immediately instead of buffering them.

This is especially useful in Docker because application logs are usually read using commands such as:

```bash
docker logs <container_name>
```

Without this setting, logs may be delayed or not appear immediately. With unbuffered output enabled, log messages from Uvicorn and the application appear in real time, which makes debugging and monitoring easier.

#### 4. Copy the dependency file first

```dockerfile
COPY requirements.txt .
```

The next step copies the `requirements.txt` file from the project directory on the host machine into the `/app` directory inside the container.

This file contains the external Python dependencies needed by the application, such as:

- FastAPI,
- Uvicorn,
- `xmlschema`,
- and any supporting packages required by the code.

Copying `requirements.txt` before the rest of the source code is an important optimization.

Docker builds images in layers. If only the application code changes later, but `requirements.txt` remains unchanged, Docker can reuse the cached dependency installation layer from a previous build. This makes rebuilds significantly faster because the dependencies do not need to be installed again every time the source code changes.

#### 5. Install the Python dependencies

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

After copying the dependency file, the next step installs all required Python packages using `pip`.

This command reads the `requirements.txt` file and installs the listed packages into the container environment.

The `--no-cache-dir` option was used to prevent `pip` from storing downloaded package archives in its cache. This helps reduce the final image size, because cached installation files are not needed after the packages are installed.

At the end of this step, the container has a complete Python environment capable of running the XML validator API.

#### 6. Copy the application source files

```dockerfile
COPY app.py .
COPY validator.py .
COPY models.py .
COPY resources ./resources
```

After installing the dependencies, the project files required by the application are copied into the container.

Each file and directory has a specific role:

##### `COPY app.py .`

This copies the main FastAPI application file into the container.

`app.py` contains:

- the FastAPI instance,
- the `/health` endpoint,
- and the `/validate` endpoint.

This file is the entry point used later by Uvicorn in the `CMD` instruction.

##### `COPY validator.py .`

This copies the XML validation logic into the container.

`validator.py` is responsible for:

- loading the schema file,
- parsing XML input,
- validating the XML against the XSD,
- and returning the structured validation response.

This file is required because `app.py` imports and uses the `validate_xml_content()` function defined there.

##### `COPY models.py .`

This copies the typed response model definitions.

`models.py` contains the `TypedDict`-based response structures used by the rest of the project, including:

- `ValidationErrorItem`
- `ValidationResponse`

Since both `app.py` and `validator.py` depend on these types, this file must also be included in the image.

##### `COPY resources ./resources`

This copies the full `resources` directory into the container. This folder contains XSD schema file.

#### 7. Document the application port

```dockerfile
EXPOSE 8000
```

The `EXPOSE` instruction documents that the application inside the container listens on port `8000`.

This matches the port used by Uvicorn to serve the FastAPI application.

It is important to note that `EXPOSE` does not automatically publish the port to the host machine. Instead, it serves as metadata that indicates which port the containerized application is expected to use.

When running the container, port publishing is still done explicitly with a command such as:

```bash
docker run -p 8000:8000 ...
```

#### 8. Define the container startup command

```dockerfile
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

The final instruction defines the command that is executed when a container is started from the image.

This command launches the FastAPI application using Uvicorn.

##### `uvicorn`

Uvicorn is the ASGI server used to run the FastAPI application.

##### `app:app`

This tells Uvicorn how to locate the application object:

- the first `app` refers to the file `app.py`,
- the second `app` refers to the FastAPI instance created inside that file.

In other words, Uvicorn loads the `app` object from `app.py`.

##### `--host 0.0.0.0`

This option is required so that the server listens on all available network interfaces inside the container.

If the application were started with the default localhost binding only, it would not be reachable from outside the container, even if port mapping were configured. By using `0.0.0.0`, the FastAPI service becomes accessible from the host system through the published Docker port.

##### `--port 8000`

This tells Uvicorn to run the application on port `8000`, which matches the `EXPOSE 8000` instruction and the port mapping used later during container testing.

### Result of writing a Dockerfile

At the end of this step, the project had a complete `Dockerfile` capable of packaging the FastAPI XML validator API into a Docker image.

The image definition included:

- the Python runtime,
- all required Python dependencies,
- the application source files,
- the XSD schema file required for XML validation,
- environment configuration for cleaner Python execution,
- and the command needed to start the API automatically.

This Dockerfile was then used in the following step to build the image and test the application inside a running container.

---

## Build the Docker image

After creating the `Dockerfile`, the next step was to build a Docker image containing the complete Python application and all of its dependencies.

### Build command used

The image was built using the following command:

```bash
docker build -t saft-validator:1.0 .
```

This command contains three important parts:

#### `docker build`
This tells Docker to build a new image from the instructions in the `Dockerfile`.

#### `-t saft-validator:1.0`
The `-t` option assigns a tag to the image.

In this case:

- `saft-validator` is the image name
- `1.0` is the version tag

#### `.`
The dot at the end represents the **build context**.

This means Docker uses the current directory as the source of all files referenced by the `Dockerfile`, such as:

- `requirements.txt`
- `app.py`
- `validator.py`
- `models.py`
- `resources/`

### What happened during the build

When the build command was executed, Docker processed the `Dockerfile` step by step:

1. downloaded the `python:3.12-slim` base image if it was not already available locally,
2. created the `/app` working directory inside the image,
3. applied the Python environment variables,
4. copied `requirements.txt` into the image,
5. installed all Python dependencies listed in the file,
6. copied the application source files into the image,
7. copied the `resources` directory containing the Portugal SAF-T XSD file,
8. documented port `8000`,
9. and stored the startup command used to launch the FastAPI application with Uvicorn.

At the end of this process, Docker produced a local image named:

```text
saft-validator:1.0
```

### Verify that the image was created

After the build completed, the local Docker images were listed using:

```bash
docker images
```

This command shows all Docker images currently available on the local machine.

It was used here to verify that the build had completed successfully and that the new image was present in the local Docker environment.

The output included an entry similar to:

```text
REPOSITORY        TAG       IMAGE ID       CREATED         SIZE
saft-validator    1.0       <image_id>     <time>          <size>
```

This confirmed that the image had been built and tagged correctly.

### Result of building the Docker image

At the end of this step, a working Docker image containing the complete application was successfully created.

The built image included:

- the Python runtime,
- all required Python dependencies,
- the FastAPI application code,
- the XML validation logic,
- the typed response models,
- and the Portugal SAF-T XSD schema file.

This image was then used in the next step to create and run a Docker container for testing.

---

## Test the Docker image

After building the Docker image, the next step was to create and run a container from that image and verify that the application worked correctly inside Docker.

### Start a container from the image

The container was started using the following command:

```bash
docker run -d --name saft-validator-container -p 8000:8000 saft-validator:1.0
```

#### `docker run`
This command creates and starts a new container from an existing image.

#### `-d`
The `-d` flag stands for **detached mode**.

This means the container runs in the background, allowing the terminal to remain available for additional commands.

#### `--name saft-validator-container`
This assigns a custom name to the container.

Using a readable name makes later commands easier to understand, because the container can be referenced by name instead of by its container ID.

#### `-p 8000:8000`
This publishes a port from the container to the host machine.

In this case:

- the first `8000` is the local machine port,
- the second `8000` is the port used by the FastAPI application inside the container.

This mapping made the API accessible through:

```text
http://localhost:8000
```

#### `saft-validator:1.0`
This is the image used to create the container.

### Check whether the container is running

After starting the container, the running containers were listed using:

```bash
docker ps
```

This command displays all currently running Docker containers.

It was used to confirm that the container had started correctly and was still running after launch.

A successful result showed:

- the container name,
- the image used,
- the container status,
- and the published port mapping.

This confirmed that Docker had successfully created and started the container from the image.

### Inspect application logs

To verify that the FastAPI application had started correctly inside the container, the container logs were checked using:

```bash
docker logs saft-validator-container
```

This command displays the logs produced by the running container.

It was particularly useful for confirming that Uvicorn had started successfully and that the application was listening on port `8000`.

When the container started correctly, the logs showed Uvicorn startup messages similar to:

- server process started,
- application startup complete,
- and Uvicorn running on `http://0.0.0.0:8000`.

### Test the health endpoint

Once the logs confirmed that the application was running, the first endpoint tested was the health check endpoint.

The following command was used:

```bash
curl http://localhost:8000/health
```

The expected response was:

```json
{"status":"ok"}
```

This confirmed that:

- the container was reachable from outside,
- the FastAPI application was running correctly,
- and the port mapping between the host and the container worked as expected.

### Test the validation endpoint with XML content

To verify that schema validation worked correctly inside the container, the endpoint was also tested with XML data (both valid and invalid).

The following command was used:

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/xml" \
  --data-binary '@path-to-xml-file'
```
This test was important because it verified that:

- the API could receive XML input,
- the `xmlschema` library had been installed correctly in the container,
- the XSD file had been copied correctly into the image,
- and the application was able to perform schema validation at runtime.

In case of invalid XML content, the returned JSON response contained a list of schema validation errors, confirming that the validation logic was functioning correctly inside the containerized environment. The valid XML input resulted in a positive answer from API

Valid XML input:
```json
{
    "valid": true,
    "errors": [],
    "number_errors": 0
}
```

Invalid XML input:
```json
{
    "valid": false,
    "errors": [
        {
            "path": "...",
            "reason": "...",
            "message": "...",
        }
    ],
    "number_errors": 1
}
```

### Stop the container after testing

After finishing the tests, the running container was stopped using:

```bash
docker stop saft-validator-container
```

This command stops a running container in a controlled way.

It was used after testing was complete so that the container would no longer continue running in the background.

### Result of testing the Docker image

This step confirmed that the Docker image worked correctly when executed as a container.

The tests showed that:

- the container started successfully,
- the application logs were available through Docker,
- the `/health` endpoint returned the expected status response,
- the `/validate` endpoint correctly handled empty requests,
- and XML validation against the Portugal SAF-T XSD schema worked inside the container.

This demonstrated that the Python application had been successfully containerized and could run in an isolated Docker environment without relying on the local Python setup.

---

## Push the Docker image to a container registry

After building and testing the Docker image locally, the final step was to publish it to a container registry so that it could be downloaded and run from another machine. For this project, **Docker Hub** was used as the container registry.

### Create access to the container registry

A Docker Hub account was used to publish the image.  
The image was pushed under the following Docker Hub namespace:

```text
emacstud
```

A repository named `saft-validator` was used for this project, producing the final image reference:

```text
emacstud/saft-validator:1.0
```

### Log in to Docker Hub

Before pushing the image, authentication with Docker Hub was required.

The following command was used:

```bash
docker login
```

### Building and pushing the image to Docker Hub

After logging in to Docker Hub, the image was built and pushed to the registry using Docker Buildx with the following command:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t emacstud/saft-validator:1.0 --push .
```

#### `docker buildx build`
This command uses Docker Buildx, an extended build tool that supports multi-platform image builds.

Unlike the standard `docker build` command, `docker buildx build` can create images for different processor architectures and push them directly to a container registry.

#### `--platform linux/amd64,linux/arm64`
This option specifies the target platforms for the build.

In this project, the image was built for:

- `linux/amd64`
- `linux/arm64`

This means the final Docker image can be used on systems with different CPU architectures, making it more portable and compatible across a wider range of environments, including Linux, Windows and MacOS.

#### `-t emacstud/saft-validator:1.0`
The `-t` option assigns the image name and tag.

In this case:

- `emacstud` is the Docker Hub username,
- `saft-validator` is the repository name,
- `1.0` is the image tag.

This produced the final published image reference:

```text
emacstud/saft-validator:1.0
```

#### `--push`
This option tells Docker Buildx to push the built image directly to Docker Hub after the build process completes.

Because `--push` was used, it was not necessary to run a separate `docker push` command afterward.

#### `.`
The dot at the end specifies the current directory as the build context.

This allowed Docker to access all files required by the `Dockerfile`, including:

- `requirements.txt`
- `app.py`
- `validator.py`
- `models.py`
- `resources/saftpt1.04_01.xsd`

### Result of pushing the Docker image to a container registry

The procedure successfully built and pushed the Docker image to Docker Hub.

Because the image was built for multiple platforms, Docker Hub stored a multi-architecture image manifest under a single image tag. This means the same tag can be used on different systems, and Docker will automatically pull the correct image version for the user's architecture.

The final published image tag is:

```text
emacstud/saft-validator:1.0
```

This image can now be pulled and run using:

```bash
docker pull emacstud/saft-validator:1.0
docker run -p 8000:8000 emacstud/saft-validator:1.0
```