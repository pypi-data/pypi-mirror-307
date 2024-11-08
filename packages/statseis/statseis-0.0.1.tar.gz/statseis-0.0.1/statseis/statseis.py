"""
This module contains functions to statistically analyse seismicity (source parameters e.g. time, location, and magnitude).
Many functions require the renaming of earthquake catalog dataframe columns to: ID, MAGNITUDE, DATETIME, LON, LAT, DEPTH.
"""
import datetime as dt
import math
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.special as special
import scipy.stats as stats
from scipy.stats import gamma, poisson
import pyproj
from IPython.display import clear_output
import string
import matplotlib.collections
from matplotlib.lines import Line2D
import seaborn as sns
from pathlib import Path
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Circle
from collections import namedtuple
import shutil
from tqdm import tqdm
import statseis.utils as utils

colours = sns.color_palette("colorblind", 10)
colour_names = ['dark blue', 
               'orange',
               'green',
               'red',
               'dark pink',
               'brown',
               'light pink',
               'grey',
               'yellow',
               'light blue']
colour_dict = dict(zip(colour_names, colours))
colours

# plot_colors = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e', '#969696']
plot_colors = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d','#666666']
plot_color_dict = dict(zip(['teal', 'orange', 'purple', 'pink', 'green', 'yellow', 'brown', 'grey'], plot_colors))
# plot_color_dict

alphabet = string.ascii_lowercase
panel_labels = [letter + ')' for letter in alphabet]

scale_eq_marker = (lambda x: 10 + np.exp(1.1*x))

def gamma_law_MLE(t):
    """
    Calculate background seismicity rate based on the interevent time distribution. From CORSSA (originally in MATLAB), changed to Python (by me).
    """
    dt = np.diff(t)
    dt = dt[dt>0]
    T = sum(dt)
    N = len(dt)
    S = sum(np.log(dt))
    dg = 10**-4
    gam = np.arange(dg, 1-dg, dg) # increment from dg to 1-dg with a step of dg (dg:dg:dg-1 in matlab)
    ell = N*gam*(1-np.log(N)+np.log(T)-np.log(gam))+N*special.loggamma(gam)-gam*S # scipy gamma funcion
    ell_min = np.amin(ell)
    i = np.where(ell == ell_min)
    gam=gam[i]
    mu=N/T*gam
    return mu[0]

def freq_mag_dist(mag, mbin):
    """
    A basic frequency magnitude distribution analysis that requires an array of magnitudes (mag) and a chosen
    binning (mbin, we use 0.1). It returns magnitude bins, no. of events per bin, and cum. mag. distribution.
    [CORSSA, Lapins] - modified
    """
    mag = np.array(mag)
    minmag = math.floor(min(mag/mbin)) * mbin # Lowest bin
    maxmag = math.ceil(max(mag/mbin)) * mbin # Highest bin bin
    mi = np.arange(minmag, maxmag + mbin, mbin) # Make array of bins
    nbm = len(mi)
    cumnbmag = np.zeros(nbm) # Array for cumulative no. of events
    for i in range(nbm): # cumulative no. of events
        cumnbmag[i] = np.where(mag > mi[i] - mbin/2)[0].shape[0]
    nbmag = abs(np.diff(np.append(cumnbmag, 0))) # no. of events
    return mi, nbmag, cumnbmag

def b_val_max_likelihood(mag, mc, mbin=0.1):
    """
    Written by Sacah Lapins. This code calculates b values by maximum likelihood estimate. It takes in an array of magnitude (mag), a
    binning (mbin, we use 0.1) and a completeness magnitude (mc). It provides returns productivity (a), b value
    (b), and two estimates of uncertainty (aki_unc, shibolt_unc). [Aki 1965, Bender 1983, CORSSA, Lapins] - modified
    """
    mag = np.array(mag) # [me]
    mag_above_mc = mag[np.where(mag > round(mc,1)-mbin/2)[0]]# Magnitudes for events larger than cut-off magnitude mc
    n = mag_above_mc.shape[0] # No of. events larger than cut-off magnitude mc
    mbar = np.mean(mag_above_mc) # Mean magnitude for events larger than cut-off magnitude mc
    b = math.log10(math.exp(1)) / (mbar - (mc - mbin/2)) # b-value from Eq 2
    a = math.log10(n) + b * mc # 'a-value' for Eq 1
    aki_unc = b / math.sqrt(n) # Uncertainty estimate from Eq 3
    shibolt_unc = 2.3 * b**2 * math.sqrt(sum((mag_above_mc - mbar)**2) / (n * (n-1))) # Uncertainty estimate from Eq 4
#     return a, b, aki_unc, shibolt_unc # Return b-value and estimates of uncertainty
    return b

def Mc_by_maximum_curvature(mag, mbin=0.1, correction=0.2):
    """
    Written by Sacha Lapins. This code returns the magnitude of completeness estimates using the maximum curvature method. It takes a magnitude
    array (mag) and binning (mbin). [Wiemer & Wyss (2000), Lapins, CORSSA] - modified
    """
    mag = np.array(mag)
    this_fmd = freq_mag_dist(mag, mbin) # uses the fmd distribution (a previous function)
    maxc = this_fmd[0][np.argmax(this_fmd[1])] # Mag bin with highest no. of events
    return maxc + correction 
 
def Mc_by_goodness_of_fit(mag, mbin=0.1):
    """
    Written by Sacha Lapins. This code returns the magnitude of completeness estimates using a goodness of fit method. It takes a magnitude
    array (mag) and binning (mbin, we use 0.1). It returns the estimate (mc), the fmd (this_fmd[0]) and confidence level (R).
    The equation numbers refer to those in the CORSSA documentation(*). It defaults to maxc if confidence levels
    are not met. [Wiemer & Wyss (2000), Lapins, CORSSA] - modified
    """
    mag = np.array(mag)
    this_fmd = freq_mag_dist(mag, mbin) # FMD
    this_maxc = Mc_by_maximum_curvature(mag, mbin) # Runs the previous max curvature method first
    # Zeros to accommodate synthetic GR distributions for each magnitude bin
    a = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate a values from Eq 1
    b = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate b values from Eq 1 & 2
    R = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate R values from Eq 5
    for i in range(this_fmd[0].shape[0]): # Loop through each magnitude bin, using it as cut-off magnitude
        mi = round(this_fmd[0][i], 1) # Cut-off magnitude
        a[i], b[i], tmp1, tmp2 = b_val_max_likelihood(mag, mbin, mi) # a and b-values for this cut-off magnitude
        synthetic_gr = 10**(a[i] - b[i]*this_fmd[0]) # Synthetic GR for a and b
        Bi = this_fmd[2][i:] # B_i in Eq 5
        Si = synthetic_gr[i:] # S_i in Eq 5
        R[i] = (sum(abs(Bi - Si)) / sum(Bi)) * 100 # Eq 5
    R_to_test = [95, 90] # Confidence levels to test (95% and 90% conf levels)
    GFT_test = [np.where(R <= (100 - conf_level)) for conf_level in R_to_test] # Test whether R within confidence level
    for i in range(len(R_to_test)+1): # Loop through and check first cut-off mag within confidence level
        # If no GR distribution fits within confidence levels then use MAXC instead
        if i == (len(R_to_test) + 1):
            mc = this_maxc
            print("No fits within confidence levels, using MAXC estimate")
            break
        else:
            if len(GFT_test[i][0]) > 0:
                mc = round(this_fmd[0][GFT_test[i][0][0]], 1) # Use first cut-off magnitude within confidence level
                break
#     return mc, this_fmd[0], R
    return mc
 
def Mc_by_b_value_stability(mag, mbin=0.1, dM = 0.4, min_mc = -3, return_b=False):
    """
    Written by Sacha Lapins. This code returns the magnitude of completeness estimates using a b value stability method. It takes a magnitude
    array (mag), binning (mbin, we use 0.1), number of magnitude units to calculate a rolling average b value over (dM,
    we use 0.4) and a minimum mc to test (min_mc). The outputs are a completeness magnitude (mc), frequency magnitude
    distribution (this_fmd[0]), the b value calculated for this mc and average b(*) (b and b_average) and b value uncertainty
    estimate (shibolt_unc). The equation numbers refer to those in the CORSSA documentation(*). It defaults to maxc if
    confidence levels are not met.[ Cao & Gao (2002), Lapins, CORSSA]. - modified
    """
    mag = np.array(mag)
    this_fmd = freq_mag_dist(mag, mbin) # FMD
    this_maxc = Mc_by_maximum_curvature(mag, mbin) # Needed further down
    # Zeros to accommodate synthetic GR distributions for each magnitude bin
    a = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate a values from Eq 1
    b = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate b values from Eq 1 & 2
    b_avg = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate b values from Eq 1 & 2
    shibolt_unc = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate uncertainty values from Eq 4
    for i in range(this_fmd[0].shape[0]): # Loop through each magnitude bin, using it as cut-off magnitude
        mi = round(this_fmd[0][i], 1) # Cut-off magnitude
        if this_fmd[2][i] > 1:
            a[i], b[i], tmp1, shibolt_unc[i] = b_val_max_likelihood(mag, mbin, mi) # a and b-values for this cut-off magnitude
        else:
            a[i] = np.nan
            b[i] = np.nan
            shibolt_unc[i] = np.nan
    no_bins = round(dM/mbin)
    check_bval_stability = []
    for i in range(this_fmd[0].shape[0]): # Loop through again, calculating rolling average b-value over following dM magnitude units
        if i >= this_fmd[0].shape[0] - (no_bins + 1):
            b_avg[i] = np.nan
            next
        if any(np.isnan(b[i:(i+no_bins+1)])):
            b_avg[i] = np.nan
            check_bval_stability.append(False)
        else:
            b_avg[i] = np.mean(b[i:(i+no_bins+1)])
            check_bval_stability.append(abs(b_avg[i] - b[i]) <= shibolt_unc[i])
    if any(check_bval_stability):
        bval_stable_points = this_fmd[0][np.array(check_bval_stability)]
        mc = round(min(bval_stable_points[np.where(bval_stable_points > min_mc)[0]]), 1) # Completeness mag is first mag bin that satisfies Eq 6
    else:
        mc = this_maxc # If no stability point, use MAXC
#     return mc, this_fmd[0], b, b_avg, shibolt_unc
    return mc, b#, this_fmd[0], b, b_avg, shibolt_unc

def fmd(mag, mbin):
    """
    Written by Sacha Lapins.
    """
    minmag = math.floor(min(mag/mbin)) * mbin # Lowest bin
    maxmag = math.ceil(max(mag/mbin)) * mbin # Highest bin bin
    mi = np.arange(minmag, maxmag + mbin, mbin) # Make array of bins
    nbm = len(mi)
    cumnbmag = np.zeros(nbm) # Array for cumulative no. of events
    for i in range(nbm): # cumulative no. of events
        cumnbmag[i] = np.where(mag > mi[i] - mbin/2)[0].shape[0]
    nbmag = abs(np.diff(np.append(cumnbmag, 0))) # no. of events
    return mi, nbmag, cumnbmag
print('FMD Function Loaded')

def b_est(mag, mbin, mc):
    """
    Written by Sacha Lapins.
    """
    mag_above_mc = mag[np.where(mag > round(mc,1)-mbin/2)[0]]# Magnitudes for events larger than cut-off magnitude mc
    n = mag_above_mc.shape[0] # No of. events larger than cut-off magnitude mc
    mbar = np.mean(mag_above_mc) # Mean magnitude for events larger than cut-off magnitude mc
    b = math.log10(math.exp(1)) / (mbar - (mc - mbin/2)) # b-value from Eq 2
    a = math.log10(n) + b * mc # 'a-value' for Eq 1
    aki_unc = b / math.sqrt(n) # Uncertainty estimate from Eq 3
    shibolt_unc = 2.3 * b**2 * math.sqrt(sum((mag_above_mc - mbar)**2) / (n * (n-1))) # Uncertainty estimate from Eq 4
    return a, b, aki_unc, shibolt_unc # Return b-value and estimates of uncertainty
