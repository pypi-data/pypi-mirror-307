"""Main module."""

import glob
import logging
import shutil
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)


def run(
    pretrained_model: str,
    input_folder,
    output_folder: Path,
) -> int:
    """Runs specified model inference on inputs in specified folder, copies to
    output folder for upload into Analysis container.

    Args:
        pretrained_model (str): Name of model to run inference with.
        input_folder (str): Folder containing all inputs (or symlinks),
            hopefully in the ".*_000[0-9].nii.gz" format.
        output_folder (str): Output folder.

    Returns:
        int: 0 if successful, 1 if nnUNet_predict call errors.
    """

    # Main call, run inference by the model specified by -t and -m.
    command = [
        "nnUNet_predict",
        "-i",
        input_folder,
        "-o",
        output_folder,
        "-t",
        pretrained_model,
        "-m",
        "3d_fullres",
    ]
    try:
        subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        log.error(e)
        return 1

    # Move outputs to folder for engine to pick up and upload to instance
    # analysis output.
    for p in glob.glob(str(output_folder / "*.nii.gz")):
        # add the model name as a suffix to the file, to distinguish it
        # from the input:
        target = p.replace(".nii.gz", f"__{pretrained_model}.nii.gz")
        shutil.move(p, target)

        log.debug("p=%s", p)
        log.debug("target=%s", target)

    return 0
