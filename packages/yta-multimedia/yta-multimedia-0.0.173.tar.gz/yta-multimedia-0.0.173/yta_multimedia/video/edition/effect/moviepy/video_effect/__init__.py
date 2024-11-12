from yta_multimedia.video.edition.effect.moviepy.objects import MoviepySetPosition, MoviepyRotate, MoviepyResize
from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from moviepy.editor import CompositeVideoClip, VideoFileClip, ImageClip, VideoClip, ColorClip
from typing import Union


class MoviepyVideoEffect(VideoEffect):
    """
    Class to apply effect on moviepy video by providing
    MoviepyZoom, MoviepyRotation and/or MoviepyPosition
    arguments.
    """
    @classmethod
    def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], resize: MoviepyResize = None, set_position: MoviepySetPosition = None, rotate: MoviepyRotate = None):
        """
        Apply the effect on the provided 'video'.

        :param MoviepyResize resize: The resize effect to apply (as a lambda t function).

        :param MoviepySetPosition set_position: The position to apply (as a lambda t function).

        :param MoviepyRotate rotate: The rotation effect to apply (as a lambda t function).
        """
        return cls.apply_over_video(video = video, background_video = BasePositionMoviepyEffect.get_black_background_clip(video.duration), resize = resize, set_position = set_position, rotate = rotate)
        # TODO: Remove this below when checked
        # video = VideoEffect.parse_moviepy_video(video)
        # # We reset the mask to avoid problems with zoom
        # video = video.add_mask()

        # # TODO: Check 'resize' is instance of MoviepyResize or valid value
        # # TODO: Check 'set_position' is instance of MoviepySetPosition or valid value
        # # TODO: Check 'rotate' is instance of MoviepyRotate or valid value

        # fps = video.fps
        # duration = video.duration
        # screensize = video.size

        # # Basic configuration (is position needed here (?))
        # effected_video = video.resize(screensize).set_position(('center', 'center')).set_duration(duration).set_fps(fps)

        # if resize:
        #     effected_video = effected_video.resize(lambda t: MoviepyResize.t_function(t, duration, resize.initial_size, resize.final_size, resize.rate_func))
        # if set_position:
        #     effected_video = effected_video.set_position(lambda t: MoviepySetPosition.t_function(t, duration, set_position.initial_position, set_position.final_position, set_position.rate_func))
        # if rotate:
        #     effected_video = effected_video.rotate(lambda t: MoviepyRotate.t_function(t, duration, rotate.initial_rotation, rotate.final_rotation, rotate.rate_func))

        # return CompositeVideoClip([effected_video], size = screensize)
    
    @classmethod
    def apply_over_video(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip], background_video: Union[str, VideoClip, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], resize: MoviepyResize = None, set_position: MoviepySetPosition = None, rotate: MoviepyRotate = None):
        video = VideoEffect.parse_moviepy_video(video, True)
        background_video = VideoEffect.parse_moviepy_video(background_video)
        background_video = BasePositionMoviepyEffect.prepare_background_clip(background_video, video)

        fps = video.fps
        duration = video.duration
        screensize = video.size

        effected_video = video.resize(screensize).set_position(('center', 'center')).set_duration(duration).set_fps(fps)

        # # TODO: Check 'resize' is instance of MoviepyResize or valid value
        # # TODO: Check 'set_position' is instance of MoviepySetPosition or valid value
        # # TODO: Check 'rotate' is instance of MoviepyRotate or valid value

        if resize:
            effected_video = effected_video.resize(lambda t: resize.t_function(t, duration, resize.initial_size, resize.final_size, resize.rate_func))

        if set_position:
            BasePositionMoviepyEffect.validate_position(set_position.initial_position)
            BasePositionMoviepyEffect.validate_position(set_position.final_position)

            effected_video = effected_video.set_position(lambda t: set_position.t_function(t, duration, get_moviepy_position(video, background_video, set_position.initial_position), get_moviepy_position(video, background_video, set_position.final_position), set_position.rate_func))

        if rotate:
            effected_video = effected_video.rotate(lambda t: rotate.t_function(t, duration, rotate.initial_rotation, rotate.final_rotation, rotate.rate_func))

        return CompositeVideoClip([
            background_video,
            effected_video
        ])