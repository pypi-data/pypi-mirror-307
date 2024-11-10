#!../venv/bin/pytest

import os
import tempfile
from collections.abc import Iterator

import pytest

@pytest.fixture(autouse=True)
def no_config_file(monkeypatch: pytest.MonkeyPatch) -> 'Iterator[None]':
	path = tempfile.mkdtemp()
	monkeypatch.setitem(os.environ, 'XDG_CONFIG_HOME', path)
	yield
	os.rmdir(path)
