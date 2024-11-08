########################################################################
## Draw With yyyyy (or yyyyy Drawings, or Drawing With yyyyy)
## (C) 2021 by Yulia Voevodskaya (draw.with.zyxxy@outlook.com)
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  See <https://www.gnu.org/licenses/> for the specifics.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
########################################################################

import numpy as np
from random import random, randint

from .canvas import create_canvas_and_axes, show_and_save
from .shape_functions import draw_a_circle, draw_a_rectangle, draw_a_broken_line, draw_a_polygon, clone_a_shape, draw_a_smile
from .word_bubbles import draw_a_speech_bubble
from .shape_style import scale_default_fontsize, get_canvas_height, get_canvas_width, set_default_linewidth
from .coordinates import shape_names_params_dicts_definition, get_type_given_shapename, build_a_smile, build_a_zigzag
from .settings import slider_range
from .layers import new_layer, shift_layers, turn_layers

smile = build_a_smile(width=3, depth=0.5)
zigzag = build_a_zigzag(width=3, height=0.5, angle_start=-3, nb_segments=6)
zigzag += -zigzag[0] + smile[-1] + [0, 3.5]
a_curve = np.concatenate((smile, zigzag), axis=0)
a_random_curve = [[random()*3.5, random()*3.5] for _ in range(randint(15, 25))]

shape_names_params_dicts_definition_plus = {k : v for k, v in shape_names_params_dicts_definition.items()}
shape_names_params_dicts_definition_plus.update({'a_polygon' : {}, 'a_broken_line' : {}})

gap, text_height, shape_height = 1, 1.5, 5.5
create_canvas_and_axes(canvas_width=71, canvas_height=53)

sb = draw_a_speech_bubble(text='Run demo_shape.py to see how the shape parameters work!', 
                          x=get_canvas_width()/2, y=gap, position='cb', 
                          fontsize=10, background_color='plum')

titles_bottom = sb.top+5*gap+2*(text_height+shape_height)
titles_top = titles_bottom + 6

