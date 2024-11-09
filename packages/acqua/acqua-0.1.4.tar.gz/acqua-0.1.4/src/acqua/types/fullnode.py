#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/types/fullnode.py
# VERSION:     0.1.4
# CREATED:     2024-11-08 13:25
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List

### Third-party packages ###
from pydantic import BaseModel, Field, StrictStr


class SeedPeer(BaseModel):
  address: StrictStr
  peer_id: StrictStr = Field(alias="peer-id")


class P2pConfig(BaseModel):
  seed_peers: List[SeedPeer] = Field(alias="seed-peers")


class Fullnode(BaseModel):
  p2p_config: P2pConfig = Field(alias="p2p-config")


__all__ = ("Fullnode", "P2pConfig", "SeedPeer")
