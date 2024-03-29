from __future__ import annotations

from typing import NewType, Sequence


class Device:
    def getModel(self) -> str: ...


# Note: we don't actually know if webots offers up tuples or lists.

class CameraRecognitionObject:
    def getId(self) -> int: ...
    def getPosition(self) -> tuple[float, float, float]: ...
    def getOrientation(self) -> tuple[float, float, float, float]: ...
    def getSize(self) -> tuple[float, float]: ...
    def getPositionOnImage(self) -> tuple[int, int]: ...
    def getSizeOnImage(self) -> tuple[int, int]: ...
    def getNumberOfColors(self) -> int: ...
    def getColors(self) -> Sequence[float]: ...
    # Returns bytes <R2023a
    def getModel(self) -> bytes | str: ...


class Camera(Device):
    GENERIC, INFRA_RED, SONAR, LASER = range(4)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...

    def getType(self) -> int: ...

    def getFov(self) -> float: ...
    def getMinFov(self) -> float: ...
    def getMaxFov(self) -> float: ...
    def setFov(self, fov: float) -> None: ...

    def getFocalLength(self) -> float: ...
    def getFocalDistance(self) -> float: ...
    def getMaxFocalDistance(self) -> float: ...
    def getMinFocalDistance(self) -> float: ...
    def setFocalDistance(self, focalDistance: float) -> None: ...

    def getWidth(self) -> int: ...
    def getHeight(self) -> int: ...

    def getNear(self) -> float: ...

    def getImage(self) -> bytes: ...

    @staticmethod
    def imageGetRed(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetGreen(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetBlue(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetGray(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def pixelGetRed(pixel: int) -> int: ...
    @staticmethod
    def pixelGetGreen(pixel: int) -> int: ...
    @staticmethod
    def pixelGetBlue(pixel: int) -> int: ...
    @staticmethod
    def pixelGetGray(pixel: int) -> int: ...

    def hasRecognition(self) -> bool: ...
    def recognitionEnable(self, samplingPeriod: int) -> None: ...
    def recognitionDisable(self) -> None: ...
    def getRecognitionSamplingPeriod(self) -> int: ...
    def getRecognitionNumberOfObjects(self) -> int: ...
    def getRecognitionObjects(self) -> list[CameraRecognitionObject]: ...


class Compass(Device):
    def enable(self, samplingPeriod: int) -> None: ...
    def getValues(self) -> tuple[float, float, float]: ...


class DistanceSensor(Device):
    GENERIC, INFRA_RED, SONAR, LASER = range(4)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getValue(self) -> float: ...

    def getType(self) -> int: ...

    def getMaxValue(self) -> float: ...
    def getMinValue(self) -> float: ...
    def getAperture(self) -> float: ...


class Emitter(Device):
    CHANNEL_BROADCAST = -1

    def setChannel(self, channel: int) -> None: ...
    def getChannel(self) -> int: ...

    def send(self, data: bytes | str | list[float]) -> int: ...

    def setRange(self, range: float) -> None: ...
    def getRange(self) -> float: ...

    def getBufferSize(self) -> int: ...


class LED(Device):
    def get(self) -> int: ...
    def set(self, value: int) -> None: ...  # noqa:A003


class Motor(Device):
    def setPosition(self, position: float) -> None: ...
    def setVelocity(self, velocity: float) -> None: ...
    def setAcceleration(self, acceleration: float) -> None: ...
    def setAvailableForce(self, force: float) -> None: ...
    def setAvailableTorque(self, torque: float) -> None: ...
    def setControlPID(self, p: float, i: float, d: float) -> None: ...
    def getTargetPosition(self) -> float: ...
    def getMinPosition(self) -> float: ...
    def getMaxPosition(self) -> float: ...
    def getVelocity(self) -> float: ...
    def getMaxVelocity(self) -> float: ...
    def getAcceleration(self) -> float: ...
    def getAvailableForce(self) -> float: ...
    def getMaxForce(self) -> float: ...
    def getAvailableTorque(self) -> float: ...
    def getMaxTorque(self) -> float: ...


class Receiver(Device):
    CHANNEL_BROADCAST = -1

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...

    def getQueueLength(self) -> int: ...
    def nextPacket(self) -> None: ...

    # Returns bytes <R2023a
    def getData(self) -> bytes | str: ...
    def getDataSize(self) -> int: ...

    def getSignalStrength(self) -> float: ...
    def getEmitterDirection(self) -> list[float]: ...

    def setChannel(self, channel: int) -> None: ...
    def getChannel(self) -> int: ...


class TouchSensor(Device):
    BUMPER, FORCE, FORCE3D = range(3)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getValue(self) -> float: ...
    def getValues(self) -> list[float]: ...

    def getType(self) -> int: ...


class Keyboard(Device):
    (
        END,
        HOME,
        LEFT,
        UP,
        RIGHT,
        DOWN,
        PAGEUP,
        PAGEDOWN,
        NUMPAD_HOME,
        NUMPAD_LEFT,
        NUMPAD_UP,
        NUMPAD_RIGHT,
        NUMPAD_DOWN,
        NUMPAD_END,
        KEY,
        SHIFT,
        CONTROL,
        ALT,
    ) = range(18)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getKey(self) -> int: ...


class Display(Device):
    def getWidth(self) -> int: ...
    def getHeight(self) -> int: ...
    def setColor(self, color: int) -> None: ...
    def setAlpha(self, alpha: float) -> None: ...
    def setOpacity(self, opacity: float) -> None: ...
    def setFont(self, font: str, size: int, antiAliasing: bool) -> None: ...

    def drawPixel(self, x: int, y: int) -> None: ...
    def drawLine(self, x1: int, y1: int, x2: int, y2: int) -> None: ...
    def drawRectangle(self, x: int, y: int, width: int, height: int) -> None: ...
    def drawOval(self, cx: int, cy: int, a: int, b: int) -> None: ...
    def drawPolygon(self, x: int, y: int) -> None: ...
    def drawText(self, text: str, x: int, y: int) -> None: ...
    def fillRectangle(self, x: int, y: int, width: int, height: int) -> None: ...
    def fillOval(self, cx: int, cy: int, a: int, b: int) -> None: ...
    def fillPolygon(self, x: int, y: int) -> None: ...

    # (RGB, RGBA, ARGB, BGRA, ABGR) = range(5)

    # def imageNew(
    #     self,
    #     data,
    #     format,
    #     width: Optional[int] = None,
    #     height: Optional[int] = None,
    # ): ...
    # def imageLoad(self, filename: str): ...
    # def imageCopy(self, x: int, y: int, width: int, height: int): ...
    # def imagePaste(self, ir, x: int, y: int, blend: bool = False) -> None: ...
    # def imageSave(self, ir, filename: str) -> None: ...
    # def imageDelete(self, ir) -> None: ...


class Field:
    def getSFBool(self) -> bool: ...
    def getSFInt32(self) -> int: ...
    def getSFFloat(self) -> float: ...
    def getSFVec2f(self) -> list[float]: ...
    def getSFVec3f(self) -> list[float]: ...
    def getSFRotation(self) -> list[float]: ...
    def getSFColor(self) -> list[float]: ...
    def getSFString(self) -> str: ...
    def getSFNode(self) -> Node: ...
    def getMFBool(self, index: int) -> bool: ...
    def getMFInt32(self, index: int) -> int: ...
    def getMFFloat(self, index: int) -> float: ...
    def getMFVec2f(self, index: int) -> list[float]: ...
    def getMFVec3f(self, index: int) -> list[float]: ...
    def getMFColor(self, index: int) -> list[float]: ...
    def getMFRotation(self, index: int) -> list[float]: ...
    def getMFString(self, index: int) -> str: ...
    def getMFNode(self, index: int) -> Node: ...

    def setSFBool(self, value: bool) -> None: ...
    def setSFInt32(self, value: int) -> None: ...
    def setSFFloat(self, value: float) -> None: ...
    def setSFVec2f(self, values: list[float]) -> None: ...
    def setSFVec3f(self, values: list[float]) -> None: ...
    def setSFRotation(self, values: list[float]) -> None: ...
    def setSFColor(self, values: list[float]) -> None: ...
    def setSFString(self, value: str) -> None: ...
    def setMFBool(self, index: int, value: bool) -> None: ...
    def setMFInt32(self, index: int, value: int) -> None: ...
    def setMFFloat(self, index: int, value: float) -> None: ...
    def setMFVec2f(self, index: int, values: list[float]) -> None: ...
    def setMFVec3f(self, index: int, values: list[float]) -> None: ...
    def setMFRotation(self, index: int, values: list[float]) -> None: ...
    def setMFColor(self, index: int, values: list[float]) -> None: ...
    def setMFString(self, index: int, value: str) -> None: ...


class Node:
    def getField(self, fieldName: str) -> Field: ...
    def getProtoField(self, fieldName: str) -> Field: ...

    def remove(self) -> None: ...

    def restartController(self) -> None: ...

    def setVelocity(self, velocity: list[float]) -> None: ...
    def resetPhysics(self) -> None: ...


class Robot:
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def step(self, duration: int) -> int: ...
    def getTime(self) -> float: ...
    def getBasicTimeStep(self) -> float: ...

    def getCustomData(self) -> str: ...
    def setCustomData(self, data: str) -> None: ...

    # Various type-specific getThing methods exist but are deprecated. Remove
    # them from the stub to prevent use.

    def getDevice(self, name: str) -> Device | None: ...


# Beware: this type doesn't actually exist in Webots. It's just here for type
# safety.
SimulationMode = NewType('SimulationMode', int)


class Supervisor(Robot):
    SIMULATION_MODE_PAUSE: SimulationMode
    SIMULATION_MODE_REAL_TIME: SimulationMode
    SIMULATION_MODE_RUN: SimulationMode
    SIMULATION_MODE_FAST: SimulationMode

    def getRoot(self) -> Node: ...
    def getSelf(self) -> Node: ...
    def getFromDef(self, name: str) -> Node | None: ...
    def getFromId(self, id: int) -> Node | None: ...
    def getSelected(self) -> Node | None: ...

    def animationStartRecording(self, file: str) -> bool: ...
    def animationStopRecording(self) -> bool: ...

    def movieStartRecording(
        self,
        file: str,
        width: int,
        height: int,
        codec: int,
        quality: int,
        acceleration: int,
        caption: bool,
    ) -> bool: ...
    def movieStopRecording(self) -> bool: ...
    def movieIsReady(self) -> bool: ...
    def movieFailed(self) -> bool: ...

    def simulationQuit(self, status: int) -> None: ...
    def simulationReset(self) -> None: ...
    def simulationGetMode(self) -> SimulationMode: ...
    def simulationSetMode(self, mode: SimulationMode) -> None: ...

    def worldLoad(self, file: str) -> None: ...
    def worldSave(self, file: str | None = None) -> bool: ...
    def worldReload(self) -> None: ...
