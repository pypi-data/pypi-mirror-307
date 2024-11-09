"""
This is an adaption of the rate functions found in manim
library for the moviepy library. I have to use lambda t
functions with the current frame time to be able to resize
or reposition a video, so I have adapted the manim rate
functions to be able to return a factor that, with specific
moviepy functions, will make a change with the factor that
has been calculated with the corresponding rate function.

You can see 'manim/utils/rate_functions.py'.

This is the way I have found to make it work and to be able
to build smoother animations. As manim docummentation says,
the rate functions have been inspired by the ones listed in
this web page: https://easings.net/
"""
from yta_general_utils.math.rate_functions import RateFunction

# TODO: This method could be private
def rate_function(t: float, duration: float, rate_func: type, *args, **kwargs):
    """
    You need to provide one of the functions of RateFunction class
    as the 'rate_func' parameter to be able to make it work, and 
    pass the needed args to it.
    """
    return rate_func(t / duration, *args, **kwargs)

class TFunction:
    """
    Class to simplify and encapsulate the functionality related
    with the t functions used in moviepy '.set_position' and
    '.resize' functions.
    """
    @staticmethod
    def zoom_from_to(t: float, duration: float, zoom_start: float, zoom_end: float, rate_func: type = RateFunction.linear, *args, **kwargs):
        """
        A function to be applied in moviepy '.resize()' as 'lambda t:
        zoom_from_to()'.

        A zoom value of 1 means no zoom, while a value greater than 1
        is a zoom_in effect, and a value lower than 1 is a zoom_out
        effect. The zoom must be always greater than 0.

        The 'rate_func' must be one of the existing functions in the
        yta_general_utils.math.rate_functions.RateFunction class.
        """
        # TODO: Check 'zoom_start', 'zoom_end' and 'rate_func'
        # are valid
        return zoom_start + (zoom_end - zoom_start) * rate_function(t, duration, rate_func, *args, **kwargs)
    
    @staticmethod
    def move_from_to(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear, *args, **kwargs):
        """
        A function to be applied in moviepy '.set_position()' as 'lambda
        t: move_from_to()'.

        The 'initial_position' and the 'final_position' must be, each
        one, a tuple containing a x,y position.

        The 'rate_func' must be one of the existing functions in the
        yta_general_utils.math.rate_functions.RateFunction class.
        """
        # TODO: Check 'initial_position', 'final_position' and 
        # 'rate_func' are valid
        
        # By now I'm assuming that x and y axis use the same
        # rate function to move, but it could be different so we
        # could need to enable two 'rate_func' and arguments
        # I need to calculate the movement in each axis
        return (initial_position[0] + (final_position[0] - initial_position[0]) * rate_function(t, duration, rate_func, *args, *kwargs), initial_position[1] + (final_position[1] - initial_position[1]) * rate_function(t, duration, rate_func, *args, *kwargs))

    @staticmethod
    def rotate_from_to(t: float, duration: float, initial_rotation: int, final_rotation: int, rate_func: type = RateFunction.linear, *args, **kwargs):
        """
        A function to be applied in moviepy '.rotate()' as 'lambda
        t: rotate_from_to()'.

        The 'initial_rotation' and the 'final_rotation' must be, each
        one, the expected rotation, expressed in degrees.

        The 'rate_func' must be one of the existing functions in the
        yta_general_utils.math.rate_functions.RateFunction class.
        """
        # TODO: Check 'initial_rotation', 'final_rotation' and 
        # 'rate_func' are valid
        return initial_rotation + (final_rotation - initial_rotation) * rate_function(t, duration, rate_func, *args, *kwargs)

# TODO: I can create my own curves by setting nodes with
# different values (as speed curves in a famous video
# editor) to make my own animations