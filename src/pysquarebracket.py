#!/usr/bin/python3

import sys

from typing import Union, List

_escape = b'\x1b'
_with = b';'

_formats = {
  'plain': b'0',
  'bright': b'1',
  'dim': b'2',
  'italic': b'3',
  'underline': b'4',
  'reverse': b'7'
}

_formats.update({f'not_{k}': b'2' + v
  for k, v in _formats.items() if k != 'plain'})

def _format(styles: Union[str, List[str]]) -> bytes:
  if isinstance(styles, str):
    styles = [styles]
  return b'\x1b[' + b';'.join(map(lambda style: _formats[style], styles)) + b'm'

def set_format(styles: Union[str, List[str]]) -> None:
  sys.stdout.buffer.write(_format(styles))
  sys.stdout.buffer.flush()

if __name__ == '__main__':
  for style1 in _formats.keys():
    if not style1.startswith('not_') and style1 != 'plain':
      set_format(style1)
      print(style1)
      set_format('plain')
      for style2 in _formats.keys():
        if style2 != style1 and not style2.startswith('not_') and style2 != 'plain':
          set_format([style1, style2])
          print(f'{style1} and {style2}')
          set_format('plain')