print('MLM B Function Loaded')

def get_maxc(mag, mbin):
    """
    Written by Sacha Lapins.
    """
    this_fmd = fmd(mag, mbin) # uses the fmd distribution (a previous function)
    maxc = this_fmd[0][np.argmax(this_fmd[1])] # Mag bin with highest no. of events
    return round(maxc, 1)
print('MAXC Function Loaded')

def get_mbs(mag, mbin, dM = 0.4, min_mc = -3):
    """
    Written by Sacha Lapins.
    """
    this_fmd = fmd(mag, mbin) # FMD
    this_maxc = get_maxc(mag, mbin) # Needed further down
    # Zeros to accommodate synthetic GR distributions for each magnitude bin
    a = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate a values from Eq 1
    b = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate b values from Eq 1 & 2
    b_avg = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate b values from Eq 1 & 2
    shibolt_unc = np.zeros(this_fmd[0].shape[0]) # Pre-allocate array to accommodate uncertainty values from Eq 4
    for i in range(this_fmd[0].shape[0]): # Loop through each magnitude bin, using it as cut-off magnitude
        mi = round(this_fmd[0][i], 1) # Cut-off magnitude
        if this_fmd[2][i] > 1:
            a[i], b[i], tmp1, shibolt_unc[i] = b_est(mag, mbin, mi) # a and b-values for this cut-off magnitude
        else:
            a[i] = np.nan
            b[i] = np.nan
            shibolt_unc[i] = np.nan
    no_bins = round(dM/mbin)
    check_bval_stability = []
    for i in range(this_fmd[0].shape[0]): # Loop through again, calculating rolling average b-value over following dM magnitude units
        if i >= this_fmd[0].shape[0] - (no_bins + 1):
            b_avg[i] = np.nan
            next
        if any(np.isnan(b[i:(i+no_bins+1)])):
            b_avg[i] = np.nan
            check_bval_stability.append(False)
        else:
            b_avg[i] = np.mean(b[i:(i+no_bins+1)])
            check_bval_stability.append(abs(b_avg[i] - b[i]) <= shibolt_unc[i])
    if any(check_bval_stability):
        bval_stable_points = this_fmd[0][np.array(check_bval_stability)]
        mc = round(min(bval_stable_points[np.where(bval_stable_points > min_mc)[0]]), 1) # Completeness mag is first mag bin that satisfies Eq 6
    else:
        mc = this_maxc # If no stability point, use MAXC
        mc = np.nan # my addition
    return mc, this_fmd[0], b, b_avg, shibolt_unc
print('MBS Funtion Loaded')

def get_Mcs_400(mainshocks_file, earthquake_catalogue, catalogue_name, start_radius=10, inc=5, max_r=50, min_n=400):
    """
    Calculate Mc using b-value stability (Mbass) and maximumum curvature (Maxc) around mainshock epicenters.
    """
    date = str(dt.datetime.now().date().strftime("%y%m%d"))
    Mbass = []
    Maxc = []
    n_local_cat = []
    radii = []
    Mbass_b = []
    Maxc_b = []
    Gft_Mc = []
    i = 1
    for mainshock in tqdm(mainshocks_file.itertuples(), total=len(mainshocks_file)):
        # print(f"{catalogue_name}")
        # print(f"{i} of {len(mainshocks_file)} mainshocks")
        radius = start_radius
        local_cat = create_local_catalogue(mainshock, earthquake_catalogue, catalogue_name=catalogue_name, save=False, radius_km=radius)
        while len(local_cat)<min_n:
            if radius <max_r:
                radius+=inc
                local_cat = create_local_catalogue(mainshock, earthquake_catalogue, catalogue_name=catalogue_name, save=False, radius_km=radius)
            elif radius>=max_r:
                break
        Mbass_mc = get_mbs(np.array(local_cat['MAGNITUDE']), mbin=0.1)[0]
        Mbass.append(Mbass_mc)
        Maxc_mc = get_maxc(local_cat['MAGNITUDE'], mbin=0.1)+0.2
        Maxc.append(Maxc_mc)
        n_local_cat.append(len(local_cat))
        radii.append(radius)
        Mbass_b.append(b_est(np.array(local_cat['MAGNITUDE']), mbin=0.1, mc=Mbass_mc)[1])
        Maxc_b.append(b_est(np.array(local_cat['MAGNITUDE']), mbin=0.1, mc=Maxc_mc)[1])
        i+=1
        clear_output(wait=True)
    mainshocks_file[f'Mbass_50'] = Mbass
    mainshocks_file[f'b_Mbass_50'] = Mbass_b
    mainshocks_file[f'Mc'] = Mbass
    mainshocks_file[f'Maxc_50'] = Maxc
    mainshocks_file[f'b_Maxc_50'] = Maxc_b
    mainshocks_file[f'n_for_Mc_50'] = n_local_cat
    mainshocks_file[f'radii_50'] = radii
    # mainshocks_file[f'Mbass_{max_r}'] = Mbass
    # mainshocks_file[f'b_Mbass_{max_r}'] = Mbass_b
    # mainshocks_file[f'Mc'] = Mbass
    # mainshocks_file[f'Maxc_{max_r}'] = Maxc
    # mainshocks_file[f'b_Maxc_{max_r}'] = Maxc_b
    # mainshocks_file[f'n_for_Mc_{max_r}'] = n_local_cat
    # mainshocks_file[f'radii_{max_r}'] = radii
    return mainshocks_file

def get_Mc_expanding_r(mainshocks_file, earthquake_catalogue, catalogue_name, start_radius=10, inc=5, max_r=100, min_n=1000):
    """
    Calculate Mc using b-value stability (Mbass) and maximumum curvature (Maxc) around mainshock epicenters
    at each point for an expanding radius.
    """
    
    mainshock_results = []
    for mainshock in tqdm(mainshocks_file.itertuples(), total=len(mainshocks_file)):
        results_list = []
        for radius in np.arange(start_radius,max_r,inc):
            if radius==0:
                radius+=1

            local_cat = create_local_catalogue(mainshock, earthquake_catalogue, catalogue_name=catalogue_name, save=False, radius_km=radius)
            # print(radius, len(local_cat))
            try:
                Mbass_mc = get_mbs(np.array(local_cat['MAGNITUDE']), mbin=0.1)[0]
                Maxc_mc = get_maxc(np.array(local_cat['MAGNITUDE']), mbin=0.1)+0.2

                results_dict = {'radii':radius,
                                'n_local_cat':len(local_cat),
                                'Mbass':Mbass_mc,
                                'Maxc':Maxc_mc,
                                'b_Mbass':b_est(np.array(local_cat['MAGNITUDE']), mbin=0.1, mc=Mbass_mc)[1],
                                'b_Maxc':b_est(np.array(local_cat['MAGNITUDE']), mbin=0.1, mc=Maxc_mc)[1]}
                
            except:
                results_dict = {'radii':radius,
                                'n_local_cat':len(local_cat),
                                'Mbass':np.nan,
                                'Maxc':np.nan,
                                'b_Mbass':np.nan,
                                'b_Maxc':np.nan}

            results_list.append(results_dict)

        mainshock_results.append({'ID':mainshock.ID, 'df':pd.DataFrame.from_dict(results_list)})
        clear_output(wait=True)

    return mainshock_results

def apply_Mc_cut(earthquake_catalogue):
    mag = np.array(earthquake_catalogue['MAGNITUDE'])
    Mc = get_mbs(mag, mbin=0.1)[0]
    earthquake_catalogue = earthquake_catalogue.loc[earthquake_catalogue['MAGNITUDE']>= Mc].copy()
    return earthquake_catalogue

def plot_fmd(local_cat, save_path=None, ID=np.nan, radius=50):

    local_cat = local_cat.loc[local_cat['DISTANCE_TO_MAINSHOCK']<radius].copy()
    print(len(local_cat))
    magnitudes = np.array(local_cat['MAGNITUDE'])
    bins = np.arange(math.floor(magnitudes.min()), math.ceil(magnitudes.max()), 0.1)
    values, base = np.histogram(magnitudes, bins=bins)
    cumulative = np.cumsum(values)
    Mc, this_fmd, b, b_avg, shibolt_unc = get_mbs(mag=magnitudes, mbin=0.1)
    a, b_value, _a, _b = b_est(mag=magnitudes, mbin=0.1, mc=Mc)
    N = [10**(a-b_value*M) for M in this_fmd]
    ratio_above_Mc = round(100*len(magnitudes[magnitudes>Mc])/len(magnitudes))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot([], [], label=f"ID: {ID}", marker=None, linestyle='')
    ax.plot([], [], label=f'{ratio_above_Mc}% above $M_c$', marker=None, linestyle='')
    ax.plot([], [], label=f'N: {len(magnitudes)}', marker=None, linestyle='')
    ax.plot([], [], label=f'Radius: {radius}', marker=None, linestyle='')
    ax.step(base[:-1], len(magnitudes)-cumulative, color='black')
    ax.axvline(x=Mc, linestyle='--', label=r'$M_{c}$: ' + str(round(Mc,1)), color=plot_colors[0])
    ax.plot(this_fmd, N, label=f'b: {round(b_value,2)}',  color=plot_colors[1])

    ax.set_xlabel('Magnitude')
    ax.set_ylabel('N')
    ax.set_yscale('log')
    ax.legend()
    if save_path!=None:
        plt.savefig(save_path)

def plot_FMD_mainshock_subset(mshock_file, name, outfile_name, catalog, stations=None):
    Path(f'../outputs/{outfile_name}/FMD').mkdir(parents=True, exist_ok=True)
    for mainshock in tqdm(mshock_file.itertuples(), total=len(mshock_file)):
        local_cat = create_local_catalogue(mainshock, earthquake_catalogue=catalog, catalogue_name=name, radius_km=100)
        plot_local_cat(mainshock=mainshock, local_cat=local_cat, catalogue_name=name, Mc_cut=False, stations=stations, earthquake_catalogue=catalog,
                    min_days=math.ceil(local_cat['DAYS_TO_MAINSHOCK'].max()), max_days=0,
                    radius_km=mainshock.radii_50, box_halfwidth_km=100, aftershock_days=math.floor(local_cat['DAYS_TO_MAINSHOCK'].min()))
        print(mainshock.n_for_Mc_50)
        plot_fmd(local_cat, save_path=f'../outputs/{outfile_name}/FMD/{mainshock.ID}.png', ID=mainshock.ID, radius=mainshock.radii_50)
        plt.close()
        clear_output(wait=True)

def move_plots(mshock_file, catalog, plot_type, out_folder_name):
    for mainshock in mshock_file.itertuples():
        filename = f'{mainshock.ID}.png'

        source_folder = f'../outputs/{catalog}/{plot_type}/'

        destination_folder = f'../outputs/{out_folder_name}/{plot_type}'
        Path(destination_folder).mkdir(parents=True, exist_ok=True)

        source_file = os.path.join(source_folder, filename)
        
        if os.path.exists(source_file):
            destination_file = os.path.join(destination_folder, filename)
            
            shutil.copyfile(source_file, destination_file)
            print(f"File '{filename}' copied to '{destination_folder}'")
        else:
            print(f"File '{filename}' not found in '{source_folder}'")

def mainshock_selections_counts(mainshock_file):
    print('Total', len(mainshock_file))
    for s in mainshock_file['Selection'].unique():
        print(s, len(mainshock_file.loc[mainshock_file['Selection']==s]))

def select_within_box(LON, LAT, df, r):
    min_box_lon, min_box_lat = utils.add_distance_to_position_pyproj(LON, LAT, -r, -r)
    max_box_lon, max_box_lat = utils.add_distance_to_position_pyproj(LON, LAT, r, r)

    selections = df.loc[(df['LON']>= min_box_lon) &\
                        (df['LON']<= max_box_lon) &\
                        (df['LAT']>= min_box_lat) &\
                        (df['LAT']<= max_box_lat)
                        ].copy()

    selections['DISTANCE_TO_MAINSHOCK'] = utils.calculate_distance_pyproj_vectorized(LON, LAT, selections['LON'],  selections['LAT'])
    return selections

