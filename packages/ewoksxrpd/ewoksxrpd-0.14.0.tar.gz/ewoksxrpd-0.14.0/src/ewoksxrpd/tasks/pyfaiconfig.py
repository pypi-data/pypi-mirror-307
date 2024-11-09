import logging
from pyFAI import method_registry
from ewokscore import Task

from .utils import pyfai_utils, xrpd_utils

__all__ = ["PyFaiConfig"]

logger = logging.getLogger(__name__)


class PyFaiConfig(
    Task,
    optional_input_names=[
        "filename",
        "filenames",
        "energy",
        "geometry",
        "mask",
        "flatfield",
        "darkcurrent",
        "darkflatmethod",
        "detector",
        "detector_config",
        "calibrant",
        "integration_options",
    ],
    output_names=[
        "energy",
        "geometry",
        "detector",
        "detector_config",
        "calibrant",
        "mask",
        "flatfield",
        "darkcurrent",
        "integration_options",
    ],
):
    """Parse pyFAI calibration and integration parameters"""

    def run(self):
        input_values = self.input_values
        integration_options = self.merged_integration_options()

        if "poni" in integration_options and integration_options.get("version", 0) > 3:
            integration_options.update(integration_options.pop("poni"))

        wavelength = integration_options.pop("wavelength", None)
        energy = input_values.get("energy", None) or integration_options.pop(
            "energy", None
        )
        if energy is None:
            if wavelength is not None:
                energy = xrpd_utils.energy_wavelength(wavelength)

        detector = integration_options.pop("detector", None)
        if not self.missing_inputs.detector:
            detector = input_values["detector"]

        detector_config = integration_options.pop("detector_config", None)
        if not self.missing_inputs.detector_config:
            detector_config = input_values["detector_config"]

        calibrant = input_values.get("calibrant", None)

        mask = input_values.get("mask", None)
        flatfield = input_values.get("flatfield", None)
        darkcurrent = input_values.get("darkcurrent", None)
        if not self.missing_inputs.darkflatmethod:
            integration_options["darkflatmethod"] = self.inputs.darkflatmethod

        geometry = {
            k: integration_options.pop(k)
            for k in ["dist", "poni1", "poni2", "rot1", "rot2", "rot3"]
            if k in integration_options
        }
        if not self.missing_inputs.geometry:
            geometry = input_values["geometry"]

        do_poisson = integration_options.pop("do_poisson", None)
        do_azimuthal_error = integration_options.pop("do_azimuthal_error", None)
        error_model = integration_options.pop("error_model", None)
        if not error_model:
            if do_poisson:
                error_model = "poisson"
            if do_azimuthal_error:
                error_model = "azimuthal"
        if error_model:
            integration_options["error_model"] = error_model

        # Check method and integrator function
        method = integration_options.get("method", "")
        if not isinstance(method, str):
            method = "_".join(method)
        pmethod = method_registry.Method.parsed(method)

        integrator_name = integration_options.get("integrator_name", "")
        if integrator_name in ("sigma_clip", "_sigma_clip_legacy"):
            logger.warning(
                "'%s' is not compatible with the pyfai worker: use 'sigma_clip_ng'",
                integrator_name,
            )
            integration_options["integrator_name"] = "sigma_clip_ng"
        if "sigma_clip_ng" == integrator_name and pmethod.split != "no":
            raise ValueError(
                "to combine sigma clipping with pixel splitting, use 'sigma_clip_legacy'"
            )

        # Split integration and worker options
        self.outputs.energy = energy
        self.outputs.geometry = geometry
        self.outputs.detector = detector
        self.outputs.detector_config = detector_config
        self.outputs.calibrant = calibrant
        self.outputs.mask = mask
        self.outputs.flatfield = flatfield
        self.outputs.darkcurrent = darkcurrent
        self.outputs.integration_options = integration_options

    def merged_integration_options(self) -> dict:
        """Merge integration options in this order of priority:

        - filename (lowest priority)
        - filenames[0]
        - filenames[1]
        - ...
        - integration_options (highest priority)
        """
        integration_options = dict()
        filenames = list()
        if self.inputs.filename:
            filenames.append(self.inputs.filename)
        if self.inputs.filenames:
            filenames.extend(self.inputs.filenames)
        for filename in filenames:
            integration_options.update(pyfai_utils.read_config(filename))
        if self.inputs.integration_options:
            integration_options.update(
                pyfai_utils.normalize_parameters(self.inputs.integration_options)
            )
        return integration_options
