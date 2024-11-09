#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/core.py
# VERSION:     0.1.3
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from click import group

### Local modules ###
from acqua.commands import auth, build, clean, dashboard, deploy, pull


@group
def cli() -> None:
  """acqua"""


cli.add_command(auth, "auth")
cli.add_command(build, "build")
cli.add_command(clean, "clean")
cli.add_command(dashboard, "dashboard")
cli.add_command(deploy, "deploy")
cli.add_command(pull, "pull")


if __name__ == "__main__":
  cli()
