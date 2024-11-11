from typing import Dict

from awsglue.dynamicframe import DynamicFrame, DynamicFrameCollection
from awsglue.transforms import GlueTransform as GlueTransform

class RenameField(GlueTransform):
    @staticmethod
    def apply(
        frame: DynamicFrame,
        old_name: str,
        new_name: str,
        transformation_ctx: str = "",
        info: str = '""',
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ) -> DynamicFrame: ...

class DropFields(GlueTransform):
    @staticmethod
    def apply(
        frame: DynamicFrame,
        paths: list[str],
        transformation_ctx: str = "",
        info: str = '""',
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ) -> DynamicFrame: ...

class SelectFields(GlueTransform):
    @staticmethod
    def apply(
        frame: DynamicFrame,
        paths: list[str],
        transformation_ctx: str = "",
        info: str = '""',
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ) -> DynamicFrame: ...

class SplitFields(GlueTransform):
    @staticmethod
    def apply(
        frame: DynamicFrame,
        paths: list[str],
        frame1: str = "frame1",
        frame2: str = "frame2",
        transformation_ctx: str = "",
        info: str = '""',
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ) -> DynamicFrameCollection: ...

class SplitRows(GlueTransform):
    @staticmethod
    def apply(
        frame: DynamicFrame,
        comparison_dict: Dict[str, str],
        frame1: str = "frame1",
        frame2: str = "frame2",
        transformation_ctx: str = "",
        info: str = '""',
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ) -> DynamicFrameCollection: ...

class Join(GlueTransform):
    @staticmethod
    def apply(frame1: DynamicFrame, frame2: DynamicFrame, keys1: str, keys2: str, transformation_ctx: str = "") -> DynamicFrame: ...

class Spigot(GlueTransform):
    @staticmethod
    def apply(frame: DynamicFrame, path: str, options: Dict[str, str], transformation_ctx: str = "") -> DynamicFrame: ...
