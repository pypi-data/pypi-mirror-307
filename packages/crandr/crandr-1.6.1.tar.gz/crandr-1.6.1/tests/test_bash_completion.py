#!../venv/bin/pytest -vv

import re
import os
import subprocess
import shlex
import pytest


# ------- utils -------

COMPLETION_FILE = os.path.join(os.path.split(__file__)[0], '..', 'src', 'crandr', 'doc', 'complete.bash')

def get_completions(line: str) -> 'list[str]':
	comp_words = split_command_line(line)
	return shlex.split(subprocess.run(
		['bash', '-i', '-c', f'''
			. '{COMPLETION_FILE}';
			COMP_WORDS=({shlex.join(comp_words)})
			COMP_CWORD={len(comp_words)-1}
			_crandr_completions;
			echo "${{COMPREPLY[*]}}"
		'''],
		stdout = subprocess.PIPE,
		text = True,
		check = True,
	).stdout.strip())

def split_command_line(line: str, wordbreaks: str = os.environ.get('COMP_WORDBREAKS', '''"'><=;|&(:''')) -> 'list[str]':
	pattern = r'(?P<break>[%s])|\s+' % re.escape(wordbreaks)
	def repl(m: 're.Match[str]') -> 'str|None':
		breakc = m.group('break')
		if breakc is not None:
			return breakc
		return None
	out = [w for w in re.split(pattern, line) if w]
	if line[-1].isspace():
		out.append('')
	return out


# ------- tests -------

ALL_CONNECTIONS = "any,external,internal,display-port,hdmi,vga".split(",")
ALL_SUBCOMMANDS = "cycle,toggle,extend,mirror,scale,rotate,reset,list,config".split(",")

def test_subcommands_empty() -> None:
	 assert get_completions('crandr ') == ALL_SUBCOMMANDS

def test_subcommand_started() -> None:
	 assert get_completions('crandr exte') == ["extend"]


def test_subcommand_empty_arg() -> None:
	 assert get_completions('crandr extend ') == "left, right, above, below".split(", ")

def test_subcommand_started_arg() -> None:
	 assert get_completions('crandr extend le') == ["left"]

def test_subcommand_second_empty_arg() -> None:
	 assert get_completions('crandr extend left ') == ALL_CONNECTIONS

def test_subcommand_second_started_arg() -> None:
	 assert get_completions('crandr extend left display') == ["display-port"]

def test_subcommand_second_arg_empty_after_comma() -> None:
	 assert get_completions('crandr extend left display-port,') == ALL_CONNECTIONS

def test_subcommand_second_arg_started_after_comma() -> None:
	 assert get_completions('crandr extend left display-port,ext') == ["display-port,external"]

def test_subcommand_after_args() -> None:
	 assert get_completions('crandr extend left display-port,external ') == []


def test_option() -> None:
	 assert get_completions('crandr --ver') == ["--version", "--verbose"]


def test_option_with_separate_empty_value() -> None:
	 assert get_completions('crandr --backend ') == ["swaymsg", "xrandr", "auto"]

def test_option_with_separate_started_value() -> None:
	 assert get_completions('crandr --backend au') == ["auto"]

def test_option_with_equal_empty_value() -> None:
	 assert get_completions('crandr --backend=') == ["swaymsg", "xrandr", "auto"]

def test_option_with_equal_started_value() -> None:
	 assert get_completions('crandr --backend=x') == ["xrandr"]

def test_subcommand_after_options() -> None:
	 assert get_completions('crandr --verbose --backend=xrandr --backend auto ') == ALL_SUBCOMMANDS

def test_arg_after_options() -> None:
	 assert get_completions('crandr --verbose --backend=xrandr --backend auto list -f whatever ') == ALL_CONNECTIONS
