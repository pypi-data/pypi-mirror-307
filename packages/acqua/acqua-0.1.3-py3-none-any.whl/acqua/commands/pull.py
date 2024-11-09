#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/commands/pull.py
# VERSION:     0.1.3
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List, Set

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import DockerException
from docker.models.images import Image
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from acqua.configs import BUILDS


@command
@option(
  "--devnet",
  is_flag=True,
  help="Pull acqua-sui-devnet image from GitHub container registry",
  type=bool,
)
@option(
  "--mainnet", is_flag=True, help="Pull acqua-sui image from GitHub container registry", type=bool
)
@option(
  "--testnet",
  is_flag=True,
  help="Pull acqua-sui-testnet image from GitHub container registry",
  type=bool,
)
def pull(
  devnet: bool,
  mainnet: bool,
  testnet: bool,
) -> None:
  """Pull daemon images from GitHub container registry."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  image_names: List[str] = list(
    map(
      lambda image: image.tags[0].split(":")[0],
      filter(lambda image: len(image.tags) != 0, client.images.list()),
    )
  )
  pull_select: Dict[str, bool] = {
    "acqua-sui": mainnet,
    "acqua-sui-devnet": devnet,
    "acqua-sui-testnet": testnet,
  }

  ### Checks if specified images had been built previously ###
  outputs: List[str] = []
  built: Set[str] = {tag for tag in BUILDS.keys() if pull_select[tag] and tag in image_names}
  outputs += map(lambda tag: f"<Image: '{tag}'> already exists in local docker images.", built)
  list(map(rich_print, outputs))

  outputs = []
  pullables: List[str] = [
    tag for tag in BUILDS.keys() if pull_select[tag] and tag not in image_names
  ]
  pull_count: int = len(pullables)
  if pull_count != 0:
    for pullable in track(pullables, "Pulling images from ghcr.io".ljust(35)):
      client.images.pull(f"ghcr.io/aekasitt/{ pullable }:latest")
      image: Image = client.images.get(f"ghcr.io/aekasitt/{ pullable }:latest")
      image.tag(pullable)
      outputs.append(f"<Image '{ pullable }'> pulled from registry.")
  list(map(rich_print, outputs))


__all__ = ("pull",)
