
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import cmocean.cm as cmo

from .find_stages import find_intensification_period, find_decay_period, find_mature_stage

def plot_phase(df, phase, ax=None, show_title=True):
    # Create a copy of the DataFrame
    """
    Plot a specific phase of the cyclone's lifecycle on a given axis.

    Parameters:
    df (pd.DataFrame): DataFrame containing vorticity data and phase information.
    phase (str): The phase to plot, e.g., 'incipient', 'intensification', etc.
    ax (matplotlib.axes.Axes, optional): Matplotlib Axes object to plot on. 
                                         If None, a new figure and axes are created.
    show_title (bool, optional): Whether to display the phase name as a title on the plot.

    The function fills the area corresponding to the specified phase with a color 
    defined in the `colors_phases` dictionary, plots the unsmoothed vorticity series, 
    and overlays the smoothed vorticity on a twin y-axis.
    """
    df_copy = df.copy()

    zeta = df_copy['z_unfil']
    vorticity_smoothed = df_copy['z']

    colors_phases = {'incipient': '#65a1e6', 'intensification': '#f7b538',
                     'mature': '#d62828', 'decay': '#9aa981', 'residual': 'gray'}

    # Find the start and end indices of the period
    phase_starts = df_copy[(df_copy['periods'] == phase) &
                            (df_copy['periods'].shift(1) != phase)].index
    phase_ends = df_copy[(df_copy['periods'] == phase) &
                          (df_copy['periods'].shift(-1) != phase)].index

    # Use the provided axes or create new ones
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    ax.axhline(0, c='gray', linewidth=0.5)

    # Iterate over the periods and fill the area
    for start, end in zip(phase_starts, phase_ends):
        ax.fill_between(df_copy.index, zeta, where=(df_copy.index >= start) &
                        (df_copy.index <= end), alpha=0.7, color=colors_phases[phase])

    ax.plot(df_copy.index, zeta, c='gray', lw=3, alpha=0.8)
    ax2 = ax.twinx()
    ax2.axis('off')
    ax2.plot(df_copy.index, vorticity_smoothed, c='k')

    if show_title:
        title = ax.set_title(f'{phase}', fontweight='bold', horizontalalignment='center')
        title.set_position([0.5, 1.05])  # Adjust the title position as needed


    if ax is None:
        plt.show()

def plot_specific_peaks_valleys(df, ax, *kwargs):
    """
    Plot peaks and valleys of specific series in a DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing the series and their respective peaks and valleys.
    ax (matplotlib.axes.Axes): Matplotlib Axes object to plot on.
    *kwargs (str): Specify the series and whether to plot peaks or valleys, e.g., 'z_peaks', 'dz_valleys', etc.

    The function plots the specified series and their corresponding peaks and valleys on the given axes. The color and marker size are determined by the series name ('z', 'dz', or 'dz2').
    """
    # Define the series and colors for plotting
    series_colors = {'z': 'k', 'dz': '#d62828', 'dz2': '#f7b538'}
    marker_sizes = {'z': 190, 'dz': 120, 'dz2': 50}

    zeta = df['z']

    ax2 = ax.twinx()
    ax2.axis('off')

    for key in kwargs:
        key_name = key.split('_')[0]
        peak_or_valley = key.split('_')[1][:-1]

        peaks_valleys_series = df[f"{key_name}_peaks_valleys"]

        color = series_colors[key_name]
        marker_size = marker_sizes[key_name]
        zorder = 99 if key_name == 'z' else 100 if key_name == 'dz' else 101

        mask_notna = peaks_valleys_series.notna()
        mask_peaks = peaks_valleys_series == 'peak'

        # Plot peaks
        ax2.scatter(df.index[mask_notna & mask_peaks],
                   zeta[mask_notna & mask_peaks],
                   marker='o', color=color, s=marker_size, zorder=zorder)

        # Plot valleys
        ax2.scatter(df.index[mask_notna & ~mask_peaks],
                   zeta[mask_notna & ~mask_peaks],
                   marker='o', edgecolors=color, facecolors='none',
                   s=marker_size, linewidth=2, zorder=zorder)

