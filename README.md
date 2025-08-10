# wkhtmltopdf

## Description

Python HTTP server to convert simple HTML to PDF documents.

## How to use?

### Installing dependencies

Install [Docker](https://docs.docker.com/engine/install/) first, then build the image.

```bash
docker build -t wkhtmltopdf .
```

#### Running the server

Assuming the Docker image was built successfully, run it, exposing any host port to port 8000.

```bash
docker run --rm -it -p 8000:8000 --name wkhtmltopdf wkhtmltopdf:latest
```

There is a `run.sh` script in the root of the repository which runs the command above. To modify the host and port, run the script with the PORT environment variable:

```bash
PORT=8001 ./run.sh
```

If the server has started interactively (-it flags of the `docker run` command), it will output the current date, time, host, and port it is running on:

```
12-15-2024, 10:12:27
HTML to PDF Converter is running on 0.0.0.0:8000
Press Ctrl-C to exit...
```

To run the server in the background, run the following:

```bash
docker run --rm -d -p 8000:8000 --name wkhtmltopdf wkhtmltopdf:latest
```

To stop the server when it was started in the background run:

```bash
docker stop wkhtmltopdf
```

Or press `Ctrl-C` if it was started interactively.

#### Sending HTML document

To convert an HTML document, send it to the `/` server endpoint:

```bash
curl --silent -X POST -L localhost:8000 --data-binary "@path/to/file" > file.pdf
```

Converted PDF will be stored in `file.pdf`
