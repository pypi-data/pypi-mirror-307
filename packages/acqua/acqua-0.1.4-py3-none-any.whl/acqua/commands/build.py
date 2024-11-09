#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/commands/build.py
# VERSION:     0.1.4
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from io import BytesIO
from typing import Dict, List, Set

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import BuildError, DockerException
from rich import print as rich_print

### Local modules ###
from acqua.configs import BUILDS
from acqua.inlets import Fjord
from acqua.types import Build


@command
@option("--devnet", is_flag=True, help="Build acqua-sui-devnet image", type=bool)
@option("--mainnet", is_flag=True, help="Build acqua-sui image", type=bool)
@option("--testnet", is_flag=True, help="Build acqua-sui-testnet image", type=bool)
def build(devnet: bool, mainnet: bool, testnet: bool) -> None:
  """Build peripheral images for the desired cluster."""
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
  build_select: Dict[str, bool] = {
    "acqua-sui": mainnet,
    "acqua-sui-devnet": devnet,
    "acqua-sui-testnet": testnet,
  }

  ### Checks if specified images had been built previously ###
  outputs: List[str] = []
  built: Set[str] = {tag for tag in BUILDS.keys() if build_select[tag] and tag in image_names}
  outputs += map(lambda tag: f"<Image: '{tag}'> already exists in local docker images.", built)
  list(map(rich_print, outputs))

  builds: Dict[str, Build] = {
    tag: build for tag, build in BUILDS.items() if build_select[tag] and tag not in image_names
  }
  build_count: int = len(builds.keys())
  if build_count != 0:
    builds_items = builds.items()
    with Fjord(row_count=10) as fjord:
      task_id: int = fjord.add_task("", progress_type="primary", total=build_count)
      for tag, build in builds_items:
        build_task_id: int = fjord.add_task(tag, progress_type="build", total=100)
        with BytesIO("\n".join(build.instructions.values()).encode("utf-8")) as fileobj:
          try:
            fjord.progress_build(  # type: ignore[misc]
              client.api.build(
                container_limits={
                  "cpusetcpus": "0-3",
                  "cpushares": 4,
                  "memory": 8_589_934_592,  # 8GB
                  "memswap": 8_589_934_592,  # 8GB
                },
                decode=True,
                fileobj=fileobj,
                gzip=True,
                platform=build.platform,
                rm=True,
                shmsize=68_719_476_736,  # 64GB
                tag=tag,
              ),
              build_task_id,
            )
          except BuildError:
            fjord.update(build_task_id, completed=0)
          fjord.update(build_task_id, completed=100)
          fjord.update(task_id, advance=1)
      fjord.update(task_id, completed=build_count, description="[blue]Complete[reset]")


__all__ = ("build",)
