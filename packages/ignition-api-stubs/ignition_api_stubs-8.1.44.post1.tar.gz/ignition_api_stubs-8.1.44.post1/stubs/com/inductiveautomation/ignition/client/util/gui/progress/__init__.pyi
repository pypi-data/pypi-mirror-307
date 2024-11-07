from typing import Any, List, Optional

from com.inductiveautomation.ignition.common.gui.progress import (
    TaskProgressListener,
    TaskProgressState,
)
from dev.coatl.helper.types import AnyStr
from java.lang import Object
from java.util.concurrent import CompletableFuture
from java.util.function import Consumer

class AsyncClientTask:
    def canCancel(self) -> bool: ...
    def getTaskTitle(self) -> AnyStr: ...
    def run(self, progressListener: TaskProgressListener) -> None: ...

class TaskHandle:
    def cancel(self) -> None: ...
    def getUid(self) -> AnyStr: ...
    def waitForResult(self, timeout: int) -> Object: ...

class ClientProgressManager(Object):
    def addListener(self, listener: ClientProgressManager.ModelListener) -> None: ...
    def cancelAllTasks(self) -> None: ...
    def cancelTask(self, uid: AnyStr) -> None: ...
    @staticmethod
    def getInstance() -> ClientProgressManager: ...
    def getStates(self) -> List[TaskProgressState]: ...
    def registerGatewayTask(self, taskId: AnyStr) -> TaskHandle: ...
    def removeListener(self, listener: ClientProgressManager.ModelListener) -> None: ...
    def run(self, cf: CompletableFuture, handler: Consumer, owner: Object) -> None: ...
    def runTask(
        self, task: AsyncClientTask, dominant: Optional[bool] = ...
    ) -> TaskHandle: ...
    def setClientContext(self, context: Any) -> None: ...
    def setUIPaused(self, value: bool) -> None: ...
    def shutdown(self) -> None: ...
    def startup(self) -> None: ...

    class ModelListener:
        def progressModelChanged(self) -> None: ...
