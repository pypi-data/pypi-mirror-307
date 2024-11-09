import os
import importlib.util
import numpy as np
import scipy


class ArrayModule:
    use_cython = True

    def __init__(self, device="cpu"):
        self.device = device.lower()

        if device == "cpu":
            self.np = np
            self.scipy = scipy
            self.array_transport = self.asarray
        elif self.device.startswith("cuda"):
            import cupy as cp
            import cupyx.scipy

            self.np = cp
            self.scipy = cupyx.scipy
            self.array_transport = cp.asnumpy
            cuda_device = int(self.device.split(":")[1]) if ":" in self.device else 0
            cp.cuda.Device(cuda_device).use()

        else:
            raise ValueError(f"Unsupported device: {self.device}")

        self.sspd_cross_product, self.sspd_pairwise = self._get_sspd_module()

    def __getattr__(self, name):
        return getattr(self.np, name)

    def __repr__(self) -> str:
        return f"{self.device} array module with {self.np} as numpy and {self.scipy} as scipy"

    def free_all_blocks(self):
        if self.device.startswith("cuda"):
            self.get_default_memory_pool().free_all_blocks()
            self.get_default_pinned_memory_pool().free_all_blocks()

    @property
    def dtype(self):
        return self.complex64

    @property
    def _is_cython_compiled(self):
        return (
            importlib.util.find_spec("qubit_measurement_analysis.cython._sspd")
            is not None
        )

    def _get_sspd_module(self):
        if self.device == "cpu":
            if self._is_cython_compiled and self.use_cython:
                from qubit_measurement_analysis.cython import _sspd as sspd

                return sspd.cross_product, sspd.pairwise
            else:
                from qubit_measurement_analysis import _sspd

                return _sspd.cross_product, _sspd.pairwise
        else:
            from qubit_measurement_analysis.cuda import sspd

            return sspd.cross_product, sspd.pairwise

    def _compile_cython(self):
        import subprocess
        import sys

        try:
            subprocess.check_call(
                [sys.executable, "setup.py", "build_ext", "--inplace"],
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            )
        except subprocess.CalledProcessError:
            print(
                "Failed to compile Cython modules. Falling back to Python implementation."
            )
            self.use_cython = False
