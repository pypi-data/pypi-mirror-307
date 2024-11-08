"""
This is an adaption of the rate functions found in manim
library for the moviepy library. I have to use lambda t
functions with the current frame time to be able to resize
or reposition a video, so I have adapted the manim rate
functions to be able to return a factor that, with specific
moviepy functions, will make a change with the factor that
has been calculated with the corresponding rate function.

You can see 'manim\utils\rate_functions.py'.

This is the way I have found to make it work and to be able
to build smoother animations. As manim docummentation says,
the rate functions have been inspired by the ones listed in
this web page: https://easings.net/
"""
from yta_general_utils.math import Math
from math import pow, sqrt

import numpy as np
import typing


def _get_current_frame_factor(t: float, duration: float, fps: int):
    """
    Get the animation factor to the frame of the provided
    time 't'. This factor is used in the different rate
    functions to calculate the animation progress and value
    to apply.
    """
    # TODO: Check 't', 'duration' and 'fps' are valid
    return fps * t / (duration * fps - 1)

# Decorator
def t_to_frame_factor(func):
    """
    Transform the time 't' into the corresponding frame factor
    that must be applied in that moment of the animation.
    """
    def inner(t: float, duration: float, fps: int, *args, **kwargs):
        t = _get_current_frame_factor(t, duration, fps)

        return func(t, duration, fps, *args, **kwargs)
    return inner

@t_to_frame_factor
def linear(t: float, duration: float, fps: int):
    return t

@t_to_frame_factor
def slow_into(t: float, duration: float, fps: int):
    return np.sqrt(1 - (1 - t) * (1 - t))

@t_to_frame_factor
def smooth(t: float, duration: float, fps: int, inflection: float = 10.0) -> float:
    error = Math.sigmoid(-inflection / 2)

    return min(
        max((Math.sigmoid(inflection * (t - 0.5)) - error) / (1 - 2 * error), 0),
        1,
    )

@t_to_frame_factor
def smoothstep(t: float, duration: float, fps: int) -> float:
    """Implementation of the 1st order SmoothStep sigmoid function.
    The 1st derivative (speed) is zero at the endpoints.
    https://en.wikipedia.org/wiki/Smoothstep
    """
    return 0 if t <= 0 else 3 * t**2 - 2 * t**3 if t < 1 else 1

@t_to_frame_factor
def smootherstep(t: float, duration: float, fps: int) -> float:
    """Implementation of the 2nd order SmoothStep sigmoid function.
    The 1st and 2nd derivatives (speed and acceleration) are zero at the endpoints.
    https://en.wikipedia.org/wiki/Smoothstep
    """
    return 0 if t <= 0 else 6 * t**5 - 15 * t**4 + 10 * t**3 if t < 1 else 1

@t_to_frame_factor
def smoothererstep(t: float, duration: float, fps: int) -> float:
    """Implementation of the 3rd order SmoothStep sigmoid function.
    The 1st, 2nd and 3rd derivatives (speed, acceleration and jerk) are zero at the endpoints.
    https://en.wikipedia.org/wiki/Smoothstep
    """
    alpha = 0
    if 0 < t < 1:
        alpha = 35 * t**4 - 84 * t**5 + 70 * t**6 - 20 * t**7
    elif t >= 1:
        alpha = 1
    return alpha

def rush_into(t: float, duration: float, fps: int, inflection: float = 10.0) -> float:
    return 2 * smooth(t / 2.0, duration, fps, inflection)

def rush_from(t: float, duration: float, fps: int, inflection: float = 10.0) -> float:
    return 2 * smooth(t / 2.0 + 0.5, duration, fps, inflection) - 1

@t_to_frame_factor
def slow_into(t: float, duration: float, fps: int) -> float:
    return np.sqrt(1 - (1 - t) * (1 - t))

def double_smooth(t: float, duration: float, fps: int) -> float:
    if _get_current_frame_factor(t, duration, fps) < 0.5:
        return 0.5 * smooth(2 * t)
    else:
        return 0.5 * (1 + smooth(2 * t - 1))
    
