import logging
import os
import re
import shutil
import sys
from pathlib import Path

import nibabel

from nnunet.inference.pretrained_models.download_pretrained_model import (
    install_model_from_zip_file,
)

log = logging.getLogger(__name__)


def prepare_and_check_inputs(
    modality_inputs, work_folder, prepared_input_folder, pretrained_model
):
    """
    Args:
        modality_inputs (Dict[str, Optional[str]]): Dictionary containing path
            for input files.
        work_folder (str): Work directory.
        prepared_input_folder (str): Folder for prepared inputs to feed to
            model.
        pretrained_model (str): Name of pretrained model to use for inference.
    """
    # Split the input if there is a single 4d input provided.
    modality_inputs = split_input_as_needed(
        modality_inputs=modality_inputs, work_folder=work_folder
    )

    # Check that the modality_inputs is a dict, as expected.
    if not isinstance(modality_inputs, dict):
        log.error(
            "Modality_inputs %s is not a dict, but %s, check for previous error messages.",
            modality_inputs,
            type(modality_inputs),
        )
        sys.exit(1)

    # Check that number of returned modalities is as expected.
    expected_number_of_modality_inputs = (
        get_available_models()
        .get(pretrained_model, {})
        .get("number_of_modalities", "'Not found'")
    )
    if len(modality_inputs) != expected_number_of_modality_inputs:
        log.error(
            "len(modality_inputs) %s not equal to expected_number_of_modality_inputs %s",
            len(modality_inputs),
            expected_number_of_modality_inputs,
        )
        sys.exit(1)

    # Move inputs to prepared_input_folder.
    if not os.path.exists(prepared_input_folder):
        os.mkdir(prepared_input_folder)
    for input_path in modality_inputs.values():
        if input_path != Path(prepared_input_folder) / Path(input_path).name:
            shutil.move(input_path, prepared_input_folder)


def process_file_name(
    input_path,
    work_folder=Path("/flywheel/v0/work"),
    modality_number=None,
    stem_0=None,
):
    """
    If needed, and it's a 3-D single/multiple inputs, prepare to comply with
    .*_000[0-9].nii.gz requirement.
    Args:
        input_path (str): Initial path to an input file.
        work_folder (str): Work directory.
        modality_number (int): Modality number, corresponding to the volume
            number / specified by the input name (e.g., "modality_0",
            "modality_1", etc.). See stem_0 def below.
        stem_0 (str): File name stem of modality_0 input (or None if it has
            not been found yet). Actual inputs to the model should be of the
            form {stem_0}_000{modality_number}.nii.gz, and all (1 or multiple)
            located in the same folder, {work_folder}/prepared_input.
    Returns
        new_input_link (str): Symlink to input, if created.
        stem_0 (str): Newly found or existing stem of modality_0 input.
    """

    matcher = re.compile("^.*_000[0-9].nii.gz")
    if matcher.match(input_path):
        return None, None

    log.info(
        "Input file path %s does not comply with .*_dddd.nii.gz format, addressing.",
        input_path,
    )

    split = os.path.basename(input_path).split(".nii.gz")

    check_filename_split(split, input_path)

    # Add the suffix expected by the model and save in links folder.
    if not stem_0:
        if modality_number != 0:
            log.error(
                "modality_number %s !=0. stem_0 should be already set but is not.",
                modality_number,
            )
            sys.exit(1)
        stem_0 = split[0]

    new_input_link = (
        work_folder / "prepared_input" / f"{stem_0}_000{modality_number}.nii.gz"
    )
    log.info("Renaming file %s to %s.", input_path, new_input_link)
    if not os.path.exists(work_folder / "prepared_input"):
        os.mkdir(work_folder / "prepared_input")
    if not os.path.exists(new_input_link):
        os.symlink(input_path, new_input_link)
        # shutil.copy(input_path, new_input_link)

    return new_input_link, stem_0


def correct_input_if_needed(modality_inputs, modality_number, work_folder, stem_0):
    """
    Args:
        modality_inputs (dict): File path for each modality input.
        modality_number (int): Modality number, corresponding to the volume
            number / specified by the input name (e.g., "modality_0",
            "modality_1", etc.). See stem_0 def below.
        work_folder (str): Work directory.
        stem_0 (str): File name stem of modality_0 input (or None if it has
            not been found yet). Actual inputs to the model should be of the
            form {stem_0}_000{modality_number}.nii.gz, and all (1 or multiple)
            located in the same folder, {work_folder}/prepared_input.
    Returns:
    """

    input_path = modality_inputs[f"modality_{modality_number}"]
    new_input_link, stem_0 = process_file_name(
        input_path=input_path,
        work_folder=work_folder,
        modality_number=modality_number,
        stem_0=stem_0,
    )
    if new_input_link:
        input_path = new_input_link
        # Update modality_inputs
        modality_inputs[f"modality_{modality_number}"] = input_path

    return modality_inputs, stem_0


