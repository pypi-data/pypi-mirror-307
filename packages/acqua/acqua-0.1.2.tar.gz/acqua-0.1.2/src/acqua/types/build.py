#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/types/build_enum.py
# VERSION:     0.1.2
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, Literal

from pydantic import BaseModel, StrictStr


class Build(BaseModel):
  instructions: Dict[int, StrictStr]
  platform: StrictStr = "linux/amd64"


BuildEnum = Literal["acqua-sui", "acqua-sui-devnet", "acqua-sui-testnet"]


__all__ = ("Build", "BuildEnum")
