"""Parser module to parse gear config.json."""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from flywheel_gear_toolkit import GearToolkitContext

log = logging.getLogger(__name__)


# This function mainly parses gear_context's config.json file and returns
# relevant inputs and options.
def parse_config(
    context: GearToolkitContext, possible_modality_inputs: List[str]
) -> Tuple[str, Dict[str, Optional[Path]]]:
    """
    Parses gear context.
    Args:
        gear_context (GearToolkitContext): Flywheel gear context.
        possible_modality_inputs List(str): Possible modalities of intput file.

    Returns:
        pretrained_model (str): Name of model to be used for inference.
        modality_inputs (Dict[str, Optional[Path]]]): Modality input folder
            paths, entered by modality. E.g.,
            {
                "modality_0": "/flywheel/v0/input/modality_0/prostate_01_000.nii.gz",
                "modality_1": "/flywheel/v0/input/modality_1/prostate_01_001.nii.gz"
            }
    """

    # Get pretrained_model, and modality_inputs from gear context.
    # Some defaults are built-in using or's.
    pretrained_model = context.config.get("pretrained_model", "Task004_Hippocampus")

    modality_inputs = {}
    for modality in possible_modality_inputs:
        if context.get_input_path(modality):
            modality_inputs[modality] = context.get_input_path(modality)

    log.info("modality_inputs = %s", modality_inputs)

    return pretrained_model, modality_inputs
