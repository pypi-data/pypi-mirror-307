from yta_multimedia.video.generation.manim.constants import HALF_SCENE_HEIGHT, HALF_SCENE_WIDTH
from yta_multimedia.video.generation.manim.utils.dimensions import ManimDimensions
from yta_general_utils.random import randrangefloat
from yta_general_utils.programming.enum import YTAEnum as Enum
from random import choice as randchoice


def get_center(video, background_video):
    """
    Returns the x,y coords in which the provided 'video' will
    be centered according to the provided 'background_video' in
    which it will be overlayed.

    This method returns two elements, first one is the x and the
    second one is the y.
    """
    # TODO: Ensure 'video' and 'background_video' are valid videos
    return background_video.w / 2 - video.w / 2, background_video.h / 2 - video.h / 2

class Position(Enum):
    """
    Enum class that represents a position inside the screen
    scene. This is used to position a video or an image inside
    the scene in an specific position defined by itself. It is
    useful with Manim and Moviepy video positioning and has
    been prepared to work with those engines.
    """
    OUT_TOP_LEFT = 'out_top_left'
    """
    Out of the screen, on the top left corner, just one pixel
    out of bounds.
    """
    IN_EDGE_TOP_LEFT = 'in_edge_top_left'
    """
    The center of the video is on the top left corner, so only
    the bottom right quarter part of the video is shown (inside
    the screen).
    """
    TOP_LEFT = 'top_left'
    """
    The video is completely visible, just at the top left 
    corner of the screen.
    """
    OUT_TOP = 'out_top'
    IN_EDGE_TOP = 'in_edge_top'
    TOP = 'top'
    OUT_TOP_RIGHT = 'out_top_right'
    IN_EDGE_TOP_RIGHT = 'in_edge_top_right'
    TOP_RIGHT = 'top_right'
    CENTER = 'center'
    OUT_RIGHT = 'out_right'
    IN_EDGE_RIGHT = 'in_edge_right'
    RIGHT = 'right'
    OUT_BOTTOM_RIGHT = 'out_bottom_right'
    IN_EDGE_BOTTOM_RIGHT = 'in_edge_bottom_right'
    BOTTOM_RIGHT = 'bottom_right'
    OUT_BOTTOM = 'out_bottom'
    IN_EDGE_BOTTOM = 'in_edge_bottom'
    BOTTOM = 'bottom'
    OUT_BOTTOM_LEFT = 'out_bottom_left'
    IN_EDGE_BOTTOM_LEFT = 'in_edge_bottom_left'
    BOTTOM_LEFT = 'bottom_left'
    OUT_LEFT = 'out_left'
    IN_EDGE_LEFT = 'in_edge_left'
    LEFT = 'left'

    HALF_TOP = 'half_top'
    HALF_TOP_RIGHT = 'half_top_right'
    HALF_RIGHT = 'half_right'
    HALF_BOTTOM_RIGHT = 'half_bottom_right'
    HALF_BOTTOM = 'half_bottom'
    HALF_BOTTOM_LEFT = 'half_bottom_left'
    HALF_LEFT = 'half_left'
    HALF_TOP_LEFT = 'half_top_left'

    QUADRANT_1_TOP_RIGHT_CORNER = 'quadrant_1_top_right_corner'
    QUADRANT_1_BOTTOM_RIGHT_CORNER = 'quadrant_1_bottom_right_corner'
    QUADRANT_1_BOTTOM_LEFT_CORNER = 'quadrant_1_bottom_left_corner'
    QUADRANT_2_TOP_LEFT_CORNER = 'quadrant_2_top_left_corner'
    QUADRANT_2_BOTTOM_RIGHT_CORNER = 'quadrant_2_bottom_right_corner'
    QUADRANT_2_BOTTOM_LEFT_CORNER = 'quadrant_2_bottom_left_corner'
    QUADRANT_3_TOP_RIGHT_CORNER = 'quadrant_3_top_right_corner'
    QUADRANT_3_TOP_LEFT_CORNER = 'quadrant_3_top_left_corner'
    QUADRANT_3_BOTTOM_LEFT_CORNER = 'quadrant_3_bottom_left_corner'
    QUADRANT_4_TOP_RIGHT_CORNER = 'quadrant_4_top_right_corner'
    QUADRANT_4_TOP_LEFT_CORNER = 'quadrant_4_top_left_corner'
    QUADRANT_4_BOTTOM_RIGHT_CORNER = 'quadrant_4_bottom_right_corner'

    RANDOM_INSIDE = 'random_inside'
    """
    A random position inside the screen with no pixels out of bounds.
    It is randomly chosen from one of all the options inside the limits
    we have.
    """
    RANDOM_OUTSIDE = 'random_outside'
    """
    A random position out of the screen limits. It is randomly chosen 
    from one of all the options outside the limits we have.
    """
    # TODO: Add more positions maybe (?)

    @classmethod
    def outside_positions_as_list(cls):
        """
        Returns the Position enums that are located out of
        the screen limits.
        """
        return [
            cls.OUT_TOP_LEFT,
            cls.OUT_TOP,
            cls.OUT_RIGHT,
            cls.OUT_BOTTOM_RIGHT,
            cls.OUT_BOTTOM,
            cls.OUT_BOTTOM_LEFT,
            cls.OUT_LEFT
        ]
    
    @classmethod
    def inside_positions_as_list(cls):
        """
        Returns the Position enums that are located inside
        the screen limits.
        """
        return list(set(cls.get_all()) - set(cls.outside_positions_as_list()) - set([cls.RANDOM_INSIDE]) - set([cls.RANDOM_OUTSIDE]))
    
    def get_manim_limits(self):
        """
        Return the left, right, top and bottom limits for this
        screen position. This edges represent the limits of the
        region in which the video should be placed to fit this
        screen position.

        We consider each screen region as a limited region of
        half of the scene width and height.

        Corner limits:
        [-7-1/9,  4, 0]   [0,  4, 0]   [7+1/9,  4, 0]
        [-7-1/9,  0, 0]   [0,  0, 0]   [7+1/9,  0, 0]
        [-7-1/9, -4, 0]   [0, -4, 0]   [7+1/9, -4, 0]
        """
        # TODO: I think I should consider regions of 1/8 of width and height
        # so 1 quadrant is divided into 4 pieces and I build all the positions
        # for also those quadrants
        # TODO: I'm missing the QUADRANT_1_HALF_TOP and HALF_TOP_OUT, ...
        if self == Position.TOP:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT, 0
        elif self == Position.BOTTOM:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT, 0
        elif self == Position.LEFT:
            return -HALF_SCENE_WIDTH, 0, HALF_SCENE_HEIGHT / 2, -HALF_SCENE_HEIGHT / 2
        elif self == Position.RIGHT:
            return 0, HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT / 2, -HALF_SCENE_HEIGHT / 2
        # TODO: Add missing

        # TODO: Is this method necessary (?)

    def get_manim_position(self, width: float, height: float):
        """
        Return the position in which the mobject must be placed to
        be exactly in this position.

        This method returns a x,y,z position.
        """
        # TODO: 'width' and 'height' must be manim

        if self == Position.TOP:
            return 0, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.TOP_RIGHT:
            return HALF_SCENE_WIDTH - width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.RIGHT:
            return HALF_SCENE_WIDTH - width / 2, 0, 0
        elif self == Position.BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH - width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.BOTTOM:
            return 0, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH + width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.LEFT:
            return -HALF_SCENE_WIDTH + width / 2, 0, 0
        elif self == Position.TOP_LEFT:
            return -HALF_SCENE_WIDTH + width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.CENTER:
            return 0, 0, 0
        elif self == Position.IN_EDGE_TOP_LEFT:
            return -HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_TOP_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.IN_EDGE_TOP:
            return 0, HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_TOP:
            return 0, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.IN_EDGE_TOP_RIGHT:
            return HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_TOP_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.IN_EDGE_RIGHT:
            return HALF_SCENE_WIDTH, 0, 0
        elif self == Position.OUT_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, 0, 0
        elif self == Position.IN_EDGE_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.IN_EDGE_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.IN_EDGE_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.IN_EDGE_LEFT:
            return -HALF_SCENE_WIDTH, 0, 0
        elif self == Position.OUT_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, 0, 0
        elif self == Position.HALF_TOP:
            return 0, HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_TOP_RIGHT:
            return HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_RIGHT:
            return HALF_SCENE_WIDTH / 2, 0, 0
        elif self == Position.HALF_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_LEFT:
            return -HALF_SCENE_WIDTH / 2, 0, 0
        elif self == Position.HALF_TOP_LEFT:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.QUADRANT_1_TOP_RIGHT_CORNER:
            return -width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            return -width / 2, height / 2, 0
        elif self == Position.QUADRANT_1_BOTTOM_LEFT_CORNER:
            return -HALF_SCENE_WIDTH + width / 2, height / 2, 0
        elif self == Position.QUADRANT_2_TOP_LEFT_CORNER:
            return width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            return HALF_SCENE_WIDTH - width / 2, height / 2, 0
        elif self == Position.QUADRANT_2_BOTTOM_LEFT_CORNER:
            return width / 2, height / 2, 0
        elif self == Position.QUADRANT_3_TOP_LEFT_CORNER:
            return width / 2, -height / 2, 0
        elif self == Position.QUADRANT_3_TOP_RIGHT_CORNER:
            return HALF_SCENE_WIDTH - width / 2, -height / 2, 0
        elif self == Position.QUADRANT_3_BOTTOM_LEFT_CORNER:
            return width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.QUADRANT_4_TOP_LEFT_CORNER:
            return -HALF_SCENE_WIDTH + width / 2, -height / 2, 0
        elif self == Position.QUADRANT_4_TOP_RIGHT_CORNER:
            return -width / 2, -height / 2, 0
        elif self == Position.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            return -width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.RANDOM_INSIDE:
            return randchoice(Position.inside_positions_as_list()).get_manim_position(width, height)
        elif self == Position.RANDOM_OUTSIDE:
            return randchoice(Position.outside_positions_as_list()).get_manim_position(width, height)
        
    def get_manim_random_position(self, width: float, height: float):
        """
        Calculate the position in which the center of the element 
        with the provided 'width' and 'height' must be placed to
        obtain this position.

        The position will be provided as a 3D vector but the z
        axis will be always 0.

        The provided 'width' and 'height' must be in pixels.
        """
        # TODO: Check if the provided 'width' and 'height' are in
        # in pixels and valid or if not

        # TODO: By now I'm just using the limits as numeric limits
        # for random position that will be used as the center of the
        # video, but we will need to consider the video dimensions 
        # in a near future to actually position it well, because the
        # video can be out of the scene right now with this approach
        left, right, top, bottom = self.get_manim_limits()

        x, y = randrangefloat(left, right, ManimDimensions.width_to_manim_width(1)), randrangefloat(top, bottom, ManimDimensions.height_to_manim_height(1))

        # If video is larger than HALF/2 it won't fit correctly.
        if width > HALF_SCENE_WIDTH or height > HALF_SCENE_HEIGHT:
            # TODO: Video is bigger than the region, we cannot make
            # it fit so... what can we do (?)
            return x, y

        if x - width / 2 < left:
            x += left - (x - width / 2)
        if x + width / 2 > right:
            x -= (x + width / 2) - right
        if y - height / 2 < bottom:
            y += bottom - (y - height / 2)
        if y + height / 2 > top:
            y -= (y + height / 2) - top

        return x, y, 0
        # TODO: Is this method necessary (?) I think yes, because
        # it generates a random position in a region, not a random
        # choice of our predefined (and always the same) positions

    def get_moviepy_position(self, video, background_video):
        """
        This method will calculate the (x, y) tuple position for the provided
        'video' over the also provided 'background_video' that would be,
        hypothetically, a 1920x1080 black color background static image. The
        provided 'position' will be transformed into the (x, y) tuple according
        to our own definitions.
        """
        # TODO: Do 'video' and 'background_video' checkings
        position_tuple = None

        if self == Position.CENTER:
            position_tuple = (get_center(video, background_video))

        #           Edges below
        # TOP
        elif self == Position.OUT_TOP:
            position_tuple = ((background_video.w / 2) - (video.w / 2), -video.h)
        elif self == Position.IN_EDGE_TOP:
            position_tuple = ((background_video.w / 2) - (video.w / 2), -(video.h / 2))
        elif self == Position.TOP:
            position_tuple = ((background_video.w / 2) - (video.w / 2), 0)
        # TOP RIGHT
        elif self == Position.OUT_TOP_RIGHT:
            position_tuple = (background_video.w, -video.h)
        elif self == Position.IN_EDGE_TOP_RIGHT:
            position_tuple = (background_video.w - (video.w / 2), -(video.h / 2))
        elif self == Position.TOP_RIGHT:
            position_tuple = (background_video.w - video.w, 0)
        # RIGHT
        elif self == Position.OUT_RIGHT:
            position_tuple = (background_video.w, (background_video.h / 2) - (video.h / 2))
        elif self == Position.IN_EDGE_RIGHT:
            position_tuple = (background_video.w - (video.w / 2), (background_video.h / 2) - (video.h / 2))
        elif self == Position.RIGHT:
            position_tuple = (background_video.w - video.w, (background_video.h / 2) - (video.h / 2))
        # BOTTOM RIGHT
        elif self == Position.OUT_BOTTOM_RIGHT:
            position_tuple = (background_video.w, background_video.h)
        elif self == Position.IN_EDGE_BOTTOM_RIGHT:
            position_tuple = (background_video.w - (video.w / 2), background_video.h - (video.h / 2))
        elif self == Position.BOTTOM_RIGHT:
            position_tuple = (background_video.w - video.w, background_video.h - video.h)
        # BOTTOM
        elif self == Position.OUT_BOTTOM:
            position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h)
        elif self == Position.IN_EDGE_BOTTOM:
            position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h - (video.h / 2))
        elif self == Position.BOTTOM:
            position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h - video.h)
        # BOTTOM LEFT
        elif self == Position.OUT_BOTTOM_LEFT:
            position_tuple = (-video.w, background_video.h)
        elif self == Position.IN_EDGE_BOTTOM_LEFT:
            position_tuple = (-(video.w / 2), background_video.h - (video.h / 2))
        elif self == Position.BOTTOM_LEFT:
            position_tuple = (0, background_video.h - video.h)
        # LEFT
        elif self == Position.OUT_LEFT:
            position_tuple = (-video.w, (background_video.h / 2) - (video.h / 2))
        elif self == Position.IN_EDGE_LEFT:
            position_tuple = (-(video.w / 2), (background_video.h / 2) - (video.h / 2))
        elif self == Position.LEFT:
            position_tuple = (0, (background_video.h / 2) - (video.h / 2))
        # TOP LEFT
        elif self == Position.OUT_TOP_LEFT:
            position_tuple = (-video.w, -video.h)
        elif self == Position.IN_EDGE_TOP_LEFT:
            position_tuple = (-(video.w / 2), -(video.h / 2))
        elif self == Position.TOP_LEFT:
            position_tuple = (0, 0)

        # HALF POSITIONS
        elif self == Position.HALF_TOP:
            position_tuple = (background_video.w / 2 - video.w / 2, background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_RIGHT:
            position_tuple = (3 * background_video.w / 4 - video.w / 2, background_video.h / 2 - video.h / 2)
        elif self == Position.HALF_BOTTOM:
            position_tuple = (background_video.w / 2 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_LEFT:
            position_tuple = (background_video.w / 4 - video.w / 2, background_video.h / 2 - video.h / 2)
        elif self == Position.HALF_TOP_RIGHT:
            position_tuple = (3 * background_video.w / 4 - video.w / 2, background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_BOTTOM_RIGHT:
            position_tuple = (3 * background_video.w / 4 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_BOTTOM_LEFT:
            position_tuple = (background_video.w / 4 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_TOP_LEFT:
            position_tuple = (background_video.w / 4 - video.w / 2, background_video.h / 4 - video.h / 2)

        # QUADRANT CORNERS
        elif self == Position.QUADRANT_1_TOP_RIGHT_CORNER:
            position_tuple = (background_video.w / 2 - video.w, 0)
        elif self == Position.QUADRANT_1_BOTTOM_LEFT_CORNER:
            position_tuple = (0, background_video.h / 2 - video.h)
        elif self == Position.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            position_tuple = (background_video.w / 2 - video.w, background_video.h / 2 - video.h)
        elif self == Position.QUADRANT_2_BOTTOM_LEFT_CORNER:
            position_tuple = (background_video.w / 2, background_video.h / 2 - video.h)
        elif self == Position.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            position_tuple = (background_video.w - video.w, background_video.h / 2 - video.h)
        elif self == Position.QUADRANT_2_TOP_LEFT_CORNER:
            position_tuple = (background_video.w / 2, 0)
        elif self == Position.QUADRANT_3_BOTTOM_LEFT_CORNER:
            position_tuple = (background_video.w / 2, background_video.h - video.h)
        elif self == Position.QUADRANT_3_TOP_LEFT_CORNER:
            position_tuple = (background_video.w / 2, background_video.h / 2)
        elif self == Position.QUADRANT_3_TOP_RIGHT_CORNER:
            position_tuple = (background_video.w - video.w, background_video.h / 2)
        elif self == Position.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            position_tuple = (background_video.w / 2 - video.w, background_video.h - video.h)
        elif self == Position.QUADRANT_4_TOP_LEFT_CORNER:
            position_tuple = (0, background_video.h / 2)
        elif self == Position.QUADRANT_4_TOP_RIGHT_CORNER:
            position_tuple = (background_video.w / 2 - video.w, background_video.h / 2)

        # RANDOMs
        elif self == Position.RANDOM_INSIDE:
            return randchoice(Position.inside_positions_as_list()).get_moviepy_position(video, background_video)
        elif self == Position.RANDOM_OUTSIDE:
            return randchoice(Position.outside_positions_as_list()).get_moviepy_position(video, background_video)

        return position_tuple