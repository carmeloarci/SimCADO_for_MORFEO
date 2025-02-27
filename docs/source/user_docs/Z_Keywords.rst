
Keywords for Controlling SimCADO
================================
Observation Parameters
-----------------------

::

    Keyword                 Default     [units] Explanation
    -----------------------------------------------------------------------------------------------
    
    OBS_DATE                0                       # [dd/mm/yyyy] Date of the observation [not yet implemented]
    OBS_TIME                0                       # [hh:mm:ss] Time of the observation [not yet implemented]
    OBS_RA                  90.                     # [deg] RA of the object
    OBS_DEC                 -30.                    # [deg] Dec of the object
    OBS_ALT                 0                       # [deg] Altitude of the object [not yet implemented]
    OBS_AZ                  0                       # [deg] Azimuth of the object [not yet implemented]
    OBS_ZENITH_DIST         0                       # [deg] from zenith
    OBS_PARALLACTIC_ANGLE   0                       # [deg] rotation of the source relative to the zenith
    OBS_SEEING              0.6                     # [arcsec]
    
    OBS_FIELD_ROTATION      0                       # [deg] field rotation with respect to the detector array
    
    OBS_DIT                 60                      # [sec] simulated exposure time
    OBS_NDIT                1                       # [#] number of exposures taken
    OBS_NONDESTRUCT_TRO     2.6                     # [sec] time between non-destructive readouts in the detector
    OBS_REMOVE_CONST_BG     no                      # remove the median background value
    OBS_READ_MODE           single                  # [single, fowler, ramp] Only single is implemented at the moment
    OBS_SAVE_ALL_FRAMES     no                      # yes/no to saving all DITs in an NDIT sequence
    
    OBS_INPUT_SOURCE_PATH   none                    # Path to input Source FITS file
    OBS_FITS_EXT            0                       # the extension number where the useful data cube is
    
    OBS_OUTPUT_DIR          "./output.fits"         # [filename] Path to save output in.
    
    
Simulation Parameters
----------------------

::

    Keyword                 Default     [units] Explanation
    -----------------------------------------------------------------------------------------------
    
    SIM_DETECTOR_PIX_SCALE  0.004                   # [arcsec] plate scale of the detector
    SIM_OVERSAMPLING        1                       # The factor of oversampling inside the simulation
    SIM_PIXEL_THRESHOLD     1                       # photons per pixel summed over the wavelength range. Values less than this are assumed to be zero
    
    SIM_LAM_TC_BIN_WIDTH    0.001                   # [um] wavelength resolution of spectral curves
    SIM_SPEC_MIN_STEP       1E-4                    # [um] minimum step size where resampling spectral curves
    
    SIM_FILTER_THRESHOLD    1E-9                    # transmission below this threshold is assumed to be 0
    SIM_USE_FILTER_LAM      yes                     # [yes/no] to basing the wavelength range off the filter non-zero range - if no, specify LAM_MIN, LAM_MAX
    # if "no"
    SIM_LAM_MIN             1.9                     # [um] lower wavelength range of observation
    SIM_LAM_MAX             2.41                    # [um] upper wavelength range of observation
    SIM_LAM_PSF_BIN_WIDTH   0.1                     # [um] wavelength resolution of the PSF layers
    SIM_ADC_SHIFT_THRESHOLD 1                       # [pixel] the spatial shift before a new spectral layer is added (i.e. how often the spectral domain is sampled for an under-performing ADC)
    
    SIM_PSF_SIZE            1024                    # size of PSF
    SIM_PSF_OVERSAMPLE      no                      # use astropy's inbuilt oversampling technique when generating the PSFs. Kills memory for PSFs over 511 x 511
    SIM_VERBOSE             no                      # [yes/no] print information on the simulation run
    SIM_SIM_MESSAGE_LEVEL   3                       # the amount of information printed [5-everything, 0-nothing]
    
    SIM_OPT_TRAIN_IN_PATH   none                    # Options for saving and reusing optical trains. If "none": "./"
    SIM_OPT_TRAIN_OUT_PATH  none                    # Options for saving and reusing optical trains. If "none": "./"
    SIM_DETECTOR_IN_PATH    none                    # Options for saving and reusing detector objects. If "none": "./"
    SIM_DETECTOR_OUT_PATH   none                    # Options for saving and reusing detector objects. If "none": "./"
    
    
Atmospheric Parameters
-----------------------

