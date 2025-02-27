"""
Helper functions for SimCADO
"""
###############################################################################
# utils.py
#
# DESCRIPTION
#
#
# Classes:
#
#
# Functions:
#  read_config(config_file)
#  update_config(config_file, config_dict)
#  unify(x, unit, length=1)
#  parallactic_angle(ha, de, lat=-24.589167)
#  parallactic_angle_2(ha, de, lat=-24.589167)
#  moffat(r, alpha, beta)
#
import os
import sys
import inspect

try:
    import wget
except ImportError:
    print("Package wget is not available. simcado.get_extras() will not work.")

import numpy as np
from astropy import units as u
from astropy.io import fits
from astropy.io import ascii as ioascii

__pkg_dir__ = os.path.dirname(inspect.getfile(inspect.currentframe()))

#__all__ = []
#__all__ = ["unify", "parallactic_angle", "poissonify",
#           "atmospheric_refraction", "nearest", "add_keyword"]


def msg(cmds, message, level=3):
    """
    Prints a message based on the level of verbosity given in cmds

    Parameters
    ----------
    cmds : UserCommands
        just for the SIM_VERBOSE and SIM_MESSAGE_LEVEL keywords
    message : str
        message to be printed
    level : int, optional
        all messages with level <= SIM_MESSAGE_LEVEL are printed. I.e. level=5
        messages are not important, level=1 are very important
    """
    if cmds["SIM_VERBOSE"] == "yes" and level <= cmds["SIM_MESSAGE_LEVEL"]:
        print(message)



def unify(x, unit, length=1):
    """
    Convert all types of input to an astropy array/unit pair

    Parameters
    ----------
    x : int, float, np.ndarray, astropy.Quantity
        The array to be turned into an astropy.Quantity
    unit : astropy.Quantity
        The units to attach to the array
    length : int, optional
        If ``x`` is a scalar, and the desired output is an array with ``length``

    Returns
    -------
    y : astropy.Quantity
    """

    if isinstance(x, u.quantity.Quantity):
        if isinstance(x.value, np.ndarray):
            y = x.to(unit)
        elif length == 1:
            y = x.to(unit)
        else:
            y = ([x.value] * length * x.unit).to(unit)
    else:
        if hasattr(x, "__len__"):
            y = x * unit
        elif length == 1:
            y = x * unit
        else:
            y = [x] * length * unit

    return y


def parallactic_angle(ha, de, lat=-24.589167):
    r"""
    Compute the parallactic angle

    Parameters
    ----------
    ha : float
        [hours] hour angle of target point
    de : float
        [deg] declination of target point
    lat : float
        [deg] latitude of observatory, defaults to Armazones

    Returns
    -------
    parang : float
       The parallactic angle

    Notes
    -----
    The parallactic angle is defined as the angle PTZ, where P is the
    .. math::
    \tan\eta = \frac{\cos\phi\sin H}{\sin\phi \cos\delta - \cos\phi \sin\delta \cos H}
    It is negative (positive) if the target point is east (west) of the meridian.

    References
    ----------
    R. Ball: "A Treatise on Spherical Astronomy", Cambridge 1908
    """
    # Convert angles to radians
    ha = ha / 12. * np.pi
    de = np.deg2rad(de)
    lat = np.deg2rad(lat)

    eta = np.arctan2(np.cos(lat) * np.sin(ha),
                     np.sin(lat) * np.cos(de) - \
                     np.cos(lat) * np.sin(de) * np.cos(ha))

    return np.rad2deg(eta)


def moffat(r, alpha, beta):
    """
    !!Unfinished!! Return a Moffat function

    Parameters
    ----------
    r
    alpha
    beta

    Returns
    -------
    eta
    """
    return (beta - 1)/(np.pi * alpha**2) * (1 + (r/alpha)**2)**(-beta)


def poissonify(arr):
    """
    Add a realisation of the poisson process to the array 'arr'.

    Parameters
    ----------
    arr : np.ndarray
        The input array which needs a Poisson distribution applied to items

    Returns
    -------
    arr : np.ndarray
        The input array, but with every pixel altered according to a poisson
        distribution
    """
    return np.random.poisson(arr).astype(np.float32)