def plot_vorticity(ax, vorticity):
    """
    Plot vorticity and its second smoothed derivative.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib Axes object to plot on.
    vorticity : Cyclophaser.vorticity.Vorticity
        Vorticity object.

    The function plots the vorticity and its second smoothed derivative on the given axes. The smoothed derivative is the second derivative of the vorticity, which is filtered twice to remove high-frequency noise.
    """
    zeta = vorticity.zeta

    vorticity_smoothed = vorticity.vorticity_smoothed2

    ax.axhline(0, c='gray', linewidth=0.5)
    
    ax.plot(vorticity.time, zeta, c='gray', linewidth=0.75, label='ζ')

    ax2 = ax.twinx()
    ax2.axis('off')
    ax2.plot(vorticity.time, vorticity_smoothed, c='k', linewidth=2, label=r"$ζ_{filt}$")

    ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))

    ax.legend(loc='best')

    ax.set_title("filter ζ", fontweight='bold', horizontalalignment='center')

def plot_series_with_peaks_valleys(df, ax):
    """
    Plot the vorticity and its first and second derivatives, along with their peaks and valleys.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the vorticity and its derivatives, as well as the peaks and valleys.
    ax : matplotlib.axes.Axes
        Axes to plot on.
    """
    ax.axhline(0, c='gray', linewidth=0.5)

    # Define the series and colors for plotting
    series_names = ['z', 'dz', 'dz2']
    labels = ['ζ',
              r"$\frac{∂ζ_{filt}}{∂t} \times 10^{3}$",
               r"$\frac{∂^{2}ζ_{filt}}{∂t^{2}} \times 20^{4}$"]
    series_colors = ['k', '#d62828', '#f7b538']
    marker_sizes = [190, 120, 50]
    peaks_valleys_columns = ['z_peaks_valleys', 'dz_peaks_valleys', 'dz2_peaks_valleys']
    scaling_factors = [1, 100, 2000]

    # Plot the series and their peaks/valleys
    for series_name, label, series_color, peaks_valleys_col, marker_size, scaling_factor in zip(series_names,
                                                                                         labels,
                                                                                         series_colors,
                                                                                         peaks_valleys_columns,
                                                                                         marker_sizes,
                                                                                         scaling_factors):
        ax.plot(df.index, df[series_name] * scaling_factor, color=series_color, label=label)
        ax.scatter(df.index[df[peaks_valleys_col] == 'peak'],
                    df[series_name][df[peaks_valleys_col] == 'peak'] * scaling_factor,
                   color=series_color, marker='o', s=marker_size)
        ax.scatter(df.index[df[peaks_valleys_col] == 'valley'],
                    df[series_name][df[peaks_valleys_col] == 'valley'] * scaling_factor,
                   color=series_color, marker='o', facecolor='None', linewidth=2, s=marker_size)

    ax.set_title('derivate ζ', fontweight='bold', horizontalalignment='center')

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.5), ncol=4)

def plot_peaks_valleys_series(series, ax, *peaks_valleys_series_list):
    """
    Plot a time series along with its identified peaks and valleys.

    Parameters:
    series (pd.Series): The main time series data to be plotted.
    ax (matplotlib.axes.Axes): Matplotlib Axes object to plot on.
    *peaks_valleys_series_list (pd.Series): Variable number of series indicating 
                                            peaks and valleys for 'z', 'dz', and 'dz2'.

    The function plots the main series and highlights the peaks and valleys
    with different colors and markers. It also draws vertical lines at specific
    valleys and peaks to indicate key stage changes in the series.
    """
    # Plot the series
    ax.plot(series, color='k')

    # Plot peaks and valleys
    colors = ['k', '#d62828', '#f7b538','#9aa981'] 
    marker_size = [190, 120, 50]
    zorder = [99, 100, 101]
    for i, peaks_valleys_series in enumerate(peaks_valleys_series_list):
        mask_notna = peaks_valleys_series.notna()
        mask_peaks = peaks_valleys_series == 'peak'

        # Plot peaks
        ax.scatter(series.index[mask_notna & mask_peaks], series[mask_notna & mask_peaks],
                    marker='o', color=colors[i], s=marker_size[i], zorder=zorder[i])

        # Plot valleys
        ax.scatter(series.index[mask_notna & ~mask_peaks], series[mask_notna & ~mask_peaks],
                    marker='o', edgecolors=colors[i], facecolors='None', s=marker_size[i],
                      linewidth=2,  zorder=zorder[i])
        
    # Plot vertical lines at valleys of z, valleys of dz, and peaks of dz
    valleys_z = peaks_valleys_series_list[0][peaks_valleys_series_list[0] == 'valley']
    valleys_dz = peaks_valleys_series_list[1][peaks_valleys_series_list[1] == 'valley']
    peaks_dz = peaks_valleys_series_list[1][peaks_valleys_series_list[1] == 'peak']

    for x in valleys_z.index:
        ax.axvline(x=x, color=colors[1], linestyle='-', linewidth=1.5, zorder=10)
    for x in valleys_dz.index:
        ax.axvline(x=x, color=colors[2], linestyle='-', linewidth=1.5, zorder=11)
    for x in peaks_dz.index:
        ax.axvline(x=x, color=colors[3], linestyle='-', linewidth=1.5, zorder=12)

    ax.set_title('stages centers', fontweight='bold', horizontalalignment='center')
    ax.title.set_position([0.5, 1.05])

