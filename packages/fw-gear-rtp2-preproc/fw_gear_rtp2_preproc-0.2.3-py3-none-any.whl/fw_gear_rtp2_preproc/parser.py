"""Parser module to parse gear config.json."""

from typing import Tuple
import logging

from flywheel_gear_toolkit import GearToolkitContext
from fw_gear_rtp2_preproc.utils import die
from fw_gear_rtp2_preproc.utils import get_valid_qmap_list

log = logging.getLogger(__name__)


def validate_ants_string(ants_string: str) -> None:
    """Validates that the config input for ANTs is correct.

    Incorrect arguments in ANTs strings would cause the gear to fail after it already did
    a lot of processing. This function, called early in the gear run, will validate the
    string and make the gear fail early if there are any incorrect arguments.

    FIRST: if option -d 2 or -d 3 is not found in the string, the gear will stop
    SECOND: check that the options are valid

    the default for the gear in the manifest is: "-d 3 -t r"

    Optional arguments:

        -n:  Number of threads (default = ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS if defined, otherwise 1)

        -i:  initial transform(s) --- order specified on the command line matters

        -t:  transform type (default = 's')
           t: translation (1 stage)
           r: rigid (1 stage)
           a: rigid + affine (2 stages)
           s: rigid + affine + deformable syn (3 stages)
           sr: rigid + deformable syn (2 stages)
           so: deformable syn only (1 stage)
           b: rigid + affine + deformable b-spline syn (3 stages)
           br: rigid + deformable b-spline syn (2 stages)
           bo: deformable b-spline syn only (1 stage)

        -r:  radius for cross correlation metric used during SyN stage (default = 4)

        -s:  spline distance for deformable B-spline SyN transform (default = 26)

        -g:  gradient step size for SyN and B-spline SyN (default = 0.1)

        -x:  mask(s) for the fixed image space, or for the fixed and moving image space in the format
             "fixedMask,MovingMask". Use -x once to specify mask(s) to be used for all stages or use
             -x for each "stage" (cf -t option).  If no mask is to be used for a particular stage,
             the keyword 'NULL' should be used in place of file names.

        -p:  precision type (default = 'd')
           f: float
           d: double

        -j:  use histogram matching (default = 0)
           0: false
           1: true

        -y:  use 'repro' mode for exact reproducibility of output.  Uses GC metric for linear
             stages and a fixed random seed (default = 0).
           0: false
           1: true

        -z:  collapse output transforms (default = 1)

        -e:  Fix random seed to an int value

        NB:  Multiple image pairs can be specified for registration during the SyN stage.
             Specify additional images using the '-m' and '-f' options.  Note that image
             pair correspondence is given by the order specified on the command line.
             Only the first fixed and moving image pair is used for the linear registration
             stages.

    Testing:
        ants_string = '-d 3 -t r'
        ants_string = '-d 4 -t r'
        ants_string = '-n 3 -t r'
        ants_string = '-d 3 -a r'
        ants_string = '-d 3 -a r'
        ants_string = '-d 3 -t so -j 1'
        ants_string = '-d 3 -t so -j 1,2'
        ants_string = '-d 3 -t so -j'
        validate_ants_string(ants_string)
    """

    # ants_string = '-d 3 -t r'  # This is the default in manifest.json

    # Check if it has an even number of arguments
    elements = ants_string.split()
    if not len(elements) % 2 == 0:
        die("The config string for ANTs needs to have an even number of components.")

    # Check -d
    if "-d " not in ants_string:
        die("-d parameter not found, and it is mandatory")

    # Check that all the passed values are valid
    valid_options = [
        "-d",
        "-n",
        "-i",
        "-t",
        "-r",
        "-s",
        "-g",
        "-x",
        "-p",
        "-j",
        "-y",
        "-z",
        "-e",
    ]
    for i in range(0, len(elements), 2):
        opt, val = elements[i : i + 2]
        if opt not in valid_options:
            die("'%s' parameter not found in the allowed list: %s", opt, valid_options)

        # Check the values asigned to the params are ok
        if opt == "-d":
            if val not in (valid_vals := ["2", "3"]):
                die(
                    "'%s' option passed '%s', valid options are: %s",
                    opt,
                    val,
                    valid_vals,
                )
        elif opt in ["-n", "-r", "-s", "-e"]:
            if not val.isdigit():
                die("'%s' option passed '%s', valid options are intergers", opt, val)
        elif opt == "-t":
            if val not in (
                valid_vals := ["t", "r", "a", "s", "sr", "so", "b", "br", "bo"]
            ):
                die(
                    "'%s' option passed '%s', valid options are: '%s' ",
                    opt,
                    val,
                    valid_vals,
                )
        elif opt == "-g":
            if not val.replace(".", "").isnumeric():
                die(
                    "'%s' option passed '%s', valid options are: '%s' ",
                    opt,
                    val,
                    valid_vals,
                )
        elif opt == "-p":
            if val not in (valid_vals := ["f", "d"]):
                die(
                    "'%s' option passed '%s', valid options are: '%s'",
                    opt,
                    val,
                    valid_vals,
                )
        elif opt in ["-j", "-y", "-z"]:
            if val not in (valid_vals := ["0", "1"]):
                die(
                    "'%s' option passed '%s', valid options are: '%s'",
                    opt,
                    val,
                    valid_vals,
                )
        elif opt in ["-i", "-x"]:
            pass
            # Todo check

    log.info('ANTs string "%s" passed the validation test', ants_string)


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[dict, dict]:
    """Inputs and config options parser.

    Parses gear_context's config.json file and returns relevant inputs and options.

    Arguments:
        gear_context (GearToolkitContext): gear context.

    Returns:
        tuple: dictionaries with inputs and configs
    """

    # Gear inputs
    # Validate qmap inputs first
    out_dir = gear_context.output_dir
    qmap_input = gear_context.get_input_path("QMAP")

    if qmap_input:
        list_of_paths_with_valid_maps = get_valid_qmap_list(out_dir, qmap_input)
    else:
        list_of_paths_with_valid_maps = []

    # Gear inputs
    gear_inputs = {
        "DIFF": gear_context.get_input_path("DIFF"),
        "BVAL": gear_context.get_input_path("BVAL"),
        "BVEC": gear_context.get_input_path("BVEC"),
        "ANAT": gear_context.get_input_path("ANAT"),
        "FSMASK": gear_context.get_input_path("FSMASK"),
        "RDIF": gear_context.get_input_path("RDIF"),
        "RBVL": gear_context.get_input_path("RBVL"),
        "RBVC": gear_context.get_input_path("RBVC"),
        "QMAP_LIST": list_of_paths_with_valid_maps,
        "output_dir": gear_context.output_dir,
    }

    # Gear configs
    gear_config = {
        "debug": gear_context.config.get("debug"),
        "denoise": gear_context.config.get("denoise"),
        "degibbs": gear_context.config.get("degibbs"),
        "eddy": gear_context.config.get("eddy"),
        "pe_dir": gear_context.config.get("pe_dir"),
        "bias": gear_context.config.get("bias"),
        "ricn": gear_context.config.get("ricn"),
        "norm": gear_context.config.get("norm"),
        "nval": gear_context.config.get("nval"),
        "anatalign": gear_context.config.get("anatalign"),
        "save_extra_output": gear_context.config.get("save_extra_output"),
        "doreslice": gear_context.config.get("doreslice"),
        "reslice": gear_context.config.get("reslice"),
        "bias_method": gear_context.config.get("bias_method"),
        "antsb": gear_context.config.get("antsb"),
        "antsc": gear_context.config.get("antsc"),
        "antss": gear_context.config.get("antss"),
        "ants_dwi2anat_options": gear_context.config.get("ants_dwi2anat_options"),
        "ants_qmap2anat_options": gear_context.config.get("ants_qmap2anat_options"),
        "eddy_data_is_shelled": gear_context.config.get("eddy_data_is_shelled"),
        "eddy_slm": gear_context.config.get("eddy_slm"),
        "eddy_niter": gear_context.config.get("eddy_niter"),
        "eddy_repol": gear_context.config.get("eddy_repol"),
        # "eddy_mporder": gear_context.config.get("eddy_mporder"),
        # "eddy_slspec": gear_context.config.get("eddy_slspec"),
        "topup_lambda": gear_context.config.get("topup_lambda"),
    }

    # Do some checks in the inputs that can stop the gear if not correct
    if gear_config["anatalign"]:
        validate_ants_string(gear_config["ants_dwi2anat_options"])
    if gear_inputs["QMAP_LIST"]:
        validate_ants_string(gear_config["ants_qmap2anat_options"])

    if gear_config["doreslice"]:
        log.warning(
            "Reslicing of the diffusion images was requested by setting the "
            "'doreslice' config to True. If this analysis is part of the RTP2 suite, "
            "the recommended procedure is to do 'anatalign' without reslicing. If "
            "reslicing is requested, the best option is to choose the same voxel "
            "size as the T1w."
        )
    if gear_config["doreslice"] and gear_config["reslice"] is None:
        die(
            "Reslicing of the diffusion images was requested by setting the "
            "'doreslice' config to True. Therefore, a numeric value must be provided "
            "in the 'reslice' config option, None was passed."
        )
    if gear_config["doreslice"] and gear_config["reslice"] <= 0.1:
        die(
            "Reslicing of the diffusion images was requested by setting the "
            "'doreslice' config to True. A numeric value of %d was provided in the"
            "'reslice' config option, but this value should be greated than 0.1",
            gear_config["reslice"],
        )

    return gear_inputs, gear_config