def atmospheric_refraction(lam, z0=60, temp=0, rel_hum=60, pres=750,
                           lat=-24.5, h=3064):
    """Compute atmospheric refraction

    The function computes the angular difference between the apparent position
    of a star seen from the ground and its true position.

    Parameters
    ----------
    lam : float, np.ndarray
        [um] wavelength bin centres
    z0 : float, optional
        [deg] zenith distance. Default is 60 deg from zenith
    temp : float, optional
        [deg C] ground temperature. Default is 0 deg C
    rel_hum : float, optional
        [%] relative humidity. Default is 60%
    pres : float, optional
        [millibar] air pressure. Default is 750 mbar
    lat : float, optional
        [deg] latitude. Default set for Cerro Armazones: 24.5 deg South
    h : float, optional
        [m] height above sea level. Default is 3064 m

    Returns
    -------
    ang : float, np.ndarray
        [arcsec] angle between real position and refracted position

    References
    ----------
    See Stone 1996 and the review by S. Pedraz -
    http://www.caha.es/newsletter/news03b/pedraz/newslet.html
    """

    # need T, P, RH for Ps, Pw Pa
    T = 273.15 + temp

    Ps = -10474. + 116.43 * T - 0.43284 * T**2 + 0.0005384 * T**3
    Pw = Ps * rel_hum / 100.
    Pa = pres - Pw

    # need n0 for gamma
    sig = 1. / lam
    Da = (Pa / T) * (1. + Pa * (57.9E-8 - 0.0009325 / T + 0.25844 / T**2))
    Dw = (Pw / T) * (1. + Pw * (1. + 3.7E-4 * Pw) *
                     (-2.37321E-3 + 2.23366 / T - 710.792 / T**2 +
                      77514.1 / T**3))

    na = Da * (2371.34 + 683939.7 / (130. - sig**2) + 4547.3 / (38.9 - sig**2))
    nw = Dw * (6487.31 + 58.058 * sig**2 - 0.7115 * sig**4 + 0.08851 * sig**6)
    n0 = 1E-8 * (na + nw) + 1.

    # need gamma, kappa and beta for R
    g = n0 - 1.
    b = 0.001254 * (273.15 + temp) / 273.15
    k = 1. + 0.005302 * np.sin(np.deg2rad(lat))**2 \
        - 0.00000583 * np.sin(2. * np.deg2rad(lat))**2 - 0.000000315 * h

    R = k * g * (1 - b) * np.tan(np.deg2rad(z0)) \
        - k * g * (b - g/2.) * np.tan(np.deg2rad(z0))**3

    # the refraction is the side of a triangle, although the triangle
    # side makes an arc across the sky.
    # We want the angle that this triangle side is subtending
    # Using the small angle approximation (which is in radians),
    # we can get the angle of refraction

    ang = np.rad2deg(R * 3600)

    # return value is in arcsec
    return ang


def nearest(arr, val):
    """
    Return the index of the value from 'arr' which is closest to 'val'

    Parameters
    ----------
    arr : np.ndarray, list, tuple
        Array to be searched
    val : float, int
        Value to find in ``arr``

    Returns
    -------
    i : int
        index of array where the nearest value to ``val`` is
    """
    if isinstance(val, (list, tuple, np.ndarray)):
        arr = np.array(arr)
        return [nearest(arr, i) for i in val]

    return np.argmin(abs(arr - val))


def deriv_polynomial2d(poly):
    '''Derivatives (gradient) of a Polynomial2D model

    Parameters
    ----------
    poly : astropy.modeling.models.Polynomial2D

    Output
    ------
    gradient : tuple of Polynomial2d
    '''
    import re
    from astropy.modeling.models import Polynomial2D
    degree = poly.degree
    dpoly_dx = Polynomial2D(degree=degree - 1)
    dpoly_dy = Polynomial2D(degree=degree - 1)
    regexp = re.compile(r'c(\d+)_(\d+)')
    for pname in poly.param_names:
        # analyse the name
        match = regexp.match(pname)
        i = int(match.group(1))
        j = int(match.group(2))
        cij = getattr(poly, pname)
        pname_x = "c%d_%d" % (i-1, j)
        pname_y = "c%d_%d" % (i, j-1)
        setattr(dpoly_dx, pname_x, i * cij)
        setattr(dpoly_dy, pname_y, j * cij)

    return dpoly_dx, dpoly_dy


def add_keyword(filename, keyword, value, comment="", ext=0):
    """
    Add a keyword, value pair to an extension header in a FITS file

    Parameters
    ----------
    filename : str
        Name of the FITS file to add the keyword to
    keyword : str
    value : str, float, int
    comment : str
    ext : int, optional
        The fits extension index where the keyword should be added.
        Default is 0
    """
    f = fits.open(filename, mode="update")
    f[ext].header[keyword] = (value, comment)
    f.flush()
    f.close()


# ############ Check the server for data extras
def download_file(url, save_dir=os.path.join(__pkg_dir__, "data")):
    """
    Download the extra data that aren't in the SimCADO package
    """

    local_filename = os.path.join(save_dir, url.split('/')[-1])
    try:
        temp_file = wget.download(url,
                                  out=wget.tempfile.mktemp(dir=save_dir,
                                                           suffix='.tmp'),
                                  bar=wget.bar_adaptive)
        print("\n")
        if os.path.exists(local_filename):
            os.remove(local_filename)
        os.rename(temp_file, local_filename)
    except wget.ulib.HTTPError:
        print(url + " not found")

    return local_filename