def plot_all_periods(phases_dict, df, ax=None, vorticity=None, periods_outfile_path=None):    
    """
    Plot vorticity data with periods.

    Parameters
    ----------
    phases_dict : dict
        A dictionary where the keys are the phase names and the values are tuples
        containing the start and end times of each phase.
    df : pandas.DataFrame
        The DataFrame containing the vorticity data.
    ax : matplotlib.axes.Axes, optional
        The Axes object to plot on. If not provided, a new figure will be created.
    vorticity : Cyclophaser.vorticity.Vorticity, optional
        The Vorticity object containing the vorticity data. If not provided, the
        DataFrame will be used instead.
    periods_outfile_path : str, optional
        The path to save the plot to. If not provided, the plot will not be saved.

    Notes
    -----
    The plot will be saved to a PNG file with the same name as the provided path,
    but with a '.png' extension added. The plot will be saved at a resolution of 500
    dpi.

    Returns
    -------
    None
    """
    # Define base colors for phases
    colors_phases = {
        'incipient': '#65a1e6',
        'intensification': '#f7b538',
        'mature': '#d62828',
        'decay': '#9aa981',
        'residual': 'gray'
    }

    # Create a new figure if ax is not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(6.5, 5))

    if vorticity is not None:
        ax.plot(vorticity.time, vorticity.zeta, linewidth=2.5, color='gray', label=r'ζ')

        ax2 = ax.twinx()
        ax2.axis('off')
        ax2.plot(vorticity.time, vorticity.filtered_vorticity, linewidth=2, c='#d68c45', label=r'$ζ_{f}$')
        ax2.plot(vorticity.time, vorticity.vorticity_smoothed, linewidth=2, c='#1d3557', label=r'$ζ_{fs}$')
        ax2.plot(vorticity.time, vorticity.vorticity_smoothed2, linewidth=2, c='#e63946', label=r'$ζ_{fs^{2}}$')

    else:
        ax.plot(df.time, df.z, linewidth=0.75, color='gray', label=r'ζ')

    # Initialize legend labels and tracked phases
    legend_labels = [r'ζ']
    added_phases = set()  # Track which phases have been added to the legend

    # Shade the areas between the beginning and end of each period
    for phase, (start, end) in phases_dict.items():
        # Extract the base phase name (remove any numbers)
        base_phase = phase.split()[0].strip()

        # Access the color based on the base phase name
        color = colors_phases.get(base_phase, 'gray')  # Default to gray if phase not found

        # Fill between the start and end indices with the corresponding color
        ax.fill_between(vorticity.time, vorticity.zeta.values,
                        where=(vorticity.time >= start) & (vorticity.time <= end),
                        alpha=0.4, color=color, label=base_phase)

        # Add the base phase name to the legend if it hasn't been added yet
        if base_phase not in added_phases:
            legend_labels.append(base_phase)
            added_phases.add(base_phase)

    # Set the title
    ax.set_title('Vorticity Data with Periods')

    # Remove duplicate labels from the legend
    handles, labels = ax.get_legend_handles_labels()

    # Get handles and labels from ax2 if it exists
    if 'ax2' in locals():
        handles2, labels2 = ax2.get_legend_handles_labels()
        handles += handles2
        labels += labels2

    # Create a unique list of labels
    unique_labels = []
    unique_handles = []
    for handle, label in zip(handles, labels):
        if label not in unique_labels and label in legend_labels:
            unique_labels.append(label)
            unique_handles.append(handle)

    # Set the legend
    ax.legend(unique_handles, unique_labels, loc='upper right', bbox_to_anchor=(1.5, 1))

    # Format the date axis
    ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
    date_format = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(date_format)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    # Save the plot if an output file path is provided
    if periods_outfile_path is not None:
        fname = f"{periods_outfile_path}.png"
        plt.savefig(fname, dpi=500)
        print(f"{fname} created.")