def split_input_as_needed(modality_inputs, work_folder):
    """
    Args:
        modality_inputs (dict): File path for each modality input.
        work_folder (str): Work directory.
    Returns
        modality_inputs (dict): Possibly updated modality_inputs
    """
    # Only one input.
    if len(modality_inputs) == 1:
        modality_number = 0
        input_path = modality_inputs[f"modality_{modality_number}"]

        # Load NIfTI image.
        loaded_image = nibabel.load(input_path)

        # If it's 3-D:
        if len(loaded_image.shape) == 3:
            # Correct input filename if needed.
            modality_inputs, stem_0 = correct_input_if_needed(
                modality_inputs, modality_number, work_folder, stem_0=None
            )

        # If it's 4-D, split it (into assumed different modalities).
        elif len(loaded_image.shape) == 4:
            # Stuff for splits' save filepaths.
            parent_folder = Path(input_path).parent.parent
            filename_stem = Path(input_path).name.split(".nii.gz")[0]

            # Iterate over and split off volumes:
            for modality_number in range(loaded_image.shape[3]):
                # Make new modality folder
                if not (os.path.exists(parent_folder / f"modality_{modality_number}")):
                    os.mkdir(parent_folder / f"modality_{modality_number}")

                # Save 3-D volumes, update modality_inputs
                # Note no need for correct_input_if_needed() since we decide names.
                out_file = (
                    parent_folder
                    / f"modality_{modality_number}"
                    / f"{filename_stem}_000{modality_number}.nii.gz"
                )
                loaded_image.slicer[:, :, :, modality_number].to_filename(out_file)
                modality_inputs[f"modality_{modality_number}"] = out_file

        # If it's neither 3-D nor 4-D, error:
        else:
            if len(loaded_image.shape) != 4:
                log.error(
                    "Dimension of input image %s is %i, rather than 3 or 4.",
                    input_path,
                    len(loaded_image.shape),
                )
                sys.exit(1)

    # Multiple inputs.
    elif len(modality_inputs) > 1:
        # Check that they're all be 3-D volumes and names have required format
        stem_0 = None
        for modality_number in range(len(modality_inputs)):
            input_path = modality_inputs[f"modality_{modality_number}"]

            # Check that image is 3-D.
            image_n_dimensions = len(nibabel.load(input_path).shape)

            # If it's not 3-D:
            if image_n_dimensions != 3:
                log.error(
                    "Dimension of input image %s is %i, rather than 3.",
                    input_path,
                    image_n_dimensions,
                )
                sys.exit(1)

            # Correct input filename if needed. Note that the filename stem
            # of input for "modality_0" will be used as the stem beginning for
            # all inputs, with only the final character (modality number)
            # varying between them. E.g., the result for
            # - modality_0: prostate_04.nii.gz
            # - modality_1: prostate_abc.nii.gz
            # would be
            # - prostate_04_0000.nii.gz
            # - prostate_04_0001.nii.gz
            modality_inputs, stem_0 = correct_input_if_needed(
                modality_inputs, modality_number, work_folder, stem_0=stem_0
            )

    # Else, error.
    else:
        log.error(
            "Length of modality inputs should be >= 1; instead getting value of %i.",
            len(modality_inputs),
        )

    return modality_inputs


def check_filename_split(split, input_path):
    """
    Some quick checks on the input filepath, split by expected extension.

    Args:
        split (list[str]):  os.path.basename(input_path).split(".nii.gz")
        input_path (str): Path to input file.
    """
    # Some checks.
    if len(split) != 2:
        log.error(
            "Input file's length when p.split('.nii.gz') is %s, " + "rather than 2.",
            len(split),
        )
        sys.exit(1)
    expected_blank = split[1]
    if expected_blank != "":
        log.error(
            "For input file %s, suffix from p.split('.nii.gz')[1] !="
            + "'', instead it is %s.",
            input_path,
            expected_blank,
        )
        sys.exit(1)


