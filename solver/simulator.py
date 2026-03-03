"""Python wrapper around omsim's libverify for solution verification."""
from __future__ import annotations
import ctypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class VerifyResult:
    """Result of verifying a solution."""
    valid: bool
    error: Optional[str] = None
    cycles: int = -1
    cost: int = -1
    area: int = -1
    instructions: int = -1

    def __repr__(self) -> str:
        if not self.valid:
            return f"VerifyResult(INVALID: {self.error})"
        return f"VerifyResult({self.cost}g/{self.cycles}c/{self.area}a/{self.instructions}i)"


class Simulator:
    """Wrapper around omsim's libverify shared library."""

    def __init__(self, lib_path: Optional[str] = None):
        if lib_path is None:
            # Default to the built library in tools/omsim
            base = Path(__file__).parent.parent / "tools" / "omsim"
            # Try .so first (Linux), then .dylib (macOS)
            for ext in ['libverify.so', 'libverify.dylib']:
                candidate = base / ext
                if candidate.exists():
                    lib_path = str(candidate)
                    break
            if lib_path is None:
                lib_path = str(base / "libverify.so")

        self._lib = ctypes.CDLL(lib_path)
        self._setup_functions()

    def _setup_functions(self):
        lib = self._lib

        # verifier_create
        lib.verifier_create.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib.verifier_create.restype = ctypes.c_void_p

        # verifier_create_from_bytes
        lib.verifier_create_from_bytes.argtypes = [
            ctypes.c_char_p, ctypes.c_int,
            ctypes.c_char_p, ctypes.c_int
        ]
        lib.verifier_create_from_bytes.restype = ctypes.c_void_p

        # verifier_destroy
        lib.verifier_destroy.argtypes = [ctypes.c_void_p]
        lib.verifier_destroy.restype = None

        # verifier_error
        lib.verifier_error.argtypes = [ctypes.c_void_p]
        lib.verifier_error.restype = ctypes.c_char_p

        # verifier_error_clear
        lib.verifier_error_clear.argtypes = [ctypes.c_void_p]
        lib.verifier_error_clear.restype = None

        # verifier_evaluate_metric
        lib.verifier_evaluate_metric.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.verifier_evaluate_metric.restype = ctypes.c_int

        # verifier_evaluate_approximate_metric
        lib.verifier_evaluate_approximate_metric.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.verifier_evaluate_approximate_metric.restype = ctypes.c_double

        # verifier_set_cycle_limit
        lib.verifier_set_cycle_limit.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.verifier_set_cycle_limit.restype = None

        # verifier_disable_limits
        lib.verifier_disable_limits.argtypes = [ctypes.c_void_p]
        lib.verifier_disable_limits.restype = None

    def verify_files(self, puzzle_path: str, solution_path: str,
                     cycle_limit: int = 150000) -> VerifyResult:
        """Verify a solution from file paths."""
        v = self._lib.verifier_create(
            puzzle_path.encode('utf-8'),
            solution_path.encode('utf-8')
        )
        if not v:
            return VerifyResult(valid=False, error="Failed to create verifier")

        try:
            err = self._lib.verifier_error(v)
            if err:
                return VerifyResult(valid=False, error=err.decode('utf-8'))

            if cycle_limit > 0:
                self._lib.verifier_set_cycle_limit(v, cycle_limit)

            return self._evaluate(v)
        finally:
            self._lib.verifier_destroy(v)

    def verify_bytes(self, puzzle_bytes: bytes, solution_bytes: bytes,
                     cycle_limit: int = 150000) -> VerifyResult:
        """Verify a solution from raw bytes."""
        v = self._lib.verifier_create_from_bytes(
            puzzle_bytes, len(puzzle_bytes),
            solution_bytes, len(solution_bytes)
        )
        if not v:
            return VerifyResult(valid=False, error="Failed to create verifier")

        try:
            err = self._lib.verifier_error(v)
            if err:
                return VerifyResult(valid=False, error=err.decode('utf-8'))

            if cycle_limit > 0:
                self._lib.verifier_set_cycle_limit(v, cycle_limit)

            return self._evaluate(v)
        finally:
            self._lib.verifier_destroy(v)

    def _evaluate(self, v) -> VerifyResult:
        """Evaluate all metrics on a verifier."""
        result = VerifyResult(valid=True)

        # Cost (doesn't need simulation)
        result.cost = self._lib.verifier_evaluate_metric(v, b"cost")
        err = self._lib.verifier_error(v)
        if err:
            return VerifyResult(valid=False, error=err.decode('utf-8'))

        # Instructions
        result.instructions = self._lib.verifier_evaluate_metric(v, b"instructions")
        err = self._lib.verifier_error(v)
        if err:
            self._lib.verifier_error_clear(v)

        # Cycles (runs simulation)
        result.cycles = self._lib.verifier_evaluate_metric(v, b"cycles")
        err = self._lib.verifier_error(v)
        if err:
            return VerifyResult(valid=False, error=err.decode('utf-8'))

        # Area
        result.area = self._lib.verifier_evaluate_metric(v, b"area")
        err = self._lib.verifier_error(v)
        if err:
            self._lib.verifier_error_clear(v)

        return result

    def evaluate_metric(self, puzzle_path: str, solution_path: str,
                       metric: str) -> int:
        """Evaluate a single metric."""
        v = self._lib.verifier_create(
            puzzle_path.encode('utf-8'),
            solution_path.encode('utf-8')
        )
        if not v:
            return -1
        try:
            val = self._lib.verifier_evaluate_metric(v, metric.encode('utf-8'))
            return val
        finally:
            self._lib.verifier_destroy(v)
