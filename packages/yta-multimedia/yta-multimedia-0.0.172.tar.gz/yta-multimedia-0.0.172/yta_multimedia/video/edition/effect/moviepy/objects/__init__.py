from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition, TFunctionResize, TFunctionRotate
from yta_general_utils.math.rate_functions import RateFunction
# TODO: Maybe unify all these to a MoviepyArgument (?) as
# they are very similar: 'start', 'end', 'rate_func'
# TODO: Maybe rename to MoviepyResize

class MoviepyResize:
    def __init__(self, initial_size: float, final_size: float, t_function: type = TFunctionResize.resize_from_to, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check that all params are provided and valid
        self.initial_size = initial_size
        self.final_size = final_size
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

class MoviepySetPosition:
    def __init__(self, initial_position: tuple, final_position: float, t_function: type = TFunctionSetPosition.linear, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check that all params are provided and valid
        self.initial_position = initial_position
        self.final_position = final_position
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

class MoviepyRotate:
    # TODO: Check that all params are provided and valid
    def __init__(self, initial_rotation: int, final_rotation: int, t_function: type = TFunctionRotate.rotate_from_to, rate_func: type = RateFunction.linear, *args, **kwargs):
        self.initial_rotation = initial_rotation
        self.final_rotation = final_rotation
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'