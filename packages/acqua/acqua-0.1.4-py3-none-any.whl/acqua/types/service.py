#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/types/service.py
# VERSION:     0.1.4
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List, Literal
from typing_extensions import Annotated

### Third-party packages ###
from pydantic import BaseModel, Field, StrictStr

PortMapping = Annotated[StrictStr, Field(pattern=r"^\d{1,5}:\d{1,5}$")]


class Service(BaseModel):
  command: Dict[int, StrictStr] = {}
  env_vars: List[StrictStr] = []
  image: StrictStr
  ports: List[PortMapping]
  service_type: Literal["middleware", "node"] = Field(alias="type")


ServiceName = Literal["acqua-postgres", "acqua-sui", "acqua-sui-devnet", "acqua-sui-testnet"]

__all__ = ("PortMapping", "Service", "ServiceName")
