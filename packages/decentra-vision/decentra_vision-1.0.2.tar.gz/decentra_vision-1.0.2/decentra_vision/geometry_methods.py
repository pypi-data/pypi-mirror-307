import math
import numpy as np


# method for computing the determinant of 
# a matrix M corespondent of the triangle 
# determined by points A(x1, y1), B(x2, y2), C(x3, y3)
#           x1 y1 1
# where M = x2 y2 1
#           x3 y3 1
def triangle_area_determinant(A, B, C):
  points = [A, B, C]
  N = len(points)
  # extracting the coordinates
  x = [x_coord for (x_coord, _) in points]
  y = [y_coord for (_, y_coord) in points]

  det = np.sum([((x[it] * y[(it + 1) % N]) - (x[(it + 1) % N] * y[it])) for it in range(N)])

  return det


# method for computing area of a triangle
# determined by points A, B, C
def triangle_area(A, B, C):
  return np.abs(triangle_area_determinant(A, B, C) / 2)


# method for checking if points C and D are on the same side
# of the line determined by the points A and B
def same_side_of_line(A, B, C, D):
  det1 = triangle_area_determinant(A, B, C)
  det2 = triangle_area_determinant(A, B, D)

  sgn1, sgn2 = np.sign([det1, det2])

  if sgn1 * sgn2 < 0:
    return False
  return True


# bool method that returns true if point A is on
# the right side of point B
def right_side_of(A, B):
  return A[1] > B[1]


# method for computing the euclidian distance
# between two points A an B
def euclidian_distance(A, B):
  return math.sqrt(sum([(a-b)**2 for a, b in zip(A, B)]))


def distance_points_point(points: np.ndarray, point: np.ndarray, method='l2'):
  """
  Method for computing the distance from a list of points to a point.
  Parameters
  ----------
  points - np.ndarray, array of points
  point - np.ndarray, point
  method - str, method used to compute the distance
  - if 'l2' it will compute the l2 distance
  - if 'l1' it will compute the l1 distance

  Returns
  -------
  res - np.ndarray, array of the same length as points containing
  the distances corresponding to each point in points from the specified point
  """
  if method == 'l1':
    return np.sum([np.abs((points-point)[:, i]) for i in range(points.shape[-1])], axis=0)
  elif method == 'l2':
    return np.linalg.norm(points-point, axis=1)



# returns ratio between lengths of 2 segments or None if points C and D are the same
def segments_ratio(A, B, C, D):
  x, y = euclidian_distance(A, B), euclidian_distance(C, D)
  if y == 0:
    return None
  return x / y


def swap_axes(A):
  x, y = A
  return y, x


# method for computing distance between 2 rectangles
# both parallel with XOY axes and where:
# rectangle 1 top-left corner in A
# rectangle 1 bottom-right corner in B
# rectangle 2 top-left corner in C
# rectangle 2 bottom-right corner in D
def rectangles_distance(A, B, C, D):
  center1 = (A + B) / 2
  center2 = (C + D) / 2
  extent1 = np.abs(A - B) / 2
  extent2 = np.abs(C - D) / 2

  res = np.abs(center1 - center2) - (extent1 + extent2)

  res = [max(x, 0) for x in res]

  dst = math.sqrt(sum([x ** 2 for x in res]))
  return dst


def line_angle(A, B, keep_first_quadrant=False):
  """
  Method for computing the angle formed by the line AB and the OX axis.
  Parameters
  ----------
  A - np.ndarray, point A
  B - np.ndarray, point B
  keep_first_quadrant - bool, if True the angle will be in [0, 90] degrees

  Returns
  -------
  angle - float, angle formed by the line AB and the OX axis
  """
  x, y = np.abs(B - A) if keep_first_quadrant else (B - A)
  return math.degrees(math.atan2(x, y))


# returns the angle formed by points A, B, C in degrees
def angle(A, B, C):
  ang = math.degrees(math.atan2(A[1] - B[1], A[0] - B[0]) - math.atan2(C[1] - B[1], C[0] - B[0]))
  return ang + 360 if ang < 0 else ang


