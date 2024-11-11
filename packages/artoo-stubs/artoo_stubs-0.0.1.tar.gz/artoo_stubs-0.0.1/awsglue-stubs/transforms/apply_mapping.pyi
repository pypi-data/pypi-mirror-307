from awsglue.dynamicframe import DynamicFrame
from awsglue.transforms import DropFields as DropFields, GlueTransform as GlueTransform

class ApplyMapping(GlueTransform):
    @staticmethod
    def apply(
        frame: DynamicFrame,
        mappings: list[tuple[str, str, str, str]],
        case_sensitive: bool = False,
        transformation_ctx: str = "",
        info: str = '""',
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ) -> DynamicFrame: ...
