"""
TODO:
  1. Separate cv2 low level from main & low engine on demand only
  2. Setup smart way of handling channels (RGB vs BGR required by cv2)
  3. Define types for rgb, and bgr np arrays, for chw and hwc formats
"""

import os

import cv2
import numpy as np
from naeural_client import BaseDecentrAIObject

from . import constants as ct
from . import geometry_methods as gmt

__VER__ = '0.7.7.0'

DEFAULT_FONT = cv2.FONT_HERSHEY_SIMPLEX
DEFAULT_FONT_SIZE = 0.5
DEFAULT_FONT_THICKNESS = 2

COLOR_BLUE = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

IMG_EXT = ['.png', '.jpg', '.jpeg', '.bmp']

ENGINE_OPENCV = 'opencv'


class OpenCVPainter:
  def __init__(self):
    return

  @staticmethod
  def read(path):
    assert os.path.exists(path)
    return cv2.imread(path)

  @staticmethod
  def resize(image, new_h, new_w):
    image = cv2.resize(
      src=image,
      dsize=(new_w, new_h)
    )
    return image

  @staticmethod
  def line(image, pt1, pt2, color, thickness):
    if not isinstance(pt1, tuple):
      pt1 = tuple(pt1)
    if not isinstance(pt2, tuple):
      pt2 = tuple(pt2)

    image = cv2.line(
      img=image,
      pt1=pt1,
      pt2=pt2,
      color=color,
      thickness=thickness
    )
    return image

  @staticmethod
  def rectangle_target(image, pt1, pt2, color, thickness=2):
    """
    pt1 = left, top
    pt2 = right, bottom
    """

    x1, y1 = pt1
    x2, y2 = pt2
    w = x2 - x1
    h = y2 - y1
    seg_h = h // 8
    seg_w = w // 8
    coords = [
        (x1, y1, x1 + seg_w, y1),
        (x2 - seg_w, y1, x2, y1),
        (x2, y1, x2, y1 + seg_h),
        (x2, y2 - seg_h, x2, y2),
        (x2 - seg_w, y2, x2, y2),
        (x1, y2, x1 + seg_w, y2),
        (x1, y2, x1, y2 - seg_h),
        (x1, y1 + seg_h, x1, y1)
    ]
    for (x1, y1, x2, y2) in coords:
      image = cv2.line(
        img=image,
        pt1=(x1, y1),
        pt2=(x2, y2),
        color=color,
        thickness=thickness
      )

    return image

  @staticmethod
  def rectangle(image, pt1, pt2, color, thickness):
    if not isinstance(pt1, tuple):
      pt1 = tuple(pt1)
    if not isinstance(pt2, tuple):
      pt2 = tuple(pt2)

    image = cv2.rectangle(
      img=image,
      pt1=pt1,
      pt2=pt2,
      color=color,
      thickness=thickness
    )
    return image

  @staticmethod
  def polygon(image, pts, color, thickness):
    is_closed = pts[0] == pts[-1]
    if isinstance(pts, list):
      pts = np.array(pts)
    pts = pts.reshape(-1, 1, 2)
    image = cv2.polylines(
      img=image,
      pts=[pts],
      isClosed=is_closed,
      color=color,
      thickness=thickness
    )
    return image

  @staticmethod
  def circle(image, center, radius, color, thickness):
    if not isinstance(center, tuple):
      center = tuple(center)

    image = cv2.circle(image, center, radius, color, thickness)
    return image

  @staticmethod
  def arrow(image, pt1, pt2, color, thickness):
    image = cv2.arrowedLine(image, tuple(pt1), tuple(pt2), color, thickness)
    return image

  @staticmethod
  def text(image, text, org, font, font_scale, color, thickness=None):
    if not isinstance(org, tuple):
      org = tuple(org)

    if font is None:
      font = DEFAULT_FONT
    if font_scale is None:
      font_scale = DEFAULT_FONT_SIZE
    if thickness is None:
      thickness = 1
    image = cv2.putText(
      img=image,
      text=text,
      org=org,
      fontFace=font,
      fontScale=font_scale,
      color=color,
      thickness=thickness
    )
    return image

  @staticmethod
  def text_size(text, font, font_scale, thickness):
    (text_width, text_height), baseline = cv2.getTextSize(
      text=text,
      fontFace=font,
      fontScale=font_scale,
      thickness=thickness
    )
    return (text_width, text_height), baseline

  @staticmethod
  def scale_blur(image, min_resize=6, blur_resize_factor=30):
    h, w = image.shape[:2]
    if not (h >= min_resize and w >= min_resize):
      return image

    min_size = min(h, w)
    resize = max(min_resize, min_size // blur_resize_factor)
    if h > w:
      rw = resize
      rh = int(h / w * resize)
    else:
      rh = resize
      rw = int(w / h * resize)
    image = cv2.resize(image, dsize=(rw, rh))
    image = cv2.resize(image, dsize=(w, h))
    return image

  @staticmethod
  def blur(image, kernel_size):
    image = cv2.blur(
      src=image,
      ksize=kernel_size
    )
    return image

  @staticmethod
  def gaussian_blur(image, ksize, sigmaX):
    image = cv2.GaussianBlur(
      src=image,
      ksize=ksize,
      sigmaX=sigmaX
    )
    return image

  @staticmethod
  def show(name, image, orig=None):
    cv2.imshow(name, image)
    if orig is not None:
      if isinstance(orig, int):
        orig = orig, orig
      cv2.moveWindow(name, orig[0], orig[1])
    # endif orig provided
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

  @staticmethod
  def save(path, image):
    subfolder = os.path.split(path)[0]
    if not os.path.exists(subfolder):
      os.makedirs(subfolder)
    cv2.imwrite(path, image)
    return

  @staticmethod
  def cross(image, point, color, thickness, size_factor=1e-2):
    h, w, _ = image.shape
    x, y = point
    length = 3 * size_factor * h
    x1 = int(max(0, x - length))
    x2 = int(min(x + length, w))
    y1 = int(max(0, y - length))
    y2 = int(min(y + length, h))
    image = OpenCVPainter.line(
      image=image,
      pt1=(x1, y),
      pt2=(x2, y),
      color=color,
      thickness=thickness
    )
    image = OpenCVPainter.line(
      image=image,
      pt1=(x, y1),
      pt2=(x, y2),
      color=color,
      thickness=thickness
    )
    return image


class DrawUtils(BaseDecentrAIObject):
  def __init__(self, engine=ENGINE_OPENCV, timers_section=None, **kwargs):
    self._engine = engine
    self._timers_section = timers_section
    if self._engine == ENGINE_OPENCV:
      self.draw_engine = OpenCVPainter()
    else:
      raise NotImplementedError()

    super().__init__(**kwargs)
    return

  def str_to_color(self, color):
    if color is None:
      return None
    if type(color) != str:
      return color
    s_color = color.upper()
    clr = None
    if 'RED' in s_color:
      if 'DEEP' in s_color:
        clr = ct.DEEP_RED
      else:
        clr = ct.RED
    elif 'ORANGE' in s_color:
      clr = ct.ORANGE
    elif 'BLUE' in s_color:
      if 'DARK' in s_color:
        clr = ct.DARK_BLUE
      elif 'LIGHT' in s_color:
        clr = ct.LIGHT_BLUE
      else:
        clr = ct.BLUE
    elif 'GREEN' in s_color:
      if 'DARK' in s_color:
        clr = ct.DARK_GREEN
      elif 'PALE' in s_color:
        clr = ct.PALE_GREEN
      else:
        clr = ct.GREEN
    elif 'YELLOW' in s_color:
      clr = ct.YELLOW
    elif 'BROWN' in s_color:
      clr = ct.BROWN

    if clr is None:
      clr = (0, 0, 0)
    return clr

  def is_image(self, path):
    return any(path.endswith(x) for x in IMG_EXT)

  def read(self,
           path,
           reverse_channels=False,
           return_path=False,
           verbose=True
           ):
    from tqdm import tqdm
    out, out_path = None, None
    if os.path.isdir(path):
      files = os.listdir(path)
      files = list(filter(lambda x: self.is_image(x), files))
      files = [os.path.join(path, x) for x in files]
      out = [self.draw_engine.read(x) for x in tqdm(files)]
      if reverse_channels:
        out = [x[:, :, ::-1] for x in out]
      out_path = files
    else:
      out = self.draw_engine.read(path)
      if reverse_channels:
        out = out[:, :, ::-1]
      out_path = path

    if return_path:
      ret = out_path, out
    else:
      ret = out
    return ret

  def show(self, name, image, orig=None):
    return self.draw_engine.show(
      name=name,
      image=image,
      orig=orig
    )

  def resize(self, image, new_h, new_w):
    return self.draw_engine.resize(image=image, new_h=new_h, new_w=new_w)

  def line(self, image, pt1, pt2, color, thickness):
    if type(color) == str:
      color = self.str_to_color(color)
    image = self.draw_engine.line(
      image=image,
      pt1=pt1,
      pt2=pt2,
      color=color,
      thickness=thickness
    )
    return image

  def rectangle_target_tlbr(self, image, top, left, bottom, right, color, thickness=2):
    color = self.str_to_color(color)
    image = self.draw_engine.rectangle_target(
      image=image,
      pt1=(left, top),
      pt2=(right, bottom),
      color=color
    )
    return image

  def alpha_outer_area(self, image, left, top, right, bottom, intensity=170):
    self.log.start_timer('alpha_outer_area', section=self._timers_section)

    np_image = image.astype(np.uint16).copy()
    np_alpha = np.ones_like(np_image) * intensity
    np_alpha[top:bottom, left:right, :] = 0
    np_image = np_image + np_alpha
    np_image = np_image.clip(0, 255).astype(np.uint8)

    self.log.stop_timer('alpha_outer_area', section=self._timers_section)

    image = np_image
    return image

  def alpha_inner_area(self, image, left, top, right, bottom, intensity=170):
    self.log.start_timer('alpha_inner_area', section=self._timers_section)
    np_image = image.astype(np.uint16).copy()
    np_alpha = np.zeros_like(np_image)
    np_alpha[top:bottom, left:right, :] = intensity
    np_image = np_image + np_alpha
    np_image = np_image.clip(0, 255).astype(np.uint8)
    image = np_image
    self.log.stop_timer('alpha_inner_area', section=self._timers_section)
    return image

  def alpha_area(self, image, intensity=170):
    self.log.start_timer('alpha_area', section=self._timers_section)
    np_image = image.astype(np.uint16).copy()
    np_alpha = np.ones_like(np_image) * intensity
    np_image = np_image + np_alpha
    np_image = np_image.clip(0, 255).astype(np.uint8)
    image = np_image
    self.log.stop_timer('alpha_area', section=self._timers_section)
    return image

  def alpha_outer_poly_area(self, image, points, intensity=170):
    self.log.start_timer('alpha_outer_poly_area', section=self._timers_section)
    np_image = image.astype(np.uint16).copy()
    mask = 255
    img_canvas = np.zeros(shape=np_image.shape[:-1]).astype(np.uint8)
    cv2.fillPoly(img_canvas, [np.array(points)], mask)
    sel = img_canvas != mask
    np_image[sel] = np_image[sel] + intensity
    np_image[sel] = np_image[sel].clip(0, 255).astype(np.uint8)
    image = np_image
    self.log.stop_timer('alpha_outer_poly_area', section=self._timers_section)
    return image

  def alpha_inner_poly_area(self, image, points, intensity=170):
    self.log.start_timer('alpha_inner_poly_area', section=self._timers_section)
    np_image = image.astype(np.uint16).copy()
    mask = 255
    img_canvas = np.zeros(shape=np_image.shape[:-1]).astype(np.uint8)
    cv2.fillPoly(img_canvas, [np.array(points)], mask)
    sel = img_canvas == mask
    np_image[sel] = np_image[sel] + intensity
    np_image[sel] = np_image[sel].clip(0, 255).astype(np.uint8)
    image = np_image
    self.log.stop_timer('alpha_inner_poly_area', section=self._timers_section)
    return image

  def rectangle_target(self, image, pt1, pt2, color, thickness=2):
    color = self.str_to_color(color)
    image = self.draw_engine.rectangle_target(
      image=image,
      pt1=pt1,
      pt2=pt2,
      color=color,
      thickness=thickness,
    )
    return image

  def rectangle(self, image, pt1, pt2, color, thickness, force_in_frame=False):
    color = self.str_to_color(color)
    if force_in_frame:
      offset = [
        -pt1[0] if pt1[0] < 0 else 0,
        -pt1[1] if pt1[1] < 0 else 0
      ]
      pt1 = [pt1[i] + offset[i] for i in range(len(pt1))]
      pt2 = [pt2[i] + offset[i] for i in range(len(pt2))]
    # endif
    image = self.draw_engine.rectangle(
      image=image,
      pt1=pt1,
      pt2=pt2,
      color=color,
      thickness=thickness
    )
    return image

  def polygon(self, image, pts, color, thickness=2):
    image = self.draw_engine.polygon(
      image=image,
      pts=pts,
      color=color,
      thickness=thickness
    )
    return image

  def rectangle_tlbr(self, image, top, left, bottom, right, color=None, thickness=None):
    color = self.str_to_color(color)
    if color is None:
      color = ct.GREEN
      thickness = 1
    if thickness is None:
      thickness = 1
    image = self.draw_engine.rectangle(
      image=image,
      pt1=(left, top),
      pt2=(right, bottom),
      color=color,
      thickness=thickness
    )
    return image

  def circle(self, image, center, radius, color, thickness):
    image = self.draw_engine.circle(
      image=image,
      center=center,
      radius=radius,
      color=color,
      thickness=thickness
    )
    return image

  def arrow(self, image, pt1, pt2, color, thickness):
    image = self.draw_engine.arrow(
      image=image,
      pt1=pt1,
      pt2=pt2,
      color=color,
      thickness=thickness
    )
    return image

  def cross(self, image, point, color, thickness, size_factor=1e-2):
    image = self.draw_engine.cross(
      image=image,
      point=point,
      color=color,
      thickness=thickness,
      size_factor=size_factor
    )
    return image

  def crosses(self, image, points, color=ct.GREEN, thickness=DEFAULT_FONT_THICKNESS, size_factor=1e-2):
    self.log.start_timer('draw_crosses', section=self._timers_section)
    for point in points:
      image = self.cross(
        image=image,
        point=point,
        color=color,
        thickness=thickness,
        size_factor=size_factor
      )
    self.log.stop_timer('draw_crosses', section=self._timers_section)
    return image

  def cross_from_tlbr(self, image, tlbr, color=ct.GREEN, thickness=DEFAULT_FONT_THICKNESS):
    self.log.start_timer('cross_from_tlbr', section=self._timers_section)
    top, left, bottom, right = tlbr
    points = [
      [left, top],
      [right, top],
      [right, bottom],
      [left, bottom]
    ]
    image = self.crosses(
      image=image,
      points=points,
      color=color,
      thickness=thickness
    )
    self.log.stop_timer('cross_from_tlbr', section=self._timers_section)
    return image

  def text(self, image, text, org, font, font_scale, color, thickness=None):
    color = self.str_to_color(color)
    image = self.draw_engine.text(
      image=image,
      text=text,
      org=org,  # absolute value to keep label in image
      font=font,
      font_scale=font_scale,
      color=color,
      thickness=thickness
    )
    return image

  def text_size(self, text, font, font_scale, thickness):
    res = self.draw_engine.text_size(
      text=text,
      font=font,
      font_scale=font_scale,
      thickness=thickness
    )
    return res

  def multi_line_text(self,
                      image,
                      lst_texts,
                      org=None,
                      font=None,
                      font_scale=None,
                      color=None,
                      thickness=None,
                      line_spacing=None):
    if org is None:
      org = (10, 10)
    if font is None:
      font = DEFAULT_FONT
    if font_scale is None:
      font_scale = DEFAULT_FONT_SIZE
    if thickness is None:
      thickness = DEFAULT_FONT_THICKNESS
    if color is None:
      color = 'green'
    color = self.str_to_color(color)
    x, y = org
    line_spacing = None
    for text in lst_texts:
      twc, thc = self.text_size(text, font, font_scale, thickness)[0]
      line_spacing = int(thc * 1.2) if line_spacing is None else int(line_spacing)
      y += thc + line_spacing
      org = (x, y)
      image = self.text(
        image=image,
        text=text,
        org=org,
        font=font,
        font_scale=font_scale,
        color=color,
        thickness=thickness
      )
    return image

  def blur(self, image, kernel_size):
    image = self.draw_engine.blur(
      image=image,
      kernel_size=kernel_size
    )
    return image

  def gaussian_blur(self, image, ksize, sigmaX):
    image = self.draw_engine.gaussian_blur(
      image=image,
      ksize=ksize,
      sigmaX=sigmaX
    )
    return image

  def save(self, image, fn='', folder='output', show_prefix=False):
    assert folder in [None, 'data', 'output', 'models']
    lfld = self.log.get_target_folder(target=folder)

    file_prefix, file_ext = os.path.splitext(fn)
    if file_ext == '':
      file_ext = '.jpg'
    fn = file_prefix

    if lfld is not None:
      file_prefix = '' if not show_prefix else self.log.file_prefix + "_"
      save_path = lfld
      file_name = file_prefix + fn + file_ext
      out_file = os.path.join(save_path, file_name)
    else:
      out_file = fn + file_ext

    self.draw_engine.save(
      path=out_file,
      image=image
    )
    return

  def alpha_text_line_bottom_right(self,
                                   image,
                                   text,
                                   color=None,
                                   font=None,
                                   size=None,
                                   thickness=1,
                                   ):
    """
    Draws a nice semi-opaque line with text inside it using bottom left coord

    Parameters
    ----------
    image : TYPE
      the input image.
    bottom : TYPE
      top coord.
    left : TYPE
      left coord.
    text : str or list[str]
      text to display.
    color : TYPE, optional
      color . The default is None (blue).
    font : TYPE, optional
      font. The default is None.
    size : TYPE, optional
      font size. The default is None.
    thickness : TYPE, optional
      font boldness. The default is None.

    Returns
    -------
    TYPE
      modified image.

    """
    color = self.str_to_color(color)

    if font is None:
      font = DEFAULT_FONT
    if size is None:
      size = 0.5
    if thickness is None:
      thickness = 2
    if color is None:
      color = ct.DARK_BLUE

    twc, thc = self.text_size(
        text=text,
        font=font,
        font_scale=size,
        thickness=thickness
    )[0]
    bottom = image.shape[0] - 1
    left = image.shape[1] - (twc + 10)
    top = bottom - thc
    right = left + twc

    np_image = image.astype(np.uint16).copy()
    np_image[top:bottom, left:right, :] += 100
    np_image = np_image.clip(0, 255).astype(np.uint8)

    np_image = self.text(
        image=np_image,
        text=text,
        org=(left + 1, bottom),
        font=font,
        font_scale=size,
        color=color,
        thickness=thickness
    )

    return np_image

  def alpha_text_rectangle_position(self,
                                    image,
                                    text,
                                    y_position='top',
                                    x_position='left',
                                    y_offset=None,
                                    x_offset=None,
                                    color=None,
                                    font=None,
                                    size=None,
                                    thickness=None,
                                    return_shape=False,
                                    background_opacity=100
                                    ):
    """
    Draws semi-opaque box with text inside it at specified location (ex: top-left, top-right, etc)    

    """
    assert x_position in ['left', 'right']
    assert y_position in ['top', 'bottom']

    H, W, _ = image.shape
    top, left, bottom, right = None, None, None, None
    _OFFSET = 10
    _SEPARATOR = 8

    color = self.str_to_color(color)
    if font is None:
      font = DEFAULT_FONT
    if size is None:
      size = 0.7
    if thickness is None:
      thickness = 2
    if color is None:
      color = ct.DARK_BLUE

    # calculate text size

    texts = text if isinstance(text, list) else [text]
    n_texts = len(texts)

    tw, th = 0, 0
    for t in texts:
      twc, thc = self.text_size(
        text=t,
        font=font,
        font_scale=size,
        thickness=thickness
      )[0]
      th = max(th, thc)
      tw = max(tw, twc)

    height = (th + _SEPARATOR) * n_texts
    width = tw + _SEPARATOR

    if y_position == 'top':
      top = y_offset or _OFFSET
      bottom = top + height
      if x_position == 'left':
        left = x_offset or _OFFSET
        right = left + width
      else:
        right = W - (x_offset or _OFFSET)
        left = right - width
    else:
      bottom = H - (y_offset or _OFFSET)
      top = bottom - height
      if x_position == 'left':
        left = x_offset or _OFFSET
        right = left + width
      else:
        right = W - (x_offset or _OFFSET)
        left = right - width

    res = self.alpha_text_rectangle(
      image=image,
      text=text,
      left=left,
      top=top,
      color=color,
      font=font,
      size=size,
      thickness=thickness,
      return_shape=return_shape,
      background_opacity=background_opacity
    )
    return res

  def alpha_text_rectangle(self,
                           image,
                           text,
                           left,
                           top=None,
                           bottom=None,
                           color=None,
                           font=None,
                           size=None,
                           thickness=None,
                           return_shape=False,
                           background_opacity=100):
    """
    Draws a nice semi-opaque box with text inside it

    Parameters
    ----------
    image : TYPE
      the input image.
    top : TYPE
      top coord.
    bottom : TYPE
      bottom coord.
    left : TYPE
      left coord.
    text : str or list[str]
      text to display.
    color : TYPE, optional
      color . The default is None (blue).
    font : TYPE, optional
      font. The default is None.
    size : TYPE, optional
      font size. The default is None.
    thickness : TYPE, optional
      font boldness. The default is None.
    return_shape : TYPE, optional
      return the shape of the drawn rectangle with text. The default is False.

    Returns
    -------
    TYPE
      modified image.

    """
    if image is None:
      return

    assert any(x is not None for x in [top, bottom]), 'You should either provide top or bottom'
    assert not all(x is not None for x in [top, bottom]), 'You should either provide top or bottom'

    self.log.start_timer('alpha_text_rectangle', section=self._timers_section)
    color = self.str_to_color(color)
    if font is None:
      font = DEFAULT_FONT
    if size is None:
      size = 0.7
    if thickness is None:
      thickness = 2
    if color is None:
      color = ct.DARK_BLUE

    _SEPARATOR = 8

    texts = text if isinstance(text, list) else [text]
    n_texts = len(texts)

    tw, th = 0, 0
    for text in texts:
      twc, thc = self.text_size(
        text=text,
        font=font,
        font_scale=size,
        thickness=thickness
      )[0]
      th = max(th, thc)
      tw = max(tw, twc)

    height = (th + _SEPARATOR) * n_texts
    width = tw + _SEPARATOR

    if top is not None:
      bottom = top + height
    else:
      top = bottom - height

    # bottom = top + (th + _SEPARATOR) * n_texts
    right = left + width

    np_image = image.astype(np.uint16).copy()
    np_image[top:bottom, left:right, :] += background_opacity
    np_image = np_image.clip(0, 255).astype(np.uint8)

    text_bottom = top + th + 1
    for text in texts:
      np_image = self.text(
        image=np_image,
        text=text,
        org=(left + 1, text_bottom),
        font=font,
        font_scale=size,
        color=color,
        thickness=thickness
      )
      text_bottom += th + _SEPARATOR

    self.log.stop_timer('alpha_text_rectangle', section=self._timers_section)
    if return_shape:
      return np_image, (left, top, bottom, right)
    else:
      return np_image

  def draw_interest_point(
      self,
      img,
      point,
      conf,
      color=None,
      threshold=0.5,
      make_square=False,
      thickness=4,
      inner_thickness=None,
      outer_thickness=None,
      to_flip=False,
      **kwargs
  ):
    """
    Helper method that draws a point of interest on an image.
    A point of interest has a center area and a border area.
    The color of the border is based on the confidence score
    of the point and the provided threshold.
    Parameters
    ----------
    img : np.ndarray, input image
    point : tuple, (x, y)
    conf : float, confidence score of the point
    color : tuple, (r, g, b)
    threshold : float, threshold for the confidence score
    make_square : bool, if True the point will be drawn as a square
    thickness : int, default thickness for both inner and outer areas
    inner_thickness : int, thickness of the inner area
    outer_thickness : int, thickness of the border area
    to_flip : bool, if True the point will be flipped
    kwargs : dict, additional parameters

    Returns
    -------
    img : np.ndarray, drawn image
    """
    if to_flip:
      point = np.flip(point)
    border_color = ct.RED if conf < threshold else ct.GREEN
    inner_thickness = thickness if inner_thickness is None else inner_thickness
    outer_thickness = thickness if outer_thickness is None else outer_thickness
    inner_thickness, outer_thickness = int(inner_thickness), int(outer_thickness)
    if color is None:
      # if no color is specified the entire point will be
      # colored based on its confidence
      color = border_color
    if make_square:
      if inner_thickness > 0:
        p1, p2 = gmt.make_square(point, radius=inner_thickness)
        img = self.rectangle(img, p1, p2, color=color, thickness=inner_thickness)
      if outer_thickness > 0:
        p1, p2 = gmt.make_square(point, radius=inner_thickness + outer_thickness)
        img = self.rectangle(img, p1, p2, color=border_color, thickness=outer_thickness)
    else:
      if inner_thickness > 0:
        img = self.circle(
          img, point, radius=inner_thickness,
          color=color, thickness=inner_thickness
        )
      if outer_thickness > 0:
        img = self.circle(
          img, point, radius=inner_thickness + outer_thickness,
          color=border_color, thickness=outer_thickness
        )

    return img

  def draw_interest_points(
      self,
      img,
      points,
      scores,
      color=None,
      threshold=0.5,
      make_square=False,
      to_flip=False,
      **kwargs
    ):
    """
    Helper method that draws a list of interest points on an image.
    Parameters
    ----------
    points : list, list of points
    scores : list, list of confidence scores
    img : np.ndarray, input image
    color : tuple, (r, g, b)
    threshold : float, threshold for the confidence score
    make_square : bool, if True the point will be drawn as a square
    to_flip : bool, if True the point will be flipped
    kwargs : dict, additional parameters

    Returns
    -------
    img : np.ndarray, drawn image
    """
    assert len(points) == len(scores), "Arrays points and scores should have the same length"
    for it in range(len(points)):
      point = np.flip(points[it]).astype(int) if to_flip else points[it].astype(int)
      img = self.draw_interest_point(img=img, point=point,
                                     conf=scores[it], color=color,
                                     threshold=threshold, make_square=make_square)

    return img

  def draw_box_with_alpha_text(self,
                               image,
                               box_top,
                               box_left,
                               box_bottom,
                               box_right,
                               box_color=COLOR_BLUE,
                               text=None,
                               text_font=DEFAULT_FONT,
                               text_font_scale=DEFAULT_FONT_SIZE,
                               text_thickness=DEFAULT_FONT_THICKNESS,
                               text_color=COLOR_WHITE
                               ):
    # draw object rectangle
    pt1 = (box_left, box_top)
    pt2 = (box_right, box_bottom)
    image = self.rectangle(
      image=image,
      pt1=pt1,
      pt2=pt2,
      color=box_color,
      thickness=2
    )

    if text:
      image = self.alpha_text_rectangle(
        image=image,
        bottom=box_top,
        left=box_left,
        text=text,
        color=text_color,
        font=text_font,
        size=text_font_scale,
        thickness=text_thickness
      )
    return image

  def draw_detection_box(self, image,
                         top,
                         left,
                         bottom,
                         right,
                         label=None,
                         index=None,
                         prc=None,
                         text=None,
                         font=DEFAULT_FONT,
                         font_scale=DEFAULT_FONT_SIZE,
                         thickness=DEFAULT_FONT_THICKNESS,
                         color=COLOR_BLUE,
                         color_label=COLOR_WHITE
                         ):
    # draw object rectangle
    left = int(left)
    top = int(top)
    right = int(right)
    bottom = int(bottom)
    pt1 = (left, top)
    pt2 = (right, bottom)
    image = self.rectangle(
      image=image,
      pt1=pt1,
      pt2=pt2,
      color=color,
      thickness=2
    )

    # calculate label dimensions
    # text = '{}, {}, {}, {} '.format(top, left, bottom, right)
    # text = ''
    if text is None:
      text = ''
    elif not isinstance(text, str):
      text = str(text)

    if index:
      text_idx = '{} '.format(index)
      image = self.text(
        image=image,
        text=text_idx,
        org=(int(right - ((right - left) / 2)), int(bottom - ((bottom - top) / 2))),
        font=font,
        font_scale=font_scale,
        color=(0, 255, 0),
        thickness=thickness
      )

    if label:
      text += '{}'.format(label)
    if prc:
      if prc > 1:
        text += ' {:.1f}%'.format(prc)
      else:
        text += ' {:.3f}'.format(prc)

    if text != '':
      (tw, th), baseline = self.text_size(
        text=text,
        font=font,
        font_scale=font_scale,
        thickness=thickness
      )

      top_offset = min(top - 2 * th, 0) * -1

      # draw label rectangle
      image = self.rectangle(
        image=image,
        pt1=(left, top - 2 * th + top_offset),
        pt2=(left + tw, top + top_offset),
        color=color,
        thickness=-1,
        force_in_frame=True
      )

      # draw label
      image = self.text(
        image=image,
        text=text,
        org=(left, top - th + top_offset),
        font=font,
        font_scale=font_scale,
        color=color_label,
        thickness=thickness
      )
    return image

  def wrap_text(self, text, font, font_size, thickness, width):
    """
    Split a text in parts such that each part can fit in the width of an image.

    The method has 2 while loops. The 2nd one is an iterative approximation of the number of 
    characters that can fit in the image, and generally does not perform more than 3 loops. 

    Parameters
    ----------
    text : str
        The text
    font : Any
        the font used
    font_size : Any
        The font size
    thickness : int
        The thickness of the text
    width : int
        The width of the image.

    Returns
    -------
    list[str]
        A list of text parts that can fit perfectly in the width of the image.
    """
    wrap_text = []
    while (len(text) > 0):
      max_chr_per_W = len(text)
      twc, _ = self.text_size(
          text=text[:max_chr_per_W],
          font=font,
          font_scale=font_size,
          thickness=thickness
        )[0]
      while twc > width:
        max_chr_per_W = int(width / twc * max_chr_per_W)
        twc, _ = self.text_size(
          text=text[:max_chr_per_W],
          font=font,
          font_scale=font_size,
          thickness=thickness
        )[0]
      wrap_text.append(text[:max_chr_per_W])
      text = text[max_chr_per_W:]

    return wrap_text

  def draw_text_outer_image(self, image, text, font=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE, color=COLOR_WHITE, thickness=DEFAULT_FONT_THICKNESS, location="top"):
    """
    Draw text outside the image, either on top or on bottom. This will add a black bar nad therefore change the shape of the image.
    Location must be one of ["top", "bottom"]
    """
    assert location in ["top", "bottom"]

    H, W, C = image.shape
    top, left, bottom, right = None, None, None, None
    _OFFSET = 10
    _SEPARATOR = 8

    color = self.str_to_color(color)
    if font is None:
      font = DEFAULT_FONT
    if font_size is None:
      font_size = 0.7
    if thickness is None:
      thickness = 2
    if color is None:
      color = ct.DARK_BLUE

    texts = text if isinstance(text, list) else [text]
    wrapped_texts = []
    for text in texts:
      wrapped_texts += self.wrap_text(text, font, font_size, thickness, W)
    n_texts = len(wrapped_texts)

    th = 0
    for t in wrapped_texts:
      _, thc = self.text_size(
        text=t,
        font=font,
        font_scale=font_size,
        thickness=thickness
      )[0]
      th = max(th, thc)

    height = (th + _SEPARATOR) * n_texts

    empty_img = np.full((H + height, W, C), 0, dtype=image.dtype)
    if location == "top":
      empty_img[height:, :, :] = image
      image = empty_img

      text_bottom = 1 + th
      for text in wrapped_texts:
        image = self.text(
          image=image,
          text=text,
          org=(1, text_bottom),
          font=font,
          font_scale=font_size,
          color=color,
          thickness=thickness,
        )
        text_bottom += th + _SEPARATOR

    else:
      empty_img[:-height, :, :] = image
      image = empty_img

      text_bottom = H + 1 + th
      for text in wrapped_texts:
        image = self.text(
          image=image,
          text=text,
          org=(1, text_bottom),
          font=font,
          font_scale=font_size,
          color=color,
          thickness=thickness,
        )
        text_bottom += th + _SEPARATOR

    return image

  def blur_raw(
      self,
      image, top, left, bottom, right,
      color=None,
      method='scale', scale_resize=6, blur_resize_factor=30
    ):
    assert method in ['scale', 'gaussian']
    top = int(top)
    left = int(left)
    bottom = int(bottom)
    right = int(right)
    if top >= bottom or left >= right:
      print('Please check your object coordinates: [{}, {}, {}, {}]'.format(top, left, bottom, right))
    if color is not None:
      small_img = np.ones((bottom - top, right - left, 3), dtype='uint8') * color
    else:
      ksize = (91, 91)
      sigmaX = 0
      self.log.start_timer('blur_raw_copy', section=self._timers_section)
      small_img = image[top:bottom, left:right, :]
      self.log.stop_timer('blur_raw_copy', section=self._timers_section)

      self.log.start_timer('blur_raw_' + method, section=self._timers_section)
      if method == 'gaussian':
        small_img = self.draw_engine.gaussian_blur(small_img, ksize, sigmaX)
      elif method == 'scale':
        small_img = self.draw_engine.scale_blur(
          small_img,
          min_resize=scale_resize,
          blur_resize_factor=blur_resize_factor
        )
      else:
        raise ValueError("Unknown blur method '{}'".format(method))
      self.log.stop_timer('blur_raw_' + method, section=self._timers_section)

    self.log.start_timer('blur_raw_paste', section=self._timers_section)
    image[top:bottom, left:right, :] = small_img
    del small_img
    self.log.stop_timer('blur_raw_paste', section=self._timers_section)
    return image

  def blur_adaptive(self, np_img, left, top, right, bottom,
                    color=None, DIRECT=False,
                    method='scale', scale_resize=6, blur_resize_factor=30
                    ):
    assert method in ['scale', 'gaussian']
    ksize = (91, 91)
    sigmaX = 0
    width = right - left
    height = bottom - top
    if DIRECT:
      y1, x1, y2, x2 = int(top), int(left), int(bottom), int(right)
    else:
      if width > height:
        x_scal = 20
        y_scal = 8
      else:
        x_scal = 8
        y_scal = 20
      y1 = int(top + (height // y_scal))
      x1 = int(left + (width // x_scal))
      y2 = int(y1 + height // 1.5)
      x2 = int(x1 + width - (width // x_scal * 2))

    if color is not None:
      np_img[y1:y2, x1:x2, :] = color
    else:
      self.log.start_timer('blur_adaptive_copy', section=self._timers_section)
      np_src = np_img[y1:y2, x1:x2, :]
      self.log.stop_timer('blur_adaptive_copy', section=self._timers_section)

      self.log.start_timer('blur_adaptive_' + method, section=self._timers_section)
      if method == 'gaussian':
        np_dst = self.draw_engine.gaussian_blur(np_src, ksize, sigmaX)
      elif method == 'scale':
        np_dst = self.draw_engine.scale_blur(
          np_src,
          min_resize=scale_resize,
          blur_resize_factor=blur_resize_factor
        )
      else:
        raise ValueError("Unknown blur method '{}'".format(method))
      self.log.stop_timer('blur_adaptive_' + method, section=self._timers_section)

      self.log.start_timer('blur_adaptive_paste', section=self._timers_section)
      np_img[y1:y2, x1:x2, :] = np_dst
      del np_src
      del np_dst
      self.log.stop_timer('blur_adaptive_paste', section=self._timers_section)
    return np_img

  def blur_person(self, frame,
                  top,
                  left,
                  bottom,
                  right,
                  object_type=ct.FACE,
                  color=None,
                  blur_type=ct.BLUR_ADAPTIVE,
                  method='scale',
                  scale_resize=6, blur_resize_factor=30
                  ):
    object_type = object_type.upper()
    blur_type = blur_type.upper()
    assert object_type in [ct.FACE, ct.PERSON]
    assert blur_type in [ct.BLUR_ADAPTIVE, ct.BLUR_RAW]

    top = max(top, 0)
    left = max(left, 0)
    bottom = min(bottom, frame.shape[0])
    right = min(right, frame.shape[1])

    if top >= bottom or left >= right:
      return frame

    if blur_type == ct.BLUR_ADAPTIVE:
      direct = object_type == ct.FACE
      frame = self.blur_adaptive(
        np_img=frame,
        top=top,
        left=left,
        bottom=bottom,
        right=right,
        DIRECT=direct,
        color=color,
        method=method,
      )
    else:
      _bottom = bottom
      if object_type != ct.FACE:
        _bottom = int(top + (_bottom - top) / 2)
      frame = self.blur_raw(
        image=frame,
        top=top,
        left=left,
        bottom=_bottom,
        right=right,
        color=color,
        method=method,
        scale_resize=scale_resize,
        blur_resize_factor=blur_resize_factor
      )
    return frame

  def blur_persons(self, frame, lst_persons, blur_type=ct.BLUR_ADAPTIVE, color=None, method='scale',
                   scale_resize=6, blur_resize_factor=30
                   ):
    for obj in lst_persons:
      top, left, bottom, right = obj[ct.TLBR_POS]
      frame = self.blur_person(
        frame=frame,
        top=top,
        left=left,
        bottom=bottom,
        right=right,
        object_type=ct.PERSON,
        blur_type=blur_type,
        color=color,
        method='scale',
        scale_resize=scale_resize,
        blur_resize_factor=blur_resize_factor
      )
    return frame

  def blur_faces(self, frame, lst_faces, color=None, blur_type=ct.BLUR_ADAPTIVE):
    for obj in lst_faces:
      top, left, bottom, right = obj[ct.TLBR_POS]
      frame = self._painter.blur_person(
        frame=frame,
        top=top,
        left=left,
        bottom=bottom,
        right=right,
        object_type=ct.FACE,
        color=color,
        blur_type=blur_type
      )
    return frame

  def draw_inference_boxes(self, image,
                           lst_inf,
                           color=COLOR_BLUE,
                           color_label=COLOR_GREEN,
                           draw_label=True,
                           draw_box_index=False,
                           font=DEFAULT_FONT,
                           font_scale=DEFAULT_FONT_SIZE,
                           min_confidence=0
                           ):
    """
    This method is obsolete. Please use `draw_inference_boxes_advanced`
    """
    image = self.draw_inference_boxes_advanced(
      image=image,
      lst_inf=lst_inf,
      color=color,
      color_label=color_label,
      show_label=draw_label,
      show_percent=draw_label,
      draw_random_box_index=draw_box_index,
      font=font,
      font_scale=font_scale,
      min_confidence=min_confidence
    )
    return image

  def draw_inference_boxes_advanced(self,
                                    image,
                                    lst_inf,
                                    show_label=False,
                                    show_percent=False,
                                    draw_custom_property=None,
                                    custom_text_callback=None,
                                    draw_random_box_index=False,
                                    color=COLOR_BLUE,
                                    color_label=COLOR_GREEN,
                                    font=DEFAULT_FONT,
                                    font_scale=DEFAULT_FONT_SIZE,
                                    min_confidence=0
                                    ):
    for idx, res in enumerate(lst_inf):
      top, left, bottom, right = res['TLBR_POS']

      text, prc, lbl = None, None, None
      if show_label:
        lbl = res.get('META_TYPE', res.get('TYPE'))

      if show_percent:
        prc = res['PROB_PRC']

      if draw_custom_property:
        text = res.get(draw_custom_property, None)

      if custom_text_callback:
        text = custom_text_callback(res)

      track_id = res.get('TRACK_ID')
      if track_id is not None:
        lbl = str(track_id) if lbl is None else lbl + '({})'.format(track_id)

      if res['PROB_PRC'] >= min_confidence:
        image = self.draw_detection_box(
          image=image,
          top=top,
          left=left,
          bottom=bottom,
          right=right,
          index=idx if draw_random_box_index else None,
          label=lbl,
          prc=prc,
          text=text,
          font=font,
          font_scale=font_scale,
          color=color,
          color_label=color_label
        )
    return image

  def detect_and_plot(self,
                      path_src,
                      path_dst,
                      graph,
                      lst_filter=None,
                      save_inferences=False,
                      color=COLOR_BLUE,
                      color_label=COLOR_GREEN,
                      font=DEFAULT_FONT,
                      font_scale=DEFAULT_FONT_SIZE
                      ):
    from tqdm import tqdm
    os.makedirs(path_dst, exist_ok=True)

    self.P('Reading images...')
    lst_paths, lst_imgs = self.read(
      path=path_src,
      reverse_channels=self._engine == ENGINE_OPENCV,
      return_path=True
    )

    self.P('Infering and drawing images....')
    for path_img, img in tqdm(zip(lst_paths, lst_imgs)):
      np_imgs = np.expand_dims(img, axis=0)
      lst_inf = graph.predict(np_imgs)['INFERENCES'][0]
      if lst_filter:
        lst_inf = list(filter(lambda x: x['TYPE'] in lst_filter, lst_inf))

      img_draw = img[:, :, ::-1] if self._engine == ENGINE_OPENCV else img
      img_draw = self.draw_inference_boxes(
        image=img_draw,
        lst_inf=lst_inf,
        color=color,
        color_label=color_label,
        font=font,
        font_scale=font_scale
      )

      name = os.path.basename(path_img)
      fn = os.path.join(path_dst, name)
      self.save(
        image=img_draw,
        fn=fn
      )

      if save_inferences:
        self.log.save_json(
          dct={'INFERENCES': lst_inf},
          fname=fn + '.txt'
        )
    # endfor
    return

  def read_texture(self, path):
    texture = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if texture is not None:
      texture = cv2.cvtColor(texture, cv2.COLOR_BGRA2RGBA)
    return texture

  def draw_texture(self, image, texture, x, y, angle=None, color=None):
    hx = int(texture.shape[1] / 2)
    hy = int(texture.shape[0] / 2)

    cx = x - hx
    cy = y - hy

    bottom_x = min(image.shape[1], cx + 2 * hx)
    bottom_y = min(image.shape[0], cy + 2 * hy)

    top_x = max(0, -cx)
    top_y = max(0, -cx)

    texture_copy = texture

    if angle is not None:
      texture_copy = self.rotate_image(
        image=texture,
        angle=angle
      )

    # if color is not None:
    #   base_gray = cv2.cvtColor(texture_copy, cv2.COLOR_RGBA2GRAY)
    #   texture_copy = np.array([base_gray * color[0], base_gray*color[1], base_gray*color[2]])

    alpha_s = texture_copy[max(0, -cy):bottom_y - cy, max(0, -cx):bottom_x - cx, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(3):
      image[max(0, cy):bottom_y, max(0, cx):bottom_x, c] = (alpha_s * texture_copy[max(0, -cy):bottom_y - cy, max(0, -cx):bottom_x - cx, c] +
                                                            alpha_l * image[max(0, cy):bottom_y, max(0, cx):bottom_x, c])

    return image

  def apply_sticker(self, image, sticker, offset=0, frame_color=None, start_x=0, start_y=0, return_endpoint=False):
    if sticker is None:
      return image if not return_endpoint else (image, (0, 0))
    if frame_color is None:
      frame_color = ct.GREEN
    img_h, img_w, _ = image.shape
    crop_h, crop_w, _ = sticker.shape
    min_h, min_w = min(crop_h, img_h - 2 * offset - start_x), min(crop_w, img_w - 2 * offset - start_y)
    frame_top, frame_bottom = int(start_x), int(start_x + min_h + 2 * offset)
    frame_left, frame_right = int(start_y), int(start_y + min_w + 2 * offset)
    image[frame_top: frame_bottom, frame_left: frame_right] = frame_color
    # image[:min_h + 2 * offset, :min_w + 2 * offset] = frame_color
    sticker_top, sticker_bottom = int(start_x + offset), int(start_x + min_h + offset)
    sticker_left, sticker_right = int(start_y + offset), int(start_y + min_w + offset)
    image[sticker_top: sticker_bottom, sticker_left: sticker_right] = sticker[:min_h, :min_w]
    return image if not return_endpoint else (image, (frame_bottom, frame_right))

  def apply_stickers(self, image, stickers, offset=0, frame_color=None):
    start_x = 0
    for sticker in stickers:
      image, (x, y) = self.apply_sticker(
        image=image,
        sticker=sticker,
        offset=offset,
        frame_color=frame_color,
        start_x=start_x,
        return_endpoint=True
      )
      start_x = x
    # endfor sticker in stickers
    return image

  def rotate_image(self, image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result