def iterable_mainshock(ID, mainshock_file):
    mainshock = mainshock_file.loc[mainshock_file['ID']==ID].copy()
    RowTuple = namedtuple('RowTuple', mainshock.columns)
    mainshock = [RowTuple(*row) for row in mainshock.values][0]
    return mainshock

def load_local_catalogue(mainshock, catalogue_name='unspecified'):
    local_catalogue = pd.read_csv(f'../data/{catalogue_name}/local_catalogues/{mainshock.ID}.csv')
    utils.string_to_datetime_df(local_catalogue)
    return local_catalogue

def create_local_catalogue(mainshock, earthquake_catalogue, catalogue_name, radius_km = 30, box=False, save=True):

    mainshock_LON = mainshock.LON
    mainshock_LAT = mainshock.LAT
    mainshock_DATETIME = mainshock.DATETIME

    box_halfwidth_km = radius_km

    local_catalogue = select_within_box(mainshock.LON, mainshock.LAT, earthquake_catalogue, r=box_halfwidth_km)
    # min_box_lon, min_box_lat = utils.add_distance_to_position_pyproj(mainshock_LON, mainshock_LAT, -box_halfwidth_km, -box_halfwidth_km)
    # max_box_lon, max_box_lat = utils.add_distance_to_position_pyproj(mainshock_LON, mainshock_LAT, box_halfwidth_km, box_halfwidth_km)

    # local_catalogue = earthquake_catalogue.loc[
    #                                 (earthquake_catalogue['LON']>= min_box_lon) &\
    #                                 (earthquake_catalogue['LON']<= max_box_lon) &\
    #                                 (earthquake_catalogue['LAT']>= min_box_lat) &\
    #                                 (earthquake_catalogue['LAT']<= max_box_lat)
    #                                 ].copy()
    local_catalogue['DISTANCE_TO_MAINSHOCK'] = utils.calculate_distance_pyproj_vectorized(mainshock_LON, mainshock_LAT, local_catalogue['LON'],  local_catalogue['LAT'])

    if box==False:
        local_catalogue = local_catalogue.loc[local_catalogue['DISTANCE_TO_MAINSHOCK']<radius_km].copy()

    local_catalogue['DAYS_TO_MAINSHOCK'] = (mainshock_DATETIME - local_catalogue['DATETIME']).apply(lambda d: (d.total_seconds()/(24*3600)))

    if save==True:
        Path(f'../data/{catalogue_name}/local_catalogues/').mkdir(parents=True, exist_ok=True)
        local_catalogue.to_csv(f'../data/{catalogue_name}/local_catalogues/{mainshock.ID}.csv', index=False)
    return local_catalogue

def create_spatial_plot(mainshock, local_cat, catalogue_name, Mc_cut, min_days=365, max_days=0, radius_km=10, save=True):
    
    mainshock_ID = mainshock.ID
    mainshock_M = mainshock.MAGNITUDE
    mainshock_LON = mainshock.LON
    mainshock_LAT = mainshock.LAT
    mainshock_DATETIME = mainshock.DATETIME

    box_halfwidth_km = 30
    min_box_lon, min_box_lat = utils.add_distance_to_position_pyproj(mainshock_LON, mainshock_LAT, -box_halfwidth_km, -box_halfwidth_km)
    max_box_lon, max_box_lat = utils.add_distance_to_position_pyproj(mainshock_LON, mainshock_LAT, box_halfwidth_km, box_halfwidth_km)

    aftershocks = local_cat.loc[(local_cat['DAYS_TO_MAINSHOCK'] < 0) &\
                                (local_cat['DAYS_TO_MAINSHOCK'] > -20)].copy()

    local_cat = local_cat.loc[(local_cat['DAYS_TO_MAINSHOCK'] < min_days) &\
                              (local_cat['DAYS_TO_MAINSHOCK'] > max_days)].copy()

    magnitude_fours = local_cat.loc[local_cat['MAGNITUDE']>=4].copy()

    fig = plt.figure()

    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax.set_title(f"ID: {mainshock_ID}", loc='right')
    
    # ax.set_extent(utils.get_catalogue_extent(local_cat, buffer=0.025), crs=ccrs.PlateCarree())
    ax.set_extent([min_box_lon, max_box_lon, min_box_lat, max_box_lat], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.OCEAN, edgecolor='none')
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, zorder=0)
    gl.top_labels = False
    gl.right_labels = False

    ax.scatter(mainshock_LON, mainshock_LAT, color='red', s=np.exp(mainshock_M), marker='*', label=f'$M_w$ {mainshock_M} mainshock')
    new_LON, new_LAT = utils.add_distance_to_position_pyproj(mainshock_LON, mainshock_LAT, radius_km, 0)
    radius_degrees = new_LON - mainshock_LON
    circle = Circle((mainshock_LON, mainshock_LAT), radius_degrees, edgecolor='r', facecolor='none', transform=ccrs.PlateCarree())
    ax.add_patch(circle)
    z = np.exp(local_cat['MAGNITUDE'])
    local_cat = ax.scatter(local_cat['LON'], local_cat['LAT'], s=z, #c=utils.datetime_to_decimal_year(local_cat['DATETIME']),
                c=local_cat['DAYS_TO_MAINSHOCK'], label=f'{len(local_cat)} earthquakes (1 year prior)', alpha=0.9)
    cbar = fig.colorbar(local_cat, ax=ax)
    cbar.set_label('Days to mainshock') 
    z = np.exp(aftershocks['MAGNITUDE'])
    ax.scatter(aftershocks['LON'], aftershocks['LAT'], s=z, #c=utils.datetime_to_decimal_year(local_cat['DATETIME']),
                color='grey', label=f'{len(aftershocks)} aftershocks (20 days post)', alpha=0.3, zorder=0)
    # ax.scatter(magnitude_fours['LON'], magnitude_fours['LAT'], s=z, #c=utils.datetime_to_decimal_year(local_cat['DATETIME']),
    #             c='black', label=f'{len(magnitude_fours)} $M_w$ $\ge$ 4 (1 year prior)', alpha=0.9)
    
    ax.legend(loc='lower right', bbox_to_anchor=(0.575,1))
    # ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    # ax.legend()
    ax.set_xlabel('LON')
    ax.set_ylabel('LAT')
    
    if save==True:
        if Mc_cut==False:
            Path(f"../outputs/{catalogue_name}/spatial_plots").mkdir(parents=True, exist_ok=True)
            plt.savefig(f"../outputs/{catalogue_name}/spatial_plots/{mainshock_ID}_{radius_km}km_{min_days}_to_{max_days}.png")
        elif Mc_cut==True:
            Path(f"../outputs/{catalogue_name}/Mc_cut/spatial_plots").mkdir(parents=True, exist_ok=True)
            plt.savefig(f"../outputs/{catalogue_name}/Mc_cut/spatial_plots/{mainshock_ID}_{radius_km}km_{min_days}_to_{max_days}.png")
    plt.show()

