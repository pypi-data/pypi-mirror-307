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
    action_units: np.ndarray
        `batch x number_of_units` array where each row contains action unit IDs detected in each batch frame.

    intensities: np.ndarray
        `batch x number_of_units` array where each row represents intensities of action units detected in each batch frame.
    """

    action_units: np.ndarray[tuple[int, int], np.dtype[np.int64]]
    intensities: np.ndarray[tuple[int, int], np.dtype[np.float64]]


class Extractor:
    """
    Action Unit extractor.

    Methods
    ----------
    predict(frame, region)
        Perform prediction.
    """

    # Import from API here to avoid exposition of raw C++ bindings
    from .api import AUExtractor as __RawExtractor  # type: ignore

    __model: __RawExtractor
    __time: Generator[float, None, None]

    def __init__(
        self,
        *,
        landmark_mode: PredictionMode,
        au_mode: PredictionMode,
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
        Initializes action unit extractor instance.

        Parameters
        ----------
        landmark_mode: PredictionMode)
            The prediction mode used in **face landmark detection** stage (image or video).

        au_mode: PredictionMode
            The prediction mode used in **AU estimation stage** (image or video).

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

        self.__model = Extractor.__RawExtractor(
            str(models_directory),
            landmark_mode == PredictionMode.VIDEO,
            au_mode == PredictionMode.VIDEO,
            wild,
            multiple_views,
            limit_angles,
            optimization_iterations,
            regularization_factor,
            weight_factor,
        )

        self.__time = Extractor.__timer(1.0 / float(fps))

    @staticmethod
    def __timer(step: float) -> Generator[float, None, None]:
        current = 0.0

        while True:
            yield current
            current += step

    @staticmethod
    def __convert(au_label: str) -> int:
        return int("".join(filter(str.isdigit, au_label)) or "0")

    # skip typing - ndarray dtype is an absolute garbage
    @staticmethod
    def __as_padded_and_imputed_with_zeros_array(
        data: list[list | None], dtype
    ) -> np.ndarray:
        n_rows = len(data)
        n_columns: int = len(max(filter(None, data), key=len, default=[]))

        if n_columns == 0:
            return np.zeros((1, 1), dtype=dtype)

        array = np.zeros((n_rows, n_columns), dtype=dtype)

        for i, row in enumerate(data):
            if row is None:
                continue

            np.copyto(array[i, : len(row)], row, casting="same_kind")

        return array

    def predict(
        self,
        frame: np.ndarray[tuple[int, int, Literal[3]], np.dtype[np.uint8]]
        | np.ndarray[tuple[int, int, int, Literal[3]], np.dtype[np.uint8]],
        region: np.ndarray[tuple[Literal[4]], np.dtype[np.uint32]]
        | np.ndarray[tuple[int, Literal[4]], np.dtype[np.uint32]],
    ) -> Result | None:
        """
        Predict Action Units for one face.

        Parameters
        ----------
        frame: np.ndarray
            Image (`height x width x 3`) or batch of images (batch x height x width x 3) in 0-255 RGB format to perform prediction on.

        region: np.ndarray
            Bounding box (`4` elements) or batch of bounding boxes (`batch x 4`) in xyxy format, **one per frame**, containing faces to analyze.

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

                prediction = self.__model.detect_au_intensity(
                    frame, next(self.__time), tuple(region)
                )

                if prediction is None:
                    return None

                units = np.array(
                    ([Extractor.__convert(unit[0]) for unit in prediction],),
                    dtype=np.int64,
                )

                intensities = np.array(
                    ([unit[1] for unit in prediction],), dtype=np.float64
                )

                units.flags.writeable = False
                units.flags.writeable = False

                return Result(units, intensities)

            case (n_frames, _, _, n_channels), (n_regions, n_elements):
                assert (
                    n_frames == n_regions
                ), f"Number of frames ({n_frames}) doesn't match the number of regions ({n_regions})"
                assert (
                    n_elements == 4
                ), f"Wrong region format: expected 4 elements, got {n_elements}"
                assert (
                    n_channels == 3
                ), f"Wrong frame format: expected 3-channel RGB image, got {n_channels} channels"

                predictions = [
                    self.__model.detect_au_intensity(frame, timestamp, tuple(region))
                    for frame, timestamp, region in zip(frame, self.__time, region)
                ]

                units = [
                    [Extractor.__convert(unit[0]) for unit in prediction]
                    if prediction is not None
                    else None
                    for prediction in predictions
                ]

                intensities = [
                    [unit[1] for unit in prediction] if prediction is not None else None
                    for prediction in predictions
                ]

                units = Extractor.__as_padded_and_imputed_with_zeros_array(
                    units, np.int64
                )
                intensities = Extractor.__as_padded_and_imputed_with_zeros_array(
                    intensities, np.float64
                )

                units.flags.writeable = False
                intensities.flags.writeable = False

                return Result(units, intensities)

            case _:
                raise RuntimeError(
                    f"Wrong shapes of arguments:\n"
                    f"frame.shape: expected ([batch,] height, width, 3), got {frame.shape},\n"
                    f"region.shape: expected ([batch,] 4), got {region.shape}"
                )
