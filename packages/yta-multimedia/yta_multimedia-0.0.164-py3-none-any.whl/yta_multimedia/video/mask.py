"""
Extracted from official documentation:
- https://zulko.github.io/moviepy/getting_started/videoclips.html?highlight=mask#mask-clips

The fundamental difference between masks and standard clips is that standard clips output frames with 3 components (R-G-B) per pixel, comprised between 0 and 255, while a mask has just one composant per pixel, between 0 and 1 (1 indicating a fully visible pixel and 0 a transparent pixel). Seen otherwise, a mask is always in greyscale.
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames import VideoFrameExtractor
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file.handler import FileHandler
from yta_general_utils.temp import create_custom_temp_filename 
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, VideoClip, ImageSequenceClip
from typing import Union

import numpy as np
import cv2


class VideoMaskHandler:
    """
    Class created to simplify and encapsulate the working process
    with moviepy video masks.

    TODO: Maybe move this to VideoParser or to FrameHandler
    """
    @classmethod
    def frame_is_normal_clip_frame(cls, frame: np.ndarray):
        """
        Checks if the provided 'frame' numpy array is recognized as
        a frame of a normal moviepy clip with values between 0 and
        255.

        This numpy array should represent a frame of a clip.
        
        A non-modified clip is '.ndim = 3' and '.dtype = np.uint8'.
        """
        if not isinstance(frame, np.ndarray):
            raise Exception('The provided "clip" parameter is not a numpy array.')
        
        # TODO: We check if it is a normal clip frame (we didn't
        # do '.to_mask()' on it)
        if (
            frame.ndim != 3 or
            frame.dtype != np.uint8 or
            np.all((frame >= 0) & (frame <= 255))
        ):
            # You can convert a clip to mask with '.to_mask()' and it would
            # still be a clip (but with mask numpy types)
            return False
        
    @classmethod
    def frame_is_mask_clip_frame(cls, frame: np.ndarray):
        """
        Checks if the provided 'mask_clip' numpy array is recognized
        as an original moviepy mask clip with values between 0 and 1.
        This numpy array should represent a frame of a mask clip.
        
        A non-modified mask clip is '.ndim = 2' and '.dtype = np.float64'.
        """
        if not isinstance(frame, np.ndarray):
            raise Exception('The provided "mask_clip" parameter is not a numpy array.')
        
        # TODO: We check if it is an original mask clip frame (we didn't
        # do '.to_RGB()' on it)
        if (
            frame.ndim != 2 or
            frame.dtype not in (np.float64, np.float32) or
            np.all((frame >= 0) & (frame <= 1))
        ):
            # You can convert a mask clip to clip with '.to_RGB()' and it would
            # still be a mask clip (but with clip numpy types)
            return False

    @classmethod
    def clip_is_normal_clip(cls, clip):
        """
        Normal clips have frames as numpy arrays with values between
        0 and 255 (where 255 means full of color).

        A non-modified clip is '.ndim = 3' and '.dtype = uint8'.
        """
        # TODO: What if I receive the numpy array (?)

        # TODO: I'm not sure, maybe a CompositeVideoClip is a mask (?)
        if not isinstance(clip, VideoClip):
            # TODO: False or Exception (?)
            return False
        
        return cls.frame_is_normal_clip_frame(clip.get_frame(t = 0))

    @classmethod
    def clip_is_mask_clip(cls, clip):
        """
        Mask clips have frames as numpy arrays with values only between
        0 and 1 (where 1 means completely transparent). 
        
        A non-modified mask is '.ndim = 2' and '.dtype = float64'.
        """
        # TODO: What if I receive the numpy array (?)

        # TODO: I'm not sure, maybe a CompositeVideoClip is a mask (?)
        if not isinstance(clip, VideoClip):
            # TODO: False or Exception (?)
            return False

        return cls.frame_is_mask_clip_frame(clip.get_frame(t = 0))
    
    @classmethod
    def invert_mask_frame(cls, frame: np.ndarray):
        """
        Inverts the values in the provided mask clip 'frame'. A mask
        clip frame is a numpy array with values between 0 and 1, so
        they will be inverted.
        """
        if not cls.frame_is_mask_clip_frame(frame):
            raise Exception('The provided "frame" is not actually a mask frame.')
        
        frame[np.where(frame == 0)] = 1
        frame[np.where(frame == 1)] = 0

        return frame

    @classmethod
    def invert_mask_clip(cls, mask_clip):
        """
        Inverts all the numpy mask pixels of the provided 'mask_clip'
        if a valid mask clip is provided. Only the array of numpy
        mask pixels inverted is returned.
        """
        if not cls.clip_is_mask_clip(mask_clip):
            raise Exception('The provided "mask_clip" parameter is not actually a mask clip.')
        
        inverted_mask_frames = []
        # Mask clip is normalized (one pixel between 0 and 1)
        for frame in mask_clip.iter_frames():
            inverted_mask_frames.append(cls.invert_mask_frame(frame))

        return ImageSequenceClip(inverted_mask_frames, fps = mask_clip.fps, ismask = True)

    @classmethod
    def invert_clip_mask(cls, clip):
        """
        Inverts the provided 'clip' mask. The provided 'clip' must be
        a valid normal moviepy clip with a mask. If no mask, the mask
        will be forced.

        This method returns the provided 'clip' with its mask inverted.

        Careful: if the provided 'clip' doesn't have any mask, it will
        be forced as completely opaque, and when inverted it will be
        completely transparent so the normal 'clip' will never be
        shown.
        """
        clip = VideoParser.to_moviepy(clip, has_mask = True)

        clip.mask = cls.invert_mask_clip(clip.mask)

        return clip

# TODO: Check and refactor this below
def invert_video_mask(video: Union[str, VideoFileClip]):
    """
    This method will invert the provided video mask. Make 
    sure the video you provide has a mask. This method 
    will return a mask containing the original video
    with the mask inverted.

    This method will iterate over each frame and will
    invert the numpy array to invert the opacity by 
    chaging the zeros by ones and the ones by zeros (but
    in 0 - 255 range).

    This is useful to overlay videos that have alpha 
    channels so they can let see the video behind through
    that alpha channel. For example, if your video is 
    just a manim animation with only text in the middle,
    the other pixels in the video will be alpha, so if you
    invert them you will obtain the text-transparent 
    effect that is a pretty artistic one.

    This mask has to be used in a specific way, that is in
    a CompositeVideoClip, in second position, with the
    'use_bgclip = True' flag to be over the other video.
    """
    video = VideoParser.to_moviepy(video, has_mask = True)

    # TODO: This is actually being used to create an effect, so is
    # not only inserting a video mask. It needs to be refactored.

    # TODO: Confirm that this exist or create it if not
    FRAMES_FOLDER_NAME = 'frames_main'
    # This is to avoid memory limit exceeded
    in_memory = False

    # We will invert all frames
    # TODO: Please, try to do this with ffmpeg concatenate
    # images with alpha channel to video because it will be
    # faster but I couldn't in the past
    # TODO: Use FfmpegHandler
    clips = []
    for i in range(int(video.fps * video.duration)):
        mask_frame = VideoFrameExtractor.get_frame_by_frame_number(video.mask, i)
        frame = VideoFrameExtractor.get_frame_by_frame_number(video, i)

        # Invert the mask
        where_0 = np.where(mask_frame == 0)
        where_1 = np.where(mask_frame == 1)
        mask_frame[where_0] = 255
        mask_frame[where_1] = 0

        # Combine the fourth (alpha) channel
        mask_frame = mask_frame[:, :, np.newaxis]
        frame_rgba = np.concatenate((frame, mask_frame), axis = 2)
        if in_memory:
            # Maybe it is not possible to build with ffmpeg (https://superuser.com/a/1706440)
            clips.append(ImageClip(frame_rgba, duration = 1 / 60))
        else:
            tmp_frame_name = create_custom_temp_filename(FRAMES_FOLDER_NAME + '/frame' + str(i).zfill(5) + '.png')
            cv2.imwrite(tmp_frame_name, frame_rgba)
    
    if not in_memory:
        frames_folder = create_custom_temp_filename(FRAMES_FOLDER_NAME + '/')
        images = FileHandler.get_list(frames_folder, pattern = '*.png')
        # Maybe it is not possible to build with ffmpeg (https://superuser.com/a/1706440)
        for image in images:
            clips.append(ImageClip(image, duration = 1 / 60))

    mask = concatenate_videoclips(clips)

    return mask

# TODO: I think this will be deleted in the future, when refactored
# and when we confirm that here is another way of handling this
def apply_inverted_mask(video: Union[str, VideoFileClip], mask_video: Union[str, VideoFileClip], output_filename: Union[str, None] = None):
    """
    Applies the provided 'mask_video' with its mask inverted
    over the also provided 'video'. This is useful to make
    artistic effects. This methods applies the 
    'invert_video_mask' method to the provided 'mask_video'.
    """
    if not video:
        raise Exception('No "video" provided.')
    
    if not mask_video:
        raise Exception('No "mask_video" provided.')
    
    if isinstance(video, str):
        if not FileValidator.file_is_video_file:
            raise Exception('Provided "video" is not a valid video file.')
        
        video = VideoFileClip(video, has_mask = True)

    if isinstance(mask_video, str):
        if not FileValidator.file_is_video_file:
            raise Exception('Provided "mask_video" is not a valid video file.')
        
        mask_video = VideoFileClip(mask_video, has_mask = True)

    if not mask_video.mask:
        mask_video = VideoFileClip(mask_video.filename, has_mask = True)

    mask_video = invert_video_mask(mask_video)
    # TODO: Handle durations
    final_clip = CompositeVideoClip([video, mask_video.subclip(0, video.duration)], use_bgclip = True)
    final_clip = final_clip.set_audio(video.audio)

    if output_filename:
        final_clip.write_videofile(output_filename)

    return final_clip

# TODO: Look for the way to store the video with the inverted mask locally
# so I can use that video as usual. Normally I download video with alpha
# layers from the Internet or I create them with manim, but now I have to
# handle it manually, so this is a challenge