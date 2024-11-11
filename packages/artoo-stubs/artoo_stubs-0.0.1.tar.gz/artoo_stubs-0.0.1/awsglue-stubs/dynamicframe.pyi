from typing import Any

from _typeshed import Incomplete
from pyspark.sql.connect.dataframe import DataFrame

long = int
basestring = str
unicode = str
imap = map
ifilter = filter

class ResolveOption:
    path: Incomplete
    action: Incomplete
    target: Incomplete
    def __init__(self, path, action, target: Incomplete | None = None) -> None: ...

class DynamicFrame:
    glue_ctx: Incomplete
    name: Incomplete
    def __init__(self, jdf, glue_ctx, name: str = "") -> None: ...
    def with_frame_schema(self, schema): ...
    def schema(self): ...
    def show(self, num_rows: int = 20) -> None: ...
    def filter(self, f, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0): ...
    def mapPartitions(
        self,
        f,
        preservesPartitioning: bool = True,
        transformation_ctx: str = "",
        info: str = "",
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ): ...
    def map(
        self,
        f,
        preservesPartitioning: bool = False,
        transformation_ctx: str = "",
        info: str = "",
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ): ...
    def mapPartitionsWithIndex(
        self,
        f,
        preservesPartitioning: bool = False,
        transformation_ctx: str = "",
        info: str = "",
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ): ...
    def printSchema(self) -> None: ...
    def toDF(self, options: Any = None) -> DataFrame: ...
    @classmethod
    def fromDF(cls, dataframe: Any, glue_ctx: Any, name: str) -> DynamicFrame: ...
    def unbox(
        self, path, format, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0, **options
    ): ...
    def drop_fields(self, paths, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0): ...
    def select_fields(self, paths, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0): ...
    def split_fields(
        self, paths, name1, name2, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0
    ): ...
    def split_rows(
        self, comparison_dict, name1, name2, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0
    ): ...
    def rename_field(
        self, oldName, newName, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0
    ): ...
    def write(
        self, connection_type, connection_options={}, format: Incomplete | None = None, format_options={}, accumulator_size: int = 0
    ): ...
    def count(self): ...
    def spigot(self, path, options={}, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0): ...
    def join(
        self, paths1, paths2, frame2, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0
    ): ...
    def unnest(self, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0): ...
    def relationalize(
        self,
        root_table_name,
        staging_path,
        options={},
        transformation_ctx: str = "",
        info: str = "",
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ): ...
    def applyMapping(self, *args, **kwargs): ...
    def apply_mapping(
        self,
        mappings,
        case_sensitive: bool = False,
        transformation_ctx: str = "",
        info: str = "",
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ): ...
    def unnest_ddb_json(self, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0): ...
    def resolveChoice(
        self,
        specs: Incomplete | None = None,
        choice: str = "",
        database: Incomplete | None = None,
        table_name: Incomplete | None = None,
        transformation_ctx: str = "",
        info: str = "",
        stageThreshold: int = 0,
        totalThreshold: int = 0,
        catalog_id: Incomplete | None = None,
    ): ...
    def mergeDynamicFrame(
        self,
        stage_dynamic_frame,
        primary_keys,
        transformation_ctx: str = "",
        options={},
        info: str = "",
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ): ...
    def union(self, other_frame, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0): ...
    def getNumPartitions(self): ...
    def repartition(
        self, num_partitions, transformation_ctx: str = "", info: str = "", stageThreshold: int = 0, totalThreshold: int = 0
    ): ...
    def coalesce(
        self,
        num_partitions,
        shuffle: bool = False,
        transformation_ctx: str = "",
        info: str = "",
        stageThreshold: int = 0,
        totalThreshold: int = 0,
    ): ...
    def errorsAsDynamicFrame(self): ...
    def errorsCount(self): ...
    def stageErrorsCount(self): ...
    def assertErrorThreshold(self): ...

class DynamicFrameCollection:
    def __init__(self, dynamic_frames, glue_ctx) -> None: ...
    def __getitem__(self, key): ...
    def __len__(self) -> int: ...
    def keys(self): ...
    def values(self): ...
    def select(self, key, transformation_ctx: str = ""): ...
    def map(self, callable, transformation_ctx: str = ""): ...
    def flatmap(self, f, transformation_ctx: str = ""): ...

class DynamicFrameReader:
    def __init__(self, glue_context) -> None: ...
    def from_rdd(self, data, name, schema: Incomplete | None = None, sampleRatio: Incomplete | None = None): ...
    def from_options(
        self,
        connection_type,
        connection_options={},
        format: Incomplete | None = None,
        format_options={},
        transformation_ctx: str = "",
        push_down_predicate: str = "",
        **kwargs,
    ): ...
    def from_catalog(
        self,
        database: Incomplete | None = None,
        table_name: Incomplete | None = None,
        redshift_tmp_dir: str = "",
        transformation_ctx: str = "",
        push_down_predicate: str = "",
        additional_options={},
        catalog_id: Incomplete | None = None,
        **kwargs,
    ): ...

class DynamicFrameWriter:
    def __init__(self, glue_context) -> None: ...
    def from_options(
        self,
        frame,
        connection_type,
        connection_options={},
        format: Incomplete | None = None,
        format_options={},
        transformation_ctx: str = "",
    ): ...
    def from_catalog(
        self,
        frame,
        database: Incomplete | None = None,
        table_name: Incomplete | None = None,
        redshift_tmp_dir: str = "",
        transformation_ctx: str = "",
        additional_options={},
        catalog_id: Incomplete | None = None,
        **kwargs,
    ): ...
    def from_jdbc_conf(
        self, frame, catalog_connection, connection_options={}, redshift_tmp_dir: str = "", transformation_ctx: str = ""
    ): ...
