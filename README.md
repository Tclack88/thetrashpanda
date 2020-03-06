# Trash Panda Object Detection API

A Flask REST API to receive image data, run it through an object detection model, and send back the appropriate prediction(s).

- [Contributors](#contributors)
- [Overview](#overview)
  - [Trash Panda](#trash-panda)
  - [Object detection API](#object-detection-api)
    - [API details](#api-details)
- [Usage](#usage)
  - [Object detection](#object-detection)
    - [Weights](#weights)
    - [Routes and requests](#routes-and-requests)
  - [Database queries](#database-queries)
    - [List of clusters and materials](#list-of-clusters-and-materials)
    - [Materials list for a specific cluster](#materials-list-for-a-specific-cluster)
  - [Tests](#tests)
- [Setup](#setup)
  - [Running locally (without Docker)](#running-locally-without-docker)
    - [Setting Up the environment](#setting-up-the-environment)
    - [Running the dev server](#running-the-dev-server)
  - [Running locally (with Docker)](#running-locally-with-docker)
    - [Build the image](#build-the-image)
    - [Run the container](#run-the-container)
    - [Stop the container](#stop-the-container)
- [Deploy](#deploy)
  - [Elastic Beanstalk](#elastic-beanstalk)
  - [Heroku](#heroku)
- [Contributing](#contributing)
  - [Issue/Bug Request](#issuebug-request)
  - [Feature Requests](#feature-requests)
  - [Pull Requests](#pull-requests)
    - [Pull Request Guidelines](#pull-request-guidelines)
  - [Attribution](#attribution)
- [Documentation](#documentation)

---

## Contributors

|                                              [Timothy Hsu](https://github.com/TimTree)                                               |                                          [Tobias Reaper](https://github.com/tobiasfyi)                                          |                                              [Trevor Clack](https://github.com/tclack88)                                              |                                             [Vera Mendes](https://github.com/VeraMendes)                                             |
| :----------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------: |
|         [<img src="https://avatars2.githubusercontent.com/u/7098478?s=460&v=4" width = "200" />](https://github.com/TimTree)         |    [<img src="https://avatars0.githubusercontent.com/u/45893143?s=400&v=4" width = "200" />](https://github.com/tobias-fyi)     |        [<img src="https://avatars3.githubusercontent.com/u/39845330?s=460&v=4" width = "200" />](https://github.com/tclack88)         |       [<img src="https://avatars0.githubusercontent.com/u/54785435?s=460&v=4" width = "200" />](https://github.com/VeraMendes)       |
|                         [<img src="https://github.com/favicon.ico" width="15">](https://github.com/TimTree)                          |                     [<img src="https://github.com/favicon.ico" width="15">](https://github.com/tobias-fyi)                      |                         [<img src="https://github.com/favicon.ico" width="15">](https://github.com/tclack88)                          |                        [<img src="https://github.com/favicon.ico" width="15">](https://github.com/VeraMendes)                        |
| [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/timothy-hsu-72877a171/) | [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/tobias-ea-reaper/) | [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/trevor-clack-774696184/) | [<img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15">](https://www.linkedin.com/in/vera-mendes-1b7a60191/) |

![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)

---

## Overview

### Trash Panda

[Trello Board](https://github.com/Lambda-School-Labs/trashpanda-ds/projects)

[Product Canvas](https://www.notion.so/d2e8748fdffe4c66a0a6641582dd6b63?v=4c919ea10f204aa89cd9184d59a9e6f4)

Trash Panda is an app that, with the help of an image recognition AI, makes it easier to start and maintain better recycling habits. You may search through a list of categories, enter in a material to our search bar, or use your camera to scan the item and discover how to properly dispose of your material! A lot of things end up in garbage bags sent off to the landfill when they might have a better way of being disposed. With Trash Panda, you will become wiser at disposing items and be better to our planet!

You’ll receive proper disposal information specific to your location if you live in the USA. Currently, Trashpanda provides international users with an AI result and general information about how materials can be disposed of properly, but it will not provide disposal locations for international postal codes.

### Object detection API

This repository contains code for the object detection API that is part of the Trash Panda application. The production app (PWA) can be viewed via mobile browsers (Safari on iOS) at [thetrashpanda.com](https://thetrashpanda.com/). For Android users, the app can be installed via the [Google Play Store](https://play.google.com/store/apps/details?id=com.thetrashpanda.twa).

The application is built using a number of different technologies, as outlined in the following repositories:

- Front End
  - [trashpanda-fe: front-end built with React](https://github.com/Lambda-School-Labs/trashpanda-fe)
- Back End
  - [trashpanda-be: back-end built with Node.js, Apollo, and GraphQL](https://github.com/Lambda-School-Labs/trashpanda-be)
- Data Science / Machine Learning
  - [trashpanda-ds: Exploration and Data Engineering](https://github.com/Lambda-School-Labs/trashpanda-ds)
  - [trashpanda-ds-api: object detection API built with Flask](https://github.com/Lambda-School-Labs/trashpanda-ds-api)

#### API details

The core of the API is built on Flask and Flask-RESTPlus, and (optionally) containerized using Docker.

The production app is currently deployed to [AWS Elastic Beanstalk](http://trashpanda-detect.eba-acqmen85.us-east-2.elasticbeanstalk.com/).

A relatively simple image read/write package `imageio` is used to convert base64-encoded images into numpy arrays, which are fed directly into the object detection model. The model used for inference is built from the trained darknet weights files by way of the OpenCV [DNN](https://docs.opencv.org/trunk/d6/d0f/group__dnn.html) (Deep Neural Networks) module, which reads the weights file and provides an API for making predictions.

---

## Usage

The following directions outline how the API is currently set up to accept requests and return responses.

### Object detection

#### Weights

In order to utilize the object detection route, the proper weights file must be present in `detect/api/yolo_config/`. The latest weights to be deployed are `yolo-obj_14000.weights`, which can be downloaded from the [Trash Panda Google Drive](https://drive.google.com/drive/folders/1QCYMkHYSGpHGwbaWPkVT3IUYBkkri70y?usp=sharing).

If you want to use different weights, place the file in the `yolo_config/` directory and update the path as needed in `detect/api/detect.py`. The `weights_path` variable should match the name of the weights file in `yolo_config/`.

#### Routes and requests

The primary object detection route accepts _only_ POST requests. Therefore, accessing the `detect/` route via the browser will display a message saying that "The method is not allowed for the requested URL".

In the case of the Flask server being run locally:

    http://localhost:5000/detect

The POST request should be `JSON`, formatted as follows:

```json
{
    "imgb64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAjcAAAOWCA..."
}
```

> Note: in this example, the base64-encoded image string has been truncated. A valid base64 string will likely be hundreds of thousands, if not millions, of characters in length.
> There are functions in `detect/api/base_sixfour.py` that can assist with converting images to and from base64, in case you want to use your own images for testing.

You can send the proper post request via an app like Postman, or various command-line utilities. That process will not be outlined here.

If successful, the response object will look something like this:

```json
{
    "message": "success",
    "pred_time": 1.862464189529419,
    "confidence": 0.712219774723053,
    "cluster_name": "Plastic Bags",
    "cluster": "plastic_bags",
    "materials": [
        445,
        ...
    ]
}
```

### Database queries

There are also 2 routes that accept GET requests and query the database accordingly. To simplify things into a single container, the materials data is simply managed via the `materials.csv` file, which is read into a dataframe when the app server is initiated.

This method is fine considering how small the dataset is. For larger datasets, it may be necessary to utilize a separate Postgres instance.

Regardless of the setup, the following routes are configured to query for the materials and cluster data. They are not currently being actively used in the application — they're more just for informational and testing purposes.

#### List of clusters and materials

    http://localhost:5000/clusters

#### Materials list for a specific cluster

    http://localhost:5000/clusters/<cluster>

Where `<cluster>` is the name of the cluster for which the materials should be listed.

### Tests

Tests have been set up to test the endpoints. To run these tests, run the following from the repository root:

```shell
$ pytest detect/tests
```

Ideally, the output will be nice and green!

    ==================================== test session starts ====================================
    ...
    collected 9 items

    detect/tests/test_config.py ...                                                       [ 33%]
    detect/tests/test_detect.py ......                                                    [100%]

    ===================================== 9 passed in 2.42s =====================================

---

## Setup

The object detection API can be set up to run locally or deployed to the cloud. The following directions outline the primary methods of getting it set up locally.

To deploy your own version of the API to the cloud, look for resources based on the platform you will be using. Here are some resources to get you started:

- Elastic Beanstalk
  - [Deploy a Python Flask app with Docker and AWS Elastic Beanstalk](https://medium.com/@nadaa.taiyab/how-to-dockerize-your-flask-app-and-deploy-to-aws-elastic-beanstalk-9f761b7f3dba)
- Heroku
  - [Flask and Heroku for online Machine Learning Deployment](https://towardsdatascience.com/flask-and-heroku-for-online-machine-learning-deployment-425beb54a274)

### Running locally (without Docker)

#### Setting Up the environment

To get the app running, it is highly recommended that you install the necessary dependencies into a new Python virtual environment. If you don't have experience with these, there are plenty of good resources out there, such as this RealPython article: [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/).

Once you have a new virtual environment set up, you can install the necessary dependencies via `requirements.txt`:

```shell
$ pip install -r requirements.txt
```

Or, if you're using [Pipenv](https://pipenv.pypa.io/en/latest/) to manage your virtual environments and dependencies, you can run these commands from the repository root:

```shell
$ pipenv shell
$ pipenv install
```

#### Running the dev server

Once the dependencies are install, the development server can be run by first exporting the following environment variables:

```sh
export FLASK_APP=detect/__init__.py
export FLASK_ENV=development
```

These environment variables can be set either by running those as commands in the shell, or by inserting them into a `.env` file or shell config file such as `.bashrc` or `.zshrc`, and running the appropriate `$ source ~/.zshrc` command.

Once those are set, the following command, when run from the repository root, will start up the development server on localhost port 5000.

```shell
$ flask run
```

The output in the shell should be something like the following:

    * Serving Flask app "detect/__init__.py" (lazy loading)
    * Environment: development
    * Debug mode: on
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 691-830-190

### Running locally (with Docker)

The app can also be run inside of a Docker container by utilizing the included Dockerfile. Once the Docker image is built, the development server will (ideally) be up and running whenever the Docker image is running.

#### Build the image

To build the Docker image, run the following (with any extra flags you prefer to add, such as to add custom tags to the iamge) in the repository root:

```shell
$ docker build -f Dockerfile.dev .
```

The `-f` flag tells Docker to build the image using the `Dockerfile.dev` file. As the name implies, this is the Dockerfile meant for local development. That Dockerfile should not be used in production.

An example of tagging the image:

```shell
$ docker build -f Dockerfile.dev -t tpds-api:latest .
```

You should see something like this at the end of the output if it built successfully:

    ...
    Successfully built 47a13c4e8be1
    Successfully tagged tpds-api/detect:latest

To get the name of the image that was built, view the list of current images:

```shell
$ docker images
```

The top of the output should have something like the following:

    REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
    tpds-api/detect   latest    47a13c4e8be1   41 seconds ago   977MB

Yep...it is a large image. That's to be expected — machine learning models and weights do not tend to be simple nor small.

#### Run the container

Now that the image is built, it can be run inside a container:

```shell
$ docker run -p 5000:5000 tpds-api:latest
```

The `-p` flag tells Docker to map port 5000 of your machine to port 5000 of the container, which is where the Flask server is served. The `tpds-api/detect:latest` is the tag that was passed when the container was built.

    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

Look familiar?

That means the Flask server should be running and accessible via localhost port 5000 (`http://localhost:5000/`).

#### Stop the container

When finished using the local server, the container should probably be stopped. First, get the ID of the container, then pass that ID into the `$ docker stop` command as follows:

```shell
# List running docker containers
$ docker ps
```

The result should be a list of the currently-running containers.

    CONTAINER ID  IMAGE             COMMAND                  ...        PORTS                    NAMES
    f7d7d8703c78  tpds-api:latest   "/bin/sh -c 'python …"   ...        0.0.0.0:5000->5000/tcp   focused_colden

To stop a container, grad the ID and pass that into the stop command:

```shell
# Stop a container
$ docker stop f7d7d8703c78
```

---

## Deploy

One important benefit of Docker is ease of deployment. There are 3 different Dockerfiles in this repository, each one having a specific purpose:

- `Dockerfile.dev`
  - As detailed above, this one is used to build the image for setting up the API locally
- `Dockerfile`
  - Used to deploy to Elastic Beanstalk (and elsewhere, probably)
- `Dockerfile.prod`
  - Used to deploy to Heroku

### Elastic Beanstalk

When deploying to AWS Elastic Beanstalk, it is highly recommended to install and use the [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html). We ran into many issues attempting to deploy via the zip/upload method.

Here is the EB documentation that was used to initially [deploy to EB using a single Docker container](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/single-container-docker.html).

Note: in order to deploy using the method described here, the `.weights` file must be committed to version control (and downloaded, if not done already). One method is to create a new git branch for deployment: `$ git checkout -b deploy`.

Once that branch is created and active (both done via the command above), uncomment out the relevant line in `.gitignore`:

```.gitignore
# *.weights
```

Then commit the `.gitignore` and `*.weights` files:

```shell
$ git add .gitignore
$ git add detect/api/yolo_config/yolo-obj_14000.weights
$ git commit -m "Added weights to vc to deploy to elastic beanstalk"
```

As the `.weights` files are too large to get pushed to GitHub, be sure to only use that branch for deploying to EB. Removing large files from git history is not a very fun process, so don't forget!

Once the CLI is installed and the new deployment branch created (but not pushed to GitHub), with the weights files committed to that branch, run the following commands from the repository root:

```shell
# Initialize the EB application
$ eb init -p docker detect-api

# Create environment and deploy
# This will take a while as it needs to upload the entire ~250mb
$ eb create detect-api

# If successful, open the app in default browser (or go into AWS console)
$ eb open
```

### Heroku

To deploy to Heroku using Docker, the production image will be built from `Dockerfile.prod`, uploaded to the Heroku container registry, then released to the application. As is the case with Elastic Beanstalk, using the Heroku CLI is the recommended method and is what is outlined here.

First, create the Heroku app:

```shell
$ heroku create
```

The output should be something like this:

    Creating app... done, ⬢ gentle-mesa-73091
    https://gentle-mesa-73091.herokuapp.com/ | https://git.heroku.com/gentle-mesa-73091.git

Then log into the Heroku container registry.

```shell
$ heroku container:login
```

Build the production image using `Dockerfile.prod` and tagging it with the app name as the output will show. In the example, the app name is `gentle-mesa-73091`.

```shell
$ docker build -f Dockerfile.prod -t registry.heroku.com/gentle-mesa-73091/web .
```

Obviously you'll want to replace `gentle-mesa-73091` with the name of your app. And once again, if the build was successful you should see the final lines of the output looking like this:

    ...
    Successfully built de499972f2fa
    Successfully tagged registry.heroku.com/gentle-mesa-73091/web:latest

To test it out locally before the final deployment, run the following:

```shell
$ docker run --name trashpanda-ds-api -e "PORT=8765" -p 5002:8765 registry.heroku.com/gentle-mesa-73091/web:latest
```

If everyone worked out, you should now be able to visit `http://localhost:5002/` (or whatever post you bound it to in the above command) and test out the API.

If you're happy with it, then push it up to the Heroku container registry (once again replacing the app name with yours).

```shell
$ docker push registry.heroku.com/gentle-mesa-73091/web:latest
```

Once that pushes up, all that's left is to release the container to the web. Because of the way it's tagged, it will be associated with the Heroku app.

```shell
$ heroku container:release web
```

You should then be able to visit the app and test out the deployed API!

In this example, the app would be live at `https://gentle-mesa-73091.herokuapp.com/`.

---

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**

- Check first to see if your issue has already been reported.
- Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
- Create a live example of the problem.
- Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

---

## Documentation

See [Backend Documentation](https://github.com/Lambda-School-Labs/trashpanda-be) for details on the backend of our project.

See [Front End Documentation](https://github.com/Lambda-School-Labs/trashpanda-fe) for details on the front end of our project.

See [Exploration and Data Engineering](https://github.com/Lambda-School-Labs/trashpanda-ds) for details on the data science side of things.
