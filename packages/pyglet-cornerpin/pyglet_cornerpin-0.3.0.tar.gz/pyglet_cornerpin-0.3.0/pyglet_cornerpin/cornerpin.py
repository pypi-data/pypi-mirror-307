"""
This little library provides functions to add corner pin functionality
into python in general, and pyglet specifically.

Long time ago I used a set of javascript functions from Cihad Turhan (see
https://stackoverflow.com/a/30646172), which I now ported to python.
These computations might be faster with numpy, but for me these run only
incidently so won't really hurt performance.
"""

import pyglet
from typing import Optional
import logging
import copy

def adj(m): # Compute the adjugate of m
  return [
    m[4]*m[8]-m[5]*m[7], m[2]*m[7]-m[1]*m[8], m[1]*m[5]-m[2]*m[4],
    m[5]*m[6]-m[3]*m[8], m[0]*m[8]-m[2]*m[6], m[2]*m[3]-m[0]*m[5],
    m[3]*m[7]-m[4]*m[6], m[1]*m[6]-m[0]*m[7], m[0]*m[4]-m[1]*m[3]
  ]

def multmm(a, b) -> list[float]: # multiply two matrices
  c = [0.]*9
  for i in range(3):
    for j in range(3):
        cij = 0
        for k in range(3):
            cij += a[3*i + k]*b[3*k + j]
        c[3 * i + j] = cij
  return c

def multmv(m, v): #  multiply matrix and vector
  return [
    m[0]*v[0] + m[1]*v[1] + m[2]*v[2],
    m[3]*v[0] + m[4]*v[1] + m[5]*v[2],
    m[6]*v[0] + m[7]*v[1] + m[8]*v[2]
  ]

# def pdbg(m, v) :
#   r = multmv(m, v)
#   return r + " (" + r[0]/r[2] + ", " + r[1]/r[2] + ")"

def basisToPoints(x1, y1, x2, y2, x3, y3, x4, y4) :
  m = [
    x1, x2, x3,
    y1, y2, y3,
     1,  1,  1
  ]
  v = multmv(adj(m), [x4, y4, 1])
  return multmm(m, [
    v[0], 0, 0,
    0, v[1], 0,
    0, 0, v[2]
  ])

def general2DProjection(
  x1s, y1s, x1d, y1d,
  x2s, y2s, x2d, y2d,
  x3s, y3s, x3d, y3d,
  x4s, y4s, x4d, y4d
) :
  s = basisToPoints(x1s, y1s, x2s, y2s, x3s, y3s, x4s, y4s)
  d = basisToPoints(x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d)
  return multmm(d, adj(s))

def transform2d_wh(w, h, x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d):
   """
   Transform the image corners based on width and height of the image
   """
   return transform2d(0, 0, x1d, y1d, w, 0, x2d, y2d, 0, h, x3d, y3d, w, h, x4d, y4d)

def transform2d(x1s, y1s, x2s, y2s, x3s, y3s, x4s, y4s, x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d):
    """
    Transform the image based on 4 arbitrarily placed pins
    """
    t = general2DProjection(x1s, y1s, x1d, y1d, x2s, y2s, x2d, y2d, x3s, y3s, x3d, y3d, x4s, y4s, x4d, y4d)
    for i in range(9):
        t[i] = t[i] / t[8]
    
    t = [t[0], t[3], 0, t[6],
       t[1], t[4], 0, t[7],
       0   , 0   , 1, 0   ,
       t[2], t[5], 0, t[8]]
    return t

# Below are all pyglet specific functions

