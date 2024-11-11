import os
from typing import TypedDict
import typing


class FolderStatUnit(TypedDict, total=False):
    size: int
    modified: float


class FolderComputeUnit(TypedDict, total=False):
    sizeDiffer: typing.Literal[-1, 0, 1]
    state: typing.Literal["new", "modified", "deleted"]


class FolderSnapshot:
    def __init__(self, folderPath: str):
        self.__folderPath = folderPath
        self.__filesMap = {}
        self.__folderSerial = []
        self.__fileToFolderMap = {}
        self.__folderDepthMap = {}

        for root, dirs, files in os.walk(self.__folderPath):
            for dir in dirs:
                dirPath = os.path.join(root, dir)
                self.__folderSerial.append(dirPath)
            for file in files:
                filePath = os.path.join(root, file)
                self.__filesMap[filePath] = FolderStatUnit(
                    size=os.path.getsize(filePath), modified=os.path.getmtime(filePath)
                )
                self.__fileToFolderMap[filePath] = self.__folderSerial.index(root)
                self.__folderDepthMap[filePath] = len(
                    os.path.relpath(root, folderPath).split(os.path.sep)
                )

    def computeDifference(
        self, olderSnapshot: "FolderSnapshot"
    ) -> typing.Dict[str, FolderComputeUnit]:
        fileResults = {}
        
        for filePath, stat in self.__filesMap.items():
            if filePath in olderSnapshot.__filesMap:
                oldStat = olderSnapshot.__filesMap[filePath]
                if stat["modified"] != oldStat["modified"]:
                    fileResults[filePath] = FolderComputeUnit(
                        sizeDiffer=(1 if stat["size"] > oldStat["size"] else -1 if stat["size"] < oldStat["size"] else 0),
                        state="modified"
                    )
            else:
                fileResults[filePath] = FolderComputeUnit(
                    sizeDiffer=0,
                    state="new"
                )

        for filePath in olderSnapshot.__filesMap:
            if filePath not in self.__filesMap:
                fileResults[filePath] = FolderComputeUnit(
                    sizeDiffer=0,
                    state="deleted"
                )

        return fileResults

class FolderWatcher:
    def __init__(self, folderPath: str):
        self.__folderPath = folderPath

    @property
    def folderPath(self):
        return self.__folderPath

    def thread(self):
        pass

    def snapshot(self):
        pass

    def __watcher_thread(self):
        pass