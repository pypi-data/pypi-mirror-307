"""Data processing functionality for collection of Shots"""

# TODO: something wrong with slicing shotcollections when indexes are [:, num]

import os
import re
import glob
import warnings
import random
from typing import List, Callable, Iterator, Iterable, Union

from qubit_measurement_analysis.data.single_shot import SingleShot
from qubit_measurement_analysis._array_module import ArrayModule
from qubit_measurement_analysis.visualization.shot_collection_plotter import (
    CollectionPlotter as cp,
)
from qubit_measurement_analysis._transformations import (
    _add,
    _sub,
    _mul,
    _div,
    _mean,
    _mean_filter,
    _mean_convolve,
    _mean_centring,
    _normalize,
    _standardize,
    _demodulate,
    _whittaker_eilers_smoother,
)
from qubit_measurement_analysis.data._distance_utils import sspd_to as _sspd_to


class ShotCollection:

    def __init__(
        self, singleshots: list[SingleShot] = None, device: str = "cpu"
    ) -> None:
        self.xp = ArrayModule(device)
        self.singleshots = []
        self.all_values = None
        self.all_qubits_classes = None
        self._is_demodulated = None
        self._plotter = cp(children=self)
        self._ops = []  # List to store lazy operations

        if singleshots:
            self.extend(singleshots)

    def _validate_shots(self, shots: List[SingleShot]) -> None:
        if not shots:
            return  # Empty list is valid

        # 1. Check if all data in shots list are SingleShot objects
        if not all(isinstance(shot, SingleShot) for shot in shots):
            raise TypeError("All elements in shots must be SingleShot objects")

        # 2. Check if all singleshots have the same qubits_classes.keys()
        first_shot_keys = set(shots[0].qubits_classes.keys())
        if not all(
            set(shot.qubits_classes.keys()) == first_shot_keys for shot in shots
        ):
            raise ValueError(
                "All SingleShot objects must have the same qubits_classes keys"
            )

        # 3. Check if all singleshots are either all demodulated or all not demodulated
        first_shot_demodulated = shots[0].is_demodulated
        if not all(shot.is_demodulated == first_shot_demodulated for shot in shots):
            raise ValueError(
                "All SingleShot objects must have the same demodulation status"
            )
        self._is_demodulated = first_shot_demodulated

    def _apply_vectorized(self, func: Callable, **kwargs) -> "ShotCollection":
        self._ops.append((func, kwargs))
        return self

    def __getitem__(self, index) -> SingleShot:
        if isinstance(index, tuple):
            # The first element of the index is for selecting Shots
            shot_indices = index[0]
            # The remaining elements of the index are for each Shot's array
            shot_slices = index[1:]
            # Apply indices
            selected_shots = self.singleshots[shot_indices]
            # If selected_shots is a single Shot, make it a list
            if isinstance(selected_shots, SingleShot):
                selected_shots = [selected_shots]
            # Apply shot slices
            new_shots = [shot[shot_slices] for shot in selected_shots]
            return ShotCollection(new_shots, self.device)
        elif isinstance(index, slice):
            return ShotCollection(self.singleshots[index], self.device)
        else:
            return self.singleshots[index]

    def __len__(self) -> int:
        return len(self.singleshots)

    def __repr__(self) -> str:
        return f"ShotCollection(n_shots={len(self)}, device='{self.device}', pending_ops={len(self._ops)})"

    def __iter__(self) -> Iterator[SingleShot]:
        return iter(self.singleshots)

    def __copy__(self):
        return type(self)(self.singleshots, self.device)

    def __add__(self, other):
        if hasattr(other, "value") or hasattr(other, "all_values"):
            raise (f"cannot perform operation with {type(other)}")
        new_values = _add(self.all_values, other)
        new_shots = [
            SingleShot(value, qubits_classes, self.is_demodulated, self.device)
            for value, qubits_classes in zip(new_values, self.all_qubits_classes)
        ]
        new_collection = ShotCollection(new_shots, self.device)
        return new_collection

    def __sub__(self, other):
        if hasattr(other, "value") or hasattr(other, "all_values"):
            raise (f"cannot perform operation with {type(other)}")
        new_values = _sub(self.all_values, other)
        new_shots = [
            SingleShot(value, qubits_classes, self.is_demodulated, self.device)
            for value, qubits_classes in zip(new_values, self.all_qubits_classes)
        ]
        new_collection = ShotCollection(new_shots, self.device)
        return new_collection

    def __mul__(self, other):
        if hasattr(other, "value") or hasattr(other, "all_values"):
            raise (f"cannot perform operation with {type(other)}")
        new_values = _mul(self.all_values, other)
        new_shots = [
            SingleShot(value, qubits_classes, self.is_demodulated, self.device)
            for value, qubits_classes in zip(new_values, self.all_qubits_classes)
        ]
        new_collection = ShotCollection(new_shots, self.device)
        return new_collection

    def __truediv__(self, other):
        if hasattr(other, "value") or hasattr(other, "all_values"):
            raise (f"cannot perform operation with {type(other)}")
        new_values = _div(self.all_values, other)
        new_shots = [
            SingleShot(value, qubits_classes, self.is_demodulated, self.device)
            for value, qubits_classes in zip(new_values, self.all_qubits_classes)
        ]
        new_collection = ShotCollection(new_shots, self.device)
        return new_collection

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __itruediv__(self, other):
        return self.__truediv__(other)

    @property
    def device(self) -> str:
        return self.xp.device

    def to(self, device: str) -> "ShotCollection":
        if device == self.device:
            return self
        self.xp = ArrayModule(device)
        for shot in self.singleshots:
            shot.to(device)
        self._update_arrays()
        return self

    @property
    def shape(self):
        # TODO: add description to the method
        return self.all_values.shape

    @property
    def is_demodulated(self):
        # TODO: Change method. I want to get the one unique is_demodulated flag across all singleshot in collection (True or False)
        return self._is_demodulated

    def scatter(self, ax=None, **kwargs):
        # TODO: add docstring
        return self._plotter.scatter(ax, **kwargs)

    def plot_hist(
        self, ax=None, correct_key=None, correct_color=None, default_color="tab:blue"
    ):
        # TODO: add docstring
        return self._plotter.plot_hist(ax, correct_key, correct_color, default_color)

    def plot_hist_proba(
        self, ax=None, correct_key=None, correct_color=None, default_color="tab:blue"
    ):
        # TODO: add docstring
        return self._plotter.plot_hist_proba(
            ax, correct_key, correct_color, default_color
        )

    def append(self, shot: SingleShot) -> None:
        self.extend([shot])

    def extend(self, shots: List[SingleShot]) -> None:
        self._validate_shots(shots)
        self.singleshots.extend(shots)
        self._update_arrays()
        self._update_qubits_classes()

    def shuffle(self, seed: int = None):
        random.seed(seed)
        random.shuffle(self.singleshots)
        self._update_arrays()
        self._update_qubits_classes()
        return self

    def _update_arrays(self):
        self.all_values = None
        self.xp.free_all_blocks()  # clear device and pinned cache
        new_values = self.xp.array([shot.value for shot in self.singleshots])
        self.all_values = self.xp.stack(new_values)

    def _update_qubits_classes(self):
        self.all_qubits_classes = None
        new_qubits_classes = [shot.qubits_classes for shot in self.singleshots]
        self.all_qubits_classes = new_qubits_classes

    @property
    def all_classes(self):
        all_classes = [shot.classes for shot in self.singleshots]
        return self.xp.vstack(all_classes)

    @property
    def qubits(self):
        return self[0].qubits

    def mean(self, axis: int = -1) -> Union["SingleShot", "ShotCollection"]:
        # TODO: add description to the function
        if len(self.singleshots) == 0:
            raise ValueError("SignalCollection is empty")

        if axis == 0:
            qubits_classes = self.singleshots[0].qubits_classes
            # check if all signleshots are of the same state
            if len(self.unique_classes_str) != 1:
                qubits_classes = {int(reg): -1 for reg in list(self._qubits_str)}
                warnings.warn(
                    "ShotCollection contains more than 1 unique state. Taking mean regardless of state. Assigned state is '<UNK>'"
                )
            return SingleShot(
                self.all_values.mean(axis),
                qubits_classes,
                self.is_demodulated,
                self.device,
            )
        else:
            return self._apply_vectorized(_mean, axis=axis)

    @property
    def unique_classes(self):
        # TODO: add description to the method
        return self.xp.unique(self.all_classes, axis=0)

    @property
    def unique_classes_str(self):
        # TODO: add description to the method
        unique_classes_str = set()  # Using a set to store unique classes
        for shot in self.singleshots:
            unique_classes_str.add(shot.state)
        # Converting the set to a list before returning
        return list(unique_classes_str)

    @property
    def counts(self):
        counts = {}
        for state in self.unique_classes_str:
            counts[state] = len(self.filter_by_pattern(state))
        return counts

    @property
    def counts_proba(self):
        counts_proba = {}
        for state in self.unique_classes_str:
            counts_proba[state] = len(self.filter_by_pattern(state)) / len(self)
        return counts_proba

    def update_all_qubits_classes(self, updated_elements: dict):
        for shot in self.singleshots:
            shot.update_qubits_classes(updated_elements)
        self._update_qubits_classes()

    @property
    def _qubits_str(self):
        # TODO: add description to the method

        unique_registers = set()  # Using a set to store unique classes

        for shot in self.singleshots:
            unique_registers.add(shot._qubits_str)
        return (
            list(unique_registers)
            if len(unique_registers) > 1
            else list(unique_registers)[0]
        )

    def filter_by_pattern(self, patterns) -> "ShotCollection":
        # TODO: add description to the function
        if isinstance(patterns, str):
            patterns = [patterns]

        compiled_patterns = [re.compile(pattern) for pattern in patterns]
        matched_strings = [
            s
            for s in self.unique_classes_str
            if any(compiled_pattern.match(s) for compiled_pattern in compiled_patterns)
        ]
        target_set = set(matched_strings)
        filtered_singleshots = [
            shot for shot in self.singleshots if shot.state in target_set
        ]
        return ShotCollection(filtered_singleshots, self.device)

    def demodulate_all(
        self, intermediate_freq: dict, meas_time: Iterable, direction: str
    ) -> "ShotCollection":
        # TODO: add description to the function
        # Conversion from dict to array
        intermediate_freq = self.xp.array(list(intermediate_freq.values())).reshape(
            -1, 1
        )
        # Reshape meas_time to match the shape required for broadcasting
        meas_time = meas_time.reshape(1, -1)
        return self._apply_vectorized(
            _demodulate,
            intermediate_freq=intermediate_freq,
            meas_time=meas_time,
            direction=direction,
            module=self.xp,
        )

    def mean_centring_all(self, axis=-1) -> "ShotCollection":
        # TODO: add description to the function
        return self._apply_vectorized(_mean_centring, axis=axis)

    def mean_filter_all(self, k) -> "ShotCollection":
        return self._apply_vectorized(_mean_filter, k=k, module=self.xp)

    def mean_convolve_all(self, kernel_size, stride) -> "ShotCollection":
        return self._apply_vectorized(
            _mean_convolve, kernel_size=kernel_size, stride=stride, module=self.xp
        )

    def normalize_all(self, axis=-1) -> "ShotCollection":
        return self._apply_vectorized(_normalize, axis=axis)

    def standardize_all(self, axis=-1) -> "ShotCollection":
        return self._apply_vectorized(_standardize, axis=axis)

    def whittaker_eilers_smoother_all(self, lamb, d) -> "ShotCollection":
        return self._apply_vectorized(
            _whittaker_eilers_smoother, lamb=lamb, d=d, module=self.xp
        )

    def compute(self, free_all_blocks=False) -> "ShotCollection":
        """Execute all pending operations on the data."""
        if not self._ops:
            return self

        result = self.all_values
        for func, kwargs in self._ops:
            result = func(result, **kwargs)
        if result.dtype != self.xp.complex64:
            result = result.astype(self.xp.complex64)

        is_demodulated = _demodulate in [t[0] for t in self._ops] or self.is_demodulated

        new_shots = [
            SingleShot(value, qubits_classes, is_demodulated, self.device)
            for value, qubits_classes in zip(result, self.all_qubits_classes)
        ]

        new_collection = ShotCollection(new_shots, self.device)
        self._ops.clear()
        if free_all_blocks:
            self.xp.free_all_blocks()
        return new_collection

    def sspd_to(self, other, method: str = "cross_product"):
        return _sspd_to(self.all_values, other, self.xp, method)

    def save_all(
        self,
        parent_dir: str,
        train_ratio: float,
        val_ratio: float,
        test_ratio: float,
        clear_existing: bool = False,
        verbose: bool = False,
    ) -> None:
        """Save the ShotCollection to the specified directory with train, val, test splits

        Args:
            parent_dir (str): The parent directory where the data will be saved.
            train_ratio (float): _description_
            val_ratio (float): _description_
            test_ratio (float): _description_
            clear_existing (bool, optional): _description_. Defaults to False.
            verbose (bool): Whether to print verbose output.
        """
        if not (0 <= train_ratio <= 1 and 0 <= val_ratio <= 1 and 0 <= test_ratio <= 1):
            raise ValueError("Ratios must be between 0 and 1")
        if not abs(train_ratio + val_ratio + test_ratio - 1) < 1e-6:
            raise ValueError("Ratios must sum up to 1")
        if clear_existing:
            if verbose:
                print("[INFO] Deleting files...")
            for subfolder in ["train", "val", "test"]:
                for state in self.unique_classes_str:
                    directory = os.path.join(
                        parent_dir, self._qubits_str, subfolder, state
                    )
                    for file in glob.glob(os.path.join(directory, "*.npy")):
                        os.remove(file)

        self.xp.random.shuffle(self.singleshots)
        num_shots = len(self.singleshots)
        train_end = int(train_ratio * num_shots)
        val_end = train_end + int(val_ratio * num_shots)
        if verbose:
            print("[INFO] Start saving files...")
        for idx, shot in enumerate(self.singleshots):
            if idx < train_end:
                subfolder = "train"
            elif idx < val_end:
                subfolder = "val"
            else:
                subfolder = "test"
            shot.save(parent_dir, subfolder, verbose)

    @classmethod
    def load(
        cls,
        parent_dir: str,
        qubits_dir: str,
        state: str,
        subfolder: str,
        num_samples: int = None,
        verbose: bool = False,
    ) -> "ShotCollection":
        """Load a specified number of SingleShot instances from a directory.

        Args:
            parent_dir (str): The parent directory where the data will be saved.
            qubits_dir (str): The folder indicating qubit number set of the readout signal ('123' for instance).
            state (str): The state of the system. For instance '001'
            subfolder (str): Subfolder within the state folder ('train', 'val', or 'test').
            num_samples (int, optional): Number of samples to load. If None, load all available samples. Defaults to None.
            verbose (bool): Whether to print verbose output.

        Returns:
            ShotCollection: A collection of SingleShot instances.
        """
        collection = cls()

        if num_samples is None:
            directory = os.path.join(parent_dir, qubits_dir, subfolder, state)
            num_samples = len(glob.glob(os.path.join(directory, "*")))

        for idx in range(num_samples):
            singleshot = SingleShot.load(
                parent_dir, qubits_dir, state, subfolder, idx, verbose
            )
            collection.append(singleshot)
        return collection
