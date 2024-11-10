#!/usr/bin/env python3

'''
Parse the output of $EXE --help and generate a bash completion based on it.
The bash completion script is saved in FN_OUT.
'''

import os
import re
import sys
import subprocess
import typing
from dataclasses import dataclass

TYPE_VAL: 'typing.TypeAlias' = 'str|list[str]|None'

PROGRAM = 'crandr'
EXE = os.path.join(os.path.split(__file__)[0], 'venv', 'bin', PROGRAM)
FN_OUT = os.path.join(os.path.split(__file__)[0], 'src', PROGRAM, 'doc', 'complete.bash')


# ------- model -------

@dataclass
class Command:

	name: str
	options: 'list[Option]'
	positional_args: 'list[Command]|list[PositionalArgument]'

@dataclass
class MainCommand(Command):

	version: str

@dataclass
class Option:

	names: 'list[str]'
	values: 'AllowedValues'

@dataclass
class PositionalArgument:

	name: str
	values: 'AllowedValues'

	def __init__(self, name: str) -> None:
		self.name = name
		if name.startswith('connections'):
			self.values = ListOf('any,external,internal,display-port,hdmi,vga'.split(','))
		elif name == 'rotation':
			self.values = OneOf('normal,inverted,left,right'.split(','))
		elif name == 'direction':
			self.values = OneOf('left,right,above,below'.split(','))
		else:
			self.values = None

AllowedValues: 'typing.TypeAlias' = 'OneOf|ListOf|UnknownValue|None'

@dataclass
class OneOf:
	values: 'list[str]'

@dataclass
class ListOf:
	values: 'list[str]'

@dataclass
class UnknownValue:
	name: 'str'

def is_list_of_positional_arguments(l: 'list[Command]|list[PositionalArgument]') -> 'typing.TypeGuard[list[PositionalArgument]]':
	return bool(l) and isinstance(l[0], PositionalArgument)

def is_list_of_commands(l: 'list[Command]|list[PositionalArgument]') -> 'typing.TypeGuard[list[Command]]':
	return bool(l) and isinstance(l[0], Command)


# ------- parse argparse output -------

def get_help() -> MainCommand:
	doc = get_help_str()
	version = get_version_str()
	return MainCommand(
		name = PROGRAM,
		options = extract_options(doc),
		positional_args = extract_subparsers(doc),
		version = version,
	)

def get_help_str(subparser: 'str|None' = None) -> str:
	cmd = [EXE]
	if subparser:
		cmd.append(subparser)
	cmd.append('--help')
	return subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True).stdout

def get_version_str() -> str:
	cmd = [EXE, '--version']
	version = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True).stdout
	version = next(ln for ln in version.splitlines() if ln.startswith(PROGRAM))
	version = version.split()[-1]
	return version

def extract_subparsers(doc: str) -> 'list[Command]':
	out = []
	for name in extract_subparser_names(doc):
		doc = get_help_str(name)
		out.append(Command(
			name = name,
			options = extract_options(doc),
			positional_args = extract_positional_arguments(doc),
		))
	return out

def extract_subparser_names(doc: str) -> 'list[str]':
	usage = doc[:doc.find('\n\n')]
	reo = re.compile(
		    r'\{(?P<subparsers>[^}]*)\}'
		'|' r'\[[^]]+\]'
		'|' r'[^[{]*'
	)
	subparsers_list = [m.group('subparsers') for m in reo.finditer(usage) if m.group('subparsers')]
	n = len(subparsers_list)
	if n == 0:
		return []
	elif n == 1:
		return subparsers_list[0].split(',')
	else:
		assert False, "multiple subparser lists found: %s" % ''.join("\n- %s" % i for i in subparsers_list)

def extract_options(doc: str) -> 'list[Option]':
	doc_without_usage = doc[doc.find('\n\n'):]
	re_val = r'([^ \n,{]+|\{[^}]*\})'
	reo = re.compile(r'^  ((?P<short>-[^-])( (?P<short_val>%s))?(,\s+)?)?((?P<long>--[^ \n]+)( (?P<long_val>%s))?)?' % (re_val, re_val), re.M)
	options = []
	for m in reo.finditer(doc_without_usage):
		short = m.group('short')
		if short:
			options.append(Option([short], parse_val(m.group('short_val'))))
		long = m.group('long')
		if long:
			options.append(Option([long], parse_val(m.group('long_val'))))

	return options

def parse_val(val: 'str|None') -> AllowedValues:
	if not val:
		return None
	elif val.startswith('{'):
		return OneOf(val[1:-1].split(','))
	else:
		return UnknownValue(val)

def extract_positional_arguments(doc: str) -> 'list[PositionalArgument]':
	caption = '\npositional arguments:\n'
	try:
		i0 = doc.index(caption) + len(caption)
	except ValueError:
		return[]
	doc = doc[i0:]
	m = next(re.finditer(r'^\S', doc, re.M))
	if m:
		doc = doc[:m.start()]

	reo = re.compile(r'^  (?P<arg>\S+)', re.M)
	return [PositionalArgument(m.group('arg')) for m in reo.finditer(doc)]


# ------- generate bash completion -------