shape_positions_colors_params = [ 
                            [['a_square', 'superBlue'], 
                             ['a_rectangle', 'superGold'], 
                             ['a_triangle', 'superOrange'],
                             ['a_rhombus', 'superViolet'],
                             ['a_star', 'Purple', .6, ['orchid', .8, {'ends_qty' : 8, 'radius_1' : 3}]], 
                             ['a_regular_polygon', 'red', .9, ['orangered', .9, {'vertices_qty' : 8}]],
                             ['a_polygon', 'turquoise', 1.0, ['darkturquoise', 1.]]],  
                                  
                            [['a_circle', 'superPink', .8],
                             ['an_ellipse', 'Burgundy'],                             
                             ['a_drop', 'BubblePink'], 
                             ['an_egg', 'BrightGreen'], 
                             ['a_heart', 'RoyalBlue', 3.5], 
                             ['a_sector', 'DarkTeal', .8, ['SeaWave', .8, {'radius' : 0, 'angle_end' : 1}]], 
                             ['an_elliptic_sector', 'Yellow', 2, 
                                      ['yellowgreen', 1.2, {'angle_start' : 3, 'angle_end' : 12}]],
                             ['a_crescent', 'dimgray', 1., 
                                          ['darkgray', 1.35, {'depth_2' : -2.5, 'turn' : -3}]],
                             ['a_squiggle', 'orchid', .8, ['darkorchid', .8, {'speed_x' : 5}]]],
                            [['a_segment', 'yellow'],
                             ['a_zigzag', 'LightBlue'],
                             ['a_power_curve', 'red', 0.7],
                             ['an_arc', 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                             ['a_smile', 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                             ['a_wave', 'palegreen'],
                             ['a_coil', 'lightcoral', 1., 
                              ['coral', .075, {'speed_x' : 0, 'speed_out' : 3.5}]],
                             ['a_squiggle_curve', 'orchid', .7, 
                              ['darkorchid', .7, {'speed_x' : 1.5}],
                              ['Hyacinth', .7, {'speed_x' : 5/6, 'angle_end':160}]],
                             ['a_broken_line', 'turquoise', 1., ['darkturquoise', 1.]]],
                             [['a_wave', 'superBlue', 'shift', (3, .5), 0.5], 
                               ['a_triangle', 'superBlue', 'turn', 3], 
                               ['a_rhombus', 'superBlue', 'stretch', 1.8], 
                               ['a_drop', 'aquamarine', 'stretch_x', 1.5], 
                               ['a_crescent', 'turquoise', 'stretch_y', 1.5], 
                               ['an_arc', 'turquoise', 'shift_x', 1.5], 
                               ['a_zigzag', 'turquoise', 'shift_y', 1.5]]]

for width_coeff, color, bottom in [[1,  'plum',  0], 
                                   [1, 'white',  sb.top+gap], 
                                   [.5, 'black', titles_bottom+gap/2],
                                   [1, 'black',  titles_top-gap*.5], 
                                   [1,  'plum',  titles_top+3*gap+(text_height+shape_height)]]:
  draw_a_rectangle(bottom=bottom, height=get_canvas_height(), left=0, 
                   width=width_coeff*get_canvas_width(), color=color, layer_nb=-2, outline_linewidth=0)

set_default_linewidth(5)
c1, c2 = 2, 1
for text_, coeff, text_color, bt, pos_y, eye_color in \
                [['patches', .75, 'black', 'b', titles_bottom, 'white'], 
                 ['lines', .25, 'white', 't', titles_top, 'black'],
                 ['transformations', .5, 'black', 'b', titles_top+6*gap+2*(text_height+shape_height), 'plum']]:

  lnb0 = new_layer()
  title = draw_a_speech_bubble(text=text_, fontsize=20,
                       x=get_canvas_width()*coeff, y=pos_y, 
                       position='c'+bt, color=text_color, background_color='none')
  lnb1 = new_layer()
  y1, y2 = title.top + gap/2, title.bottom - gap/2
  draw_a_broken_line([[title.left-gap*(c1+c2), y2], [title.left-gap*c1, y1], 
                      [title.right+gap*c1, y1], [title.right+gap*(c1+c2), y2]], color=text_color)
  draw_a_broken_line([[title.left-gap*(c1-c2), y2], [title.left-gap*c1, y1], 
                      [title.right+gap*c1, y1], [title.right+gap*(c1-c2), y2]], color=text_color)
  
  for j in [-1, 1]:
    center_x = title.center_x + j * 3
    draw_a_smile(diamond=(center_x, y1), width=1.8, depth=-1.8, color=text_color)
    draw_a_circle(center=(center_x, y1+.7), radius=.5, color=text_color, outline_linewidth=0)
    draw_a_circle(center=(center_x-.25, y1+.7-.25), radius=.2, color=eye_color, outline_linewidth=0)
  
  lnb2 = new_layer()
  draw_a_broken_line([[0, y2],[get_canvas_width(), y2]], color=text_color)
  if eye_color == 'black':
    turn_layers(turn=6, diamond=[title.center_x, y1], layer_nbs=[lnb1, lnb2]) 
    shift_layers(shift=(0, title.bottom - title.top - gap), layer_nbs=[lnb1, lnb2])


scale_default_fontsize(.36)

bg_colors = ['black', 'black', 'white', 'black']
text_ys = [sb.top+3*gap, sb.top+4*gap+1*(text_height+shape_height), 
           titles_top+1*gap, titles_top+5*gap+1*(text_height+shape_height)]
#######################################################
# Now let's draw the shapes!                         ##

for i, (text_color, text_y, shapes_infos) in enumerate(zip(bg_colors, text_ys, shape_positions_colors_params)):
  layer_nb_bg = new_layer()
  layer_nb = new_layer()

  x_so_far = gap
  shape_y = text_y + text_height + 0.5 * shape_height
  for nb_shape, shapes_info in enumerate(shapes_infos):
    shapename = shapes_info[0]
    
    sb = draw_a_speech_bubble(text=shapename if i < 3 else shapes_info[2], 
                              x=x_so_far, y=text_y, color=text_color, background_color='none')
    long_params = shape_names_params_dicts_definition_plus[shapename]

    shape_params = {p_name : slider_range[p_slider_params][2] 
                               if isinstance(p_slider_params, str) else p_slider_params[1] 
                                          for p_name, p_slider_params in long_params.items()}

    func = draw_a_polygon if get_type_given_shapename(shapename) == 'patch' else draw_a_broken_line
    if len(shapes_info) >= 3:
      zoom_or_params = shapes_info[2]
      if isinstance(zoom_or_params, dict):
        shape_params.update(zoom_or_params)

    shs = [func(diamond_x=0, diamond_y=0, color=shapes_info[1], **shape_params,
              contour=a_curve if shapename in ('a_polygon', 'a_broken_line') else shapename)]

    zoom_factor = 1.
    if (len(shapes_info) >= 3 and i != 3) or (len(shapes_info) == 5 and i == 3):
      zoom_or_params = shapes_info[2 if i != 3 else -1]
      if not isinstance(zoom_or_params, dict):
        zoom_factor = zoom_or_params

    shs[0].stretch(zoom_factor)
    shs[0].shift_to_position(xy=[x_so_far, shape_y], position='lc')

    if i != 3:
      x_so_far += shs[-1].get_bbox().width
      for sh_ in shapes_info[3:]:
        x_so_far += gap
        if len(sh_) > 2:
          shape_params.update(sh_[2])
        shs.append(func(diamond_x=0, diamond_y=0, color=sh_[0], **shape_params,
                        contour=a_random_curve if shapename in ('a_polygon', 'a_broken_line') else shapename))
        shs[-1].stretch(sh_[1])
        shs[-1].shift_to_position(xy=[x_so_far, shape_y], position='lc')
        x_so_far += shs[-1].get_bbox().width
       
    else:
      shs[0].shift_to_position(xy=[x_so_far, shape_y], position='lc')
      shs.append(clone_a_shape(shs[0]))
      an_attr = getattr(shs[0], shapes_info[2])
      an_attr(shapes_info[3])
      shift_value = x_so_far - min([sh2.left for sh2 in shs])
      for sh in shs:
        sh.left += shift_value
      shs[0].color = 'Purple'
      shs[0].opacity = .5
      shs[1].color = 'superPink'

    center_shapes = (min([sh.left for sh in shs]) + max([sh.right for sh in shs])) / 2
    center_text = sb.center_x
    if center_shapes > center_text:
      sb.shift_to_position(xy=[center_shapes, text_y], position='cb')
    else:
      for sh_ in shs:
        sh_.shift_x(center_text - center_shapes)
    
    left, right = min([sh.left for sh in shs + [sb]]), max([sh.right for sh in shs + [sb]])
    draw_a_rectangle(left=left-gap/2, width=right-left+gap, bottom=text_y-gap/2, height=text_height+shape_height+gap,
                     outline_color=text_color, layer_nb=layer_nb_bg, color='none')
    x_so_far = right+gap

  shift_layers(shift=[get_canvas_width() / 2 - x_so_far / 2, 0], layer_nbs=[layer_nb_bg, layer_nb])

show_and_save()