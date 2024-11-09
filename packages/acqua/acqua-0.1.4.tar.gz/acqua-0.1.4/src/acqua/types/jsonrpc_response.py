#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/types/jsonrpc_response.py
# VERSION:     0.1.4
# CREATED:     2024-11-07 02:00
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Generic, Literal, TypeVar

### Third-party packages ###
from pydantic import BaseModel, StrictInt, StrictStr


T = TypeVar("T")


class JsonrpcResponse(BaseModel, Generic[T]):
  jsonrpc: Literal["2.0"]
  id: StrictInt | StrictStr
  result: T


__all__ = ("JsonrpcResponse",)