# given a list of N points, the degrees to rotate by and the
# origin point we will return the list of N points rotated
# by :degrees: degrees around the origin point
def rotate_points(points, degrees, orig=[0, 0], flipped_axes=False):
  if len(points) < 1 or degrees == 0:
    return points
  
  if flipped_axes:
    points = np.flip(points, 1)
  s = math.sin(math.radians(degrees))
  c = math.cos(math.radians(degrees))

  res = np.array([
    [
      orig[0] + c * (p[0] - orig[0]) - s * (p[1] - orig[1]),
      orig[1] + s * (p[0] - orig[0]) + c * (p[1] - orig[1])
    ]
    for p in points
  ])

  return res


def convert_detections(tlbr, keypoint_coords, to_flip=False, inverse_keypoint_coords=False):
  """
  Method for converting keypoints detections coordinates from
  [0, 1]^2 to N^2
  Parameters
  ----------
  tlbr - list, [top, left, bottom, right] coordinates of the bounding box
  keypoint_coords - np.ndarray, array of shape (N, 2) containing the keypoints coordinates
  to_flip - bool, if True the resulting coordinates will be flipped
  inverse_keypoint_coords - bool,
    if True the first value of the coordinates will be scaled by the width and the second by the height
    if False the first value of the coordinates will be scaled by the height and the second by the width
  Returns
  -------
  keypoint_coords - np.ndarray, array of shape (N, 2) containing the keypoints coordinates
  height - int, height of the bounding box
  width - int, width of the bounding box
  """
  top, left, bottom, right = tlbr

  height, width = bottom - top, right - left

  if inverse_keypoint_coords:
    keypoint_coords[:, 1] = (keypoint_coords[:, 1] * height + top).astype(np.int32)
    keypoint_coords[:, 0] = (keypoint_coords[:, 0] * width + left).astype(np.int32)
  else:
    keypoint_coords[:, 0] = (keypoint_coords[:, 0] * height + top).astype(np.int32)
    keypoint_coords[:, 1] = (keypoint_coords[:, 1] * width + left).astype(np.int32)
  #endif

  if to_flip:
    keypoint_coords = np.flip(keypoint_coords, 1)

  return keypoint_coords, height, width


# method that given a list of points returns their bounding box
def points_to_tlbr(points):
  x, y = tuple(zip(*points))
  top, bottom = min(x), max(x)
  left, right = min(y), max(y)

  return top, left, bottom, right


def center_point(points):
  if len(points) < 1:
    return None

  if not isinstance(points, np.ndarray):
    points = np.array(points)

  s = points.sum(axis=0)
  return s / len(points)


def compute_points_spreadness(tlbr, points):
  t, l, b, r = tlbr
  area = (b - t + 1) * (r - l + 1)
  center = center_point(points)

  diff = points - center
  dist = np.array([(x * x + y * y) / area for (x, y) in diff])

  std = np.std(dist)
  return std


# method for making a square with center in point and inscribed in a circle with a given radius
def make_square(point, radius=0):
  p1 = np.array([max(point[0] - radius, 0), max(point[1] - radius, 0)])
  p2 = np.array([point[0] + radius, point[1] + radius])

  return p1, p2


# method for checking if point p is inside the rectange determined by points
# A(x1, y1) and B(x2, y2)
def is_in_rectangle(p, x1, y1, x2, y2):
  xmin, ymin = min(x1, x2), min(y1, y2)
  xmax, ymax = x1 + x2 - xmin, y1 + y2 - ymin

  if xmin > p[0] or xmax < p[0]:
    return False

  if ymin > p[1] or ymax < p[1]:
    return False

  return True


def tlbr_area(tlbr):
  return (tlbr[2] - tlbr[0] + 1) * (tlbr[3] - tlbr[1] + 1)


