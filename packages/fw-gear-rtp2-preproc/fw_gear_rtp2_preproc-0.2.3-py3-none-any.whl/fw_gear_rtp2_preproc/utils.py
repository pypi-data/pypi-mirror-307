"""Shared utility functions."""

import logging
import os
import sys
import zipfile
import glob
import shutil

import nibabel as nb
import subprocess as sp
import pandas as pd

log = logging.getLogger(__name__)

join = os.path.join


def die(*args):
    """Log the given error message and exit with 1."""
    log.error(*args)
    sys.exit(1)


def create_zipinfo(out_dir: str, zip_fname: str) -> None:
    """Writes the zipinfo command into a text file.

    All zipped output files of the gear will have a sidecar text file with the
    zipinfo output information.

    Arguments:
        out_dir (str): output folder that gets uploaded in Flywheel.
        zip_fname (str): path and name to the zipfile.
    """
    log.info("Extracting zipinfo for file %s", zip_fname)
    columns = [
        "FileName",
        "FileSize",
        "CompressSize",
        "DateTime",
        "IsEncrypted",
        "CompressionType",
    ]
    df = pd.DataFrame(columns=columns)
    # Open the zip file
    with zipfile.ZipFile(zip_fname, "r") as zip_ref:
        # Get a list of all archived file names from the zip
        all_files_info = zip_ref.infolist()

        # Iterate over the file information
        for file_info in all_files_info:
            # Create line for the data frame per each file or folder
            tmp = pd.DataFrame(columns=columns)
            # Populate the line
            tmp.loc[0, "FileName"] = file_info.filename
            tmp.loc[0, "FileSize"] = file_info.file_size
            tmp.loc[0, "CompressSize"] = file_info.compress_size
            tmp.loc[0, "DateTime"] = file_info.date_time
            tmp.loc[0, "IsEncrypted"] = "Yes" if file_info.flag_bits & 0x1 else "No"
            tmp.loc[0, "CompressionType"] = file_info.compress_type
            # Concatenate to the main dataframe
            df = pd.concat([df, tmp], ignore_index=True)

    df.to_csv(
        os.path.join(out_dir, os.path.basename(zip_fname).replace("zip", "csv")),
        index=False,
    )


def check_archive_for_bad_filename(file: str) -> bool:
    """Checks if a zip file contains bad filenames.

    Specifically, we check for OS files from MacOS.

    Arguments:
        file (str): name of the zip file to check.

    Returns:
        bool: True if bad filenames are encountered
    """

    with zipfile.ZipFile(file, "r") as zip_file:
        for filename in zip_file.namelist():
            if filename.startswith("__MACOSX/"):
                return True


def remove_bad_filename_from_archive(original_file: str, temporary_file: str) -> None:
    """Remove MacOS-specific auto-generated metadata files from the given ZIP.

    Specifically, we are removing '__MACOSX' and 'DS_Store' files and folders, created
    by MacOS,

    Arguments:
        original_file (str): file path to the original zip file
        temporary_file (str): file path to the cleaned zip file
    """

    with zipfile.ZipFile(original_file, "r") as zip_file:
        for item in zip_file.namelist():
            if not (item.startswith("__MACOSX/") or item.endswith("DS_Store")):
                if item.endswith("nii.gz") or item.endswith("nii"):
                    buffer = zip_file.read(item)
                    if not os.path.exists(temporary_file):
                        with zipfile.ZipFile(temporary_file, "w") as new_zip:
                            new_zip.writestr(item, buffer)
                    else:
                        with zipfile.ZipFile(temporary_file, "a") as append_zip:
                            append_zip.writestr(item, buffer)


def get_valid_qmap_list(data_dir: str, qmap_file: str) -> list:
    """Ensure that the qmap input is valid and extract it if so.

    We only accept a zip file with nifti files, or a single nifti file or a single
    zipped nifti file. This function will check that the input is correct.

    Arguments:
        data_dir (str): path to data directory
        qmap_file (str): file path to the qmap file(s)

    Returns:
        list: list of the validated qmap files.
    """

    qmap_dir = join(data_dir, "qmap")
    os.makedirs(qmap_dir, exist_ok=True)

    # Check if it has valid extension
    valid_extensions = [".zip", ".gz", ".nii"]
    file_extension = os.path.splitext(qmap_file)[1]
    if file_extension in valid_extensions:
        log.info("qmap is a file with extension '%s'", file_extension)
    else:
        log.info("qmap is a file with a non valid extension '%s'.", file_extension)
        log.info("Valid options are %s", valid_extensions)
        return []

    # Check if it is a valid zip file
    if file_extension == ".zip":
        if not zipfile.is_zipfile(qmap_file):
            log.info(
                "%s exists but it is not a valid zipfile. "
                "The QMAPs will NOT be converted.",
                qmap_file,
            )
            return []
        # We have a valid zipfile
        log.info(
            "%s exists and it is a zipfile. "
            "The QMAPs will be coregistered and resliced to the T1w image.",
            qmap_file,
        )
        # Check if it has macosx compress files
        mac_result = check_archive_for_bad_filename(qmap_file)
        if mac_result:
            log.info("Removing MACOSX file from archive.")
            temp_filename = join(data_dir, "nomacosx.zip")
            remove_bad_filename_from_archive(qmap_file, temp_filename)
            qmap_file = temp_filename
        log.info(
            "Unzipping qmap zip file and removing all folder information, just files."
        )
        with zipfile.ZipFile(qmap_file) as zip_ref:
            for member in zip_ref.namelist():
                filename = os.path.basename(member)
                # skip directories
                if not filename:
                    continue
                # copy file (taken from zipfile's extract)
                source = zip_ref.open(member)
                target = open(join(qmap_dir, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
                # Check if this is a nifti file, otherwise remove
                if "nifti" not in str(type(nb.load(join(qmap_dir, filename)))):
                    log.info(
                        "'%s' exists but it is not a valid nifti file. "
                        "This qmap will not be coregistered.",
                        filename,
                    )
                    os.remove(join(qmap_dir, filename))
                    continue
                # If a nii is passed, compress it
                if file_extension == ".nii":
                    cmd = (
                        f"mrconvert {join(qmap_dir, filename)} "
                        f"{join(qmap_dir, filename +'.gz')}"
                    )
                    log.info("Compressing file with command:\n%s", cmd)
                    sp.run(cmd, shell=True)
                    os.remove(join(qmap_dir, filename))
        if mac_result:
            os.remove(temp_filename)
        # Check if there is at least one valid nifti in qmap_dir
        if len(glob.glob(join(qmap_dir, "*.nii.gz"))) == 0:
            log.info("After the checks, not valid maps where passed on the zip")
            return []

    if file_extension in (".gz", ".nii"):
        if "nifti" not in str(type(nb.load(qmap_file))):
            log.info(
                "%s exists but it is not a valid nifti file. "
                "The QMAPs will NOT be converted.",
                qmap_file,
            )
            return []

        log.info(
            "%s exists and it will be checked and copied to the right location.",
            qmap_file,
        )

        if file_extension == ".gz":
            shutil.copy(qmap_file, join(qmap_dir, os.path.basename(qmap_file)))

        if file_extension == ".nii":
            cmd = (
                f"mrconvert {qmap_file} "
                f"{join(qmap_dir, os.path.basename(qmap_file)+'.gz')}"
            )
            log.info("Compressing file with command:\n%s", cmd)
            sp.run(cmd, shell=True)
    return glob.glob(join(qmap_dir, "*.nii.gz"))
