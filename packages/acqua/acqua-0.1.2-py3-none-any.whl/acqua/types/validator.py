#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/types/validator.py
# VERSION:     0.1.2
# CREATED:     2024-11-07 14:00
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List

### Third-party packages ###
from pydantic import BaseModel, StrictFloat, StrictStr


class Apy(BaseModel):
  address: StrictStr
  apy: StrictFloat

class Validator(BaseModel):
  apys: List[Apy]
  epoch: str


__all__ = ("Apy", "Validator")
