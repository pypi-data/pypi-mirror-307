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


def rate_function(t: float, duration: float, rate_func: type, *args, **kwargs):
    """
    You need to provide one of the functions of RateFunction class
    as the 'rate_func' parameter to be able to make it work, and 
    pass the needed args to it.
    """
    return rate_func(t / duration, *args, **kwargs)

# TODO: Move this above to its corresponding module
class TFunction:
    """
    Class to simplify and encapsulate the functionality related
    with the t functions used in moviepy '.set_position' and
    '.resize' functions.
    """
    @staticmethod
    def zoom_from_to(t: float, duration: float, zoom_start: float, zoom_end: float, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check 'zoom_start', 'zoom_end' and 'rate_func'
        # are valid
        return zoom_start + (zoom_end - zoom_start) * rate_function(t, duration, rate_func, *args, **kwargs)
    
    @staticmethod
    def move_from_to(t: float, duration: float, initial_position: tuple, final_position: tuple, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check 'initial_position', 'final_position' and 
        # 'rate_func' are valid
        
        # By now I'm assuming that x and y axis use the same
        # rate function to move, but it could be different so we
        # could need to enable two 'rate_func' and arguments
        # I need to calculate the movement in each axis
        return (initial_position[0] + (final_position[0] - initial_position[0]) * rate_function(t, duration, rate_func, *args, *kwargs), initial_position[1] + (final_position[1] - initial_position[1]) * rate_function(t, duration, rate_func, *args, *kwargs))
# TODO: Move this above to its corresponding module





# TODO: I can create my own curves by setting nodes with
# different values (as speed curves in a famous video
# editor) to make my own animations

# TODO: I think I've doing this bad due to a misconcept
# with the n-1 frames
# def _get_current_frame_factor(t: float, duration: float, fps: int):
#     """
#     Get the animation factor to the frame of the provided
#     time 't'. This factor is used in the different rate
#     functions to calculate the animation progress and value
#     to apply.
#     """
#     # TODO: Check 't', 'duration' and 'fps' are valid
#     return fps * t / (duration * fps - 1)

# # Decorator
# def t_to_frame_factor(func):
#     """
#     Transform the time 't' into the corresponding frame factor
#     that must be applied in that moment of the animation.
#     """
#     def inner(t: float, duration: float, fps: int, *args, **kwargs):
#         t = _get_current_frame_factor(t, duration, fps)

#         return func(t, duration, *args, **kwargs)
#     return inner

# TODO: Remove all below as we will use the 'rate_function'
# @t_to_frame_factor
# def linear(t: float, duration: float, fps: int):
#     return RateFunction.linear(t)

# @t_to_frame_factor
# def slow_into(t: float, duration: float, fps: int):
#     return RateFunction.slow_into(t)

# @t_to_frame_factor
# def smooth(t: float, duration: float, fps: int, inflection: float = 10.0) -> float:
#     return RateFunction.smooth(t, inflection)

# @t_to_frame_factor
# def smoothstep(t: float, duration: float, fps: int) -> float:
#     """Implementation of the 1st order SmoothStep sigmoid function.
#     The 1st derivative (speed) is zero at the endpoints.
#     https://en.wikipedia.org/wiki/Smoothstep
#     """
#     return RateFunction.smoothstep(t)

# @t_to_frame_factor
# def smootherstep(t: float, duration: float, fps: int) -> float:
#     """Implementation of the 2nd order SmoothStep sigmoid function.
#     The 1st and 2nd derivatives (speed and acceleration) are zero at the endpoints.
#     https://en.wikipedia.org/wiki/Smoothstep
#     """
#     return RateFunction.smootherstep(t)

# @t_to_frame_factor
# def smoothererstep(t: float, duration: float, fps: int) -> float:
#     """Implementation of the 3rd order SmoothStep sigmoid function.
#     The 1st, 2nd and 3rd derivatives (speed, acceleration and jerk) are zero at the endpoints.
#     https://en.wikipedia.org/wiki/Smoothstep
#     """
#     return RateFunction.smoothererstep(t)

# @t_to_frame_factor
# def rush_into(t: float, duration: float, fps: int, inflection: float = 10.0) -> float:
#     return RateFunction.rush_into(t, inflection)

# @t_to_frame_factor
# def rush_from(t: float, duration: float, fps: int, inflection: float = 10.0) -> float:
#     return RateFunction.rush_from(t, inflection)

# @t_to_frame_factor
# def double_smooth(t: float, duration: float, fps: int) -> float:
#     return RateFunction.double_smooth(t)
    
# @t_to_frame_factor
# def there_and_back(t: float, duration: float, fps: int, inflection: float = 10.0) -> float:
#     return RateFunction.there_and_back(t, inflection)

# @t_to_frame_factor
# def there_and_back_with_pause(t: float, duration: float, fps: int, pause_ratio: float = 1.0 / 3) -> float:
#     return RateFunction.there_and_back_with_pause(t, pause_ratio)
    
# @t_to_frame_factor
# def running_start(t: float, duration: float, fps: int, pull_factor: float = -0.5) -> typing.Iterable:  # what is func return type?
#     return RateFunction.running_start(t, pull_factor)

# @t_to_frame_factor
# def wiggle(t: float, duration: float, fps: int, wiggles: float = 2) -> float:
#     # Manim says 'not_quite_there' function is not working
#     return RateFunction.wiggle(t, wiggles)

# @t_to_frame_factor
# def ease_in_cubic(t: float, duration: float, fps: int) -> float:
#     return RateFunction.ease_in_cubic(t)

# @t_to_frame_factor
# def ease_out_cubic(t: float, duration: float, fps: int) -> float:
#     return RateFunction.ease_out_cubic(t)

# @t_to_frame_factor
# def lingering(t: float, duration: float, fps: int) -> float:
#     return RateFunction.lingering(t)

# @t_to_frame_factor
# def exponential_decay(t: float, duration: float, fps: int, half_life: float = 0.1) -> float:
#     # The half-life should be rather small to minimize
#     # the cut-off error at the end
#     return RateFunction.exponential_decay(t, half_life)

# @t_to_frame_factor
# def ease_in_sine(t: float, duration: float, fps: int) -> float:
#     return RateFunction.ease_in_sine(t)

# @t_to_frame_factor
# def ease_out_sine(t: float, duration: float, fps: int) -> float:
#     return RateFunction.ease_out_sine(t)

# @t_to_frame_factor
# def ease_in_out_sine(t: float, duration: float, fps: int) -> float:
#     return RateFunction.ease_in_out_sine(t)

# @t_to_frame_factor
# def ease_in_quad(t: float, duration: float, fps: int) -> float:
#     return t * t

# @t_to_frame_factor
# def ease_out_quad(t: float, duration: float, fps: int) -> float:
#     return 1 - (1 - t) * (1 - t)

# @t_to_frame_factor
# def ease_in_out_quad(t: float, duration: float, fps: int) -> float:
#     return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2

# @t_to_frame_factor
# def ease_in_cubic(t: float, duration: float, fps: int) -> float:
#     return t * t * t

# @t_to_frame_factor
# def ease_out_cubic(t: float, duration: float, fps: int) -> float:
#     return 1 - pow(1 - t, 3)

# @t_to_frame_factor
# def ease_in_out_cubic(t: float, duration: float, fps: int) -> float:
#     return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

# @t_to_frame_factor
# def ease_in_quart(t: float, duration: float, fps: int) -> float:
#     return t * t * t * t

# @t_to_frame_factor
# def ease_out_quart(t: float, duration: float, fps: int) -> float:
#     return 1 - pow(1 - t, 4)

# @t_to_frame_factor
# def ease_in_out_quart(t: float, duration: float, fps: int) -> float:
#     return 8 * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 4) / 2

# @t_to_frame_factor
# def ease_in_quint(t: float, duration: float, fps: int) -> float:
#     return t * t * t * t * t

# @t_to_frame_factor
# def ease_out_quint(t: float, duration: float, fps: int) -> float:
#     return 1 - pow(1 - t, 5)

# @t_to_frame_factor
# def ease_in_out_quint(t: float, duration: float, fps: int) -> float:
#     return 16 * t * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 5) / 2

# @t_to_frame_factor
# def ease_in_expo(t: float, duration: float, fps: int) -> float:
#     return 0 if t == 0 else pow(2, 10 * t - 10)

# @t_to_frame_factor
# def ease_out_expo(t: float, duration: float, fps: int) -> float:
#     return 1 if t == 1 else 1 - pow(2, -10 * t)

# @t_to_frame_factor
# def ease_in_out_expo(t: float, duration: float, fps: int) -> float:
#     if t == 0:
#         return 0
#     elif t == 1:
#         return 1
#     elif t < 0.5:
#         return pow(2, 20 * t - 10) / 2
#     else:
#         return (2 - pow(2, -20 * t + 10)) / 2

# @t_to_frame_factor
# def ease_in_circ(t: float, duration: float, fps: int) -> float:
#     return 1 - sqrt(1 - pow(t, 2))

# @t_to_frame_factor
# def ease_out_circ(t: float, duration: float, fps: int) -> float:
#     return sqrt(1 - pow(t - 1, 2))

# @t_to_frame_factor
# def ease_in_out_circ(t: float, duration: float, fps: int) -> float:
#     return (
#         (1 - sqrt(1 - pow(2 * t, 2))) / 2
#         if t < 0.5
#         else (sqrt(1 - pow(-2 * t + 2, 2)) + 1) / 2
#     )

# @t_to_frame_factor
# def ease_in_back(t: float, duration: float, fps: int) -> float:
#     c1 = 1.70158
#     c3 = c1 + 1
#     return c3 * t * t * t - c1 * t * t

# @t_to_frame_factor
# def ease_out_back(t: float, duration: float, fps: int) -> float:
#     c1 = 1.70158
#     c3 = c1 + 1
#     return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

# @t_to_frame_factor
# def ease_in_out_back(t: float, duration: float, fps: int) -> float:
#     c1 = 1.70158
#     c2 = c1 * 1.525
#     return (
#         (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
#         if t < 0.5
#         else (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2
#     )

# @t_to_frame_factor
# def ease_in_elastic(t: float, duration: float, fps: int) -> float:
#     c4 = (2 * np.pi) / 3
#     if t == 0:
#         return 0
#     elif t == 1:
#         return 1
#     else:
#         return -pow(2, 10 * t - 10) * np.sin((t * 10 - 10.75) * c4)

# @t_to_frame_factor
# def ease_out_elastic(t: float, duration: float, fps: int) -> float:
#     c4 = (2 * np.pi) / 3
#     if t == 0:
#         return 0
#     elif t == 1:
#         return 1
#     else:
#         return pow(2, -10 * t) * np.sin((t * 10 - 0.75) * c4) + 1

# @t_to_frame_factor
# def ease_in_out_elastic(t: float, duration: float, fps: int) -> float:
#     c5 = (2 * np.pi) / 4.5
#     if t == 0:
#         return 0
#     elif t == 1:
#         return 1
#     elif t < 0.5:
#         return -(pow(2, 20 * t - 10) * np.sin((20 * t - 11.125) * c5)) / 2
#     else:
#         return (pow(2, -20 * t + 10) * np.sin((20 * t - 11.125) * c5)) / 2 + 1

# def ease_in_bounce(t: float, duration: float, fps: int) -> float:
#     return 1 - ease_out_bounce(1 - t, duration, fps)

# @t_to_frame_factor
# def ease_out_bounce(t: float, duration: float, fps: int) -> float:
#     n1 = 7.5625
#     d1 = 2.75

#     if t < 1 / d1:
#         return n1 * t * t
#     elif t < 2 / d1:
#         return n1 * (t - 1.5 / d1) * (t - 1.5 / d1) + 0.75
#     elif t < 2.5 / d1:
#         return n1 * (t - 2.25 / d1) * (t - 2.25 / d1) + 0.9375
#     else:
#         return n1 * (t - 2.625 / d1) * (t - 2.625 / d1) + 0.984375

# @t_to_frame_factor
# def ease_in_out_bounce(t: float, duration: float, fps: int) -> float:
#     if t < 0.5:
#         return (1 - ease_out_bounce(1 - 2 * t)) / 2
#     else:
#         return (1 + ease_out_bounce(2 * t - 1)) / 2

