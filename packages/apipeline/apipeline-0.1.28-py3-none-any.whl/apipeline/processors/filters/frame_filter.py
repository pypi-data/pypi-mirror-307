from typing import List

from apipeline.frames.sys_frames import Frame, SystemFrame
from apipeline.frames.control_frames import ControlFrame
from apipeline.frames.app_frames import AppFrame
from apipeline.processors.frame_processor import FrameDirection, FrameProcessor


class FrameFilter(FrameProcessor):

    def __init__(self, types: List[type]):
        super().__init__()
        self._types = types

    #
    # Frame processor
    #

    def _should_passthrough_frame(self, frame):
        for t in self._types:
            if isinstance(frame, t):
                return True

        return (isinstance(frame, AppFrame)
                or isinstance(frame, ControlFrame)
                or isinstance(frame, SystemFrame))

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if self._should_passthrough_frame(frame):
            await self.push_frame(frame, direction)
