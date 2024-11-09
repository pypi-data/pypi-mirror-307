from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file import enums as file_enums
from yta_general_utils.file.filename import filename_is_type
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip
from typing import Union


class VideoParser:
    """
    Class to simplify the way we parse video parameters.
    """
    @classmethod
    def to_moviepy(cls, video: Union[str, VideoFileClip, CompositeVideoClip, ColorClip, ImageClip], has_mask: bool = False):
        """
        This method is a helper to turn the provided 'video' to a moviepy
        video type. If it is any of the moviepy video types specified in
        method declaration, it will be returned like that. If not, it will
        be load as a VideoFileClip if possible, or will raise an Exception
        if not.
        """
        if not video:
            raise Exception('No "video" provided.')
        
        if not PythonValidator.is_string(video) and not PythonValidator.is_instance(video, VideoFileClip) and not PythonValidator.is_instance(video, CompositeVideoClip) and not PythonValidator.is_instance(video, ColorClip) and not PythonValidator.is_instance(video, ImageClip):
            raise Exception('The "video" parameter provided is not a valid type. Check valid types in method declaration.')
        
        if PythonValidator.is_string(video):
            if not filename_is_type(video, file_enums.FileType.VIDEO):
                raise Exception('The "video" parameter provided is not a valid video filename.')
            
            if not FileValidator.file_is_video_file(video):
                raise Exception('The "video" parameter is not a valid video file.')
            
            video = VideoFileClip(video, has_mask = has_mask)

        # TODO: Maybe '.add_mask()' (?)

        return video