# Temporarily removing eddy_mporder and eddy_slspec
# json files cannot be commented, therefore maintaining here the options.

"""

MOVED FROM MANIFEST

        "eddy_mporder": {
            "description": "If one wants to do slice-to-vol motion correction --mporder should be set to an integer value greater than 0 and less than the number of excitations in a volume. Only when --mporder > 0 will any of the parameters prefixed by --s2v_ be considered. The larger the value of --mporder, the more degrees of freedom for modelling movement. If --mporder is set to N-1, where N is the number of excitations in a volume, the location of each slice/MB-group is individually estimated. We don't recommend going that high and in our tests we have used values of N/4 -- N/2. The underlying temporal model of movement is a DCT basis-set of order N. Slice-to-vol motion correction is computationally very expensive so it is only implemented for the CUDA version. See FSL Eddy User Guide for more details.  [default=5]",
            "default": 0,
            "type": "number"
        },
        "eddy_slspec": {
            "description": "Specifies a text-file that describes how the slices/MB-groups were acquired. This information is necessary for eddy to know how a temporally continuous movement translates into location of individual slices/MB-groups. Let us say a given acquisition has N slices and that m is the MB-factor (also known as Simultaneous Multi-Slice (SMS)). Then the file pointed to be --slspec will have N/m rows and m columns. Let us for example assume that we have a data-set which has been acquired with an MB-factor of 3, 15 slices and interleaved slice order. The file would then be [0 5 10;2 7 12;4 9 14;1 6 11;3 8 13] where the first row [0 5 10] specifies that the first, sixth and 11th slice are acquired first and together, followed by the third, eighth and 13th slice etc. For single-band data and for multi-band data with an odd number of excitations/MB-groups it is trivial to work out the --slspec file using the logic of the example. For an even number of excitations/MB-groups it is considerably more difficult and we recommend using a DICOM->niftii converter that writes the exact slice timings into a .JSON file. This can then be used to create the --slspec file. See FSL Eddy User Guide for more details",
            "default": "",
            "type": "string"
        },
        
        
        
        
        
        
        
MOVED FROM README.MD

- *eddy_mporder*
  - __Name__: *eddy_mporder*
  - __Type__: *number*
  - __Description__: *If one wants to do slice-to-vol motion correction --mporder 
      should be set to an integer value greater than 0 and less than the number 
      of excitations in a volume. Only when --mporder > 0 will any of the parameters 
      prefixed by --s2v_ be considered. The larger the value of --mporder, the more 
      degrees of freedom for modelling movement. If --mporder is set to N-1, where N 
      is the number of excitations in a volume, the location of each slice/MB-group 
      is individually estimated. We don't recommend going that high and in our 
      tests we have used values of N/4 -- N/2. The underlying temporal model of 
      movement is a DCT basis-set of order N. Slice-to-vol motion correction is 
      computationally very expensive so it is only implemented for the CUDA version.*
  - __Default__: *0*  


- *eddy_slspec*
  - __Name__: *eddy_slspec*
  - __Type__: *string*
  - __Description__: *Specifies a text-file that describes how the slices/MB-groups 
      were acquired. This information is necessary for eddy to know how a temporally 
      continuous movement translates into location of individual slices/MB-groups. 
      Let us say a given acquisition has N slices and that m is the MB-factor (also 
      known as Simultaneous Multi-Slice (SMS)). Then the file pointed to be --slspec 
      will have N/m rows and m columns. Let us for example assume that we have a 
      data-set which has been acquired with an MB-factor of 3, 15 slices and interleaved 
      slice order. The file would then be [0 5 10;2 7 12;4 9 14;1 6 11;3 8 13] where 
      the first row [0 5 10] specifies that the first, sixth and 11th slice are acquired 
      first and together, followed by the third, eighth and 13th slice etc. 
      For single-band data and for multi-band data with an odd number of excitations/MB-groups 
      it is trivial to work out the --slspec file using the logic of the example. For an even 
      number of excitations/MB-groups it is considerably more difficult and we recommend 
      using a DICOM->niftii converter that writes the exact slice timings into a .JSON file. 
      This can then be used to create the --slspec file.*
  - __Default__: *hi there\n1 1 1\n3 3 3*  


        
"""
