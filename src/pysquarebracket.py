import sys
import termios
import tty
import struct
import fcntl
import contextlib
import select

from typing import Union, List, Any, Tuple

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

_cursors = {
  'block_blink': b'0',
  'block_steady': b'2',
  'underline_blink': b'3',
  'underline_steady': b'4',
  'beam_blink': b'5',
  'beam_steady': b'6'
}

def format(styles: StyleType) -> bytes:
  if isinstance(styles, str):
    styles = [styles]
  return b'\x1b[' + b';'.join(map(lambda style: _FORMATS[style], styles)) + b'm'

def cursor_style(style: str) -> bytes:
  return b'\x1b[' + _cursors[style] + b' q'

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

def set_cursor_style(style: str) -> None:
  write_bytes(cursor_style(style))

def set_cursor_enabled(enabled: bool) -> None:
  if enabled:
    write_bytes(b'\x1b[?25h')
  else:
    write_bytes(b'\x1b[?25l')

def get_rows_cols() -> Tuple[int, int]:
    packed = fcntl.ioctl(1, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0))
    rows, cols, _, _ = struct.unpack('HHHH', packed)
    return rows, cols

class AltMode:
  @staticmethod
  def clear() -> None:
    write_bytes(b'\x1b[2J')

  @staticmethod
  def enter() -> List[Any]:
    write_bytes(b'\x1b[?1049h')
    set_cursor_enabled(False)
    AltMode.clear()
    AltMode.go(1, 1)
    original_attr = termios.tcgetattr(1)
    tty.setraw(1, termios.TCSANOW)
    return original_attr
  
  @staticmethod
  def exit(original_attr: List[Any]) -> None:
    AltMode.clear()
    set_cursor_enabled(True)
    write_bytes(b'\x1b[?1049l')
    termios.tcsetattr(1, termios.TCSANOW, original_attr)
  
  @staticmethod
  def go(row: int, col: int) -> None:
    write_bytes(b'\x1b[' + str(row).encode() + b';' + str(col).encode() + b'H')
  
  @staticmethod
  def poll_ch() -> str:
    ready, _, _ = select.select([sys.stdin], [], [], 0.0)
    if ready:
      return sys.stdin.read(1)
    else:
      return ''
  
  def wait_ch() -> str:
    return sys.stdin.read(1)

@contextlib.contextmanager
def alternate_mode() -> None:
  try:
    original_attr = AltMode.enter()
    yield
  finally:
    if 'original_attr' in locals():
      AltMode.exit(original_attr)

def write_creturn() -> None:
  write_str('\r')
