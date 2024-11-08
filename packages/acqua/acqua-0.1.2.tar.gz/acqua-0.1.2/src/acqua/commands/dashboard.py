#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/commands/dashboard.py
# VERSION:     0.1.2
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import List

### Third-party packages ###
from click import command
from docker import DockerClient, from_env
from docker.errors import DockerException
from docker.models.containers import Container
from rich import print as rich_print

### Local modules ###
from acqua.inlets import Lagoon


@command
def dashboard() -> None:
  """Dashboard for checking current state of images deployed."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to daemon.")
    return

  daemon: Container
  try:
    daemon = next(
      filter(
        lambda container: match(r"acqua-(sui|sui-devnet|sui-testnet)", container.name),
        reversed(client.containers.list()),
      )
    )
  except StopIteration:
    rich_print("[red bold] Cannot find active daemon.")
    return

  ### Retrieve other containers ###
  acqua_containers: List[Container] = list(
    filter(lambda container: match(r"acqua-*", container.name), reversed(client.containers.list()))
  )
  container_names: List[str] = [
    name for name in map(lambda container: container.name, acqua_containers) if name is not None
  ]
  lagoon: Lagoon = Lagoon(
    containers=acqua_containers,
    container_index=0,
    container_names=container_names,
    daemon=daemon,
  )
  lagoon.display()


__all__ = ("dashboard",)
