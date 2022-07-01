import pandas as pd

def percent_cover_by_plot(neon_data_path, plot_name):
    """Calculates percent cover by NEON subplot.

    The percent cover for vegetation, standing dead, soil, and litter
    are calculated from the NEON Plant Presence and Percent Cover data
    product. The percent cover for standing dead, soil, and litter are
    weighted by the non-vegetation fraction.

    Parameters
    ----------
    neon_data_path : str
       Relative path to NEON Plant Presence and Percent Cover csv file.
    plot_name : str
       Plot name given in named location syntax used by NEON Terrestrial
       Observation System. For example, for Plot 55 of NEON site GRSM,
       the plot name is 'GRSM_055.basePlot.div'.

    Returns
    -------
    percent_cover_df : pandas.DataFrame
       Dataframe containing the subplot ID and percent cover fraction
       for vegetation, standing dead, soil, and litter.
    """
    # Open NEON plant presence percent cover data
    all_df = pd.read_csv(neon_data_path)
    # Define dataframe for plot
    plot_df = (all_df[all_df['namedLocation'] == plot_name])
    # Subset data
    plot_subset = plot_df[['plotID', 'subplotID', 'family',
                           'otherVariables', 'percentCover']]
    # Define and initialize variables
    ov = 'otherVariables'
    std = 'standingDead'
    pc = 'percentCover'
    so = 'soil'
    li = 'litter'
    percent_cover_ls = []
    subplot_ls = ['40.1.1', '40.3.1', '41.1.1', '41.4.1',
                  '31.1.1', '31.4.1', '32.2.1', '32.4.1']
    for plot in subplot_ls:
        # Subset data for subplot
        subplot = plot_subset[plot_subset['subplotID']==plot]
        # Select other variables
        subpl_othervar = subplot.dropna(subset=[ov])
        # Extract percent cover for standing dead, soil, litter
        if 'standingDead' in subpl_othervar[ov].unique():
            stdead = subpl_othervar[subpl_othervar[ov]==std][pc].iloc[0]
        else:
            stdead = 0
        if 'soil' in subpl_othervar[ov].unique():
            soil = subpl_othervar[subpl_othervar[ov]==so][pc].iloc[0]
        else:
            soil = 0
        if 'litter' in subpl_othervar[ov].unique():
            litter = (
                subpl_othervar[subpl_othervar[ov]==li][pc].iloc[0])
        else:
            litter = 0
        # Store percent cover values
        subpl_ls = [stdead, soil, litter]
        # Define vegetation fraction
        veg = subplot[pc].sum() - subpl_othervar[pc].sum()
        # Weight by non-vegetation fraction
        wt_subpl = [i * (100.0 - veg) / 100.0 for i in subpl_ls]
        # Add veg fraction to list
        wt_subpl[:0] = [veg]
        # Add subplot id to list
        wt_subpl[:0] = [plot]
        percent_cover_ls += [wt_subpl]
    percent_cover_df = pd.DataFrame(
        percent_cover_ls,
        columns=['name', 'veg', 'standingDead', 'soil', 'litter'])
    return percent_cover_df
