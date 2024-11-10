#!/usr/bin/env python3

import argparse
from collections.abc import Iterable

from . import model

CONNECTION_ANY = 'any'
CONNECTION_EXTERNAL = 'external'
ALL_CONNECTION_VALUES = (CONNECTION_ANY, CONNECTION_EXTERNAL) + model.ALL_CONNECTIONS
possible_connections = ','.join(f'{ac}' for ac in ALL_CONNECTION_VALUES)


def connection(connections: str) -> 'list[str]':
	group: 'Iterable[str]'
	out = []
	for c in connections.split(','):
		if c == CONNECTION_ANY:
			group = model.ALL_CONNECTIONS
		elif c == CONNECTION_EXTERNAL:
			group = model.EXTERNAL_CONNECTIONS
		elif c in model.ALL_CONNECTIONS:
			group = [c]
		else:
			raise argparse.ArgumentTypeError(f'invalid connection {c!r}, should be one of {possible_connections}')

		for ci in group:
			if ci not in out:
				out.append(ci)
	return out
