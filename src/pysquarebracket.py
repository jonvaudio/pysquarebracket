#!/usr/bin/python3

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

if __name__ == '__main__':
  print(_format('not_bright'))