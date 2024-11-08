import logging
import os
import shutil as sh
import subprocess as sp
import sys

log = logging.getLogger(__name__)

join = os.path.join


def pca_denoising(difm: str, common: str, do_denoise: bool) -> str:
    """Performs MRtrix's PCA denoising.

    It performs a series of MRtrix tools calls to perform PCA denoising,
    updating the file names with new suffixes. This function can be called
    if the do_denoise option is set to true (then the difm name will be updated)
    or it can be used as a requirement to other functions (the name is not
    updated). Right now it is only required for Rician noise reduction.

    Arguments:
        difm (str): diffusion file name.
        common (str): common option for MRtrix function calls.
        do_denoise (bool): option from the input config.

    Returns:
        str: updated file name
    """

    cmd = (
        f"dwidenoise -extent 5,5,5 -noise fpe_noise.mif -estimator Exp2 "
        f"{difm}.mif {difm}_denoise.mif {common}"
    )
    log.info("Performing PCA denoising with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    if os.path.isfile(f"rpe_{difm}.mif"):
        cmd = (
            f"dwidenoise -extent 5,5,5 -noise rpe_noise.mif -estimator Exp2 "
            f"rpe_{difm}.mif rpe_{difm}_denoise.mif {common}"
        )
        log.info("Performing PCA denoising on the rpe files with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

        cmd = f"mrcalc fpe_noise.mif rpe_noise.mif -add 2 -divide noise.mif {common}"
        log.info("Combining with:\n '%s'", cmd)
        sp.run(cmd, shell=True)
    else:
        sh.move("fpe_noise.mif", "noise.mif")

    if do_denoise:
        difm = f"{difm}_denoise"

    return difm


def do_degibbs(difm: str, common: str) -> str:
    """Performs MRtrix's Gibbs ringing correction.

    It will call MRtrix's mrdegibbs to perform ringing correction.
    It does it separately for forward and reverse phase encoding.

    Arguments:
        difm (str): diffusion file name.
        common (str): common option for MRtrix function calls.

    Returns:
        str: updated file name
    """

    cmd = (
        f"mrdegibbs -nshifts 20 -minW 1 -maxW 3 {difm}.mif "
        f"{difm}_degibbs.mif {common}"
    )
    log.info("Performing Gibbs ringing correction with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    if os.path.isfile(f"rpe_{difm}.mif"):
        cmd = (
            f"mrdegibbs -nshifts 20 -minW 1 -maxW 3 rpe_{difm}.mif "
            f"rpe_{difm}_degibbs.mif {common}"
        )
        log.info("Performing Gibbs on the rpe files with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

    difm = f"{difm}_degibbs"

    return difm


def do_eddy(
    difm: str,
    mask: str,
    common: str,
    common_fslpreproc: str,
    RPE: str,
    eddy_options: str,
    topup_options: str,
    ACQD: str,
) -> str:
    """Prepares and runs MRtrix's dwifslpreproc function (eddy and topup).

    It runs MRtrix's dwifslpreproc to perform eddy current correction
    with FSL's eddy function, and if reverse phase encoding files were provided,
    then it will run magnetic susceptibility based geometric distortion
    correction using FSL's topup. It does all the file manipulation operations
    required, and after this function is called, forward and reverse phase
    encoding files will be merged into one.


    Arguments:
        difm (str): diffusion file name.
        mask (str): masked brain file name.
        common (str): common option for MRtrix function calls.
        common_fslpreproc (str): common options for fslpreproc call.
        RPE (str): code for input file configuration, can be none, all, pairs
        eddy_options (str): config options for FSL's eddy.
        topup_options (str): config options for FSL's topup.
        ACQD (str): phase encoding direction in the PA,AP,RL,LR,IS,SI format.

    Returns:
        str: updated file name
    """

    if RPE == "none":
        cmd = (
            f"dwifslpreproc {difm}.mif {difm}_eddy.mif -rpe_none -pe_dir "
            f'{ACQD} -eddy_options "{eddy_options}" {common_fslpreproc} {common}'
        )
        log.info("Performing FSL eddy correction with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

    elif RPE == "pairs":
        log.info("Performing FSL topup and eddy correction")

        ## pull and merge the b0s
        cmd = f"dwiextract -bzero {difm}.mif fpe_b0.mif {common}"
        log.info(" pull and merge the b0s with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

        cmd = f"dwiextract -bzero rpe_{difm}.mif rpe_b0.mif {common}"
        log.info(" pull and merge the rpe b0s with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

        nb0F = int(
            sp.check_output(["mrinfo", "-size", "fpe_b0.mif"]).decode().split()[-1]
        )
        nb0R = int(
            sp.check_output(["mrinfo", "-size", "rpe_b0.mif"]).decode().split()[-1]
        )

        if nb0F > nb0R:
            cmd = f"mrconvert fpe_b0.mif tmp.mif -coord 3 0:{nb0R-1} {common}"
            log.info(" nb0F > nb0R, so doing mrconvert with:\n '%s'", cmd)
            sp.run(cmd, shell=True)

            cmd = f"mrcat tmp.mif rpe_b0.mif b0_pairs.mif -axis 3 {common}"
            log.info(" ... and now mrcat with:\n '%s'", cmd)
            sp.run(cmd, shell=True)

        elif nb0F == nb0R:
            cmd = f"mrcat fpe_b0.mif rpe_b0.mif b0_pairs.mif -axis 3 {common}"
            log.info(" nb0F = nb0R, so doing mrcat only with:\n '%s'", cmd)
            sp.run(cmd, shell=True)

        else:
            cmd = f"mrconvert rpe_b0.mif tmp.mif -coord 3 0:{nb0F-1} {common}"
            log.info(" nb0F < nb0R, so doing mrconvert with:\n '%s'", cmd)
            sp.run(cmd, shell=True)

            cmd = f"mrcat fpe_b0.mif tmp.mif b0_pairs.mif -axis 3 {common}"
            log.info(" ... and now mrcat with:\n '%s'", cmd)
            sp.run(cmd, shell=True)

        # call to dwifslpreproc w/ new options
        cmd = (
            f"dwifslpreproc {difm}.mif {difm}_eddy.mif -rpe_pair -se_epi "
            f"b0_pairs.mif -pe_dir {ACQD} -align_seepi "
            f'-topup_options "{topup_options}" '
            f'-eddy_options "{eddy_options}" '
            f"{common_fslpreproc} {common}"
        )
        log.info(" Call dwifslpreproc with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

    elif RPE == "all":
        cmd = (
            f"dwifslpreproc {difm}.mif {difm}_eddy.mif -rpe_all -pe_dir "
            f'{ACQD} -topup_options "{topup_options}" '
            f'-eddy_options "{eddy_options}" '
            f"{common_fslpreproc} {common}"
        )
        log.info(
            "Performing FSL eddy correction for merged input DWI sequences with:\n '%s'",
            cmd,
        )
        sp.run(cmd, shell=True)

    else:
        sys.exit("Option RPE '%s' not found", RPE)

    # rebuild mask after eddy motion
    difm = f"{difm}_eddy"
    cmd = f"dwi2mask {difm}.mif {mask}.mif {common}"
    log.info(" rebuild mask after eddy motion with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    return difm


def do_bias(
    difm: str,
    bias_method: str,
    out_dir: str,
    common: str,
    antsb: str,
    antsc: str,
    antss: str,
    mask: str,
) -> str:
    """Runs ANTs or FSLs bias correction.

    It runs the bias correction software based on the user's configuration.

    Arguments:
        difm (str): diffusion file name.
        bias_method: bias correction method. Allowed values: "ants", "fsl".
        out_dir: output directory of the gear.
        common (str): common option for MRtrix function calls.
        antsb: b params for ANTs.
        antsc: c params for ANTs.
        antss: s param for ANTs.
        mask (str): masked brain file name.

    Returns:
        str: updated file name
    """

    if bias_method == "ants":
        cmd = (
            f"dwibiascorrect ants -ants.b {antsb} -ants.c {antsc} "
            f"-ants.s {antss} -mask {mask}.mif {difm}.mif {difm}_bias.mif "
            f"-scratch {join(out_dir, 'tmp')} {common}"
        )
        log.info("Performing bias correction with ANTs with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

    elif bias_method == "fsl":
        cmd = (
            f"dwibiascorrect fsl -mask {mask}.mif {difm}.mif {difm}_bias.mif "
            f"-scratch {join(out_dir, 'tmp')} {common}"
        )
        log.info("Performing bias correction with FSL with:\n '%s'", cmd)
        sp.run(cmd, shell=True)

    difm = f"{difm}_bias"

    return difm


def do_rician(difm: str, common: str) -> str:
    """Performs MRtrix's Rician background noise removal.

    It uses previously calculated noise estimations to remove them from the dwi image,
    using standard MRtrix tools.

    Arguments:
        difm (str): diffusion file name.
        common (str): common option for MRtrix function calls.

    Returns:
        str: updated file name
    """

    cmd1 = f"mrinfo {difm}.mif -export_grad_mrtrix tmp.b  {common}"
    cmd2 = f"mrcalc noise.mif -finite noise.mif 0 -if lowbnoisemap.mif  {common}"
    cmd3 = (
        f"mrcalc {difm}.mif 2 -pow lowbnoisemap.mif 2 -pow -sub -abs -sqrt "
        f"- {common} | mrcalc - -finite - 0 -if tmp.mif {common}"
    )
    log.info(
        f"Performing Rician background noise removal with:\n {cmd1}\n{cmd2}\n{cmd3}"
    )
    sp.run(cmd1, shell=True)
    sp.run(cmd2, shell=True)
    sp.run(cmd3, shell=True)

    # Name the file
    difm = f"{difm}_ricn"

    # Add back bval and bvec and give proper name
    cmd = f"mrconvert tmp.mif -grad tmp.b {difm}.mif {common}"
    log.info(" mrconvert with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    # Remove the tmp files
    os.remove("tmp.mif")
    os.remove("tmp.b")

    return difm


def do_norm(difm: str, mask: str, common: str, nval: str) -> str:
    """Performs intensity normalization of DWI data using dwinormalise.

    Creates a mask based on FA and normalises the diffusion file based on a value
    given by the user in the config (nval).

    Arguments:
        difm (str): diffusion file name.
        mask (str): masked brain file name.
        common (str): common option for MRtrix function calls.
        nval (str): a number coming from the config, normalizes WM to this value.

    Returns:
        str: updated file name
    """

    cmd = (
        f"dwi2tensor -mask {mask}.mif  {difm}.mif - {common} | "
        f"tensor2metric  - -fa - {common} | "
        f"mrthreshold  -abs 0.5 - wm.mif {common}"
    )
    log.info("Create fa wm mask of input subject with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    ## normalize intensity of high FA white matter mask to 1000 (the default)
    cmd = f"dwinormalise individual -intensity {nval} {difm}.mif wm.mif {difm}_norm.mif {common}"
    log.info("Performing intensity normalization with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    difm = f"{difm}_norm"
    return difm


def create_ref_images(difm: str, common: str, mask: str) -> None:
    """Creates b0 based reference images.

    It uses MRtrix and FSL functions to extract b0 images and create
    b0 based DWI reference images and masked images.


    Arguments:
        difm (str): diffusion file name.
        common (str): common option for MRtrix function calls.
        mask (str): masked brain file name.
    """

    log.info("Creating dwi space b0 reference images...")

    cmd = f"dwiextract {difm}.mif - -bzero {common} | mrmath - mean b0_dwi.mif -axis 3 {common}"
    log.info(
        "create b0 and mask image in dwi space on forward direction only with:\n '%s'",
        cmd,
    )
    sp.run(cmd, shell=True)

    cmd = f"dwi2mask {difm}.mif {mask}.mif {common}"
    log.info("compute dwi mask for processing with:\n '%s'", cmd)
    sp.run(cmd, shell=True)

    cmd1 = f"mrconvert b0_dwi.mif b0_dwi.nii.gz {common}"
    cmd2 = f"mrconvert {mask}.mif {mask}.nii.gz {common}"
    log.info(
        f"Convert to nifti for alignment to anatomy later on with:\n {cmd1} and \n {cmd2}"
    )
    sp.run(cmd1, shell=True)
    sp.run(cmd2, shell=True)

    cmd = f"fslmaths b0_dwi.nii.gz -mas {mask}.nii.gz b0_dwi_brain.nii.gz"
    log.info("Apply mask to image with:\n '%s'", cmd)
    sp.run(cmd, shell=True)


def do_anatalign(
    difm: str, common: str, ANAT: str, FSMASK: str, ants_options: str
) -> str:
    """Aligns diffusion b0 with the anatomical image.

    Using MRtrix and ANTs functions, coregisters the reference dwi b0 images
    and uses the registration matrix to transform the dwi image to the anatomical
    space.

    Arguments:
        difm (str): diffusion file, the moving file in the alignment.
        common (str): common option for MRtrix function calls.
        ANAT (str): anatomical T1w reference image, the target of the alignment.
        FSMASK (str): masked brain file name.
        ants_options (str): ANTs options for coregistration.

    Returns:
        str: updated file name
    """

    log.info("Aligning dwi b0 image with anatomy ...")

    cmd = f"mrconvert {common} -stride 1,2,3 {ANAT} ./t1.nii.gz"
    log.info("create local copy of anat and make sure is RAS with:\n%s", cmd)
    sp.run(cmd, shell=True)

    cmd = f"mrconvert {common} -stride 1,2,3 {FSMASK} ./t1_brain.nii.gz"
    log.info("Provided skull stripped brain will be used as RAS with:\n%s", cmd)
    sp.run(cmd, shell=True)

    ## Align dwi data with anatomy
    ## compute BBR registration corrected diffusion data to  anatomy
    cmd = f"antsRegistrationSyN.sh -f {ANAT} -m b0_dwi_brain.nii.gz {ants_options} -o ants"
    log.info("Compute diff > anat transform mat using ANTs with:\n%s", cmd)
    sp.run(cmd, shell=True)

    # Apply the transform matrix
    cmd1 = "ConvertTransformFile 3 ants0GenericAffine.mat ants0GenericAffine.txt"
    ## apply the transform w/in mrtrix, correcting gradients
    cmd2 = "transformconvert ants0GenericAffine.txt itk_import dwi2anatalign_mrtrix.txt -force"
    cmd3 = f"mrtransform -linear dwi2anatalign_mrtrix.txt {difm}.mif {difm}_anatalign.mif {common}"
    log.info(
        "Apply the transform matrix with:\n '%s' and\n'%s' and\n'%s'", cmd1, cmd2, cmd3
    )
    sp.run(cmd1, shell=True)
    sp.run(cmd2, shell=True)
    sp.run(cmd3, shell=True)

    difm = f"{difm}_anatalign"

    return difm


def do_qmap_coreg(
    qmap: str,
    common: str,
    anat: str,
    fsmask: str,
    ants_options: str,
    do_anatalign: bool,
) -> str:
    """Aligns qMAP files with the anatomical image.

    If QMAPs are passed in the input, this function will align them with anatomy
    using MRtrix and ANTs functions. Coregisters the qMAP images
    and uses the registration matrix to transform the qMAP image to the anatomical
    space.

    Arguments:
        qmap (str): qMAP file, the moving file in the alignment.
        common (str): common option for MRtrix function calls.
        anat (str): anatomical T1w reference image, the target of the alignment.
        fsmask (str): masked brain file name.
        ants_options (str): ANTs options for coregistration.
        do_anatalign (bool): if do_anatlign was set to false, it will do extra steps
            that otherwise are done in the function do_anatalign()

    Returns:
        str: updated file name
    """

    log.info("Aligning QMAP with anatomy ...")

    qmap_filename = os.path.basename(qmap).replace(".nii.gz", "")
    qmap_aligned = qmap_filename + "_anat_aligned.nii.gz"
    qmap_resliced = qmap_filename + "_resliced.nii.gz"

    interp_method = "linear"

    if not do_anatalign:
        # T1
        cmd = f"mrconvert {common} -stride 1,2,3 {anat} ./t1.nii.gz"
        log.info("create local copy of anat and make sure is RAS with:\n %s", cmd)
        sp.run(cmd, shell=True)
        # BRAIN
        cmd = f"mrconvert {common} -stride 1,2,3 {fsmask} ./t1_brain.nii.gz"
        log.info("Freesurfer mask exists and will be used as RAS with:\n %s", cmd)
        sp.run(cmd, shell=True)

    # Align QMAP data with anatomy
    cmd = f"antsRegistrationSyN.sh -f {anat} -m {qmap} -o ants_{qmap_filename}_ {ants_options}"
    log.info("Compute qMAP > anat transform mat using ANTs with:\n %s", cmd)
    sp.run(cmd, shell=True)

    # Apply the transform matrix
    cmd1 = (
        f"ConvertTransformFile 3 ants_{qmap_filename}_0GenericAffine.mat "
        f"ants_{qmap_filename}_0GenericAffine.txt"
    )
    cmd2 = (
        f"transformconvert ants_{qmap_filename}_0GenericAffine.txt "
        f"itk_import {qmap_filename}_2anatalign_mrtrix.txt -force"
    )
    cmd3 = (
        f"mrtransform -linear {qmap_filename}_2anatalign_mrtrix.txt {qmap} "
        f"{qmap_aligned} {common}"
    )
    cmd4 = (
        f"mrgrid {qmap_aligned} regrid -template {anat} {qmap_resliced} "
        f"{common} -interp {interp_method}"
    )
    log.info(
        "Apply the transform matrix and reslice with:"
        "\n(1) %s\n(2) %s\n(3) %s\n(4) %s",
        cmd1,
        cmd2,
        cmd3,
        cmd4,
    )
    sp.run(cmd1, shell=True)
    sp.run(cmd2, shell=True)
    sp.run(cmd3, shell=True)
    sp.run(cmd4, shell=True)

    return qmap_resliced


def do_reslice(difm: str, common: str, resliceval: float) -> str:
    """Reslices the DWI data to a different voxel size.

    If doreslice is set to true and a value is passed in resliceval, the DWI data
    will be resliced to the given value.

    Arguments:
        difm (str): name of the dwi file to be resliced.
        common (str): common option for MRtrix function calls.
        resliceval (float): Numeric value in mm of the size of the new isotropic voxel.

    Returns:
        str: updated file name
    """

    log.info("Reslicing to %d ...", resliceval)
    VAL = str(resliceval).replace(".", "p")
    newname = f"{difm}_{VAL}mm"
    cmd = f"mrgrid {difm}.mif regrid -voxel {resliceval} {newname}.mif {common}"
    log.info(
        "Reslicing diffusion data to the requested isotropic voxel size "
        "of '%d' mm^3 with:\n '%s'",
        resliceval,
        cmd,
    )
    sp.run(cmd, shell=True)

    difm = newname
    return difm