def generate_bash_completion(model: MainCommand) -> None:
	print(r'''
# This file has been generated with https://gitlab.com/erzo/crandr/-/blob/dev/generate_bash_completion.py
# and is automatically overwritten after every update.

export _%(program)s_comp_version='%(version)s'

_%(program)s_comp_log_debug() {
    ## Uncomment the next line for debug output
    # echo >>_debug_%(program)s_bash_completion "$@"
    :
}

_%(program)s_comp_reply_words ()
{
    local IFS=$'\n';
    COMPREPLY=($(IFS=', ' compgen -W "$*" $prefix -- "$cur"))
}

_%(program)s_comp_reply_array ()
{
    local IFS=$'\n';
    local current="${cur##*,}";
    local pre="${cur:0:-${#current}}";
    COMPREPLY=($(IFS=', ' compgen -W "$*" -P "$pre" -- "$current"))
}
'''.lstrip() % dict(program=PROGRAM, version=model.version))

	generate_bash_completion_subfunction(model)
	if is_list_of_commands(model.positional_args):
		for subcmd in model.positional_args:
			generate_bash_completion_subfunction(subcmd)

	print('''
_%(program)s_completions() {
  COMPREPLY=()

  # Bash completion has the very surprising behaviour to parse --option=value
  # as three separate words: '--option' '=' 'value'.
  # Therefore I am first removing all '=' in COMP_WORDS.
  # Then I don't need a distinction between --option=value and --option value.

  # if the current word is a '=' keep it as empty argument
  # otherwise --option= would be indistinguishable from --option
  if [ "${COMP_WORDS[COMP_CWORD]}" = '=' ]; then
    COMP_WORDS[COMP_CWORD]=''
  fi
  # delete '=' in COMP_WORDS
  for i in "${!COMP_WORDS[@]}"; do
    if [[ ${COMP_WORDS[i]} = '=' ]]; then
      unset 'COMP_WORDS[i]'
      COMP_CWORD=$(($COMP_CWORD-1))
    fi
  done
  # reset indices
  COMP_WORDS=("${COMP_WORDS[@]}")

  local cur=${COMP_WORDS[COMP_CWORD]}
  local prev=${COMP_WORDS[COMP_CWORD-1]}

  _%(program)s_comp_log_debug "COMP_WORDS=(${COMP_WORDS[*]}); COMP_CWORD=$COMP_CWORD; cur='$cur'; prev='$prev'"

  local i=1
  "_%(program)s_completions_%(program)s"
}

complete -F _%(program)s_completions %(program)s
''' % dict(
	program = PROGRAM,
))

def generate_bash_completion_subfunction(cmd: Command) -> None:
	subcommands: 'list[str]'
	posargs: 'list[AllowedValues]'
	if not cmd.positional_args:
		subcommands = []
		posargs = []
	elif is_list_of_positional_arguments(cmd.positional_args):
		subcommands = []
		posargs = [arg.values for arg in cmd.positional_args]
	else: # it's a list of subcommands
		subcommands = [c.name for c in cmd.positional_args]
		posargs = [OneOf(subcommands)]

	print('''
_%(program)s_completions_%(cmd)s() {
  _%(program)s_comp_log_debug "  switch to command %(cmd)s"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _%(program)s_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_%(program)s_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ %(options_with_arguments)s ]]; then
        #_%(program)s_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_%(program)s_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif %(is_current_a_subcommand)s; then
      #_%(program)s_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_%(program)s_completions_$current"
      return
    else
      #_%(program)s_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _%(program)s_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_%(program)s_comp_log_debug "  the current argument is an option"
    %(options)s
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_%(program)s_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in
%(option_value)s
      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_%(program)s_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
%(posargs)s
    esac
  fi
}
''' % dict(
	program = PROGRAM,
	cmd = cmd.name,
	options_with_arguments = r"^(%s)$" % "|".join(name for o in cmd.options for name in o.names if o.values is not None),
	is_current_a_subcommand = r"""[[ "$current" =~ ^(%s)$ ]]""" % "|".join(subcommands) if subcommands else 'false',
	options = format_bash_completion_values(OneOf([name for option in cmd.options for name in option.names if len(name) > 2])),
	option_value = "\n".join("      %s) %s;;" % ('|'.join(opt.names), format_bash_completion_values(opt.values)) for opt in cmd.options if opt.values is not None),
	posargs = "\n".join("      %s) %s;;" % (i, format_bash_completion_values(val)) for i, val in enumerate(posargs, start=1)),
))

def format_bash_completion_values(val: AllowedValues) -> str:
	if isinstance(val, OneOf):
		return '''_%s_comp_reply_words '%s' ''' % (PROGRAM, ','.join(val.values))
	elif isinstance(val, ListOf):
		return '''_%s_comp_reply_array '%s' ''' % (PROGRAM, ','.join(val.values))
	return ''


# ------- main -------

def main() -> None:
	model = get_help()
	original_stdout = sys.stdout
	try:
		with open(FN_OUT, "wt") as sys.stdout:
			generate_bash_completion(model)
	finally:
		sys.stdout = original_stdout


if __name__ == '__main__':
	main()
