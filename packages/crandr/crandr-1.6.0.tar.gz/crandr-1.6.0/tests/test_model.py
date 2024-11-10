#!../venv/bin/pytest

from crandr.model import Monitor, Resolution, sort_monitors_by_connection
from crandr.connection_parser import connection

def test_sort_monitors_by_connection__prefer_external() -> None:
	monitors = [
		Monitor(name="eDP-1", long_name="", on=True),
		Monitor(name="DP-3", long_name="", on=True),
	]
	connections = connection("external,any")
	sort_monitors_by_connection(monitors, connections)
	assert monitors[0].name == "DP-3"
	assert monitors[1].name == "eDP-1"
	assert len(monitors) == 2

def test_sort_monitors_by_connection__prefer_internal() -> None:
	monitors = [
		Monitor(name="eDP-1", long_name="", on=True),
		Monitor(name="DP-3", long_name="", on=True),
	]
	connections = connection("internal,any")
	sort_monitors_by_connection(monitors, connections)
	assert monitors[0].name == "eDP-1"
	assert monitors[1].name == "DP-3"
	assert len(monitors) == 2

def test_repr_resolution() -> None:
	r = Resolution(1920, 1080)
	r2 = eval(repr(r), {}, {'Resolution': Resolution})
	assert type(r) is type(r2)
	assert r.width == r2.width
	assert r.height == r.height
