from typing import NamedTuple

from py4j.java_collections import JavaArray
from py4j.java_gateway import JavaObject

__all__ = ['SparkJobInfo', 'SparkStageInfo', 'StatusTracker']

class SparkJobInfo(NamedTuple):
    jobId: int
    stageIds: JavaArray
    status: str

class SparkStageInfo(NamedTuple):
    stageId: int
    currentAttemptId: int
    name: str
    numTasks: int
    numActiveTasks: int
    numCompletedTasks: int
    numFailedTasks: int

class StatusTracker:
    def __init__(self, jtracker: JavaObject) -> None: ...
    def getJobIdsForGroup(self, jobGroup: str | None = None) -> list[int]: ...
    def getActiveStageIds(self) -> list[int]: ...
    def getActiveJobsIds(self) -> list[int]: ...
    def getJobInfo(self, jobId: int) -> SparkJobInfo | None: ...
    def getStageInfo(self, stageId: int) -> SparkStageInfo | None: ...
