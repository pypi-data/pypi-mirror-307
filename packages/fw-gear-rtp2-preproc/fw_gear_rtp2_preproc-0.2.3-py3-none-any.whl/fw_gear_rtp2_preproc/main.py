"""Main module."""

import glob
import logging
import os
import shutil as sh
import subprocess as sp
import zipfile

import fw_gear_rtp2_preproc.preprocs as pp
from fw_gear_rtp2_preproc.utils import create_zipinfo

log = logging.getLogger(__name__)

join = os.path.join


def create_eddy_options_string(gear_config: dict) -> str:
    """Create the option string for FSL's eddy.

    Based on the user selected config options, it generates a string that will be
    passed to FSL's eddy function call.

    Arguments:
        gear_config (dict): gear configuration options.

    Returns:
        str: properly form string with eddy options
    """

    eddy_options = " "  ## must contain at least 1 space according to mrtrix doc

    if gear_config["eddy_repol"]:
        eddy_options = f"{eddy_options} --repol"

    if gear_config["eddy_data_is_shelled"]:
        eddy_options = f"{eddy_options} --data_is_shelled"

    eddy_options = f"{eddy_options} --slm={gear_config['eddy_slm']}"
    eddy_options = f"{eddy_options} --niter={gear_config['eddy_niter']}"

    # Temporarily removed, check parser.py for explanations
    # if gear_config["eddy_mporder"] != 0:
    #    eddy_options = f"{eddy_options} --mporder={gear_config['eddy_mporder']}"

    log.info("eddy options string is: '%s'", eddy_options)

    return eddy_options


def create_topup_options_string(gear_config: dict) -> str:
    """Create the advanced options string for FSL's topup.

    Based on the user selected config options, it generates a string that will be
    passed to FSL's eddy function call with topup specific options.

    Arguments:
        gear_config (dict): gear configuration options.

    Returns:
        str: properly form string with topup options
    """

    default_topup_lambda = (
        "0.005,0.001,0.0001,0.000015,0.000005,"
        "0.0000005,0.00000005,0.0000000005,0.00000000001"
    )
    topup_lambda = gear_config["topup_lambda"]
    topup_options = " "

    if topup_lambda != default_topup_lambda:
        topup_options = f"-topup_options --lambda {topup_lambda}"

    log.info("topup options string is: '%s'", topup_options)

    return topup_options


