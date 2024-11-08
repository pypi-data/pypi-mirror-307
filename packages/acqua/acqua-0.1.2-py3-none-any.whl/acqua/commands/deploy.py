#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/commands/deploy.py
# VERSION:     0.1.2
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, DockerException
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from acqua.configs import NETWORK, SERVICES
from acqua.types import Chain, Service, ServiceName


@command
@option("--devnet", cls=Chain, is_flag=True, type=bool, variants=("mainnet", "testnet"))
@option("--mainnet", cls=Chain, is_flag=True, type=bool, variants=("devnet", "testnet"))
@option("--testnet", cls=Chain, is_flag=True, type=bool, variants=("devnet", "mainnet"))
@option("--with-postgres", is_flag=True, help="Deploy postgres peripheral service", type=bool)
def deploy(
  devnet: bool,
  mainnet: bool,
  testnet: bool,
  with_postgres: bool,
) -> None:
  """Deploy cluster."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  network_select: Dict[ServiceName, bool] = {
    "acqua-sui": mainnet,
    "acqua-sui-devnet": devnet,
    "acqua-sui-testnet": testnet,
  }
  daemon_name: ServiceName = "acqua-sui"
  try:
    daemon_name = next(filter(lambda value: value[1], network_select.items()))[0]
  except StopIteration:
    pass
  daemon: Service = SERVICES[daemon_name]

  try:
    client.networks.create(NETWORK, check_duplicate=True)
  except APIError:
    pass

  for _ in track(range(1), f"Deploy { daemon_name }".ljust(42)):
    flags: List[str] = list(daemon.command.values())
    ports: Dict[str, int] = {port.split(":")[0]: int(port.split(":")[1]) for port in daemon.ports}
    client.containers.run(
      daemon.image,
      command=flags,
      detach=True,
      environment=daemon.env_vars,
      name=daemon_name,
      network=NETWORK,
      ports=ports,  # type: ignore
    )

  peripheral_selector = {"acqua-postgres": with_postgres}
  peripherals: Dict[ServiceName, Service] = {
    key: value
    for key, value in SERVICES.items()
    if value.service_type == "peripheral"
    if peripheral_selector[key]
  }
  for name, peripheral in track(peripherals.items(), f"Deploy peripheral services".ljust(42)):
    flags: List[str] = list(peripheral.command.values())
    environment: List[str] = peripheral.env_vars
    ports: Dict[str, int] = {p.split(":")[0]: int(p.split(":")[1]) for p in peripheral.ports}
    client.containers.run(
      peripheral.image,
      command=flags,
      detach=True,
      environment=environment,
      name=name,
      network=NETWORK,
      ports=ports,  # type: ignore
      volumes_from=[daemon_name],
    )


__all__ = ("deploy",)
