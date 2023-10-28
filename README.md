# Demo Project


## Dockerfile

* Rename `.env.dist` file to `.env` file <br/>
* Run `docker-compose build` <br/>
* Run `docker-compose up`

The `Dockerfile` defines the instructions for building the Docker image that is used by the bot service. The file begins
by specifying the base image that should be used for the image, which in this case is `python:3.9-buster`. The `ENV`
instruction sets the value of the `BOT_NAME` environment variable, which is used by the `WORKDIR` instruction to specify the
working directory for the container.

The `COPY` instructions are used to copy the `requirements.txt` file and the entire project directory into the image. The
`RUN` instruction is used to install the Python dependencies from the `requirements.txt` file. This allows the application
to run in the container with all the necessary dependencies.
