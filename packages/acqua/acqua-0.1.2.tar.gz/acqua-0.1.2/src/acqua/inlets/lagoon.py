#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/inlets/lagoon.py
# VERSION:     0.1.2
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from functools import reduce
from json import dumps
from re import Match, search
from typing import ClassVar, Dict, List, Optional

### Third-party packages ###
from blessed import Terminal
from blessed.keyboard import Keystroke
from docker.models.containers import Container
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr, TypeAdapter
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

### Local modules ###
from acqua.inlets.estuary import Estuary
from acqua.types import JsonrpcResponse, Validator


class Lagoon(BaseModel):
  model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)  # type: ignore[misc]
  container_index: StrictInt = 0
  container_names: List[StrictStr] = []
  containers: List[Container] = []
  daemon: Container

  ### Split layouts ###
  body: ClassVar[Layout] = Layout(name="body", minimum_size=4, ratio=8, size=17)
  straits: ClassVar[Layout] = Layout(name="straits", size=20)
  footer: ClassVar[Layout] = Layout(name="footer", size=3)
  main: ClassVar[Layout] = Layout(size=72)
  pane: ClassVar[Layout] = Layout()
  sidebar: ClassVar[Layout] = Layout(size=24)
  estuary: ClassVar[Estuary] = Estuary(height=16, width=72)

  ### Terminal ###
  terminal: ClassVar[Terminal] = Terminal()

  def model_post_init(self, _) -> None:  # type: ignore[no-untyped-def]
    self.pane.split_row(self.sidebar, self.main)
    self.main.split_column(self.body, self.footer)
    self.sidebar.split_column(self.straits)

  def display(self) -> None:
    with self.terminal.cbreak(), self.terminal.hidden_cursor(), Live(
      self.pane, refresh_per_second=4, transient=True
    ):
      try:
        while True:
          container_name: str = self.container_names[self.container_index]
          keystroke: Keystroke = self.terminal.inkey(timeout=0.25)
          if keystroke.code == self.terminal.KEY_UP and self.container_index > 0:
            self.container_index -= 1
          elif (
            keystroke.code == self.terminal.KEY_DOWN
            and self.container_index < len(self.container_names) - 1
          ):
            self.container_index += 1
          elif keystroke in {"Q", "q"}:
            raise StopIteration

          container_rows: str = ""
          if self.container_index > 0:
            container_rows = "\n".join(self.container_names[: self.container_index])
            container_rows += f"\n[reverse]{self.container_names[self.container_index]}[reset]\n"
          else:
            container_rows = f"[reverse]{self.container_names[self.container_index]}[reset]\n"
          if self.container_index < len(self.container_names) - 1:
            container_rows += "\n".join(self.container_names[self.container_index + 1 :])
          self.pane["straits"].update(Panel(container_rows, title="domains"))
          container_name: str = self.container_names[self.container_index]

          ### Body ###
          body_table: Table = Table(expand=True, show_lines=True)
          body_table.add_column(container_name, "dark_sea_green bold")
          network: Optional[Match] = search(
            r"(?<=acqua)-(sui|sui-devnet|sui-testnet)", container_name
          )
          if network:
            data: dict = {
              "id": "chain-id",
              "jsonrpc": "2.0",
              "method": "sui_getTotalTransactionBlocks",
              "params": [],
            }
            chain_identifier: JsonrpcResponse[str] = TypeAdapter(
              JsonrpcResponse[str]
            ).validate_json(
              self.daemon.exec_run(
                f"""
                curl -sSL "http://localhost:9000" -H "Content-Type: application/json" -X POST --data-raw '{dumps(data)}'
                """
              ).output
            )
            data["method"] = "sui_getLatestCheckpointSequenceNumber"
            latest_checkpoint: JsonrpcResponse[int] = TypeAdapter(JsonrpcResponse[int]).validate_json(
              self.daemon.exec_run(
                f"""
                curl -sSL "http://localhost:9000" -H "Content-Type: application/json" -X POST --data-raw '{dumps(data)}'
                """
              ).output
            )
            data["method"] = "suix_getReferenceGasPrice"
            reference_gas_price: JsonrpcResponse[str] = TypeAdapter(
              JsonrpcResponse[str]
            ).validate_json(
              self.daemon.exec_run(
                f"""
                curl -sSL "http://localhost:9000" -H "Content-Type: application/json" -X POST --data-raw '{dumps(data)}'
                """
              ).output
            )
            data["method"] = "suix_getValidatorsApy"
            validators_apy: JsonrpcResponse[Validator] = TypeAdapter(
              JsonrpcResponse[Validator]
            ).validate_json(
              self.daemon.exec_run(
                f"""
                curl -sSL "http://localhost:9000" -H "Content-Type: application/json" -X POST --data-raw '{dumps(data)}'
                """
              ).output
            )
            average_apy: float = reduce(
              lambda accumulated, validator_apy: accumulated + validator_apy.apy, validators_apy.result.apys, 0.0
            )
            body_table.add_row(
              Text.assemble(
                "\n",
                ("Chain", "bold"),
                "\n".ljust(15),
                ("Chain Identifier:".ljust(24), "green bold"),
                f"{chain_identifier.result}".rjust(16),
                "\n".ljust(15),
                ("Latest Checkpoint:".ljust(24), "bright_magenta bold"),
                f"{latest_checkpoint.result}".rjust(16),
                "\n".ljust(15),
                ("Reference Gas Price:".ljust(24), "cyan bold"),
                f"{reference_gas_price.result}".rjust(16),
                "\n".ljust(15),
                ("Average Validators APY:".ljust(24), "light_coral bold"),
                f"{average_apy}".rjust(16),
                "\n",
              )
            )
          else:
            body_table.add_row(self.estuary.renderable)
          self.pane["body"].update(body_table)

          ### Footer ###
          self.pane["footer"].update(
            Panel(
              Text.assemble(
                "Select:".rjust(16),
                (" ↑↓ ", "bright_magenta bold"),
                " " * 16,
                "Exit:".rjust(16),
                ("  Q ", "red bold"),
              )
            )
          )
      except StopIteration:
        print("If you cling to life, you live in fear of death.")


__all__ = ("Lagoon",)