# method that receives 2 rectangles (in tlbr format) and computes
# their intersection
def box_intersection(box1, box2):
  t1, l1, b1, r1 = box1
  t2, l2, b2, r2 = box2
  xA, yA = max(l1, l2), max(t1, t2)
  xB, yB = min(r1, r2), min(b1, b2)
  inter_length, inter_height = (xB - xA + 1), (yB - yA + 1)
  inter_area = np.maximum(inter_length, 0) * np.maximum(inter_height, 0)
  return inter_area


# method for checking if box1 is inside box2
def box_inside_box(box1, box2):
  return tlbr_area(box1) == box_intersection(box1, box2)


# method for checking which detections intersect or are too close
# to another detection
# CONVENTION: if detection A is fully inside detection B, then
# just detection A will be discarded
def compute_intersecting(tlbrs, min_dist=0):
  n = len(tlbrs)
  intersecting = np.zeros(n, dtype="bool")
  offset = np.array([-min_dist, -min_dist, min_dist, min_dist])

  for i in range(n):
    for j in range(i + 1, n):
      if box_inside_box(tlbrs[i], tlbrs[j]):
        intersecting[i] = True
      elif box_inside_box(tlbrs[j], tlbrs[i]):
        intersecting[j] = True
      elif box_intersection(tlbrs[i] + offset, tlbrs[j] + offset) > 0:
        intersecting[i] = True
        intersecting[j] = True
      # endif
  # endfor
  return intersecting


def intersecting_segments(segment1, segment2, strict=True):
  """
  Method for checking if 2 segments intersect
  Parameters
  ----------
  segment1 - tuple, (A, B) where A and B are points
  segment2 - tuple, (C, D) where C and D are points

  Returns
  -------
  res - bool, True if the 2 segments intersect, False otherwise
  """
  A, B = segment1
  C, D = segment2
  if strict:
    res = not same_side_of_line(A, B, C, D) and not same_side_of_line(C, D, A, B)
  else:
    res = not same_side_of_line(A, B, C, D) or not same_side_of_line(C, D, A, B)

  return res


if __name__ == '__main__':
  def test_convert_detections(n_tests=100):
    print(f"Testing convert_detections with {n_tests} attempts...")
    cnt_diff = [0, 0]
    for _ in range(n_tests):
      h, w = np.random.randint(100, 1000, 2)
      t, l = np.random.randint(0, 1000, 2)
      tlbr = [t, l, t + h, l + w]
      n_keypoints = np.random.randint(1, 100)
      keypoint_coords = np.random.rand(n_keypoints, 2)
      kc1, h1, w1 = convert_detections(tlbr, keypoint_coords, to_flip=True)
      kc2, h2, w2 = convert_detections(tlbr, keypoint_coords, inverse_keypoint_coords=True)
      if not np.all(kc1 == kc2):
        cnt_diff[0] += 1
      # endif equivalency check
      kc3, h3, w3 = convert_detections(tlbr, keypoint_coords)
      kc4, h4, w4 = convert_detections(tlbr, keypoint_coords, to_flip=True, inverse_keypoint_coords=True)
      if not np.all(kc3 == kc4):
        cnt_diff[1] += 1
      # endif reversibility check

      # keypoint_coords, height, width = convert_detections(tlbr, keypoint_coords)
      # assert np.all(keypoint_coords >= 0) and np.all(keypoint_coords <= [height, width])
      #
      # keypoint_coords, height, width = convert_detections(tlbr, keypoint_coords, to_flip=True)
      # assert np.all(keypoint_coords >= 0) and np.all(keypoint_coords <= [width, height])
      #
      # keypoint_coords, height, width = convert_detections(tlbr, keypoint_coords, inverse_keypoint_coords=True)
      # assert np.all(keypoint_coords >= 0) and np.all(keypoint_coords <= [height, width])
    # endfor tests
    print(f"Testing convert_detections with {n_tests} attempts... DONE")
    print(f"Results: {cnt_diff[0]} cases with differences between the to_flip and inverse_keypoint_coords effect.")
    print(f"Results: {cnt_diff[1]} cases where applying both to_flip and inverse_keypoint_coords changes the default case.")
    return

  test_convert_detections(n_tests=1000)