def plot_local_cat(mainshock, local_cat, earthquake_catalogue, catalogue_name, Mc_cut, min_days=365, max_days=0, radius_km=10, save=True, 
                   box_halfwidth_km=30, aftershock_days=-20, foreshock_days=20, stations=None):
    
    event_marker_size = (lambda x: 50+10**(x/1.25))

    mainshock_ID = mainshock.ID
    mainshock_M = mainshock.MAGNITUDE
    mainshock_LON = mainshock.LON
    mainshock_LAT = mainshock.LAT
    mainshock_DATETIME = mainshock.DATETIME

    local_cat = create_local_catalogue(mainshock, catalogue_name=catalogue_name, earthquake_catalogue=earthquake_catalogue, radius_km=box_halfwidth_km, box=True)

    min_box_lon, min_box_lat = utils.add_distance_to_position_pyproj(mainshock_LON, mainshock_LAT, -box_halfwidth_km, -box_halfwidth_km)
    max_box_lon, max_box_lat = utils.add_distance_to_position_pyproj(mainshock_LON, mainshock_LAT, box_halfwidth_km, box_halfwidth_km)

    local_cat = local_cat.loc[(local_cat['DAYS_TO_MAINSHOCK'] < min_days) &\
                              (local_cat['DAYS_TO_MAINSHOCK']!=0) &\
                                     (local_cat['DAYS_TO_MAINSHOCK'] > aftershock_days)].copy()
    inside = local_cat.loc[(local_cat['DISTANCE_TO_MAINSHOCK']<radius_km)].copy()
    outside = local_cat.loc[(local_cat['DISTANCE_TO_MAINSHOCK']>=radius_km)].copy()

    aftershocks = inside.loc[(inside['DAYS_TO_MAINSHOCK'] < 0) &\
                             (inside['DAYS_TO_MAINSHOCK'] > aftershock_days)].copy()

    foreshocks = inside.loc[(inside['DAYS_TO_MAINSHOCK'] < foreshock_days) &\
                               (inside['DAYS_TO_MAINSHOCK'] > 0)].copy()
    
    # outside = local_cat.loc[(local_cat['DISTANCE_TO_MAINSHOCK']>=radius_km) &\
    #                            (local_cat['DAYS_TO_MAINSHOCK'] < min_days) &\
    #                           (local_cat['DAYS_TO_MAINSHOCK'] > 0)].copy()
    
    # outside_foreshocks = local_cat.loc[(local_cat['DISTANCE_TO_MAINSHOCK']>=radius_km) &\
    #                            (local_cat['DAYS_TO_MAINSHOCK'] < foreshock_days) &\
    #                           (local_cat['DAYS_TO_MAINSHOCK'] > 0)].copy()
    
    modelling_events = inside.loc[(inside['DAYS_TO_MAINSHOCK'] < min_days) &\
                                  (inside['DAYS_TO_MAINSHOCK'] > 0)].copy()
    
    # modelling_plus_outside = pd.concat([modelling_events, outside])
    modelling_plus_aftershocks = pd.concat([modelling_events, aftershocks])

    magnitude_fours = local_cat.loc[local_cat['MAGNITUDE']>=4].copy()

    mainshock_colour = 'black'

    # vmin, vmax = max_days, min_days
    vmin, vmax = aftershock_days, min_days

    fig = plt.figure(figsize=(8,8))
    gs = fig.add_gridspec(3,3)

    ax = fig.add_subplot(gs[0, :])
    # ax = fig.add_subplot(121)
    ax.set_title('a)', fontsize=20, loc='left')
    ax.set_title(f"ID: {mainshock_ID} - {mainshock.DATETIME.strftime('%b %d %Y')} - {catalogue_name}", loc='right')

    ax.scatter(0, mainshock.MAGNITUDE, marker='*', s = event_marker_size(mainshock.MAGNITUDE), #s=400, 
               color=mainshock_colour, label=r'$M_{w}$ ' + str(mainshock.MAGNITUDE) + ' Mainshock', zorder=3)
    ax.axvline(x=foreshock_days, color='red', linestyle='--', 
                                    # label = f"{foreshock_days}-day foreshock window",
                                    zorder=4)
    ax.set_xlabel('Days to mainshock', fontsize=20)
    ax.set_ylabel('Magnitude', fontsize=20)
    # ax.set_xlim(-25,365+20)
    try:
        max_mag = math.ceil(max([mainshock.MAGNITUDE, max(local_cat['MAGNITUDE'])]))
        min_mag = round(min(local_cat['MAGNITUDE']))
        mid_mag = max_mag - (max_mag - min_mag)/2
        mag_y_ticks = [min_mag, mid_mag, max_mag]
        ax.set_yticks(mag_y_ticks)
        ax.set_yticklabels(mag_y_ticks)
    except:
        print('Auto Mag y-ticks, not manual')

    ax.invert_xaxis()

    # if len(modelling_events) >0:
    #     # ax.set_yticks(np.arange(math.floor(min(local_cat['MAGNITUDE'])), math.ceil(mainshock.MAGNITUDE), 1))
    #     ax.scatter(modelling_events['DAYS_TO_MAINSHOCK'], modelling_events['MAGNITUDE'], #s=6*np.exp(modelling_events['MAGNITUDE']),
    #                s=event_marker_size(modelling_events['MAGNITUDE']), vmin=vmin, vmax=vmax, ec='white', linewidth=0.25,
    #                label= f'{len(modelling_events)- len(foreshocks)} modelling events',
    #                                     c=modelling_events['DAYS_TO_MAINSHOCK'], alpha=0.5,  zorder=1)
    # outside_plus_foreshocks = pd.concat([outside, outside_foreshocks])
    if len(inside) > 0:
        ax.scatter(inside['DAYS_TO_MAINSHOCK'], inside['MAGNITUDE'],
            s= event_marker_size(inside['MAGNITUDE']), ec='white', linewidth=0.25,
               c=inside['DAYS_TO_MAINSHOCK'], 
               alpha=0.75, zorder=1)
    if len(foreshocks) > 0:
        ax.scatter(foreshocks['DAYS_TO_MAINSHOCK'], foreshocks['MAGNITUDE'],
                    # s=6*np.exp(foreshocks['MAGNITUDE']),
                    s = event_marker_size(foreshocks['MAGNITUDE']), ec='white', linewidth=0.25,
                   label= fr"$N_obs$: {len(foreshocks)}", color='red', alpha=0.75, zorder=2)
    if len(outside) > 0:
        ax.scatter(outside['DAYS_TO_MAINSHOCK'], outside['MAGNITUDE'], 
            #    s=np.exp(aftershocks['MAGNITUDE']),
            s = event_marker_size(outside['MAGNITUDE']), ec='white', linewidth=0.25,
               label= f"Aftershocks: {len(outside)}", color='grey', alpha=0.25, zorder=0)

    
    ax2 = ax.twinx()
    cut_off_day=min_days
    foreshock_window=foreshock_days
    range_scaler=100
    modelling_plus_foreshocks = pd.concat([modelling_events, foreshocks])
    # sliding_window_points_full = np.array(range((-cut_off_day+foreshock_window)*range_scaler, 0*range_scaler+1, 1))/range_scaler*-1
    sliding_window_points_full = np.array(range((-cut_off_day+foreshock_window), 0+1, 1))/-1
    sliding_window_counts_full = np.array([len(modelling_plus_foreshocks[(modelling_plus_foreshocks['DAYS_TO_MAINSHOCK'] > point) &\
                                                                          (modelling_plus_foreshocks['DAYS_TO_MAINSHOCK'] <= (point + foreshock_window))]) for point in sliding_window_points_full])
    average = np.mean
    # sliding_window_distances = np.array([average(modelling_plus_foreshocks.loc[(modelling_plus_foreshocks['DAYS_TO_MAINSHOCK'] > point) &\
    #                                                                 (modelling_plus_foreshocks['DAYS_TO_MAINSHOCK'] <= (point + foreshock_window)), 'DISTANCE_TO_MAINSHOCK']) for point in sliding_window_points_full])

    # sliding_window_df_full = pd.DataFrame({'points':sliding_window_points_full,
    #                                        'counts':sliding_window_counts_full,
    #                                        'distances':sliding_window_distances})
    
    ax2.step(sliding_window_points_full, sliding_window_counts_full, zorder=6,
            #  c=sliding_window_points_full.astype(int),
             color='black', alpha=0.7,
             label='20-day count')
    # ax2.axhline(y=len(foreshocks), color='red', alpha=0.5, label = r'$N_{obs}$', zorder=0)
    ax2.set_ylabel('20-day count')
    # ax.set_zorder(ax2.get_zorder()+1)
    ax.patch.set_visible(False)
    try:
        y_min, y_max = round(sliding_window_counts_full.min()), round(sliding_window_counts_full.max())
        y_mid = round(y_min + (y_max - y_min)/2)
        y_ticks = [y_min, y_mid, y_max]
        ax2.set_yticks(y_ticks)
        ax2.set_yticklabels(y_ticks)
    except:
        print('Could not update yticks')

    ax = fig.add_subplot(gs[1:3, :], projection=ccrs.PlateCarree())
    ax.set_title('b)', fontsize=20, loc='left')

    # ax = fig.add_subplot(212, projection=ccrs.PlateCarree())
    
    # ax.set_extent(utils.get_catalogue_extent(local_cat, buffer=0.025), crs=ccrs.PlateCarree())
    ax.set_extent([min_box_lon, max_box_lon, min_box_lat, max_box_lat], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.OCEAN, edgecolor='none')
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, zorder=0)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 15}
    gl.ylabel_style = {'size': 15}
    gl.xlines = False
    gl.ylines = False
    # gl.ylocator = mticker.FixedLocator([min_box_lat, max_box_lat])
    # gl.xlocator = mticker.FixedLocator([min_box_lon, max_box_lon])

    plot_scalar=6
    ax.scatter(mainshock_LON, mainshock_LAT, color=mainshock_colour, s=event_marker_size(mainshock_M), marker='*', label=f'$M_w$ {mainshock_M} mainshock')
    new_LON, new_LAT = utils.add_distance_to_position_pyproj(mainshock_LON, mainshock_LAT, radius_km, 0)
    radius_degrees = new_LON - mainshock_LON
    circle = Circle((mainshock_LON, mainshock_LAT), radius_degrees, edgecolor='r', facecolor='none', transform=ccrs.PlateCarree())
    ax.add_patch(circle)
    if len(outside)>0:
        ax.scatter(outside['LON'], outside['LAT'], s=event_marker_size(outside['MAGNITUDE']), ec='white', linewidth=0.25,
                   color='grey', alpha=0.25, zorder=0)
    if len(inside) > 0:
        local_cat_plot = ax.scatter(inside['LON'], inside['LAT'], s=event_marker_size(inside['MAGNITUDE']), zorder=1, ec='white', linewidth=0.25,
                                    c=inside['DAYS_TO_MAINSHOCK'], label=f'inside: {len(inside)}', alpha=0.75, vmin=vmin, vmax=vmax) 
        cbar = fig.colorbar(local_cat_plot, ax=ax) #, shrink=0.5
        cbar.set_label('Days to mainshock')
    if len(foreshocks) > 0:
        ax.scatter(foreshocks['LON'], foreshocks['LAT'], s=event_marker_size(foreshocks['MAGNITUDE']),
                   color='red', alpha=0.75, ec='white', linewidth=0.25, zorder=2)
    
    if stations is not None:
        stations = select_within_box(mainshock.LON, mainshock.LAT, df=stations, r=box_halfwidth_km)
        ax.scatter(stations['LON'], stations['LAT'], ec='white', linewidth=0.25, marker='^', color=plot_color_dict['orange'], zorder=100000)
    ax.set_xlabel('LON')
    ax.set_ylabel('LAT')

    cmap = matplotlib.cm.get_cmap('Spectral')
    rgba = cmap(0.5)
    
    custom_legend_items = [Line2D([], [], color='red', marker='*', markersize=10,
                                label=f'$M_w$ {mainshock_M} mainshock', linestyle='None'),
                        Line2D([], [], color=rgba, marker='o', markersize=10, 
                                label=f'{len(modelling_events)} events 1 year prior)', linestyle='None'),
                        Line2D([], [], color='grey', marker='o', markersize=10, 
                                label=f'{len(aftershocks)} aftershocks (20 days post)', linestyle='None')
                        #    Line2D([0], [0], color='black', lw=0, marker='', label=f"Spearmanr: {round(stats_dict['QTM_12_spearmanr'],2)}"),
                        #    Line2D([0], [0], color='black', lw=0, marker='', label=f"Spearmanr: {round(stats_dict['SCSN_spearmanr'],2)}")
                        ]
    # ax.legend(handles=custom_legend_items, loc='lower right', bbox_to_anchor=(0.575,1))
    # ax.legend(loc='lower right', bbox_to_anchor=(0.575,1))

    if save==True:
        Path(f"../outputs/{catalogue_name}/data_plots").mkdir(parents=True, exist_ok=True)
        plt.savefig(f"../outputs/{catalogue_name}/data_plots/{mainshock_ID}.png")
    plt.show()

def add_distance_to_position_pyproj(lon, lat, distance_km_horizontal, distance_km_vertical):
    """
    Returns the a point shifted in km by the value of its arguments using the Pyproj module
    """
    geod = pyproj.Geod(ellps="WGS84")
    new_lon_horizontal, new_lat_horizontal, _ = geod.fwd(lon, lat, 90, distance_km_horizontal * 1000)
    new_lon, new_lat, _ = geod.fwd(new_lon_horizontal, new_lat_horizontal, 0, distance_km_vertical * 1000)
    return new_lon, new_lat

def calculate_distance_pyproj_vectorized(lon1, lat1, lon2_array, lat2_array, ellipsoid="WGS84"):
    """
    Returns the distance (km) from a point to an array of points using the Pyproj module
    """
    geod = pyproj.Geod(ellps=ellipsoid)
    _, _, distance_m = geod.inv(lons1=np.full_like(lon2_array, lon1), lats1=np.full_like(lat2_array, lat1), lons2=np.array(lon2_array), lats2=np.array(lat2_array))
    distance_km = distance_m / 1000
    return distance_km

