"Single-Shot plotting functionality"
import numpy as np
from matplotlib import pyplot as plt
from qubit_measurement_analysis.visualization.base_plotter import (
    BasicShotPlotter as bsp,
)
from qubit_measurement_analysis.visualization.utils import _get_current_kwargs


class CollectionPlotter:
    # TODO: describe functionality of the class

    def __init__(self, children) -> None:
        self.children = children

    def scatter(self, ax: plt.Axes = None, **kwargs):

        if self.children.is_demodulated:
            _qubits_str = self.children._qubits_str
            states = [state for state in np.sort(self.children.unique_classes_str)]
        else:
            _qubits_str = [self.children._qubits_str]
            states = np.sort(self.children.unique_classes_str)

        if ax is None:
            _, ax = plt.subplots()

        for state in states:
            collection = self.children.filter_by_pattern(state)
            for reg_idx, reg in enumerate(_qubits_str):
                current_kwargs = _get_current_kwargs(kwargs, reg_idx)
                if current_kwargs.get("marker") is None:
                    marker = (
                        f"${state[reg_idx : len(reg) + reg_idx]}$"
                        if self.children.is_demodulated
                        else None
                    )
                    current_kwargs["marker"] = marker

                if current_kwargs.get("label") is None:
                    current_kwargs["label"] = reg

                _ = bsp.scatter_matplotlib(
                    ax,
                    collection.all_values[:, reg_idx, :],
                    **current_kwargs,
                )
        return ax

    def plot_hist(
        self,
        ax: plt.Axes = None,
        correct_key: str = None,
        correct_color: str = None,
        default_color: str = "tab:blue",
    ):
        if ax is None:
            _, ax = plt.subplots()

        # Sort the dictionary by keys
        sorted_items = sorted(self.children.counts.items())
        labels, counts = zip(*sorted_items)

        colors = [default_color] * len(labels)

        if correct_key in labels:
            index = labels.index(correct_key)
            colors[index] = correct_color

        # Plot the bar chart (histogram)
        ax.bar(labels, counts, color=colors)

        ax.set_xticks(
            range(len(labels))
        )  # Set the number of ticks to match the number of labels
        ax.set_xticklabels(labels, rotation=45, ha="right")
        return ax

    def plot_hist_proba(
        self,
        ax: plt.Axes = None,
        correct_key: str = None,
        correct_color: str = None,
        default_color: str = "tab:blue",
    ):
        if ax is None:
            _, ax = plt.subplots()

        # Sort the dictionary by keys
        sorted_items = sorted(self.children.counts_proba.items())
        labels, counts = zip(*sorted_items)

        colors = [default_color] * len(labels)

        if correct_key in labels:
            index = labels.index(correct_key)
            colors[index] = correct_color

        # Plot the bar chart (histogram)
        ax.bar(labels, counts, color=colors)

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right")
        return ax