class PygletCornerPin(pyglet.event.EventDispatcher):
    def __init__(self, window: pyglet.window.Window, corners: Optional[list[list[float]]] = None, source_points: Optional[list[list[float]]] = None) -> None:
       """
       Creates CornerPin utility for a given Pyglet window. If not given, corners default to the
       bottom left, bottom right, top left, top right corners of the window (i.e. no transform)

       Do not forget to register event handlers by running `window.register_handlers(pins)`.
       """
       self.window = window
       self.source_points = source_points if source_points else [
          [0, 0],
          [self.window.width, 0],
          [0, self.window.height],
          [self.window.width, self.window.height],
       ]
       self.pin_positions = corners if corners else copy.deepcopy(self.source_points)
       
       self.batch = pyglet.graphics.Batch()
       self.dragging: Optional[int] = None
       self.handles = [
          pyglet.shapes.Arc(c[0],c[1],20, thickness=2, color=(0,0,255,255), batch=self.batch) for c in self.pin_positions
       ]
       self.current_corner = None
    
    def update_handles(self):
       for i, c in enumerate(self.pin_positions):
          self.handles[i].x = c[0]
          self.handles[i].y = c[1]
        
    def draw(self):
       """
       Draw the handles in the on_draw loop
       """
       self.batch.draw()

    def transform2d_matrix(self,x1s, y1s, x2s, y2s, x3s, y3s, x4s, y4s, x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d):
        """
        Calculate the transform matrix
        """
        t = transform2d(
            x1s, y1s, x2s, y2s, x3s, y3s, x4s, y4s, x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d)
        return pyglet.math.Mat4(t)
    
    # event handlers

    def on_mouse_press(self, x, y, button, modifiers):
        r = 20
        currentcorner = None
        dist = r * r
        for i in range(4):
           dx = x - self.pin_positions[i][0]
           dy = y - self.pin_positions[i][1]
           if dist > dx**2 + dy ** 2:
              dist = dx**2 + dy ** 2
              currentcorner = i
        
        self.dragging = currentcorner
        return pyglet.event.EVENT_HANDLED if self.dragging else pyglet.event.EVENT_UNHANDLED

    def on_mouse_release(self, x, y, button, modifiers):
       if self.dragging is None:
          return pyglet.event.EVENT_UNHANDLED
       self.dragging = None
       logging.debug(f"Corner pins set to {self.pin_positions}")
       return pyglet.event.EVENT_HANDLED

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging is None:
            return pyglet.event.EVENT_UNHANDLED
        
        self.pin_positions[self.dragging][0] = x
        self.pin_positions[self.dragging][1] = y
        self.update_view()

    def on_key_release(self, symbol: int, modifiers: int):
      if symbol not in [
         pyglet.window.key._1, pyglet.window.key._2, pyglet.window.key._3, pyglet.window.key._4,
         pyglet.window.key.ESCAPE,
         pyglet.window.key.UP, pyglet.window.key.DOWN, pyglet.window.key.LEFT, pyglet.window.key.RIGHT,
        ]:
         return pyglet.event.EVENT_UNHANDLED
      
      if symbol == pyglet.window.key._1:
        self.current_corner = 2
      if symbol == pyglet.window.key._2:
        self.current_corner = 3
      if symbol == pyglet.window.key._3:
        self.current_corner = 0
      if symbol == pyglet.window.key._4:
        self.current_corner = 1
      if symbol == pyglet.window.key.ESCAPE:
        self.current_corner = None

      for i, h in enumerate(self.handles):
        h.color = (255,0,0,255) if i == self.current_corner else (0,0,255,255)
      
      if self.current_corner is None:
        return
      
        
      if symbol not in [pyglet.window.key.UP,pyglet.window.key.DOWN, pyglet.window.key.LEFT, pyglet.window.key.RIGHT]:
         return
      
      base = 2
      if modifiers & pyglet.window.key.MOD_SHIFT:
         base += 10
      if modifiers & pyglet.window.key.MOD_CTRL:
         base *= 2
      
      if symbol == pyglet.window.key.RIGHT:
        self.pin_positions[self.current_corner][0] += base
      if symbol == pyglet.window.key.LEFT:
        self.pin_positions[self.current_corner][0] -= base
      if symbol == pyglet.window.key.UP:
        self.pin_positions[self.current_corner][1] += base
      if symbol == pyglet.window.key.DOWN:
        self.pin_positions[self.current_corner][1] -= base
         
      self.update_view()
    
    def update_view(self):
       self.window.view = self.transform2d_matrix(*[x for c in self.source_points for x in c], *[x for c in self.pin_positions for x in c])