def select_mainshocks(earthquake_catalogue,
                      search_style='radius',
                      search_distance_km=10,
                      mainshock_magnitude_threshold = 4,
                      minimum_exclusion_distance = 20,
                      scaling_exclusion_distance = 5,
                      minimum_exclusion_time = 50,
                      scaling_exclusion_time = 25,
                      station_file=None
                      ):
    """
    Select mainshocks from an earthquake catalogue using the following methods:
    MDET - Magnitude-Dependent Exclusion Thresholds (Trugman & Ross, 2019);
    FET - Fixed Exclusion Thresholds (Moutote et al., 2021).
    DDET - Distance-Dependent Exclusion Thresholds.
    """
    
    earthquakes_above_magnitude_threshold = earthquake_catalogue.loc[earthquake_catalogue['MAGNITUDE'] >= mainshock_magnitude_threshold].copy()
    
    exclusion_criteria_results = []
    TR_mainshocks_to_exclude = []
    for mainshock in tqdm(earthquakes_above_magnitude_threshold.itertuples(), total=len(earthquakes_above_magnitude_threshold)):

        local_catalogue = select_within_box(mainshock.LON, mainshock.LAT, df=earthquake_catalogue, r=search_distance_km)        
        # min_box_lon, min_box_lat = add_distance_to_position_pyproj(mainshock.LON, mainshock.LAT, -search_distance_km, -search_distance_km)
        # max_box_lon, max_box_lat = add_distance_to_position_pyproj(mainshock.LON, mainshock.LAT, search_distance_km, search_distance_km)

        # local_catalogue = earthquake_catalogue.loc[
        #                                 (earthquake_catalogue['LON']>= min_box_lon) &\
        #                                 (earthquake_catalogue['LON']<= max_box_lon) &\
        #                                 (earthquake_catalogue['LAT']>= min_box_lat) &\
        #                                 (earthquake_catalogue['LAT']<= max_box_lat)
        #                                 ].copy()
        # local_catalogue['DISTANCE_TO_MAINSHOCK'] = calculate_distance_pyproj_vectorized(mainshock.LON, mainshock.LAT, local_catalogue['LON'],  local_catalogue['LAT'])

        if search_style=='radius':    
            local_catalogue = local_catalogue[(local_catalogue['DISTANCE_TO_MAINSHOCK'] < search_distance_km)].copy()    

        elif search_style=='box':
            print(f"A box has been chosen, even though a box allows a distance of 14 km between mainshock epicentre and box corner.")

        else:
            print(f"Invalid search style - we are going to craaaaash")

        n_local_catalogue = len(local_catalogue)

        local_catalogue_1yr = local_catalogue[(local_catalogue.DATETIME <= mainshock.DATETIME) &\
                                        ((mainshock.DATETIME - local_catalogue.DATETIME) < dt.timedelta(days=365)) &\
                                        (local_catalogue['ID'] != mainshock.ID)
                                        ].copy()

        n_local_catalogue_1yr = len(local_catalogue_1yr)
        
        if n_local_catalogue_1yr > 0:
            max_magnitude = max(local_catalogue_1yr['MAGNITUDE'])
            if max_magnitude <= mainshock.MAGNITUDE:
                Moutote_method = 'Selected'
                Moutote_excluded_by=[]
            elif max_magnitude > mainshock.MAGNITUDE:
                Moutote_excluded_by = list(local_catalogue_1yr.loc[local_catalogue_1yr['MAGNITUDE'] > mainshock.MAGNITUDE, 'ID'])
                Moutote_method = 'Excluded'
        else:
            max_magnitude, Mc_1yr =[float('nan')]*2
            Moutote_method = 'Selected'
            Moutote_excluded_by = []

        if n_local_catalogue > 0:
            try:
                Mbass, this_fmd, b, b_avg, mc_shibolt_unc = get_mbs(np.array(local_catalogue['MAGNITUDE']), mbin=0.1)
                a, b_Mbass, aki_unc, shibolt_unc = b_est(np.array(local_catalogue['MAGNITUDE']), mbin=0.1, mc=Mbass)
            except:
                Mbass, b_Mbass = [np.nan]*2
            maxc = get_maxc(np.array(local_catalogue['MAGNITUDE']), mbin=0.1)
            a, b_maxc, aki_unc, shibolt_unc = b_est(np.array(local_catalogue['MAGNITUDE']), mbin=0.1, mc=maxc)
        else:
            Mbass, b_Mbass, maxc, b_maxc = [np.nan]*4
                    
        subsurface_rupture_length = 10**((mainshock.MAGNITUDE - 4.38)/1.49)
        distance_exclusion_threshold = minimum_exclusion_distance + scaling_exclusion_distance * subsurface_rupture_length
        time_exclusion_threshold = minimum_exclusion_time + scaling_exclusion_time * (mainshock.MAGNITUDE - mainshock_magnitude_threshold)

        distances_between_earthquakes = calculate_distance_pyproj_vectorized(mainshock.LON, mainshock.LAT, earthquakes_above_magnitude_threshold['LON'],  earthquakes_above_magnitude_threshold['LAT'])

        earthquakes_within_exclusion_criteria = earthquakes_above_magnitude_threshold.loc[
            (mainshock.ID != earthquakes_above_magnitude_threshold.ID) &\
            (distances_between_earthquakes <= distance_exclusion_threshold) &\
            (earthquakes_above_magnitude_threshold.MAGNITUDE < mainshock.MAGNITUDE) &\
            (((earthquakes_above_magnitude_threshold['DATETIME'] - mainshock.DATETIME).apply(lambda d: d.total_seconds()/(3600*24))) < time_exclusion_threshold) &\
            (((earthquakes_above_magnitude_threshold['DATETIME'] - mainshock.DATETIME).apply(lambda d: d.total_seconds()/(3600*24)) > 0))
            ]
        
        TR_mainshocks_to_exclude.extend(list(earthquakes_within_exclusion_criteria['ID']))

        if station_file is not None and not station_file.empty:
            distance_to_stations = np.array(utils.calculate_distance_pyproj_vectorized(mainshock.LON, mainshock.LAT, station_file['LON'],  station_file['LAT']))
            distance_to_stations = np.sort(distance_to_stations)
        else:
            distance_to_stations = [np.nan]*4
        
        results_dict = {'ID':mainshock.ID,
                        'DATETIME':mainshock.DATETIME,
                        'MAGNITUDE':mainshock.MAGNITUDE,
                        'LON':mainshock.LON,
                        'LAT':mainshock.LAT,
                        'DEPTH':mainshock.DEPTH,
                        'Maxc':maxc,
                        'Mbass':Mbass,
                        'b_Mbass':b_Mbass,
                        'b_maxc':b_maxc,
                        'n_local_cat':n_local_catalogue,
                        'n_local_cat_1yr':n_local_catalogue_1yr,
                        'Largest_preceding_1yr':max_magnitude,
                        'Moutote_method':Moutote_method,
                        'Moutote_excluded_by':Moutote_excluded_by,
                        'subsurface_rupture_length':subsurface_rupture_length,
                        'distance_exclusion_threshold':distance_exclusion_threshold,
                        'time_exclusion_threshold':time_exclusion_threshold,
                        'TR_excludes':list(earthquakes_within_exclusion_criteria['ID']),
                        'km_to_STA':distance_to_stations[0:4],
                        'STA_4_km':distance_to_stations[3]}
        
        exclusion_criteria_results.append(results_dict)
        clear_output(wait=True)
    
    exclusion_criteria_results = pd.DataFrame.from_dict(exclusion_criteria_results)

    exclusion_criteria_results['TR_method'] = np.select([~exclusion_criteria_results['ID'].isin(TR_mainshocks_to_exclude),
                                                         exclusion_criteria_results['ID'].isin(TR_mainshocks_to_exclude)],
                                                         ['Selected', 'Excluded'],
                                                         default='error')

    TR_excluded_by = []
    for mainshock in exclusion_criteria_results.itertuples():
        excluded_by_list = []
        for mainshock_2 in exclusion_criteria_results.itertuples():
            if mainshock.ID in mainshock_2.TR_excludes:
                excluded_by_list.append(mainshock_2.ID)
        TR_excluded_by.append(excluded_by_list)

    exclusion_criteria_results['TR_excluded_by'] = TR_excluded_by

    selection_list = []
    for mainshock in exclusion_criteria_results.itertuples():
        if (mainshock.Moutote_method=='Selected') & (mainshock.TR_method=='Selected'):
            selection='Both'
        elif (mainshock.Moutote_method=='Selected') & (mainshock.TR_method=='Excluded'):
            selection='FET'
        elif (mainshock.Moutote_method=='Excluded') & (mainshock.TR_method=='Selected'):
            selection='MDET'
        elif (mainshock.Moutote_method=='Excluded') & (mainshock.TR_method=='Excluded'):
            selection='Neither'
        selection_list.append(selection)

    exclusion_criteria_results['Selection'] = selection_list

    return exclusion_criteria_results

# Defunct? Same as plot local cat?
def plot_single_mainshock(ID, mainshock_file, catalogue_name, earthquake_catalogue, Mc_cut = False):
    mainshock = iterable_mainshock(ID, mainshock_file)
    local_cat = create_local_catalogue(mainshock=mainshock, earthquake_catalogue=earthquake_catalogue, catalogue_name=catalogue_name)
    if Mc_cut==True:
        local_cat = apply_Mc_cut(local_cat)
    plot_local_cat(mainshock=mainshock, local_cat=local_cat, Mc_cut=Mc_cut, catalogue_name=catalogue_name, earthquake_catalogue=earthquake_catalogue)