def there_and_back(t: float, duration: float, fps: int, inflection: float = 10.0) -> float:
    if _get_current_frame_factor(t, duration, fps) < 0.5:
        t = 2 * t
    else:
        t = 2 * (1 - t)

    return smooth(t, inflection)

def there_and_back_with_pause(t: float, duration: float, fps: int, pause_ratio: float = 1.0 / 3) -> float:
    t_ = _get_current_frame_factor(t, duration, fps)
    a = 1.0 / pause_ratio
    if t_ < 0.5 - pause_ratio / 2:
        return smooth(a * t)
    elif t_ < 0.5 + pause_ratio / 2:
        return 1
    else:
        return smooth(a - a * t)
    
@t_to_frame_factor
def running_start(t: float, duration: float, fps: int, pull_factor: float = -0.5) -> typing.Iterable:  # what is func return type?
    # TODO: This is being taken from manim, maybe copy (?)
    from manim.utils.bezier import bezier

    return bezier([0, 0, pull_factor, pull_factor, 1, 1, 1])(t)

# Manim says 'not_quite_there' function is not working
def wiggle(t: float, duration: float, fps: int, wiggles: float = 2) -> float:
    return there_and_back(t) * np.sin(wiggles * np.pi * _get_current_frame_factor(t, duration, fps))

@t_to_frame_factor
def ease_in_cubic(t: float, duration: float, fps: int) -> float:
    return t * t * t

@t_to_frame_factor
def ease_out_cubic(t: float, duration: float, fps: int) -> float:
    return 1 - pow(1 - t, 3)

@t_to_frame_factor
def squish_rate_func(
    func: typing.Callable[[float], float],
    a: float = 0.4,
    b: float = 0.6,
) -> typing.Callable[[float], float]:
    def result(t: float, duration: float, fps: int):
        if a == b:
            return a

        if t < a:
            return func(0)
        elif t > b:
            return func(1)
        else:
            return func((t - a) / (b - a))

    return result

def lingering(t: float, duration: float, fps: int) -> float:
    # TODO: Careful, this is like a decorator so @t_to_frame_factor
    # could fail or work not as expected
    return squish_rate_func(lambda t: t, 0, 0.8)(t, duration, fps)

@t_to_frame_factor
def exponential_decay(t: float, duration: float, fps: int, half_life: float = 0.1) -> float:
    # The half-life should be rather small to minimize
    # the cut-off error at the end
    return 1 - np.exp(-t / half_life)

@t_to_frame_factor
def ease_in_sine(t: float, duration: float, fps: int) -> float:
    return 1 - np.cos((t * np.pi) / 2)

@t_to_frame_factor
def ease_out_sine(t: float, duration: float, fps: int) -> float:
    return np.sin((t * np.pi) / 2)

@t_to_frame_factor
def ease_in_out_sine(t: float, duration: float, fps: int) -> float:
    return -(np.cos(np.pi * t) - 1) / 2

@t_to_frame_factor
def ease_in_quad(t: float, duration: float, fps: int) -> float:
    return t * t

@t_to_frame_factor
def ease_out_quad(t: float, duration: float, fps: int) -> float:
    return 1 - (1 - t) * (1 - t)

@t_to_frame_factor
def ease_in_out_quad(t: float, duration: float, fps: int) -> float:
    return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2

@t_to_frame_factor
def ease_in_cubic(t: float, duration: float, fps: int) -> float:
    return t * t * t

@t_to_frame_factor
def ease_out_cubic(t: float, duration: float, fps: int) -> float:
    return 1 - pow(1 - t, 3)

@t_to_frame_factor
def ease_in_out_cubic(t: float, duration: float, fps: int) -> float:
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

@t_to_frame_factor
def ease_in_quart(t: float, duration: float, fps: int) -> float:
    return t * t * t * t

@t_to_frame_factor
def ease_out_quart(t: float, duration: float, fps: int) -> float:
    return 1 - pow(1 - t, 4)

