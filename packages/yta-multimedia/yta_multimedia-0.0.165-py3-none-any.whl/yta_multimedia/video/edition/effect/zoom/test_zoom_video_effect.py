from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_multimedia.video.edition.effect.utils.resize_t_functions import test_zoom_t_func
from moviepy.editor import CompositeVideoClip, VideoFileClip, ImageClip, VideoClip, ColorClip
from typing import Union


# TODO: Remove this when all tested
class TestZoomVideoEffect(VideoEffect):
    """
    Creates a linear Zoom effect in the provided video.
    """

    @classmethod
    def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip],):
        """
        Apply the effect on the provided 'video'.
        """
        video = VideoEffect.parse_moviepy_video(video)
        # We reset the mask to avoid problems with zoom
        video = video.add_mask()

        fps = video.fps
        duration = video.duration
        screensize = video.size

        effected_video = (
            video
            .resize(screensize)
            .resize(lambda t: test_zoom_t_func(t, duration))
            .set_position(('center', 'center'))
            .set_duration(duration)
            .set_fps(fps)
        )

        return CompositeVideoClip([effected_video], size = screensize)


    