def identify_foreshocks_short(mainshock, earthquake_catalogue, local_catalogue, iterations=10000,
                              local_catalogue_radius = 10, foreshock_window = 20, modelling_time_period=345, Wetzler_cutoff=3):
    """
    Identify foreshocks before mainshocks using the following methods:
        BP - Background Poisson (Trugman and Ross, 2019);
        G-IET - Gamma inter-event time (van den Ende & Ampuero, 2020);
        ESR - Empirical Seismicity Rate (van den Ende & Ampuero, 2020).
        We create code for the BP and ESR methods. We integrate the publically available code for the G-IET method (van den Ende & Ampuero, 2020).
    """
    
    mainshock_ID = mainshock.ID
    mainshock_LON = mainshock.LON
    mainshock_LAT = mainshock.LAT
    mainshock_DATETIME = mainshock.DATETIME
    mainshock_Mc = mainshock.Mc
    mainshock_MAG = mainshock.MAGNITUDE
    
    method_dict = {"ESR":'ESR',
                    "VA_method":'G-IET',
                    "Max_window":'Max_rate',
                    "VA_half_method":'R-IET',
                    "TR_method":'BP'
                    }
    
    # try:
    #     Mc = round(Mc_by_maximum_curvature(local_catalogue['MAGNITUDE']),2) + 0.2
    # except:
    #     Mc = float('nan')

    local_catalogue = local_catalogue[(local_catalogue['DATETIME'] < mainshock_DATETIME) &\
                                        (local_catalogue['DAYS_TO_MAINSHOCK'] < modelling_time_period+foreshock_window) &\
                                        (local_catalogue['DAYS_TO_MAINSHOCK'] > 0)  &\
                                        (local_catalogue['DISTANCE_TO_MAINSHOCK'] < local_catalogue_radius) &\
                                        (local_catalogue['ID'] != mainshock_ID)
                                        ].copy()

    # local_catalogue_pre_Mc_cutoff = local_catalogue.copy()
    # local_catalogue_below_Mc = local_catalogue.loc[local_catalogue['MAGNITUDE']<mainshock_Mc].copy()
    # local_catalogue_below_Mc = local_catalogue_below_Mc.loc[(local_catalogue_below_Mc['DAYS_TO_MAINSHOCK']) < modelling_time_period].copy()
    # foreshocks_below_Mc = local_catalogue_below_Mc.loc[local_catalogue_below_Mc['DAYS_TO_MAINSHOCK']<foreshock_window]

    # if Mc_cut==True:
    #     local_catalogue = local_catalogue.loc[local_catalogue['MAGNITUDE']>=mainshock_Mc].copy()
    # else:
    #     local_catalogue = local_catalogue_pre_Mc_cutoff.copy()

    regular_seismicity_period = local_catalogue[(local_catalogue['DAYS_TO_MAINSHOCK'] >= foreshock_window)]
    foreshocks = local_catalogue[(local_catalogue['DAYS_TO_MAINSHOCK'] < foreshock_window)]

    # n_local_catalogue_pre_Mc_cutoff = len(local_catalogue_pre_Mc_cutoff)
    # n_local_catalogue_below_Mc = len(local_catalogue_below_Mc)
    n_local_catalogue = len(local_catalogue)
    n_regular_seismicity_events = len(regular_seismicity_period)
    n_events_in_foreshock_window = len(foreshocks)

    b_values = []
    for seismicity_period in [local_catalogue, foreshocks, regular_seismicity_period]:
        try:
            b_value = round(b_val_max_likelihood(seismicity_period['MAGNITUDE'], mc=mainshock_Mc), 2)
        except:
            b_value = float('nan')
        b_values.append(b_value)
    overall_b_value, foreshock_b_value, regular_b_value = b_values

    ### WETZLER WINDOW METHOD ###
    Wetzler_foreshocks = foreshocks.loc[foreshocks['MAGNITUDE']>Wetzler_cutoff].copy()
    N_Wetzler_foreshocks = len(Wetzler_foreshocks)

    ### MAX RATE /ESR 2.0 METHOD ###
    catalogue_start_date = earthquake_catalogue['DATETIME'].iloc[0]
    time_since_catalogue_start = (mainshock_DATETIME - catalogue_start_date).total_seconds()/3600/24
    cut_off_day = math.floor(time_since_catalogue_start)
    if cut_off_day > 365:
        cut_off_day = 365
    range_scaler = 100    

    sliding_window_points = np.array(np.arange((-cut_off_day+foreshock_window)*range_scaler, -foreshock_window*range_scaler, 1))/range_scaler*-1
    sliding_window_counts = np.array([len(regular_seismicity_period[(regular_seismicity_period['DAYS_TO_MAINSHOCK'] > point) &\
                                                                    (regular_seismicity_period['DAYS_TO_MAINSHOCK'] <= (point + foreshock_window))]) for point in sliding_window_points])

    try:
        max_window = max(sliding_window_counts)
    except:
        max_window = float('nan')

    if n_events_in_foreshock_window > max_window:
        max_window_method = 0.0
    elif n_events_in_foreshock_window <= max_window:
        max_window_method = 1.0
    else:
        max_window_method = float('nan')

    if (len(sliding_window_counts)==0) & (n_events_in_foreshock_window > 0):
        sliding_window_probability = 0.00
        sliding_window_99CI = float('nan')
    elif (len(sliding_window_counts)==0) & (n_events_in_foreshock_window == 0):    
        sliding_window_probability = 1.00
        sliding_window_99CI = float('nan')
    else:
        sliding_window_probability = len(sliding_window_counts[sliding_window_counts >= n_events_in_foreshock_window])/len(sliding_window_counts)
    # sliding_window_probability = len(list(filter(lambda c: c >= n_events_in_foreshock_window, sliding_window_counts)))/len(sliding_window_counts)
        sliding_window_99CI = np.percentile(sliding_window_counts,99)

    ### TR BACKGROUND POISSON MODEL ###
    if not regular_seismicity_period.empty:
        time_series = np.array(regular_seismicity_period['DATETIME'].apply(lambda d: (d-regular_seismicity_period['DATETIME'].iloc[0]).total_seconds()/3600/24))
    else:
        time_series = np.array([])
    if n_regular_seismicity_events >= 2:
        background_rate = gamma_law_MLE(time_series)
        TR_expected_events = background_rate*foreshock_window
        TR_probability = poisson.sf(n_events_in_foreshock_window, TR_expected_events)
        TR_99CI = poisson.ppf(0.99, TR_expected_events)
    elif n_regular_seismicity_events < 2:
        background_rate, TR_expected_events, TR_99CI = [float('nan')]*3
        if (n_events_in_foreshock_window==0):
            TR_probability = 1.00
        elif (n_events_in_foreshock_window > n_regular_seismicity_events):
            TR_probability = 0.00
        else:
            TR_probability = float('nan')
    else:
        background_rate, TR_expected_events, TR_probability, TR_99CI = [float('nan')]*4


    if n_regular_seismicity_events > 2:
        t_day = 3600 * 24.0
        t_win = foreshock_window * t_day
        IET = np.diff(time_series) ### V&As Gamma IET method
        IET = IET[IET>0]
        try:
            y_, loc_, mu_ = stats.gamma.fit(IET, floc=0.0)
        except:
            y_, loc_, mu_ = stats.gamma.fit(IET, loc=0.0)
        # print(f"y_ {y_}, loc_ {loc_}, mu_ {mu_}")

        if (np.isnan(y_)==False) & (np.isnan(mu_)==False):
            N_eq = np.zeros(iterations, dtype=int) # Buffer for the number of earthquakes observed in each random sample
            for i in range(0,iterations):
                prev_size = 200 # Generate a random IET sample with 200 events
                IET2 = stats.gamma.rvs(a=y_, loc=0, scale=mu_, size=prev_size) * t_day # Sample from gamma distribution
                t0 = np.random.rand() * IET2[0] # Random shift of timing of first event
                t_sum = np.cumsum(IET2) - t0 # Cumulative sum of interevent times
                inds = (t_sum > t_win) # Find the events that lie outside t_win
                while (inds.sum() == 0):
                    prev_size *= 2 # If no events lie outside t_win, create a bigger sample and stack with previous sample
                    IET2 = np.hstack([IET2, stats.gamma.rvs(a=y_, loc=0, scale=mu_, size=prev_size) * t_day])
                    t_sum = np.cumsum(IET2) # Cumulative sum of event times
                    inds = (t_sum > t_win) # Find the events that lie outside t_win
                N_inside_t_win = (~inds).sum()
                if N_inside_t_win == 0: 
                    N_eq[i] = 0 # No events inside t_win, seismicity rate = 0.
                else:
                    N_eq[i] =  N_inside_t_win - 1 # Store the number of events that lie within t_win (excluding shifted event)

            try:
                y_gam_IETs, loc_gam_IETs, mu_gam_IETs = stats.gamma.fit(N_eq[N_eq > 0], floc=0.0)
            except:
                y_gam_IETs, loc_gam_IETs, mu_gam_IETs = stats.gamma.fit(N_eq[N_eq > 0], loc=0.0)
        
        # print(f"y_gam_IETs {y_gam_IETs}, loc_gam_IETs {loc_gam_IETs}, mu_gam_IETs {mu_gam_IETs}")
        VA_gamma_probability = stats.gamma.sf(n_events_in_foreshock_window, y_gam_IETs, loc_gam_IETs, mu_gam_IETs)
        VA_gamma_99CI = stats.gamma.ppf(0.99, a=y_gam_IETs, loc=loc_gam_IETs, scale=mu_gam_IETs)
        VA_IETs_probability = len(N_eq[N_eq>=n_events_in_foreshock_window])/iterations
        VA_IETs_99CI = np.percentile(N_eq,99)

    elif n_regular_seismicity_events <= 2:
        y_gam_IETs, loc_gam_IETs, mu_gam_IETs = [float('nan')]*3
        N_eq = np.array([])
        VA_gamma_99CI,  VA_IETs_99CI = [float('nan')]*2
        if (n_events_in_foreshock_window == 0):
            VA_gamma_probability, VA_IETs_probability = [1.00]*2
        elif (n_events_in_foreshock_window > n_regular_seismicity_events):
            VA_gamma_probability, VA_IETs_probability = [0.00]*2
        else:
            VA_gamma_probability, VA_IETs_probability, VA_gamma_99CI,  VA_IETs_99CI = [float('nan')]*4
    else:
        N_eq = np.array([])
        y_gam_IETs, loc_gam_IETs, mu_gam_IETs = [float('nan')]*3
        VA_gamma_probability, VA_IETs_probability, VA_gamma_99CI,  VA_IETs_99CI = [float('nan')]*4

        ########################################################
                
    results_dict = {'ID':mainshock_ID,
                    'MAGNITUDE':mainshock_MAG,
                    'LON':mainshock_LON,
                    'LAT':mainshock_LAT,
                    'DATETIME':mainshock_DATETIME,
                    'DEPTH':mainshock.DEPTH,
                    'Mc':mainshock_Mc,
                    'time_since_catalogue_start':time_since_catalogue_start,
                    'n_regular_seismicity_events':n_regular_seismicity_events,
                    'n_events_in_foreshock_window':n_events_in_foreshock_window,
                    'n_Wetzler_foreshocks':N_Wetzler_foreshocks,
                    'max_20day_rate':max_window,
                    method_dict['Max_window']:max_window_method,
                    method_dict['ESR']:sliding_window_probability,
                    method_dict['VA_method']:VA_gamma_probability,
                    method_dict['VA_half_method']:VA_IETs_probability,
                    method_dict['TR_method']:TR_probability,
                    method_dict['ESR'] + '_99CI':sliding_window_99CI,
                    method_dict['VA_method'] + '_99CI':VA_gamma_99CI,
                    method_dict['VA_half_method'] + '_99CI':VA_IETs_99CI,
                    method_dict['TR_method'] + '_99CI':TR_99CI,
                    'overall_b_value':overall_b_value,
                    'regular_b_value':regular_b_value,
                    'foreshock_b_value':foreshock_b_value,
                    'y_gam_IETs':y_gam_IETs,
                    'loc_gam_IETs':loc_gam_IETs,
                    'mu_gam_IETs':mu_gam_IETs,
                    'background_rate':background_rate,
                    'cut_off_day':cut_off_day,
                    'M3_IDs':Wetzler_foreshocks['ID']
                    }
    
    file_dict = {'local_catalogue':local_catalogue,
                #  'local_catalogue_pre_Mc_cutoff':local_catalogue_pre_Mc_cutoff,
                #  'local_catalogue_below_Mc':local_catalogue_below_Mc,
                 'foreshocks':foreshocks,
                #  'foreshocks_below_Mc':foreshocks_below_Mc,
                 'sliding_window_points':sliding_window_points,
                 'sliding_window_counts':sliding_window_counts,
                 'N_eq':N_eq
                 }
    
    return results_dict, file_dict