def plot_didactic(df, vorticity, output_directory, **periods_args):    
    """
    Plot vorticity data in a didactic way to illustrate the CycloPhaser methodology.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the vorticity data.
    vorticity : Cyclophaser.vorticity.Vorticity
        The Vorticity object containing the vorticity data.
    output_directory : str
        The directory where the plot will be saved.
    **periods_args : dict
        Additional arguments to pass to the periods detection functions.

    Notes
    -----
    This function plots the vorticity data in a step-by-step way to illustrate the
    CycloPhaser methodology. The plot is saved to a PNG file in the specified
    output directory.
    """
    # First step: filter vorticity data
    fig = plt.figure(figsize=(10, 8.5))
    ax1 = fig.add_subplot(331)
    plot_vorticity(ax1, vorticity)

    # Second step: identify peaks and valleys of vorticity
    ax2 = fig.add_subplot(332)
    plot_series_with_peaks_valleys(df, ax2)

    # Third step: look for patterns
    ax3 = fig.add_subplot(333)
    plot_peaks_valleys_series(
        df['z'], ax3,
        df['z_peaks_valleys'],
        df['dz_peaks_valleys'],
        df['dz2_peaks_valleys'], 
        )
    
    # Intensification phase
    df_int = find_intensification_period(df.copy(), **periods_args)
    ax4 = fig.add_subplot(334)
    plot_phase(df_int, "intensification", ax4)
    plot_specific_peaks_valleys(df_int, ax4, "z_peaks", "z_valleys")

    # Decay phase
    df_decay = find_decay_period(df.copy(), **periods_args)
    ax5 = fig.add_subplot(335)
    plot_phase(df_decay, "decay", ax5)
    plot_specific_peaks_valleys(df_decay, ax5, "z_peaks", "z_valleys")

    # Mature phase
    df_mature = find_mature_stage(df.copy(), **periods_args)
    ax6 = fig.add_subplot(336)
    plot_phase(df_mature, "mature", ax6)
    plot_specific_peaks_valleys(df_mature, ax6, "z_peaks", "z_valleys", "dz_valleys", "dz_peaks")

    # Residual stage
    ax7 = fig.add_subplot(337)
    plot_phase(df, "residual", ax7)
    plot_specific_peaks_valleys(df_decay, ax7, "z_peaks", "z_valleys")

    # Incipient phase
    ax8 = fig.add_subplot(338)
    plot_phase(df, "incipient", ax8, show_title=False)
    ax8.set_title("incipient", fontweight='bold', horizontalalignment='center')
    ax8.title.set_position([0.5, 1.05])
    plot_specific_peaks_valleys(df_decay, ax8, "z_valleys", "dz_valleys")

    # Put everything together
    ax9 = fig.add_subplot(339)
    plot_phase(df, "incipient", ax9, show_title=False)
    plot_phase(df, "intensification", ax9, show_title=False)
    plot_phase(df, "mature", ax9, show_title=False)
    plot_phase(df, "decay", ax9, show_title=False)
    plot_phase(df, "residual", ax9)
    ax9.set_title("post processing", fontweight='bold', horizontalalignment='center')
    ax9.title.set_position([0.5, 1.05])


    # Set y-axis labels in scientific notation (power notation) and change date format to "%m%d"
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
        date_format = mdates.DateFormatter("%m-%d %HZ")
        ax.xaxis.set_major_formatter(date_format)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    plt.subplots_adjust(hspace=0.6)
    
    outfile = f'{output_directory}.png'
    plt.savefig(outfile, dpi=500)
    print(f"{outfile} created.")