::

    Keyword                 Default     [units] Explanation
    -----------------------------------------------------------------------------------------------
    
    ATMO_USE_ATMO_BG        yes                     # [yes/no]
    
    ATMO_TC                 TC_sky_25.tbl           # [filename] for atmospheric transmission curve. Default: <pkg_dir>/data/TC_sky_25.tbl
    ATMO_EC                 EC_sky_25.tbl           # [filename, "none"] for atmospheric emission curve. Default: <pkg_dir>/data/EC_sky_25.tbl
    # If ATMO_EC is "none": set ATMO_BG_MAGNITUDE for the simulation filter.
    ATMO_BG_MAGNITUDE       13.6                    # [ph/s] background photons for the bandpass. If set to None, the ATMO_EC spectrum is assumed to return the needed number of photons
    
    ATMO_TEMPERATURE        0                       # deg Celcius
    ATMO_PRESSURE           750                     # millibar
    ATMO_REL_HUMIDITY       60                      # %
    ATMO_PWV                2.5                     # [mm] Paranal standard value
    
    
Telescope Parameters
---------------------

::

    Keyword                 Default     [units] Explanation
    -----------------------------------------------------------------------------------------------
    
    SCOPE_ALTITUDE          3060                    # meters above sea level
    SCOPE_LATITUDE          -24.589167              # decimal degrees
    SCOPE_LONGITUDE         -70.192222              # decimal degrees
    
    SCOPE_PSF_FILE          scao                    # [scao (default), <filename>, ltao, mcao, poppy] import a PSF from a file.
    SCOPE_STREHL_RATIO      1                       # [0..1] defines the strength of the seeing halo if SCOPE_PSF_FILE is "default"
    SCOPE_AO_EFFECTIVENESS  100                     # [%] percentage of seeing PSF corrected by AO - 100% = diff limited, 0% = 0.8" seeing
    SCOPE_JITTER_FWHM       0.001                   # [arcsec] gaussian telescope jitter (wind, tracking)
    SCOPE_DRIFT_DISTANCE    0                       # [arcsec/sec] the drift in tracking by the telescope
    SCOPE_DRIFT_PROFILE     linear                  # [linear, gaussian] the drift profile. If linear, simulates when tracking is off. If gaussian, simulates rms distance of tracking errors
    
    SCOPE_USE_MIRROR_BG     yes                     # [yes/no]
    
    SCOPE_NUM_MIRRORS       5                       # number of reflecting surfaces
    SCOPE_TEMP              0                       # deg Celsius - temperature of mirror
    SCOPE_M1_TC             TC_mirror_EELT.dat      # [filename] Mirror reflectance curve. Default: <pkg_dir>/data/TC_mirror_EELT.dat
    SCOPE_MIRROR_LIST       EC_mirrors_EELT_SCAO.tbl    # [filename] List of mirror sizes.     Default: <pkg_dir>/data/EC_mirrors_EELT_SCAO.tbl
    
    
Instrument Parameters
----------------------

::

    Keyword                 Default     [units] Explanation
    -----------------------------------------------------------------------------------------------
    
    INST_TEMPERATURE        -190                    # deg Celsius - inside temp of instrument
    
    INST_ENTR_NUM_SURFACES  4                       # number of surfaces on the entrance window
    INST_ENTR_WINDOW_TC     TC_window.dat           # [filename] Default: <pkg_dir>/data/TC_window.dat --> transmission = 0.98 per surface
    
    INST_DICHROIC_NUM_SURFACES  2                   # number of surfaces on the entrance window
    INST_DICHROIC_TC        TC_dichroic.dat         # [filename] Default: <pkg_dir>/data/TC_dichroic.dat --> transmission = 1 per surface
    
    INST_FILTER_TC          Ks                      # [filename, string(filter name)] List acceptable filters with >>> simcado.optics.get_filter_set()
    
    INST_PUPIL_NUM_SURFACES 2                       # number of surfaces on the pupil window
    INST_PUPIL_TC           TC_pupil.dat            # [filename] Default: <pkg_dir>/data/TC_pupil.dat --> transmission = 1 per surface
    
    # MICADO, collimator 5x, wide-field 2x (zoom 4x), camera 4x
    INST_NUM_MIRRORS        11                      # number of reflecting surfaces in MICADO
    INST_MIRROR_TC          TC_mirror_gold.dat      # [filename, "default"] If "default": INST_MIRROR_TC = SCOPE_M1_TC
    
    INST_USE_AO_MIRROR_BG   yes                     # [yes/no]
    INST_AO_TEMPERATURE     0                       # deg Celsius - inside temp of AO module
    INST_NUM_AO_MIRRORS     7                       # number of reflecting surfaces between telescope and instrument (i.e. MAORY)
    INST_MIRROR_AO_TC       TC_mirror_gold.dat      # [filename, "default"] If "default": INST_MIRROR_AO_TC = INST_MIRROR_TC
    INST_MIRROR_AO_LIST     EC_mirrors_ao.tbl       # List of mirrors in the AO. Default: <pkg_dir>/data/EC_mirrors_ao.tbl
    
    INST_ADC_PERFORMANCE    100                     # [%] how well the ADC does its job
    INST_ADC_NUM_SURFACES   8                       # number of surfaces in the ADC
    INST_ADC_TC             TC_ADC.dat              # [filename] Default: <pkg_dir>/data/TC_ADC.dat --> transmission = 0.98 per surface
    
    INST_DEROT_PERFORMANCE  100                     # [%] how well the derotator derotates
    INST_DEROT_PROFILE      linear                  # [linear, gaussian] the profile with which it does it's job
    
    INST_DISTORTION_MAP     none                    # path to distortion map
    INST_WFE                data/INST_wfe.tbl       # [nm] (float or filename) A single number for the total WFE of a table of wavefront errors for each surface in the instrument
    INST_FLAT_FIELD         none                    # path to a FITS file containing a flat field (median = 1) for each chip.
    