def download_model(model_name, work_folder="."):
    """
    Download the pre-trained nnU-Net model to be used for inference.
    Args
        model_name (str): One of the following model names, to be
            downloaded from Zenodo:
                - 'Task001_BrainTumour'
                - 'Task002_Heart'
                - 'Task003_Liver'
                - 'Task004_Hippocampus'
                - 'Task005_Prostate'
                - 'Task006_Lung'
                - 'Task007_Pancreas'
                - 'Task008_HepaticVessel'
                - 'Task009_Spleen'
                - 'Task010_Colon'
        work_folder (str): Work directory.
    Returns
        model_url (str): url from which model was downloaded. Using cURL in
            a subprocess command call for download because requests package
            approach failed (likely due to redirects).
    """

    # download zipped pretrained model from stored url
    model_url = get_available_models()[model_name]["url"]
    output_zipname = f"{work_folder}/models/zips/{model_name}.zip"
    import urllib.request

    try:
        urllib.request.urlretrieve(model_url, output_zipname)
    except Exception as e:
        log.error("Error downloading model from url %s", model_url)
        log.error(e)
        sys.exit(1)

    # install from zip into RESULTS_FOLDER
    install_model_from_zip_file(f"{work_folder}/models/zips/{model_name}.zip")

    return model_url


# ----------------[ Functionality taken from nnUNet repo ]---------------------
#                   (https://github.com/MIC-DKFZ/nnUNet)


def get_available_models():
    """
    Taken from https://github.com/MIC-DKFZ/nnUNet/blob/4f2ffabe751977ee66348560c8e99102e8553195/nnunet/inference/pretrained_models/download_pretrained_model.py#L26-L236,
    2024-10-03 and adjusted as appropriate for current application. Added
    {number_of_modalities} info derived from
    https://www.nature.com/articles/s41467-022-30695-9/tables/2.

    Returns:
        available_models (dict): Below dictionary of info on pretrained models.
    """
    available_models = {
        "Task001_BrainTumour": {
            "description": "Brain Tumor Segmentation. \n"
            "Segmentation targets are edema, enhancing tumor and necrosis, \n"
            "Input modalities are 0: FLAIR, 1: T1, 2: T1 with contrast agent, 3: T2. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task001_BrainTumour.zip?download=1",
            "number_of_modalities": 4,
        },
        "Task002_Heart": {
            "description": "Left Atrium Segmentation. \n"
            "Segmentation target is the left atrium, \n"
            "Input modalities are 0: MRI. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task002_Heart.zip?download=1",
            "number_of_modalities": 1,
        },
        "Task003_Liver": {
            "description": "Liver and Liver Tumor Segmentation. \n"
            "Segmentation targets are liver and tumors, \n"
            "Input modalities are 0: abdominal CT scan. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task003_Liver.zip?download=1",
            "number_of_modalities": 1,
        },
        "Task004_Hippocampus": {
            "description": "Hippocampus Segmentation. \n"
            "Segmentation targets posterior and anterior parts of the hippocampus, \n"
            "Input modalities are 0: MRI. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task004_Hippocampus.zip?download=1",
            "number_of_modalities": 1,
        },
        "Task005_Prostate": {
            "description": "Prostate Segmentation. \n"
            "Segmentation targets are peripheral and central zone, \n"
            "Input modalities are 0: T2, 1: ADC. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task005_Prostate.zip?download=1",
            "number_of_modalities": 2,
        },
        "Task006_Lung": {
            "description": "Lung Nodule Segmentation. \n"
            "Segmentation target are lung nodules, \n"
            "Input modalities are 0: abdominal CT scan. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task006_Lung.zip?download=1",
            "number_of_modalities": 1,
        },
        "Task007_Pancreas": {
            "description": "Pancreas Segmentation. \n"
            "Segmentation targets are pancras and pancreas tumor, \n"
            "Input modalities are 0: abdominal CT scan. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task007_Pancreas.zip?download=1",
            "number_of_modalities": 1,
        },
        "Task008_HepaticVessel": {
            "description": "Hepatic Vessel Segmentation. \n"
            "Segmentation targets are hepatic vesels and liver tumors, \n"
            "Input modalities are 0: abdominal CT scan. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task008_HepaticVessel.zip?download=1",
            "number_of_modalities": 1,
        },
        "Task009_Spleen": {
            "description": "Spleen Segmentation. \n"
            "Segmentation target is the spleen, \n"
            "Input modalities are 0: abdominal CT scan. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task009_Spleen.zip?download=1",
            "number_of_modalities": 1,
        },
        "Task010_Colon": {
            "description": "Colon Cancer Segmentation. \n"
            "Segmentation target are colon caner primaries, \n"
            "Input modalities are 0: CT scan. \n"
            "Also see Medical Segmentation Decathlon, http://medicaldecathlon.com/",
            "url": "https://zenodo.org/records/4485926/files/Task010_Colon.zip?download=1",
            "number_of_modalities": 1,
        },
    }
    return available_models
