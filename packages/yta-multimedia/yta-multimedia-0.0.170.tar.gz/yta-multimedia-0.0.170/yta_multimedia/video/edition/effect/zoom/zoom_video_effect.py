from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.edition.effect.moviepy.t_functions import TFunction
from yta_general_utils.math.rate_functions import RateFunction
from moviepy.editor import CompositeVideoClip, VideoFileClip, ImageClip, VideoClip, ColorClip
from typing import Union


class ZoomVideoEffect(VideoEffect):
    """
    Creates a Zoom effect in the provided video.
    """
    @classmethod
    def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], zoom_start: float, zoom_end: float, rate_func: type = RateFunction.linear):
        """
        Apply the effect on the provided 'video'.

        :param float zoom_start: The zoom at the start of the video, where a 1 is no zoom, a 0.8 is a zoom out of 20% and 1.1 is a zoom in of a 10%.

        :param float zoom_end: The zoom at the end of the video, where a 1 is no zoom, a 0.8 is a zoom out of 20% and 1.1 is a zoom in of a 10%.

        :param type rate_func: The rate function to apply in the animation effect. Must be one of the methods available in the RateFunction class.
        """
        video = VideoEffect.parse_moviepy_video(video)
        # We reset the mask to avoid problems with zoom
        video = video.add_mask()

        if not zoom_start or not zoom_end:
            raise Exception('No "zoom_start" or "zoom_end" provided.')
        
        # TODO: Check that the provided 'rate_func' is valid

        fps = video.fps
        duration = video.duration
        screensize = video.size

        effected_video = (
            video
            .resize(screensize)
            .resize(lambda t: TFunction.zoom_from_to(t, duration, zoom_start, zoom_end, rate_func))
            # TODO: What about position (?)
            .set_position(('center', 'center'))
            .set_duration(duration)
            .set_fps(fps)
        )

        return CompositeVideoClip([effected_video], size = screensize)


# TODO: Maybe unify all these to a MoviepyArgument (?) as
# they are very similar: 'start', 'end', 'rate_func'
# TODO: Maybe rename to MoviepyResize
class MoviepyZoom:
    def __init__(self, zoom_start: float, zoom_end: float, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check that all params are provided and valid
        self.zoom_start = zoom_start
        self.zoom_end = zoom_end
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

class MoviepyPosition:
    def __init__(self, initial_position: tuple, final_position: float, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check that all params are provided and valid
        self.initial_position = initial_position
        self.final_position = final_position
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

class MoviepyRotation:
    # TODO: Check that all params are provided and valid
    def __init__(self, initial_rotation: int, final_rotation: int, rate_func: type = RateFunction.linear, *args, **kwargs):
        self.initial_rotation = initial_rotation
        self.final_rotation = final_rotation
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

class MoviepyVideoEffect(VideoEffect):
    """
    Creates a Zoom effect in the provided video.
    """
    @classmethod
    def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], zoom: MoviepyZoom, position: MoviepyPosition, rotation: MoviepyRotation):
        """
        Apply the effect on the provided 'video'.

        :param MoviepyZoom zoom: The zoom effect to apply (as a lambda t function).

        :param MoviepyPosition position: The zoom position to apply (as a lambda t function).

        :param MoviepyRotation rotation: The rotation effect to apply (as a lambda t function).
        """
        video = VideoEffect.parse_moviepy_video(video)
        # We reset the mask to avoid problems with zoom
        video = video.add_mask()

        # TODO: Check 'zoom' is instance of MoviepyZoom or valid value
        # TODO: Check 'position' is instance of MoviepyPosition or valid value
        # TODO: Check 'rotation' is instance of MoviepyRotation or valid value

        fps = video.fps
        duration = video.duration
        screensize = video.size

        # Basic configuration (is position needed here (?))
        effected_video = video.resize(screensize).set_position(('center', 'center')).set_duration(duration).set_fps(fps)

        if zoom:
            effected_video = effected_video.resize(lambda t: TFunction.zoom_from_to(t, duration, zoom.zoom_start, zoom.zoom_end, zoom.rate_func))
        if position:
            effected_video = effected_video.set_position(lambda t: TFunction.move_from_to(t, duration, position.initial_position, position.final_position, position.rate_func))
        if rotation:
            effected_video = effected_video.rotate(lambda t: TFunction.rotate_from_to(t, duration, rotation.initial_rotation, rotation.final_rotation, rotation.rate_func))

        return CompositeVideoClip([effected_video], size = screensize)

