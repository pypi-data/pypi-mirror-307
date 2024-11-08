from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np

from .mode import PredictionMode

__all__ = ["Extractor", "Result"]


@dataclass(frozen=True)
class Result:
    """
    Represents the result of a gaze estimation.\\
    **All arrays have leading dimensions corresponding to batch**, even for a single frame detection.\\
    The class and its fields are **immutable**.

    Attributes
    ----------
    eyes: np.ndarray
        `batch x 2 x 3` array containing coordinates of pairs of eyes detected in each batch frame.

    directions: np.ndarray
        `batch x 2 x 3` array containing pairs of gaze directions corresponding to eyes in each batch frame.

    angles: np.ndarray
        `batch x 2` array where each row represents the angle between gaze directions in each batch frame.
    """

    eyes: np.ndarray[tuple[int, Literal[2], Literal[3]], np.dtype[np.float32]]
    directions: np.ndarray[tuple[int, Literal[2], Literal[3]], np.dtype[np.float32]]
    angles: np.ndarray[tuple[int, Literal[2]], np.dtype[np.float32]]


class Extractor:
    """
    Gaze extractor.

    Methods
    ----------
    predict(frame, region)
        Perform prediction.
    """

    # Import from API here to avoid exposition of raw C++ bindings
    from .api import GazeExtractor as __RawExtractor  # type: ignore

    __model: __RawExtractor
    __time: Generator[float, None, None]

    __EMPTY_ENTRY = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))

    def __init__(
        self,
        *,
        mode: PredictionMode,
        focal_length: tuple[float, float],
        optical_center: tuple[float, float],
        models_directory: Path,
        fps: int = 60,
        wild: bool = False,
        multiple_views: bool = True,
        limit_angles: bool = False,
        optimization_iterations: int | None = None,
        regularization_factor: float | None = None,
        weight_factor: float | None = None,
    ) -> None:
        """
        Initializes gaze extractor instance.

        Parameters
        ----------
        mode: PredictionMode
            The prediction mode (image or video).

        focal_length: tuple[float, float]
            A tuple of **positive** numbers representing the camera's focal lengths (fx, fy).

        optical_center: tuple[float, float]
            A tuple of **positive** numbers representing the camera's optical center (cx, cy).

        models_directory: Path
            The directory where OpenFace weights are stored.

        fps: int | None
            Video framerate, default is 60. Ignored in image mode.

        wild: bool | None
            Flag indicating if "wild" settings from OpenFace are used, default is False.

        multiple_views: bool | None
            Flag indicating if "multiple view" settings from OpenFace are used, default is True.

        limit_angles: bool | None
            Flag indicating if angle limiting should be enforced, default is False.
        """

        fx, fy = focal_length
        cx, cy = optical_center

        assert fx > 0.0, "Focal length components must be positive"
        assert fy > 0.0, "Focal length components must be positive"
        assert cx > 0.0, "Optical center coordinates must be positive"
        assert cy > 0.0, "Optical center coordinates must be positive"

        assert fps > 0, "Framerate must be positive"

        if optimization_iterations is not None:
            assert (
                optimization_iterations > 0
            ), "Number of optimization iterations must be positive"

        if regularization_factor is not None:
            assert (
                regularization_factor > 0.0
            ), "Optimization regularization factor must be positive"

        if weight_factor is not None:
            assert weight_factor > 0.0, "Optimization weight factor must be positive"

        assert (
            models_directory.exists() and models_directory.is_dir()
        ), "Invalid models directory passed"

        model = Extractor.__RawExtractor(
            str(models_directory),
            mode == PredictionMode.VIDEO,
            wild,
            multiple_views,
            limit_angles,
            optimization_iterations,
            regularization_factor,
            weight_factor,
        )

        model.set_camera_calibration(fx, fy, cx, cy)

        self.__model = model
        self.__time = Extractor.__timer(1.0 / float(fps))

    @staticmethod
    def __timer(step: float) -> Generator[float, None, None]:
        current = 0.0

        while True:
            yield current
            current += step

    def predict(
        self,
        frame: np.ndarray[tuple[int, int, Literal[3]], np.dtype[np.uint8]]
        | np.ndarray[tuple[int, int, int, Literal[3]], np.dtype[np.uint8]],
        region: np.ndarray[tuple[Literal[4]], np.dtype[np.uint32]]
        | np.ndarray[tuple[int, Literal[4]], np.dtype[np.uint32]],
    ) -> Result | None:
        """
        Predict gazes for one face.

        Parameters
        ----------
        frame: np.ndarray
            Image (`height x width x 3`) or batch of images (batch x height x width x 3) in 0-255 RGB format to perform prediction on.

        region: np.ndarray
            Array (`4` elements) or batch of arrays (`batch x 4`) of xyxy bounding boxes (**one per frame**) containing faces to analyze.

        Returns
        ----------
        result: Result | None
            Result containing detection if successful, None otherwise.

        Raises
        ----------
        ValueError
            If passed arrays don't match shape requirements
        """

        match frame.shape, region.shape:
            case (_, _, n_channels), (n_elements,):
                assert (
                    n_elements == 4
                ), "Wrong region format: expected 4 elements, got {n_elements}"
                assert (
                    n_channels == 3
                ), f"Wrong frame format: expected 3-channel RGB image, got {n_channels} channels"

                result = self.__model.detect_gaze(
                    frame, next(self.__time), tuple(region)
                )

                if result is None:
                    return None

                return Result(
                    np.array(((result.eye1, result.eye2),), dtype=np.float32),
                    np.array(
                        ((result.direction1, result.direction2),), dtype=np.float32
                    ),
                    np.array(result.angle),
                )

            case (n_frames, _, _, n_channels), (n_regions, n_elements):
                assert (
                    n_frames == n_regions
                ), f"Number of frames ({n_frames}) doesn't match number of regions ({n_regions})"
                assert (
                    n_elements == 4
                ), f"Wrong region format: expected 4 elements, got {n_elements}"
                assert (
                    n_channels == 3
                ), f"Wrong frame format: expected 3-channel RGB image, got {n_channels} channels"

                predictions = [
                    self.__model.detect_gaze(frame, timestamp, tuple(region))
                    for frame, timestamp, region in zip(frame, self.__time, region)
                ]

                eyes = np.array(
                    [
                        (prediction.eye1, prediction.eye2)
                        if prediction is not None
                        else Extractor.__EMPTY_ENTRY
                        for prediction in predictions
                    ],
                    dtype=np.float32,
                )

                directions = np.array(
                    [
                        (prediction.direction1, prediction.direction2)
                        if prediction is not None
                        else Extractor.__EMPTY_ENTRY
                        for prediction in predictions
                    ],
                    dtype=np.float32,
                )

                angles = np.array(
                    [
                        prediction.angle if prediction is not None else 0.0
                        for prediction in predictions
                    ],
                    dtype=np.float32,
                )

                eyes.flags.writeable = False
                directions.flags.writeable = False
                angles.flags.writeable = False

                return Result(eyes, directions, angles)

            case _:
                raise ValueError(
                    f"Wrong shapes of arguments:\n"
                    f"frame.shape: expected ([batch,] height, width, 3), got {frame.shape},\n"
                    f"region.shape: expected ([batch,] 4), got {region.shape}"
                )
