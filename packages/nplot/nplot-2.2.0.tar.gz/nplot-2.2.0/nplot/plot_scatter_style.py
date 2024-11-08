"""
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * - Neither the name of prim nor the names of its contributors may be used to
 * endorse or promote products derived from this software without specific prior
 * written permission.
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
"""

import numpy

class PlotScatterStyle(object):
  """
  This is a plot scatter style generator
  """

  __style_map = {}
  __default_style = None

  def __init__(self, style, plt, scatter_count):
    assert style in PlotScatterStyle.__style_map, \
      '{} is not a registered plot scatter style'.format(style)
    self._all_styles = list(zip(*PlotScatterStyle.__style_map[style](
      plt, scatter_count)))
    assert len(self._all_styles) == scatter_count, 'error in style implementation'

  @staticmethod
  def styles():
    return list(PlotScatterStyle.__style_map.keys())

  @staticmethod
  def default():
    return PlotScatterStyle.__default_style

  @staticmethod
  def registerStyle(style, func, default=False):
    assert style not in PlotScatterStyle.__style_map, \
      '{} is already a registered plot style'.format(style)
    PlotScatterStyle.__style_map[style] = func
    if default:
      PlotScatterStyle.__default_style = style

  def __getitem__(self, index):
    names = ['color', 'marker_style']
    style = self._all_styles[index]
    assert len(names) == len(style)
    return dict(zip(names, style))

def colorfulDots(plt, scatter_count):
  if scatter_count <= 3:
    cmap = plt.get_cmap('brg')
  else:
    cmap = plt.get_cmap('gist_rainbow')
  colors = [cmap(idx) for idx in numpy.linspace(0, 1, scatter_count)]
  marker_styles = ['o'] * scatter_count
  return colors, marker_styles
PlotScatterStyle.registerStyle('colorful-dots', colorfulDots, True)

def colorfulMarkers(plt, scatter_count):
  if scatter_count <= 3:
    cmap = plt.get_cmap('brg')
  else:
    cmap = plt.get_cmap('gist_rainbow')
  colors = [cmap(idx) for idx in numpy.linspace(0.0, 0.9, scatter_count)]
  marker_styles = ['s', '^', 'o', 'd', 'x', '|']
  assert len(marker_styles) > scatter_count, 'Too many scatters for plot style'
  return colors, marker_styles
PlotScatterStyle.registerStyle('colorful-markers', colorfulMarkers)

def infernoDots(plt, scatter_count):
  cmap = plt.get_cmap('inferno')
  colors = [cmap(idx) for idx in numpy.linspace(0, 0.9, scatter_count)]
  marker_styles = ['o'] * scatter_count
  return colors, marker_styles
PlotScatterStyle.registerStyle('inferno-dots', infernoDots)

def infernoMarkers(plt, scatter_count):
  cmap = plt.get_cmap('inferno')
  colors = [cmap(idx) for idx in numpy.linspace(0.0, 0.9, scatter_count)]
  marker_styles = ['s', '^', 'o', 'd', 'x', '|']
  assert len(marker_styles) > scatter_count, 'Too many scatters for plot style'
  return colors, marker_styles
PlotScatterStyle.registerStyle('inferno-markers', infernoMarkers)

def plasmaDots(plt, scatter_count):
  cmap = plt.get_cmap('plasma')
  colors = [cmap(idx) for idx in numpy.linspace(0, 0.9, scatter_count)]
  marker_styles = ['o'] * scatter_count
  return colors, marker_styles
PlotScatterStyle.registerStyle('plasma-dots', plasmaDots)

def plasmaMarkers(plt, scatter_count):
  cmap = plt.get_cmap('plasma')
  colors = [cmap(idx) for idx in numpy.linspace(0.0, 0.9, scatter_count)]
  marker_styles = ['s', '^', 'o', 'd', 'x', '|', 'None']
  assert len(marker_styles) > scatter_count, 'Too many scatters for plot style'
  return colors, marker_styles
PlotScatterStyle.registerStyle('plasma-markers', plasmaMarkers)

def generic_generator(name, color):
  def generic(plt, scatter_count):
    colors = [color] * scatter_count
    marker_styles = ['s', '^', 'o', 'd', 'x', '|', 'None']
    assert len(marker_styles) > scatter_count, 'Too many scatters for plot style'
    return colors, marker_styles
  return generic
for name, color in [('black', 'k'), ('red', 'r'), ('gray', '0.5')]:
  PlotScatterStyle.registerStyle(name, generic_generator(name, color))