def get_extras():
    """
    Downloads large files that SimCADO needs to simulate MICADO
    """

    save_dir = os.path.join(__pkg_dir__, "data")
    fname = os.path.join(save_dir, "extras.dat")

    # check_replace = 0  ## unused (OC)
    if os.path.exists(fname):
        old_extras = ioascii.read(fname)
        # check_replace = 1   ## unused (OC)
    else:
        old_extras = ioascii.read("""
        filename                version         size    group
        PSF_POPPY.fits          20151103a       48MB    typical
        """)

    url = "http://www.univie.ac.at/simcado/data_ext/"
    new_extras = ioascii.read(download_file(url + "extras.dat"))

    for name, vers, size, group in new_extras:
        check_download = 1

        # does the file exist on the users disk?
        fname = os.path.join(__pkg_dir__, "data", name)
        if os.path.exists(fname):

            # is the new name in the old list of filenames
            if name in old_extras["filename"]:
                iname = np.where(old_extras["filename"] == name)[0][0]
                # print(iname, old_extras["version"][iname] == vers)

                # Are the versions the same?
                if vers == old_extras["version"][iname]:
                    check_download = 0

        if check_download:
            print("Downloading: " + name + "  Version: " + vers +
                  "  Size: " + size)
            download_file(url + name)
        else:
            print(name + " is already the latest version: " + vers)

    print("Finished downloading data for SimCADO")


def add_SED_to_simcado(file_in, file_out=None, lam_units="um"):
    """
    Adds the SED given in ``file_in`` to the SimCADO data directory

    Parameters
    ----------
    file_in : str
        path to the SED file. Can be either FITS or ASCII format with 2 columns
        Column 1 is the wavelength, column 2 is the flux
    file_out : str, optional
        Default is None. The file path to save the ASCII file. If ``None``, the SED
        is saved to the SimCADO data directory i.e. to ``<utils.__pkg_dir__>/data/``
    lam_units : str, astropy.Units
        Units for the wavelength column, either as a string or as astropy units
        Default is [um]

    """

    file_name, file_ext = os.path.basename(file_in).split(".")

    if file_out is None:
        if "SED_" not in file_name:
            file_out = __pkg_dir__+"/data/SED_"+file_name+".dat"
        else: file_out = __pkg_dir__+"/data/"+file_name+".dat"

    if file_ext.lower() in "fits":
        data = fits.getdata(file_in)
        lam, val = data[data.columns[0].name], data[data.columns[1].name]
    else:
        lam, val = ioascii.read(file_in)[:2]

    lam = (lam * u.Unit(lam_units)).to(u.um)
    mask = (lam > 0.3*u.um) * (lam < 5.0*u.um)

    np.savetxt(file_out, np.array((lam[mask], val[mask]), dtype=np.float32).T,
               header="wavelength    value \n [um]         [flux]")


def airmass_to_zenith_dist(airmass):
    """
    returns zenith distance in degrees

    Z = arccos(1/X)
    """
    return np.rad2deg(np.arccos(1. / airmass))


def zenith_dist_to_airmass(zenith_dist):
    """
    ``zenith_dist`` is in degrees

    X = sec(Z)
    """
    return 1. / np.cos(np.deg2rad(zenith_dist))


def seq(start, stop, step=1):
    '''Replacement for numpy.arange modelled after R's seq function

    Returns an evenly spaced sequence from start to stop. stop is included if the difference
    between start and stop is an integer multiple of step.

    From the documentation of numpy.range: "When using a non-integer step, such as 0.1, the
    results will often not be consistent." This replacement aims to avoid these inconsistencies.

    Parameters
    ----------

    start, stop: [int, float]
        the starting and (maximal) end values of the sequence.

    step : [int, float]
        increment of the sequence, defaults to 1

    '''
    feps = 1e-10     # value used in R seq.default

    delta = stop - start
    if delta == 0 and stop == 0:
        return stop
    try:
        npts = delta / step
    except ZeroDivisionError:
        if step == 0 and delta == 0:
            return start
        else:
            raise ValueError("invalid '(stop - start) / step'")

    if npts < 0:
        raise ValueError("wrong sign in 'step' argument")
    if npts > sys.maxsize:
        raise ValueError("'step' argument is much too small")

    reldd = abs(delta) / max(abs(stop), abs(start))

    if reldd < 100 * sys.float_info.epsilon:
        return start

    if isinstance(delta, int) and isinstance(step, int):
        # integer sequence
        npts = int(npts)
        return start + np.asarray(range(npts + 1)) * step
    else:
        npts = int(npts + feps)
        sequence = start + np.asarray(range(npts + 1)) * step
        # correct for possible overshot because of fuzz (from seq.R)
        if step > 0:
            return np.minimum(sequence, stop)
        else:
            return np.maximum(sequence, stop)


