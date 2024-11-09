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


    