@t_to_frame_factor
def ease_in_out_quart(t: float, duration: float, fps: int) -> float:
    return 8 * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 4) / 2

@t_to_frame_factor
def ease_in_quint(t: float, duration: float, fps: int) -> float:
    return t * t * t * t * t

@t_to_frame_factor
def ease_out_quint(t: float, duration: float, fps: int) -> float:
    return 1 - pow(1 - t, 5)

@t_to_frame_factor
def ease_in_out_quint(t: float, duration: float, fps: int) -> float:
    return 16 * t * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 5) / 2

@t_to_frame_factor
def ease_in_expo(t: float, duration: float, fps: int) -> float:
    return 0 if t == 0 else pow(2, 10 * t - 10)

@t_to_frame_factor
def ease_out_expo(t: float, duration: float, fps: int) -> float:
    return 1 if t == 1 else 1 - pow(2, -10 * t)

@t_to_frame_factor
def ease_in_out_expo(t: float, duration: float, fps: int) -> float:
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return pow(2, 20 * t - 10) / 2
    else:
        return (2 - pow(2, -20 * t + 10)) / 2

@t_to_frame_factor
def ease_in_circ(t: float, duration: float, fps: int) -> float:
    return 1 - sqrt(1 - pow(t, 2))

@t_to_frame_factor
def ease_out_circ(t: float, duration: float, fps: int) -> float:
    return sqrt(1 - pow(t - 1, 2))

@t_to_frame_factor
def ease_in_out_circ(t: float, duration: float, fps: int) -> float:
    return (
        (1 - sqrt(1 - pow(2 * t, 2))) / 2
        if t < 0.5
        else (sqrt(1 - pow(-2 * t + 2, 2)) + 1) / 2
    )

@t_to_frame_factor
def ease_in_back(t: float, duration: float, fps: int) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t

@t_to_frame_factor
def ease_out_back(t: float, duration: float, fps: int) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

@t_to_frame_factor
def ease_in_out_back(t: float, duration: float, fps: int) -> float:
    c1 = 1.70158
    c2 = c1 * 1.525
    return (
        (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
        if t < 0.5
        else (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2
    )

@t_to_frame_factor
def ease_in_elastic(t: float, duration: float, fps: int) -> float:
    c4 = (2 * np.pi) / 3
    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        return -pow(2, 10 * t - 10) * np.sin((t * 10 - 10.75) * c4)

@t_to_frame_factor
def ease_out_elastic(t: float, duration: float, fps: int) -> float:
    c4 = (2 * np.pi) / 3
    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        return pow(2, -10 * t) * np.sin((t * 10 - 0.75) * c4) + 1

@t_to_frame_factor
def ease_in_out_elastic(t: float, duration: float, fps: int) -> float:
    c5 = (2 * np.pi) / 4.5
    if t == 0:
        return 0
    elif t == 1:
        return 1
    elif t < 0.5:
        return -(pow(2, 20 * t - 10) * np.sin((20 * t - 11.125) * c5)) / 2
    else:
        return (pow(2, -20 * t + 10) * np.sin((20 * t - 11.125) * c5)) / 2 + 1

def ease_in_bounce(t: float, duration: float, fps: int) -> float:
    return 1 - ease_out_bounce(1 - t, duration, fps)

@t_to_frame_factor
def ease_out_bounce(t: float, duration: float, fps: int) -> float:
    n1 = 7.5625
    d1 = 2.75

    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        return n1 * (t - 1.5 / d1) * (t - 1.5 / d1) + 0.75
    elif t < 2.5 / d1:
        return n1 * (t - 2.25 / d1) * (t - 2.25 / d1) + 0.9375
    else:
        return n1 * (t - 2.625 / d1) * (t - 2.625 / d1) + 0.984375

@t_to_frame_factor
def ease_in_out_bounce(t: float, duration: float, fps: int) -> float:
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    else:
        return (1 + ease_out_bounce(2 * t - 1)) / 2

# TODO: I can create my own curves by setting nodes with
# different values (as speed curves in a famous video
# editor) to make my own animations