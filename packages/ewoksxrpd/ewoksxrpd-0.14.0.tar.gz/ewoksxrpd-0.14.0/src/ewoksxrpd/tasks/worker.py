import logging
from contextlib import contextmanager
from collections import OrderedDict
from typing import Iterable, Dict, Mapping, Tuple

import pyFAI
import pyFAI.worker
from pyFAI.average import average_images
from ewokscore.hashing import uhash

from .utils import pyfai_utils

_WORKER_POOL = None


logger = logging.getLogger(__name__)


class WorkerPool:
    """Pool with one worker per configuration up to a maximum number of workers."""

    def __init__(self, nworkers: int = 1) -> None:
        self._workers: Dict[int, pyFAI.worker.Worker] = OrderedDict()
        self.nworkers = nworkers

    @staticmethod
    def _worker_id(*args):
        return uhash(args)

    @property
    def nworkers(self):
        return self._nworkers

    @nworkers.setter
    def nworkers(self, value: int):
        self._nworkers = value
        self._check_pool_size()

    def _check_pool_size(self):
        while self._workers and len(self._workers) > self.nworkers:
            self._workers.popitem(last=False)

    @contextmanager
    def worker(
        self, options: Mapping, demo: bool = False
    ) -> Iterable[pyFAI.worker.Worker]:
        # TODO: deal with threads and subprocesses
        worker_options, integration_options = self._split_options(options)
        logger.info("Pyfai worker options: %s", worker_options)
        logger.info("Pyfai integration options: %s", integration_options)
        worker_id = self._worker_id(worker_options, integration_options, demo)
        worker = self._workers.pop(worker_id, None)
        if worker is None:
            logger.info("Creating a new pyfai worker")
            worker = self._create_worker(worker_options, integration_options, demo)
        self._workers[worker_id] = worker
        self._check_pool_size()
        logger.info("Pyfai integration method: %s", worker._method)
        yield worker

    def _split_options(self, options: Mapping) -> Tuple[dict, dict]:
        integration_options = dict(options)
        worker_keys = "integrator_name", "extra_options", "dummy"
        worker_options = {
            k: integration_options.pop(k)
            for k in worker_keys
            if k in integration_options
        }
        nbpt_rad = integration_options.get("nbpt_rad", None)
        if nbpt_rad:
            nbpt_azim = integration_options.get("nbpt_azim", 1)
            worker_options.setdefault("shapeOut", (nbpt_azim, nbpt_rad))
        unit = integration_options.get("unit")
        if unit:
            worker_options["unit"] = unit
        worker_options.setdefault("dummy", float("nan"))
        return worker_options, integration_options

    @staticmethod
    def _create_worker(
        worker_options: Mapping, integration_options: Mapping, demo: bool
    ) -> pyFAI.worker.Worker:
        if demo:
            return DemoWorker(integration_options, worker_options)
        return EwoksWorker(integration_options, worker_options)


def _get_global_pool() -> WorkerPool:
    global _WORKER_POOL
    if _WORKER_POOL is None:
        _WORKER_POOL = WorkerPool()
    return _WORKER_POOL


def set_maximum_persistent_workers(nworkers: int) -> None:
    pool = _get_global_pool()
    pool.nworkers = nworkers


class EwoksWorker(pyFAI.worker.Worker):
    def __init__(self, integration_options: Mapping, worker_options: Mapping) -> None:
        super().__init__(**worker_options)
        self.output = "raw"
        self._i = 0

        integration_options = dict(integration_options)

        mask = pyfai_utils.extract_mask(integration_options)
        flatfield = pyfai_utils.extract_flatfield(integration_options)
        darkcurrent = pyfai_utils.extract_darkcurrent(integration_options)
        darkflatmethod = integration_options.pop("darkflatmethod", None)

        # Flat field correction:
        #   - default: Icor = (I - dark) / flat
        #   - counts:  Icor = (I - dark) / max(flat - dark, 1)
        if darkflatmethod is not None:
            if integration_options["flat_field"] and integration_options["do_flat"]:
                flatfield = average_images(
                    integration_options["flat_field"],
                    filter_="mean",
                    fformat=None,
                    threshold=0,
                )
                integration_options["flat_field"] = None
                integration_options["do_flat"] = False
            if integration_options["dark_current"] and integration_options["do_dark"]:
                darkcurrent = average_images(
                    integration_options["dark_current"],
                    filter_="mean",
                    fformat=None,
                    threshold=0,
                )
                integration_options["dark_current"] = None
                integration_options["do_dark"] = False
            if darkflatmethod == "counts":
                if flatfield is not None:
                    if darkcurrent is not None:
                        flatfield = flatfield - darkcurrent
                    flatfield[flatfield < 1] = 1

        provided = set(integration_options)
        self.set_config(integration_options, consume_keys=True)
        unused = {k: v for k, v in integration_options.items() if k in provided}
        if unused:
            logger.warning("Unused pyfai integration options: %s", unused)

        # Flat/dark correction:
        #   Icor = (I - darkcurrent) / flatfield
        if mask is not None:
            self.ai.detector.set_mask(mask)
        if flatfield is not None:
            self.ai.detector.set_flatfield(flatfield)
        if darkcurrent is not None:
            self.ai.detector.set_darkcurrent(darkcurrent)


class DemoWorker(EwoksWorker):
    def process(self, data, *args, **kwargs):
        return super().process(data[:-1, :-1], *args, **kwargs)


@contextmanager
def persistent_worker(
    integration_options: Mapping, demo: bool = False
) -> Iterable[pyFAI.worker.Worker]:
    """Get a worker for a particular configuration that stays in memory."""
    pool = _get_global_pool()
    with pool.worker(integration_options, demo) as worker:
        yield worker