def reverse_phase_encoding_operations(gear_inputs: dict, common: str) -> str:
    """Based on the inout data, obtain the reverse phase encoding parameter.

    FSL's eddy function, which is called by MRtrix's dwifslpreproc function, can take
    different configurations of files (with and without reverse phase encoded data,
    which can be from just few b0 files to a repetition of the whole acquisition).
    This functions evaluates the data and returns a code for the combination of input
    files that eddy can understand. Valid options:
    - none: no reverse phase encoding
    - all: all forward phase encodings will have a reverse counterpart
    - pairs: only some of the reverse phase encoding are passed

    Arguments:
        gear_inputs (dict): gear input files.
        common (str): common option for MRtrix function calls.

    Returns:
        str: code with the configuration of input files.
    """

    if not gear_inputs["RDIF"]:
        RPE = "none"
        log.info("RPE assigned as: '%s', no reverse phase encoding files", format(RPE))
        return RPE

    # convert reverse phase encoded data to mrtrix format
    cmd = (
        f"mrconvert -fslgrad {gear_inputs['RBVC']} {gear_inputs['RBVL']} "
        f"{gear_inputs['RDIF']} raw2.mif --export_grad_mrtrix raw2.b {common}"
    )
    log.info("Convert reverse phase encoding input with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    # determine the type of acquisition for dwipreproc eddy options
    # grab the number of volumes for each forward (F) and reversed (R) file.
    nb0F = sp.check_output(["mrinfo", "-size", "raw1.mif"]).decode().split()[-1]
    nb0R = sp.check_output(["mrinfo", "-size", "raw2.mif"]).decode().split()[-1]

    log.info("Forward phase encoded dwi volume has '%s' volumes.", format(nb0F))
    log.info("Reverse phase encoded dwi volume has '%s' volumes.", format(nb0R))

    # check the size of the inputs
    # if they match, it's "all"
    if nb0F == nb0R:
        RPE = "all"
        # just because the # of volumes match doesn't mean they're valid
        log.info("RPE assigned as: '%s'", format(RPE))
        return RPE

    # if they don't match, it's "pairs"
    RPE = "pairs"
    log.info("RPE assigned as: '%s'", format(RPE))

    # if the last dim is even
    if int(nb0R) % 2 == 0:
        # pass the file - no assurance it's valid volumes, just a valid number of them
        log.info("The RPE file has an even number of volumes. No change was made.")
        return RPE

    # drop any volumes w/ a sufficiently high bval to be a
    # direction - often makes an odd sequence even
    cmd = f"dwiextract -bzero raw2.mif raw2.mif {common}"
    log.info(
        "The RPE file has an odd number of volumes. "
        "Only the b0 volumes were extracted with:\n '%s'.",
        cmd,
    )
    sp.run(cmd, shell=True)
    ob0 = sp.check_output(["mrinfo", "-size", "raw2.mif"]).decode().split()[-1]
    log.info("This should be an even number: '%s'", format(ob0))
    # this doesn't stop or exit if it's still odd...
    return RPE


def identify_correct_gradient_orientation(
    out_dir: str, mask: str, difm: str, common: str, RPE: str
) -> None:
    """Prepare and run MRtrix's dwigradcheck for gradient checks.

    Prepares the data and performs gradients checks.

    Arguments:
        out_dir (str): output directory.
        mask (str): desired name of the masked brain file.
        difm (str): desired name for the new diffusion file.
        common (str): common option for MRtrix function calls.
        RPE (str): code with the configuration of input files.
    """

    log.info("Identifying correct gradient orientation...")

    if RPE == "all":
        # merge data
        cmd = f"mrcat raw1.mif raw2.mif raw.mif {common}"
        log.info("Merging dwi data with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

        cmd = "cat raw1.b raw2.b > raw.b"
        log.info("Merging .b data with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

        # create mask from merged data
        cmd = f"dwi2mask raw.mif {mask}.mif {common}"
        log.info("Creating processing mask with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

        # check and correct gradient orientation and create corrected image
        cmd = (
            f"dwigradcheck raw.mif -grad raw.b -mask {mask}.mif "
            f"-export_grad_mrtrix corr.b -scratch {join(out_dir,'tmp')} {common}"
        )
        log.info("Doing dwigradcheck with:\n '%s'", cmd)
        sp.call(cmd, shell=True)

        cmd = f"mrconvert raw.mif -grad corr.b {difm}.mif {common}"
        log.info("Creating new corrected file with:\n '%s'", cmd)
        sp.call(cmd, shell=True)

    else:
        log.info("Creating processing mask...")

        # create mask
        cmd = f"dwi2mask raw1.mif {mask}.mif {common}"
        log.info("Create mask with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

        # check and correct gradient orientation and create corrected image
        cmd = (
            f"dwigradcheck raw1.mif -grad raw1.b -mask {mask}.mif "
            f"-export_grad_mrtrix cor1.b -scratch {join(out_dir,'tmp')} {common}"
        )
        log.info(
            "Check and correct gradient orientation and create "
            "corrected image with:\n '%s'",
            cmd,
        )
        sp.call(cmd, shell=True)

        cmd = f"mrconvert raw1.mif -grad cor1.b {difm}.mif {common}"
        log.info("Creating new corrected file with:\n '%s'", cmd)
        sp.call(cmd, shell=True)

        if os.path.exists("raw2.mif"):
            cmd = f"dwi2mask raw2.mif rpe_{mask}.mif {common}"
            log.info("Creating mask with:\n '%s'", cmd)
            sp.call(cmd, shell=True)

            sh.copyfile("raw2.b", "cor2.b")

            cmd = f"mrconvert raw2.mif -grad cor2.b rpe_{difm}.mif {common}"
            log.info("Converting the rpe file with:\n '%s'", cmd)
            sp.call(cmd, shell=True)


def run(gear_inputs: dict, gear_config: dict) -> int:
    """Performs dwi data preprocessing, main function.

    It prepares the function calls and calls them depending on the config options.
    Cleans the working folder at the end.

    Arguments:
        gear_config (dict): gear configuration options.
        gear_inputs (dict): gear input files.

    Returns:
        int: 0 when finished successfully.
    """

    log.info("This is the beginning of the run file")

    # Create folder names
    out_dir = join(gear_inputs["output_dir"])

    ## assign output space of final data if anat align not called
    out = "proc"

    ## diffusion file that changes name based on steps performed
    difm = "dwi"
    mask = "b0_dwi_brain_mask"

    # create / remove old tmp folders / previous run files explicitly
    sh.rmtree(join(out_dir, "tmp"), ignore_errors=True)
    sh.rmtree(join(out_dir, "eddyqc"), ignore_errors=True)
    if os.path.isfile(join(out_dir, "cor1.b")):
        os.remove(join(out_dir, "cor1.b"))
    if os.path.isfile(join(out_dir, "cor2.b")):
        os.remove(join(out_dir, "cor2.b"))
    if os.path.isfile(join(out_dir, "corr.b")):
        os.remove(join(out_dir, "corr.b"))

    # create temp folders explicitly
    os.chdir(out_dir)
    os.mkdir(join(out_dir, "tmp"))

    # Start building command line
    common = "-quiet -force"

    # fill in arguments common to all dwifslpreproc calls
    common_fslpreproc = (
        f"-eddy_mask {mask}.mif -eddyqc_all "
        f"{join(out_dir,'eddyqc')} "
        f"-scratch {join(out_dir,'tmp')}"
    )

    # create the string for eddy based on configs
    eddy_options = create_eddy_options_string(gear_config)

    # create the string for topup based on configs
    topup_options = create_topup_options_string(gear_config)

    # Convert data to mrtrix format
    cmd = (
        f"mrconvert -fslgrad {gear_inputs['BVEC']} {gear_inputs['BVAL']} "
        f"{gear_inputs['DIFF']} raw1.mif --export_grad_mrtrix raw1.b {common}"
    )
    log.info("Convert input diffusion data into mrtrix format with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    # If the second input exists (reverse phase encoded or RPE) convert it as
    # well and do some operations
    RPE = reverse_phase_encoding_operations(gear_inputs, common)

    # Identify correct gradient orientation
    identify_correct_gradient_orientation(out_dir, mask, difm, common, RPE)

    # Do the preprocessing depending on options
    # pca-denoising is done either the option denoise or ricn is selected,
    # as pca_denoising  is required for ricn denoising.
    # Therefore it is possible to have:
    # (1) no denoising
    # (2) just pca_denoising
    # (3) pca anda rician denoisings
    if gear_config["denoise"] or gear_config["ricn"]:
        difm = pp.pca_denoising(difm, common, gear_config["denoise"])

    # if scanner ringing artifacts are found
    if gear_config["degibbs"]:
        difm = pp.do_degibbs(difm, common)

    # perform eddy correction with FSL for geometric susceptibility
    # distortion correction
    if gear_config["eddy"]:
        acqd = gear_config["acquisition_direction"]
        difm = pp.do_eddy(
            difm,
            mask,
            common,
            common_fslpreproc,
            RPE,
            eddy_options,
            topup_options,
            acqd,
        )

    if gear_config["bias"]:
        difm = pp.do_bias(
            difm,
            gear_config["bias_method"],
            out_dir,
            common,
            gear_config["antsb"],
            gear_config["antsc"],
            gear_config["antss"],
            mask,
        )

    # perform Rician background noise removal
    if gear_config["ricn"]:
        difm = pp.do_rician(difm, common)

    # perform intensity normalization of dwi data
    if gear_config["norm"]:
        difm = pp.do_norm(difm, mask, common, gear_config["nval"])

    # Creating dwi space b0 reference images
    pp.create_ref_images(difm, common, mask)

    # align diffusion data to T1 acpc anatomy
    if gear_config["anatalign"]:
        anat = gear_inputs["ANAT"]
        fsmask = gear_inputs["FSMASK"]
        difm = pp.do_anatalign(
            difm, common, anat, fsmask, gear_config["ants_dwi2anat_options"]
        )
        # assign output space label
        out = "anatalign"

    # if a QMAP_LIST was passed, align it/them with anatomy
    resliced_qmaps_list = []
    if gear_inputs["QMAP_LIST"]:
        for qmap in gear_inputs["QMAP_LIST"]:
            resliced_qmap = pp.do_qmap_coreg(
                qmap,
                common,
                gear_inputs["ANAT"],
                gear_inputs["FSMASK"],
                gear_config["ants_qmap2anat_options"],
                gear_config["anatalign"],
            )
            resliced_qmaps_list.append(resliced_qmap)

    if gear_config["doreslice"]:
        difm = pp.do_reslice(difm, common, gear_config["reslice"])
    else:
        # append voxel size in mm to the end of file, rename
        VAL = (
            sp.check_output(["mrinfo", "-spacing", "dwi.mif"])
            .decode()
            .split()[0]
            .replace(".", "p")[0:3]
        )
        log.info("Voxel size is '%s'", VAL)
        newname = f"{difm}_{VAL}mm"
        os.rename(f"{difm}.mif", f"{newname}.mif")

        difm = newname

    log.info("Creating '%s' space b0 reference images ...", out)
    cmd1 = (
        f"dwiextract {difm}.mif - -bzero {common} | "
        f"mrmath - mean b0_{out}.mif -axis 3 {common}"
    )
    cmd2 = f"dwi2mask {difm}.mif b0_{out}_brain_mask.mif {common}"
    log.info("Create final b0 / mask with:\n '%s' and\n'%s'", cmd1, cmd2)
    sp.run(cmd1, shell=True)
    sp.run(cmd2, shell=True)

    # create output space b0s
    cmd1 = f"mrconvert b0_{out}.mif -stride 1,2,3,4 b0_{out}.nii.gz {common}"
    cmd2 = f"mrconvert b0_{out}_brain_mask.mif -stride 1,2,3,4 b0_{out}_brain_mask.nii.gz {common}"
    cmd3 = f"fslmaths b0_{out}.nii.gz -mas b0_{out}_brain_mask.nii.gz b0_{out}_brain.nii.gz"
    log.info(
        "create output space b0s with:\n '%s' and\n'%s' and\n'%s'", cmd1, cmd2, cmd3
    )
    sp.run(cmd1, shell=True)
    sp.run(cmd2, shell=True)
    sp.run(cmd3, shell=True)

    log.info("Creating preprocessed dwi files in '%s' space...", out)
    # convert to nifti / fsl output for storage
    cmd = (
        f"mrconvert {difm}.mif -stride 1,2,3,4 dwi.nii.gz -export_grad_fsl "
        f"dwi.bvecs dwi.bvals -export_grad_mrtrix {difm}.b "
        f"-json_export {difm}.json {common}"
    )
    log.info("mrconvert with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    # Before cleanup, make sure regardless of gear_config["save_extra_output"],
    # we always save all from eddyqc because it is always useful information.
    # If the eddy_outlier file does not exist or is empty, do not copy (we
    # will delete them the empty ones at the end)

    # Cleanup
    log.info("Cleaning up working directory...")

    if not gear_config["save_extra_output"]:
        for f in glob.glob("*.mif"):
            os.remove(f)
        for f in glob.glob("*.b"):
            os.remove(f)
        for f in glob.glob("*fast*.nii.gz"):
            os.remove(f)
        for f in glob.glob("*init.mat"):
            os.remove(f)
        if os.path.isfile("dwi2anatalign.nii.gz"):
            os.remove("dwi2anatalign.nii.gz")

    for f in glob.glob("eddyqc/*"):
        sh.move(f, os.path.basename(f))

    # No matter what, delete the tmp and eddyqc folders if they exist
    if os.path.isdir(join(out_dir, "eddyqc")):
        sh.rmtree(join(out_dir, "eddyqc"))
    if os.path.isdir(join(out_dir, "tmp")):
        sh.rmtree(join(out_dir, "tmp"))

    log.info(
        "Checking if there are empty files in the output, and deleting them if it is the case"
    )
    for f in glob.glob(join(out_dir, "*")):
        if os.path.isfile(f) and os.path.getsize(f) == 0:
            log.info("'%s' is empty and will be deleted", f)
            os.remove(f)

    # Zip the coregistered and resliced qmap files
    if resliced_qmaps_list:
        with zipfile.ZipFile("qmaps_resliced.zip", "w") as zipMe:
            for file in resliced_qmaps_list:
                zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

    # Create a zipinfo.csv file per each zip file in the output.
    zip_files_in_output = glob.glob(join(out_dir, "*.zip"))
    if len(zip_files_in_output) > 0:
        log.info("There are zip files in the output, creating zipinfo.csv per file")
        for f in zip_files_in_output:
            create_zipinfo(out_dir, f)

    log.info("rtp2_preproc main.py ended succesfully. ")

    return 0
