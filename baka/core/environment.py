# -*- coding: utf-8 -*-

from baka.core.scripting import Scriptable
from baka.core.container import Container

from typing import Dict


class Environment(Scriptable):
    home_path = '/home/baka'
    path = '/home/baka'

    def __init__(self, scripts: Dict[str, str]=None):
        super().__init__(scripts)

    def setup(self, c: Container):
        self._run_script('setup', c)