def add_mags(mags):
    """
    Returns a combined magnitude for a group of objects with ``mags``
    """
    return -2.5*np.log10((10**(-0.4*np.array(mags))).sum())


def dist_mod_from_distance(d):
    """
    mu = 5 * np.log10(d) - 5
    """

    mu = 5 * np.log10(d) - 5
    return mu


def distance_from_dist_mod(mu):
    """
    d = 10**(1 + mu / 5)
    """

    d = 10**(1 + mu / 5)
    return d


def telescope_diffraction_limit(aperture_size, wavelength, distance=None):
    """
    Returns the diffraction limit of a telescope

    Parameters
    ----------
    aperture_size : float
        [m] The diameter of the primary mirror

    wavelength : float
        [um] The wavelength for diffarction

    distance : float, optional
        Default is None. If ``distance`` is given, the transverse distance for
        the diffraction limit is returned in the same units as ``distance``


    Returns
    -------
    diff_limit : float
        [arcsec] The angular diffraction limit.
        If distance is not None, diff_limit is in the same units as distance

    """

    diff_limit = (((wavelength*u.um)/(aperture_size*u.m))*u.rad).to(u.arcsec).value

    if distance is not None:
        diff_limit *= distance / u.pc.to(u.AU)

    return diff_limit


def transverse_distance(angle, distance):
    """
    Turn an angular distance into a proper transverse distance

    Parameters
    ----------
    angle : float
        [arcsec] The on-sky angle

    distance : float
        The distance to the object. Units are arbitary

    Returns
    -------
    trans_distance : float
        proper transverse distance. Has the same Units as ``distance``

    """

    trans_distance = angle * distance * u.AU.to(u.pc)

    return trans_distance


def angle_in_arcseconds(distance, width):
    """
    Returns the angular distance of an object in arcseconds. Units must be consistent
    """

    return np.arctan2(width, distance)*u.rad.to(u.arcsec)


def bug_report():
    '''Get versions of dependencies for inclusion in bug report'''

    try:
        from importlib import import_module
    except ImportError:
        import_module = __import__

    packages = ["simcado", "astropy", "synphot", "numpy", "scipy",
                "poppy", "wget"]

    # Check Python version
    print("Python:\n", sys.version)
    print("")

    # Check package dependencies
    for package_name in packages:
        try:
            pkg = import_module(package_name)
            print(package_name, ": ", pkg.__version__)
        except ImportError:
            print(package_name, "could not be loaded.")

    # Check operating system
    import platform
    osinfo = platform.uname()
    print("")
    print("Operating system: ", osinfo.system)
    print("         Release: ", osinfo.release)
    print("         Version: ", osinfo.version)
    print("         Machine: ", osinfo.machine)


def find_file(filename, path=None, silent=False):
    """
    Find a file in search path

    Parameters
    ----------
    filename : str
        name of a file to look for
    path : list
        list of directories to search (default: ['./'])
    silent : bool
        if True, remain silent when file is not found

    Returns
    -------
    Absolute path of the file
    """

    import simcado as sim

    if path is None:
        path = sim.__search_path__

    if os.path.isabs(filename):
        # absolute path: only path to try
        trynames = [filename]
    else:
        # try to find the file in a search path
        trynames = [os.path.join(trydir, filename)
                    for trydir in path]

    for fname in trynames:
        if os.path.exists(fname):   # success
            # strip leading ./
            while fname[:2] == './':
                fname = fname[2:]
            return fname
        else:
            continue

    # no file found
    if not silent:
        print("File cannot be found: " + filename)
    return None


def zendist2airmass(zendist):
    '''Convert zenith distance to airmass

    Parameters
    ----------
    zenith distance : [deg]
       Zenith distance angle

    Returns
    -------
    airmass in sec(z) approximation
    '''
    return 1. / np.cos(np.deg2rad(zendist))


def airmass2zendist(airmass):
    '''Convert airmass to zenith distance

    Parameters
    ----------
    airmass : float (>= 1)

    Returns
    -------
    zenith distance in degrees
    '''

    return np.rad2deg(np.arccos(1/airmass))


def is_fits(filename):
    """
    Checks if file is a FITS file based on extension

    Parameters
    ----------
    filename : str

    Returns
    -------
    flag : bool

    """
    flag = False
    if filename is not None:
        if filename.split(".")[-1].lower() in "fits":
            flag = True

    return flag


def quantify(item, unit):
    """
    Ensure an item is a Quantity

    Parameters
    ----------
    item : int, float, array, list, Quantity
    unit : str, Unit

    Returns
    -------
    quant : Quantity

    """

    if isinstance(item, u.Quantity):
        quant = item.to(u.Unit(unit))
    else:
        quant = item * u.Unit(unit)
    return quant
