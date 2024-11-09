# Acqua 

[![Docker](https://img.shields.io/badge/docker-2496ED?&logo=docker&logoColor=white)](https://hub.docker.com)
[![Top](https://img.shields.io/github/languages/top/aekasitt/acqua)](https://github.com/aekasitt/acqua)
[![Languages](https://img.shields.io/github/languages/count/aekasitt/acqua)](https://github.com/aekasitt/acqua)
[![Size](https://img.shields.io/github/repo-size/aekasitt/acqua)](https://github.com/aekasitt/acqua)
[![Last commit](https://img.shields.io/github/last-commit/aekasitt/acqua/master)](https://github.com/aekasitt/acqua)

[![Acqua Banner](static/acqua-banner.svg)](https://github.com/aekasitt/acqua/blob/master/static/acqua-banner.svg)

## Getting started

You can use `acqua` simply by installing via `pip` on your Terminal.

```sh
pip install acqua
```
<details>
  <summary> Sample output when running install command </summary>

![Sample Pip Install](https://github.com/aekasitt/acqua/blob/master/static/pip-install.gif)

</details>

And build required images with `build` command. The following shows you how to build a `Testnet`
Sui Validator node with one-command.

```sh
acqua pull --mainnet
```

<details>
  <summary> Sample output when running pull command </summary>

![Sample Acqua Build](https://github.com/aekasitt/acqua/blob/master/static/acqua-pull.gif)

</details>

The initial pull may take some time as it is downloading source codes from different repositories
and interfacing with `Docker Daemon` to build according to flagged requirements. Once the pull
process completes, you can begin deploying local network with middlewares as such:

```sh
acqua deploy --mainnet
```

Note: If you do not have `postgres:latest` image in your local Docker image registry, this may
take some time to deploy on your first run.

<details>
<summary>Sample output when running deploy command</summary>

![Sample Acqua Deploy](https://github.com/aekasitt/acqua/blob/master/static/acqua-deploy.gif)


</details>

You will have docker containers running in the backend, ready to be interfaced by your local
environment applications you are developing.

## Dashboard

Acqua not only facilitates the deployment of [Bitcoin](https://twentyone.world) services
such as the [Sui](https://sui.io) Validator node with a PoW relay, but allows you to view
Node's Blockchain Information, Mempool Information, Peripheral Details and etc.

In order to view relevant metrics, launch the dashboard using the following command.

```sh
acqua dashboard
```

<details>
  <summary> Sample output when running dashboard command </summary>

![Sample Acqua Dashboard](https://github.com/aekasitt/acqua/blob/master/static/acqua-dashboard.gif)
</details>

## Contributions

### Prerequisites

* [python](https://www.python.org) version 3.9 and above
* [uv](https://docs.astral.sh/uv)
* [docker](https://www.docker.com)

### Set up local environment

The following guide walks through setting up your local working environment using `pyenv`
as Python version manager and `uv` as Python package manager. If you do not have `pyenv`
installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>
  
  ```sh
  brew install pyenv --head
  ```
</details>

<details>
  <summary> Install using standalone installer (Darwin and Linux) </summary>
  
  ```sh
  curl https://pyenv.run | bash
  ```
</details>

If you do not have `uv` installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>

  ```sh
  brew install uv
  ```
</details>

<details>
  <summary> Install using standalone installer (Darwin and Linux) </summary>

  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
</details>


Once you have `pyenv` Python version manager installed, you can
install any version of Python above version 3.8 for this project.
The following commands help you set up and activate a Python virtual
environment where `uv` can download project dependencies from the `PyPI`
open-sourced registry defined under `pyproject.toml` file.

<details>
  <summary> Set up environment and synchronize project dependencies </summary>

  ```sh
  pyenv shell 3.11.9
  uv venv  --python-preference system
  source .venv/bin/activate
  uv sync --dev
  ```
</details>

Now you have the entire project set-up and ready to be tinkered with. Try out the
standard `acqua` command which brings up a help menu.

<details>
  <summary> Launch Acqua Help </summary>

  ```sh
  $ acqua
  >  Usage: acqua [OPTIONS] COMMAND [ARGS]...
  > 
  >  acqua 
  > 
  > Options:
  >   --help  Show this message and exit.
  > 
  > Commands:
  >   auth       Persist authentications in desired run-control file.
  >   build      Build peripheral images for the desired cluster.
  >   clean      Remove all active "acqua-*" containers, drop network.
  >   dashboard  Dashboard for checking current state of images deployed.
  >   deploy     Deploy cluster.
  >   pull       Pull core and peripheral images from GitHub container registry
  ```
</details>

### Known issues

You may run into this setback when first running this project. This is a
[docker-py](https://github.com/docker/docker-py/issues/3059) issue widely known as of October 2022.

```python
docker.errors.DockerException:
  Error while fetching server API version: (
    'Connection aborted.', FileNotFoundError(
      2, 'No such file or directory'
    )
  )
```

See the following issue for Mac OSX troubleshooting.
[docker from_env and pull is broken on mac](https://github.com/docker/docker-py/issues/3059#issuecomment-1294369344)
Recommended fix is to run the following command:

```sh
sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock
```

## License

This project is licensed under the terms of the MIT license.

