def get_center_of_bbox(bbox):
    """
    Calculate the (x, y) centre of a bounding box.

    Parameters
    ----------
    bbox : tuple[int, int, int, int]
        (x1, y1, x2, y2) where
        * (x1, y1) is the top-left corner
        * (x2, y2) is the bottom-right corner

    Returns
    -------
    tuple[int, int]
        (x_center, y_center) rounded down to the nearest pixel.
    """

    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2), int((y1+y2)/2)

def get_bbox_width(bbox):
    """
    Compute the width of a bounding box.

    Parameters
    ----------
    bbox : tuple[int, int, int, int]
        (x1, y1, x2, y2)

    Returns
    -------
    int
        Width in pixels.

    """
    return bbox[2] - bbox[0]

def measure_euclidean_distance(p1,p2):
    """
    Return Euclidean distance between points p1 and p2.

    Parameters
    ----------
    p1, p2 : tuple[float, float] | list[float, float]
        Coordinates formatted as (x, y).

    Returns
    -------
    float
        The straight-line distance between the two points.
    """
    dx = p1[0] - p2[0]      # horizontal difference
    dy = p1[1] - p2[1]      # vertical difference
    return (dx*dx + dy*dy) ** 0.5

def measure_xy_distance(p1,p2):
    """
    Return the horizontal and vertical pixel offsets from p2 to p1.

    Parameters
    ----------
    p1, p2 : tuple[int, int] | list[int, int]
        Coordinates formatted as (x, y).

    Returns
    -------
    tuple[int, int]
        (dx, dy) where:
          dx = p1.x - p2.x   # positive -->p1 is to the right of p2
          dy = p1.y - p2.y   # positive --> p1 is below p2 (image origin is top-left)
    """
    return p1[0]-p2[0],p1[1]-p2[1]

def get_foot_position(bbox):
    """
    Estimate a player's foot position as the centre of the bbox's bottom edge.

    Parameters
    ----------
    bbox : list[int] | tuple[int, int, int, int]
        (x1, y1, x2, y2) bounding-box where
        * (x1, y1) is top-left
        * (x2, y2) is bottom-right

    Returns
    -------
    tuple[int, int]
        (x_mid, y_bottom) - an integer pixel coordinate representing the feet.
    """
        
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int(y2)