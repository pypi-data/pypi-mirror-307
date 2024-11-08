#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import typer

from .basic_commands import app

try:
    app(prog_name='blog')
except KeyboardInterrupt:
    raise typer.Exit()