def plot_models(mainshock, results_dict, file_dict, catalogue_name, Mc_cut, foreshock_window = 20, save=True):
    min_days=365
    max_days=0
    colours = sns.color_palette("colorblind", 10)
    colour_names = ['dark blue', 
                'orange',
                'green',
                'red',
                'dark pink',
                'brown',
                'light pink',
                'grey',
                'yellow',
                'light blue']
    colour_dict = dict(zip(colour_names, colours))
    
    method_dict = {"ESR":'ESR',
                "VA_method":'G-IET',
                # "Max_window":'Max_rate',
                "VA_half_method":'R-IET',
                "TR_method":'BP'
                }
    
    # event_marker_size = (lambda x: 12*np.exp(x))
    # event_marker_size = (lambda x: 7.5**(x))
    event_marker_size = (lambda x: 50+10**(x/1.25))
    linewidth = 3
    
    mainshock_ID = results_dict['ID']
    mainshock_DATETIME = results_dict['DATETIME']
    cut_off_day = results_dict['cut_off_day']
    n_regular_seismicity_events = results_dict['n_regular_seismicity_events']
    n_events_in_foreshock_window = results_dict['n_events_in_foreshock_window']
    VA_IETs_probability = results_dict['R-IET']
    TR_expected_events = results_dict['background_rate']*foreshock_window
    TR_probability = results_dict['BP']
    y_gam_IETs = results_dict['y_gam_IETs']
    mu_gam_IETs = results_dict['mu_gam_IETs']
    loc_gam_IETs = results_dict['loc_gam_IETs']
    VA_gamma_probability = results_dict['G-IET']
    sliding_window_probability = results_dict['ESR']
    Mc = results_dict['Mc']

    local_catalogue = file_dict['local_catalogue']
    local_cat = file_dict['local_catalogue']
    # local_catalogue_pre_Mc_cutoff= file_dict['local_catalogue_pre_Mc_cutoff']
    # local_catalogue_below_Mc= file_dict['local_catalogue_below_Mc']
    foreshocks= file_dict['foreshocks']
    # foreshocks_below_Mc= file_dict['foreshocks_below_Mc']
    sliding_window_counts = file_dict['sliding_window_counts']
    N_eq = file_dict['N_eq']
    N_eq = N_eq[N_eq>0]
    
    align = 'mid' #left, or right
    # foreshocks_colour = 'red'
    # regular_earthquakes_colour = 'black'
    # mainshock_colour = 'red'
    # poisson_colour = colour_dict['orange']
    # gamma_colour = colour_dict['green']
    # ESR_colour = colour_dict['dark pink']
    # Mc_colour = colour_dict['light blue']
    # rate_colour = colour_dict['dark pink']

    foreshocks_colour = 'red'
    regular_earthquakes_colour = 'black'
    mainshock_colour = 'black'
    poisson_colour = plot_color_dict['orange']
    gamma_colour = plot_color_dict['teal']
    ESR_colour = plot_color_dict['purple']
    Mc_colour = plot_color_dict['grey']
    rate_colour = 'black'
    rate_alpha = 0.5
    vmin, vmax = 0, 365

    modelling_events = local_cat.loc[(local_cat['DAYS_TO_MAINSHOCK'] < min_days) &\
                                    (local_cat['DAYS_TO_MAINSHOCK'] > max_days+20) &\
                                    (local_cat['DISTANCE_TO_MAINSHOCK']<10)].copy()
    aftershocks = local_cat.loc[(local_cat['DAYS_TO_MAINSHOCK'] < 0) &\
                                (local_cat['DAYS_TO_MAINSHOCK'] > -20)].copy()
    
    range_scaler=100
    sliding_window_points_full = np.array(range((-cut_off_day+foreshock_window)*range_scaler, 0*range_scaler+1, 1))/range_scaler*-1
    sliding_window_counts_full = np.array([len(local_catalogue[(local_catalogue['DAYS_TO_MAINSHOCK'] > point) & (local_catalogue['DAYS_TO_MAINSHOCK'] <= (point + foreshock_window))]) for point in sliding_window_points_full])

    sliding_window_df_full = pd.DataFrame({'points':sliding_window_points_full,
                                           'counts':sliding_window_counts_full})
    
    # time_series_plot, model_plot, CDF_plot, foreshock_window_plot, Mc_plot = 0, 1, 2, 3, 4
    time_series_plot, model_plot, CDF_plot, foreshock_window_plot= 0, 1, 2, 3

    panel_labels = ['a)', 'b)', 'c)', 'd)', 'e)']

    histogram_alpha = 0.95
    fig, axs = plt.subplots(5,1, figsize=(10,15))
    # fig, axs = plt.subplots(4,1, figsize=(10,15))

    axs[time_series_plot].set_title('a)', fontsize=20, loc='left')
    axs[time_series_plot].set_title(f"ID: {mainshock_ID} - {mainshock.DATETIME.strftime('%b %d %Y')} - {catalogue_name}", loc='right')

    axs[time_series_plot].scatter(0, mainshock.MAGNITUDE, s= event_marker_size(mainshock.MAGNITUDE), #s=400, 
                                  ec=mainshock_colour, fc='grey', alpha=0.5,
                                    label=r'$M_{w}$ ' + str(mainshock.MAGNITUDE) + ' Mainshock',  
                                    zorder=1)
    axs[time_series_plot].axvline(x=20, color='red', linestyle='--', linewidth=linewidth,
                                    label = f"20-day foreshock window",
                                    zorder=4)
    axs[time_series_plot].set_xlabel('Days to mainshock', fontsize=20)
    axs[time_series_plot].set_ylabel('Magnitude', fontsize=20)
    axs[time_series_plot].set_xlim(-25,365+20)
    # axs[time_series_plot].set_ylim(axs[time_series_plot].get_extent(),365+20)
    current_ylim = axs[time_series_plot].get_ylim()
    # axs[time_series_plot].set_ylim(current_ylim[0], current_ylim[1]+0.5)
    axs[time_series_plot].invert_xaxis()

    if len(modelling_events) >0:
        # ax.set_yticks(np.arange(math.floor(min(local_cat['MAGNITUDE'])), math.ceil(mainshock.MAGNITUDE), 1))
        axs[time_series_plot].scatter(modelling_events['DAYS_TO_MAINSHOCK'], modelling_events['MAGNITUDE'],
                   s=event_marker_size(modelling_events['MAGNITUDE']), vmin=vmin, vmax=vmax, 
                                        label= f'{len(modelling_events)- len(foreshocks)} modelling events',
                                        c=modelling_events['DAYS_TO_MAINSHOCK'], alpha=0.5,  zorder=1)
        # axs[time_series_plot].scatter(local_catalogue_below_Mc['DAYS_TO_MAINSHOCK'], local_catalogue_below_Mc['MAGNITUDE'], 
        #                             label= str(len(local_catalogue_below_Mc)) + ' Earthquakes below Mc', 
        #               
        #               alpha=0.5, color=Mc_colour)
    if len(foreshocks) > 0:
        axs[time_series_plot].scatter(foreshocks['DAYS_TO_MAINSHOCK'], foreshocks['MAGNITUDE'],
                    s=event_marker_size(foreshocks['MAGNITUDE']),
                   label= fr"$N_obs$: {len(foreshocks)}", color='red', alpha=0.5, zorder=5)
        
    if len(aftershocks) > 0:
        axs[time_series_plot].scatter(aftershocks['DAYS_TO_MAINSHOCK'], aftershocks['MAGNITUDE'], 
               s=event_marker_size(aftershocks['MAGNITUDE'])/4,
               label= f"Aftershocks: {len(aftershocks)}", color='grey', alpha=0.5, zorder=0)

    
    ax2 = axs[time_series_plot].twinx()
    cut_off_day=365
    foreshock_window=20
    range_scaler=100
    modelling_plus_foreshocks = pd.concat([modelling_events, foreshocks])
    # sliding_window_points_full = np.array(range((-cut_off_day+foreshock_window)*range_scaler, 0*range_scaler+1, 1))/range_scaler*-1
    sliding_window_points_full = np.array(range((-cut_off_day+foreshock_window), 0+1, 1))/-1
    sliding_window_counts_full = np.array([len(modelling_plus_foreshocks[(modelling_plus_foreshocks['DAYS_TO_MAINSHOCK'] > point) &\
                                                                          (modelling_plus_foreshocks['DAYS_TO_MAINSHOCK'] <= (point + foreshock_window))]) for point in sliding_window_points_full])
    average = np.mean
    # sliding_window_distances = np.array([average(modelling_plus_foreshocks.loc[(modelling_plus_foreshocks['DAYS_TO_MAINSHOCK'] > point) &\
    #                                                                 (modelling_plus_foreshocks['DAYS_TO_MAINSHOCK'] <= (point + foreshock_window)), 'DISTANCE_TO_MAINSHOCK']) for point in sliding_window_points_full])

    # sliding_window_df_full = pd.DataFrame({'points':sliding_window_points_full,
    #                                        'counts':sliding_window_counts_full,
    #                                        'distances':sliding_window_distances})
    
    ax2.step(sliding_window_points_full, sliding_window_counts_full, zorder=6, linewidth=linewidth, where='post',
            #  c=sliding_window_points_full.astype(int),
             color='black', alpha=rate_alpha,
             label='Count')
    ax2.axhline(y=len(foreshocks), color='red', alpha=0.5, label = r'$N_{obs}$', zorder=100, linewidth=linewidth,)
    ax2.set_ylabel('20-day Count')
    # ax.set_zorder(ax2.get_zorder()+1)
    axs[time_series_plot].patch.set_visible(False)
    try:
        y_min, y_max = round(sliding_window_counts_full.min()), round(sliding_window_counts_full.max())
        y_mid = round(y_min + (y_max - y_min)/2)
        y_ticks = [y_min, y_mid, y_max]
        ax2.set_yticks(y_ticks)
        ax2.set_yticklabels(y_ticks)
    except:
        print('Could not update yticks')

    radius_km=10
    modelling_time_period=365
    local_catalogue_pre_Mc_cutoff = load_local_catalogue(mainshock=mainshock, catalogue_name=catalogue_name)
    # local_catalogue_pre_Mc_cutoff = create_local_catalogue(mainshock=mainshock, catalogue_name=catalogue_name, earthquake_catalogue=catalogue_dict[catalogue_name])
    local_catalogue_pre_Mc_cutoff = local_catalogue_pre_Mc_cutoff[(local_catalogue_pre_Mc_cutoff['DATETIME'] < mainshock_DATETIME) &\
                                        (local_catalogue_pre_Mc_cutoff['DAYS_TO_MAINSHOCK'] < modelling_time_period+foreshock_window) &\
                                        (local_catalogue_pre_Mc_cutoff['DAYS_TO_MAINSHOCK'] > 0)  &\
                                        (local_catalogue_pre_Mc_cutoff['DISTANCE_TO_MAINSHOCK'] < radius_km) &\
                                        (local_catalogue_pre_Mc_cutoff['ID'] != mainshock_ID)
                                        ].copy()
    
    # if len(local_catalogue_pre_Mc_cutoff)>0:
    #     print(local_catalogue_pre_Mc_cutoff['MAGNITUDE'].head())
    #     bins = np.arange(math.floor(local_catalogue_pre_Mc_cutoff['MAGNITUDE'].min()), math.ceil(local_catalogue_pre_Mc_cutoff['MAGNITUDE'].max()), 0.1)
    #     values, base = np.histogram(local_catalogue_pre_Mc_cutoff['MAGNITUDE'], bins=bins)
    #     cumulative = np.cumsum(values)
    #     axs[Mc_plot].step(base[:-1], len(local_catalogue_pre_Mc_cutoff)-cumulative, label='FMD', color='black', linewidth=linewidth)
    #     axs[Mc_plot].axvline(x=Mc, linestyle='--', color=Mc_colour, label=r'$M_{c}$: ' + str(round(Mc,1)), linewidth=linewidth)
    # axs[Mc_plot].set_title(panel_labels[Mc_plot], fontsize=20, loc='left')
    # axs[Mc_plot].set_xlabel('Magnitude')
    # axs[Mc_plot].set_ylabel('N')
    # # axs[Mc_plot].legend()
    # axs[Mc_plot].set_yscale('log')
    
    # axs[time_series_plot].set_title(panel_labels[time_series_plot], fontsize=20, loc='left')
    # axs[time_series_plot].scatter(0, mainshock.MAGNITUDE, marker='*', s=400, color=mainshock_colour,
    #                                 label=r'$M_{w}$ ' + str(mainshock.MAGNITUDE) + ' Mainshock',  
    #                                 zorder=3)
    # axs[time_series_plot].axvline(x=foreshock_window, color=foreshocks_colour, linestyle='--', 
    #                                 label = f"{foreshock_window}-day foreshock window",
    #                                 zorder=4)
    # axs[time_series_plot].set_xlabel('Days to mainshock', fontsize=20)
    # axs[time_series_plot].set_ylabel('M', fontsize=20)
    # axs[time_series_plot].set_xlim(-5,cut_off_day+foreshock_window)
    # axs[time_series_plot].invert_xaxis()

    # if len(local_catalogue) >0:
    #     # axs[time_series_plot].set_yticks(np.arange(math.floor(min(local_catalogue['MAGNITUDE'])), math.ceil(mainshock.MAGNITUDE), 1))
    #     axs[time_series_plot].scatter(local_catalogue['DAYS_TO_MAINSHOCK'], local_catalogue['MAGNITUDE'],
    #                                     label= str(n_regular_seismicity_events) + ' Earthquakes for modelling',
    #                                     color=regular_earthquakes_colour, alpha=0.5,  zorder=1)
    #     # axs[time_series_plot].scatter(local_catalogue_below_Mc['DAYS_TO_MAINSHOCK'], local_catalogue_below_Mc['MAGNITUDE'], 
    #     #                             label= str(len(local_catalogue_below_Mc)) + ' Earthquakes below Mc', 
    #     #                             alpha=0.5, color=Mc_colour)
    if len(foreshocks) > 0:
        # axs[time_series_plot].scatter(foreshocks['DAYS_TO_MAINSHOCK'], foreshocks['MAGNITUDE'],
        #                                 label= str(n_events_in_foreshock_window) + ' Earthquakes in foreshock window (' + r'$N_{obs}$)',
        #                                 color=foreshocks_colour, alpha=0.5, 
        #                                 zorder=2)
        axs[foreshock_window_plot].scatter(foreshocks['DAYS_TO_MAINSHOCK'], foreshocks['MAGNITUDE'],
                                           s=event_marker_size(foreshocks['MAGNITUDE']),
                                           label=r'$N_{obs}$: ' + str(len(foreshocks)), color='red', alpha=0.5, zorder=5)
        # axs[foreshock_window_plot].scatter(foreshocks['DAYS_TO_MAINSHOCK'], foreshocks['MAGNITUDE'], color=foreshocks_colour, alpha=0.5,
        #                                     label=r'$N_{obs}$: ' + str(n_events_in_foreshock_window))
        # axs[foreshock_window_plot].scatter(foreshocks_below_Mc['DAYS_TO_MAINSHOCK'], foreshocks_below_Mc['MAGNITUDE'], 
        #                                     label= str(len(foreshocks_below_Mc)) + ' Earthquakes below Mc', 
        #                                     alpha=0.2, color=Mc_colour)
        foreshock_sliding_window = sliding_window_df_full.loc[sliding_window_df_full['points']<=20].copy()
        ax_foreshock_window_twin = axs[foreshock_window_plot].twinx()
        ax_foreshock_window_twin.step(foreshock_sliding_window['points'], foreshock_sliding_window['counts'], color=rate_colour, label='20-day count)', where='post',
                                      alpha=rate_alpha, linewidth=linewidth)
        ax_foreshock_window_twin.set_ylabel('20-day Count')
        axs[foreshock_window_plot].set_yticks(np.arange(math.floor(foreshocks['MAGNITUDE'].min()), math.ceil(mainshock.MAGNITUDE), 1))
    if np.isnan(Mc)==False:
        axs[time_series_plot].axhline(y=Mc, color=Mc_colour, linestyle='--', linewidth=linewidth,
                                        label = r'$M_{c}$: ' + str(round(Mc,1)),
                                        zorder=5)
        axs[foreshock_window_plot].axhline(y=Mc, color=Mc_colour, linestyle='--', label = r'$M_{c}$: ' + str(round(Mc,1)), zorder=5, linewidth=linewidth)

    axs[foreshock_window_plot].set_title(panel_labels[foreshock_window_plot], fontsize=20, loc='left')
    # axs[foreshock_window_plot].scatter(1E-10, mainshock.MAGNITUDE, marker='*', s=400, color=mainshock_colour, zorder=2)
    axs[foreshock_window_plot].axvline(x=foreshock_window, color='red', linestyle='--', linewidth=linewidth,)

    axs[foreshock_window_plot].set_xlabel('Days to mainshock')
    axs[foreshock_window_plot].set_ylabel('Magnitude')
    
    axs[foreshock_window_plot].invert_xaxis()
    axs[foreshock_window_plot].set_xscale('log')
    axs[foreshock_window_plot].set_xticks([10, 1, 0.1, 0.01])
    axs[foreshock_window_plot].set_xticklabels([10, 1, 0.1, 0.01])

    # ax2 = axs[time_series_plot].twinx()
    # ax2.plot(sliding_window_points_full, sliding_window_counts_full, color=rate_colour, label='Count')
    # ax2.axhline(y=n_events_in_foreshock_window, color=foreshocks_colour, alpha=0.5, 
    #                                     label = r'$N_{obs}$', zorder=0)
    # ax2.set_ylabel('Count')
    # lines, labels = axs[time_series_plot].get_legend_handles_labels()
    # lines2, labels2 = ax2.get_legend_handles_labels()
    # ax2.set_yticks(utils.estimate_axis_labels(sliding_window_counts_full))
    # axs[time_series_plot].legend(lines + lines2, labels + labels2, loc='upper left')

    axs[model_plot].set_title(panel_labels[model_plot], fontsize=20, loc='left')
    axs[model_plot].set_xlabel('20-day Count', fontsize=20)
    axs[model_plot].set_ylabel('PDF', fontsize=20)
    axs[model_plot].axvline(x=n_events_in_foreshock_window, color=foreshocks_colour, label=r'$N_{obs}$: ' + str(n_events_in_foreshock_window), linewidth=linewidth)      
    axs[CDF_plot].axvline(x=n_events_in_foreshock_window, color='red', linewidth=linewidth,
                            label=r'$N_{obs}$: ' + str(n_events_in_foreshock_window))
    # axs[model_plot].set_xticks(range(0,20,2))

    if len(sliding_window_counts) > 0:
        event_counts_pdf = sliding_window_counts/sum(sliding_window_counts)
        event_counts_cdf = np.cumsum(event_counts_pdf)
        event_counts_sorted = np.sort(sliding_window_counts)

    if len(N_eq) > 0:
        N_eq_counts, N_eq_bins = np.histogram(N_eq, bins=range(math.floor(min(N_eq))-1, math.ceil(max(N_eq))+2))
        # axs[model_plot].step(N_eq_bins[:-1], N_eq_counts/N_eq_counts.sum(), color=gamma_colour, where='post',
        #                     label=f"{method_dict['VA_half_method']}: {round(VA_IETs_probability,3)}",
        #                     alpha=histogram_alpha)
        # axs[model_plot].hist(N_eq, bins=range(min(N_eq)-1, max(N_eq)+1), color=gamma_colour,
        #                     label=f"{method_dict['VA_half_method']}: {str(round(VA_IETs_probability,3))}",
        #                     density=True, rwidth=1.0, alpha=histogram_alpha/2, align=align)
        N_eq_pdf = N_eq/sum(N_eq)
        N_eq_cdf = np.cumsum(N_eq_pdf)
        N_eq_sorted = np.sort(N_eq)
        # axs[CDF_plot].plot(N_eq_sorted, N_eq_cdf, label=method_dict["VA_half_method"], color=gamma_colour, alpha=histogram_alpha/2)
    if (np.isnan(TR_expected_events)==False) & (TR_expected_events!=0):
        min_x, max_x = round(poisson.ppf(0.001, TR_expected_events)), round(poisson.ppf(0.999, TR_expected_events))
        x_TR_Poisson = range(min_x, max_x+1)
        y_TR_Poisson = poisson.pmf(x_TR_Poisson, TR_expected_events)
        axs[model_plot].step(x_TR_Poisson, y_TR_Poisson, label=f"{method_dict['TR_method']}: {str(round(TR_probability,3))}", where='post',
                alpha=histogram_alpha, color=poisson_colour, linewidth=linewidth)
        TR_poisson_cdf = poisson.cdf(x_TR_Poisson, TR_expected_events)
        axs[CDF_plot].step(x_TR_Poisson, TR_poisson_cdf, label=method_dict['TR_method'], alpha=histogram_alpha, color=poisson_colour, linewidth=linewidth, where='post',)

    if (np.isnan(y_gam_IETs)==False) & (np.isnan(mu_gam_IETs)==False):
        # x_gam_IETs = np.arange(gamma.ppf(0.001, a=y_gam_IETs, loc=loc_gam_IETs, scale=mu_gam_IETs),
                                # gamma.ppf(0.999, a=y_gam_IETs, loc=loc_gam_IETs, scale=mu_gam_IETs))
        # x_gam_IETs = range(min(N_eq), max(N_eq))
        min_x, max_x = round(gamma.ppf(0.001, a=y_gam_IETs, loc=loc_gam_IETs, scale=mu_gam_IETs)), round(gamma.ppf(0.999, a=y_gam_IETs, loc=loc_gam_IETs, scale=mu_gam_IETs))
        if min_x > min(sliding_window_counts):
            min_x = min(sliding_window_counts)
        x_gam_IETs = range(min_x, max_x+1)
        gamma_pdf = gamma.pdf(x_gam_IETs, a=y_gam_IETs, loc=loc_gam_IETs, scale=mu_gam_IETs)
        axs[model_plot].step(x_gam_IETs, gamma_pdf, linewidth=linewidth, where='post',
                                label= method_dict['VA_method'] + ': ' + str(round(VA_gamma_probability,3)),
                                alpha=histogram_alpha, color=gamma_colour)
        gamma_cdf = gamma.cdf(x_gam_IETs, a=y_gam_IETs, loc=loc_gam_IETs, scale=mu_gam_IETs)
        axs[CDF_plot].step(x_gam_IETs, gamma_cdf, label= method_dict['VA_method'],linewidth=linewidth, where='post',
                    color=gamma_colour, alpha=histogram_alpha)
    if len(sliding_window_counts) > 0:
        # axs[model_plot].hist(sliding_window_counts, bins=range(math.floor(min(sliding_window_counts))-1, math.ceil(max(sliding_window_counts))+2), color=ESR_colour,
        #         density=True, rwidth=1.0, alpha=histogram_alpha, align=align, label=method_dict['ESR'] + ': ' + str(round(sliding_window_probability,3)))
        min_x, max_x = min(sliding_window_counts), max(sliding_window_counts)
        ESR_counts, ESR_bins = np.histogram(sliding_window_counts, bins=range(min_x, max_x+3))
        axs[model_plot].step(ESR_bins[:-1], ESR_counts/ESR_counts.sum(), color=ESR_colour, linewidth=linewidth, alpha=histogram_alpha, where='post',
                             label=f"{method_dict['ESR']} :{round(sliding_window_probability,3)}")
        # window_counts_pdf = sliding_window_counts/sum(sliding_window_counts)
        window_counts_pdf = ESR_counts/sum(ESR_counts)
        window_counts_cdf = np.cumsum(window_counts_pdf)
        # window_counts_sorted = np.sort(sliding_window_counts)
        window_counts_sorted = np.sort(ESR_counts)

        axs[CDF_plot].step(ESR_bins[:-1], window_counts_cdf, where='post', label=method_dict['ESR'], color=ESR_colour, alpha=histogram_alpha, linewidth=linewidth)
        # axs[CDF_plot].step(window_counts_sorted, window_counts_cdf, where='post')

    for ax in [model_plot, CDF_plot]:
        axs[ax].axvline(x=results_dict['BP_99CI'], color=poisson_colour, alpha=0.5, linewidth=linewidth+1, linestyle='--')
        axs[ax].axvline(x=results_dict['G-IET_99CI'], color=gamma_colour, alpha=0.5, linewidth=linewidth+1, linestyle='--')
        axs[ax].axvline(x=results_dict['ESR_99CI'], color=ESR_colour, alpha=0.5, linewidth=linewidth+1, linestyle='--')

    # axs[model_plot].legend(fontsize=20, loc='upper center', bbox_to_anchor=(1.1, 1), ncols=1)
    axs[model_plot].set_ylim(axs[model_plot].get_ylim()[0], axs[model_plot].get_ylim()[1]+0.025)

