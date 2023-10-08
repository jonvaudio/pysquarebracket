import sys

from typing import Union, List

StyleType = Union[str, List[str]]

_FORMATS = {
  'plain': b''
}

_formats = {
  'bright': b'1',
  'dim': b'2',
  'italic': b'3',
  'underline': b'4',
  'reverse': b'7'
}
_FORMATS.update(_formats)

_not_formats = {f'not_{k}': b'2'+v for k, v in _formats.items()}
_FORMATS.update(_not_formats)

_std_colours = {
  'black': b'0',
  'red': b'1',
  'green': b'2',
  'yellow': b'3',
  'blue': b'4',
  'magenta': b'5',
  'cyan': b'6',
  'white': b'7'
}

_fg_colours = {f'fg_{k}': b'3' + v for k, v in _std_colours.items()}
_fg_bright_colours = {f'fg_bright_{k}': b'9'+v for k, v in _std_colours.items()}
_bg_colours = {f'bg_{k}': b'4'+v for k, v in _std_colours.items()}
_bg_bright_colours = {f'bg_bright_{k}': b'10'+v for k, v in _std_colours.items()}
_FORMATS.update({**_fg_colours, **_fg_bright_colours, **_bg_colours, **_bg_bright_colours})

def format(styles: StyleType) -> bytes:
  if isinstance(styles, str):
    styles = [styles]
  return b'\x1b[' + b';'.join(map(lambda style: _FORMATS[style], styles)) + b'm'

def write_bytes(msg: bytes) -> None:
  # print() doesn't send anything to stdout until there is a
  # newline, and so using print("msg", end='') actually re-orders the output
  # so that formatting resets to plain without printing anything
  sys.stdout.buffer.write(msg)
  sys.stdout.buffer.flush()

def write_str(msg: str) -> None:
  write_bytes(msg.encode())

def set_format(styles: StyleType) -> None:
  write_bytes(format(styles))

def reset_format() -> None:
  write_bytes(format('plain'))

def write_formatted(msg: str = '', styles: StyleType = 'plain') -> None:
  set_format(styles)
  write_bytes(msg.encode())
  set_format('plain')

def writeline_formatted(msg: str = '', styles: StyleType = 'plain') -> None:
  write_formatted(msg, styles)
  write_str('\n')

def write_creturn() -> None:
  write_str('\r')
