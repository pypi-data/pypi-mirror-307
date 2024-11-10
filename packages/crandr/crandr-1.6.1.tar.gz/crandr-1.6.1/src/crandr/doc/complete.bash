# This file has been generated with https://gitlab.com/erzo/crandr/-/blob/dev/generate_bash_completion.py
# and is automatically overwritten after every update.

export _crandr_comp_version='1.6.1'

_crandr_comp_log_debug() {
    ## Uncomment the next line for debug output
    # echo >>_debug_crandr_bash_completion "$@"
    :
}

_crandr_comp_reply_words ()
{
    local IFS=$'\n';
    COMPREPLY=($(IFS=', ' compgen -W "$*" $prefix -- "$cur"))
}

_crandr_comp_reply_array ()
{
    local IFS=$'\n';
    local current="${cur##*,}";
    local pre="${cur:0:-${#current}}";
    COMPREPLY=($(IFS=', ' compgen -W "$*" -P "$pre" -- "$current"))
}


_crandr_completions_crandr() {
  _crandr_comp_log_debug "  switch to command crandr"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^(--log|--test-input|--backend|--wait)$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif [[ "$current" =~ ^(cycle|toggle|extend|mirror|scale|rotate|reset|list|config)$ ]]; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help,--version,--dry-run,--verbose,--log,--test-input,--backend,--use-short-names-on-sway,--wait' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in
      --log) ;;
      --test-input) ;;
      --backend) _crandr_comp_reply_words 'swaymsg,xrandr,auto' ;;
      --wait) ;;
      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) _crandr_comp_reply_words 'cycle,toggle,extend,mirror,scale,rotate,reset,list,config' ;;
    esac
  fi
}


_crandr_completions_cycle() {
  _crandr_comp_log_debug "  switch to command cycle"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^(-t|--time-in-s)$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help,--time-in-s' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in
      -t) ;;
      --time-in-s) ;;
      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
    esac
  fi
}


_crandr_completions_toggle() {
  _crandr_comp_log_debug "  switch to command toggle"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^(-t|--time-in-s)$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help,--time-in-s' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in
      -t) ;;
      --time-in-s) ;;
      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
      2) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
    esac
  fi
}


_crandr_completions_extend() {
  _crandr_comp_log_debug "  switch to command extend"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^()$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in

      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) _crandr_comp_reply_words 'left,right,above,below' ;;
      2) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
    esac
  fi
}


_crandr_completions_mirror() {
  _crandr_comp_log_debug "  switch to command mirror"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^(-o|--original)$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help,--original' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in
      -o) ;;
      --original) ;;
      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
    esac
  fi
}


_crandr_completions_scale() {
  _crandr_comp_log_debug "  switch to command scale"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^()$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in

      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) ;;
      2) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
    esac
  fi
}


_crandr_completions_rotate() {
  _crandr_comp_log_debug "  switch to command rotate"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^()$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in

      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) _crandr_comp_reply_words 'normal,inverted,left,right' ;;
      2) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
    esac
  fi
}


_crandr_completions_reset() {
  _crandr_comp_log_debug "  switch to command reset"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^(-t|--time-in-s)$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help,--time-in-s' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in
      -t) ;;
      --time-in-s) ;;
      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
    esac
  fi
}


_crandr_completions_list() {
  _crandr_comp_log_debug "  switch to command list"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^(-f|--format)$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help,--format' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in
      -f) ;;
      --format) ;;
      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in
      1) _crandr_comp_reply_array 'any,external,internal,display-port,hdmi,vga' ;;
    esac
  fi
}


_crandr_completions_config() {
  _crandr_comp_log_debug "  switch to command config"
  local current
  posarg=0
  while [[ $i -le $COMP_CWORD ]]; do
    current="${COMP_WORDS[i]}"
    _crandr_comp_log_debug "  [i=$i][current=${current}][posarg=$posarg]"
    if [[ ${current:0:1} == [-+] ]]; then
      if [[ $current =~ = ]]; then
        #_crandr_comp_log_debug "  option with given value => next is independent"
        :
      elif [[ "$current" =~ ^()$ ]]; then
        #_crandr_comp_log_debug "  next is a value for this option => skip it"
        i=$((i+1))
      else
        #_crandr_comp_log_debug "  this option takes no value => next is independent"
        :
      fi
    elif false; then
      #_crandr_comp_log_debug "  this is a subcommand"
      i=$((i+1))
      "_crandr_completions_$current"
      return
    else
      #_crandr_comp_log_debug "  this is a positional argument"
      posarg=$(($posarg+1))
    fi
    i=$((i+1))
  done

  _crandr_comp_log_debug "  [cur=$cur][prev=$prev][posarg=$posarg]"
  local is_posarg=false
  if [[ ${cur:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  the current argument is an option"
    _crandr_comp_reply_words '--help,--list-searched-paths,--print-file-name,--edit' 
  elif [[ ${prev:0:1} == [-+] ]]; then
    #_crandr_comp_log_debug "  if the last argument was an option which takes a value, complete that"
    case "${prev}" in

      *) is_posarg=true;;
    esac
  else
    is_posarg=true
  fi
  if [ "$is_posarg" = "true" ]; then
    #_crandr_comp_log_debug "  complete the current positional argument"
    case "$posarg" in

    esac
  fi
}


_crandr_completions() {
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

  _crandr_comp_log_debug "COMP_WORDS=(${COMP_WORDS[*]}); COMP_CWORD=$COMP_CWORD; cur='$cur'; prev='$prev'"

  local i=1
  "_crandr_completions_crandr"
}

complete -F _crandr_completions crandr