Spectroscopy parameters
------------------------

::

    Keyword                 Default     [units] Explanation
    -----------------------------------------------------------------------------------------------
    
    SPEC_ORDER_SORT         HK                      # Order-sorting filter: "HK" or "IJ"
    SPEC_SLIT_WIDTH         narrow                  # Slit width: "narrow" or "wide"
    
Detector parameters
--------------------

::

    Keyword                 Default     [units] Explanation
    -----------------------------------------------------------------------------------------------
    
    FPA_USE_NOISE           yes                     # [yes/no]
    
    FPA_READOUT_MEDIAN      4                       # e-/px
    FPA_READOUT_STDEV       1                       # e-/px
    FPA_DARK_MEDIAN         0.01                    # e-/s/px
    FPA_DARK_STDEV          0.01                    # e-/s/px
    
    FPA_QE                  TC_detector_H2RG.dat    # [filename] Quantum efficiency of detector.
    FPA_NOISE_PATH          FPA_noise.fits          # [filename, "generate"] if "generate": use NGHxRG to create a noise frame.
    FPA_GAIN                1                       # e- to ADU conversion
    FPA_LINEARITY_CURVE     FPA_linearity.dat       # [filename, "none"]
    FPA_FULL_WELL_DEPTH     1E5                     # [e-] The level where saturation occurs
    
    FPA_PIXEL_MAP           none                    # path to a FITS file with the pixel sensitivity map
    # if FPA_PIXEL_MAP == none
    FPA_DEAD_PIXELS         1                       # [%] if FPA_PIXEL_MAP=none, a percentage of detector pixel which are dead
    FPA_DEAD_LINES          1                       # [%] if FPA_PIXEL_MAP=none, a percentage of detector lines which are dead
    
    FPA_CHIP_LAYOUT         centre                    # ["tiny", "small", "centre", "full", <filename>] description of the chip layout on the detector array.
    FPA_PIXEL_READ_TIME     1E-5                    # [s] read time for y pixel - typically ~10 us
    FPA_READ_OUT_SCHEME     double_corr             # "double_corr", "up-the-ramp", "fowler"
    
NXRG Noise Generator package parameters
----------------------------------------

::

    Keyword                 Default     [units] Explanation
    -----------------------------------------------------------------------------------------------
    # See Rauscher (2015) for details
    # http://arxiv.org/pdf/1509.06264.pdf
    
    HXRG_NUM_OUTPUTS        64                      # Number of
    HXRG_NUM_ROW_OH         8                       # Number of row overheads
    HXRG_PCA0_FILENAME      FPA_nirspec_pca0.fits   # if "default": <pkg_dir>/data/
    HXRG_OUTPUT_PATH        none                    # Path to save the detector noise
    HXRG_PEDESTAL           4                       # Pedestal noise
    HXRG_CORR_PINK          3                       # Correlated Pink noise
    HXRG_UNCORR_PINK        1                       # Uncorrelated Pink noise
    HXRG_ALT_COL_NOISE      0.5                     # Alternating Column noise
    
    HXRG_NAXIS1             4096                    # Size of the HAWAII 4RG detectors
    HXRG_NAXIS2             4096
    HXRG_NUM_NDRO           1                       # Number of non-destructive readouts to add to a noise cube

