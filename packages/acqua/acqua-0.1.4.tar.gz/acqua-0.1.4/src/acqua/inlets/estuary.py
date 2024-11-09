#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/acqua/inlets/estuary.py
# VERSION:     0.1.4
# CREATED:     2024-10-24 14:29
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from math import pi, sin
from random import randint
from time import time
from typing import ClassVar, List

### Third-party packages ###
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel, ConfigDict, StrictInt, StrictFloat
from rich.console import RenderableType
from rich.text import Text

BLOCK_ELEMENTS = [" ", "░", "▒", "▓", "█"]
THEME = [
  "#641401",
  "#E72802",
  "#FB6400",
  "#E48B09",
  "#FFEC2A",
  "#F6F9C0",
  "#FAFAFA",
  "#82C8FF",
  "#4078F0",
  "#0A60E1",
]


class Pixel(BaseModel):
  offset: StrictFloat
  temperature: StrictInt

  def draw(self, size_index: int) -> str:
    return Text(BLOCK_ELEMENTS[size_index], no_wrap=True, style=THEME[self.temperature]).markup


class Estuary(BaseModel):
  model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)  # type: ignore[misc]
  chars: List[str] = []
  pixels: List[Pixel] = []

  ### Dimensions ###
  height: StrictInt
  width: StrictInt
  ### Split layouts ###
  scheduler: ClassVar[BackgroundScheduler] = BackgroundScheduler()

  def model_post_init(self, _) -> None:
    self.scheduler.add_job(self.update, "interval", seconds=0.25)
    self.scheduler.start()
    for y in range(self.height):
      temp = randint(0, len(THEME) - 1)
      for x in range(self.width):
        pixel = Pixel(
          temperature=temp, offset=(x + y) * (pi / 15)
        )  # Offset for wavy effect based on position
        self.pixels.append(pixel)

  @property
  def renderable(self) -> RenderableType:
    return Text.from_markup("".join(self.chars))

  def update(self) -> None:
    chars: List[str] = []
    for pixel in self.pixels:
      size_index = int((sin(time() + pixel.offset) + 1) / 2 * (len(BLOCK_ELEMENTS) - 1))
      chars.append(pixel.draw(size_index))
    self.chars = chars


__all__ = ("Estuary",)
