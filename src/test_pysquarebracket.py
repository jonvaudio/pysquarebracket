#!/usr/bin/python3

import time

import pysquarebracket as psb

def test_combos() -> None:
  for style1 in psb._formats.keys():
    psb.writeline_formatted(f'{style1}', style1)
    for style2 in psb._formats.keys():
      if style2 != style1:
        psb.writeline_formatted(f'{style1} and {style2}', [style1, style2])

def test_colours() -> None:
  for fg in {**psb._fg_colours, **psb._fg_bright_colours}.keys():
    for bg in {**psb._bg_colours, **psb._bg_bright_colours}.keys():
      psb.writeline_formatted(f'{fg} and {bg}', [fg, bg])

def test_cr() -> None:
  blocks = ['', '▏', '▎', '▍', '▌', '▋', '▊', '▉']
  full_block = '█'
  def draw(size, max_size) -> None:
    psb.write_creturn()
    num_full_blocks = (size // 8)
    num_non_empty_blocks = num_full_blocks + (1 if size % 8 else 0)
    num_empty_blocks = (max_size // 8) - num_non_empty_blocks
    psb.write_str((full_block * num_full_blocks) + blocks[size % 8] + (' ' * num_empty_blocks))
  sleep = 0.01
  max_size = 60*8
  for i in range(0, max_size):
    draw(i, max_size)
    time.sleep(sleep)
  for i in range(max_size, -1, -1):
    draw(i, max_size)
    time.sleep(sleep)
  psb.writeline_formatted()

if __name__ == '__main__':
  test_combos()
  test_colours()
  test_cr()