#         handles, labels = plt.gca().get_legend_handles_labels()       #specify order of items in legend
#         order = range(0,len(handles))
#         order = [0,1,5,2,4,3]
#         plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])

    axs[CDF_plot].set_title(panel_labels[CDF_plot], fontsize=20, loc='left')
    axs[CDF_plot].set_xlabel('20-day Count')
    axs[CDF_plot].set_ylabel('CDF')

    fig.tight_layout()

    if save==True:
        if Mc_cut==False:
            Path(f"../outputs/{catalogue_name}/model_plots").mkdir(parents=True, exist_ok=True)
            plt.savefig(f"../outputs/{catalogue_name}/model_plots/{mainshock.ID}.png")
        elif Mc_cut==True:
            Path(f"../outputs/{catalogue_name}/Mc_cut/model_plots").mkdir(parents=True, exist_ok=True)
            plt.savefig(f"../outputs/{catalogue_name}/Mc_cut/model_plots/{mainshock.ID}.png")
    plt.show()

def process_mainshocks(mainshocks_file, earthquake_catalogue, catalogue_name, Mc_cut, save, save_name='default_params'):
    date = str(dt.datetime.now().date().strftime("%y%m%d"))

    results_list = []
    i = 1
    for mainshock in mainshocks_file.itertuples():
        print(f"{catalogue_name}")
        print(f"{i} of {len(mainshocks_file)} mainshocks")
        print(f"ID: {mainshock.ID}")
        local_cat = create_local_catalogue(mainshock, earthquake_catalogue, catalogue_name=catalogue_name, save=save)
        # try:
        #     local_cat = load_local_catalogue(mainshock, catalogue_name=catalogue_name)
        # except:
        #     local_cat = create_local_catalogue(mainshock, earthquake_catalogue, catalogue_name=catalogue_name, save=save)
        if Mc_cut==True:
            # local_cat = apply_Mc_cut(local_cat)
            local_cat = local_cat.loc[local_cat['MAGNITUDE']>=mainshock.Mc].copy()
        # create_spatial_plot(mainshock=mainshock, local_cat=local_cat, Mc_cut=Mc_cut, catalogue_name=catalogue_name, save=save)
        plot_local_cat(mainshock=mainshock, local_cat=local_cat, earthquake_catalogue=earthquake_catalogue, catalogue_name=catalogue_name, Mc_cut=Mc_cut)
        results_dict, file_dict = identify_foreshocks_short(local_catalogue=local_cat, mainshock=mainshock, earthquake_catalogue=earthquake_catalogue)
        plot_models(mainshock=mainshock, results_dict=results_dict, file_dict=file_dict, Mc_cut=Mc_cut, catalogue_name=catalogue_name, save=save)
        results_list.append(results_dict)
        clear_output(wait=True)
        i+=1
    if len(results_list)<2:
        results_df = results_dict
    else:
        results_df = pd.DataFrame.from_dict(results_list)
        if save==True:
            if Mc_cut==False:
                Path(f'../data/{catalogue_name}/foreshocks/').mkdir(parents=True, exist_ok=True)
                results_df.to_csv(f'../data/{catalogue_name}/foreshocks/{save_name}_{date}.csv', index=False)
            if Mc_cut==True:
                Path(f'../data/{catalogue_name}/Mc_cut/foreshocks/').mkdir(parents=True, exist_ok=True)
                results_df.to_csv(f'../data/{catalogue_name}/Mc_cut/foreshocks/{save_name}_{date}.csv', index=False)
    return results_df