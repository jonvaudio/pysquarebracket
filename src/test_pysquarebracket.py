#!/usr/bin/python3

import time

import pysquarebracket as psb

def test_combos():
  for style1 in psb._formats.keys():
    psb.print_format(f'{style1}', style1)
    for style2 in psb._formats.keys():
      if style2 != style1:
        psb.print_format(f'{style1} and {style2}', [style1, style2])

def test_colours():
  for fg in {**psb._fg_colours, **psb._fg_bright_colours}.keys():
    for bg in {**psb._bg_colours, **psb._bg_bright_colours}.keys():
      psb.print_format(f'{fg} and {bg}', [fg, bg])

def test_cr():
  blocks = ['', '▏', '▎', '▍', '▌', '▋', '▊', '▉']
  full_block = '█'
  for i in range(40*4):
    full_blocks = full_block * (i // 8)
    partial_block = blocks[i % 8]
    bar = full_blocks + partial_block
    psb.write_creturn()
    psb.write_now(bar)
    time.sleep(0.01)
psb.write_now('\n')

if __name__ == '__main__':
  test_combos()
  test_colours()
  test_cr()
