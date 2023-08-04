# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def plot_settlement(PSDDF_run, ax, field_data = False, field_data_type = "Settlement", layers = "All", plot_total = True, legend = True, file_type = "pgd",
                     leg_loc = "best", hold_on = True):
    # PSDDF_run: is a PSDDF_run object
    # field_data = True: plots the calcualted PSDDF settlements with the field settlement
    # layers: Controls which layer settlements are plotted. Options are:
        # "All": plots the settlement of all layers
        # "None": doesn't plot any of the layers
        # list of integers (eg. [1,2,3]): plots the selected layers
    # plot_total = True: plots the total settlements
    # ax: holds the axes that the plot should be made on
    # legend = True means the plot will have a legend

    # If field data is to be plotted
    if field_data:  ### Need to add capability for field_data to be a list
        #Check that the field data exists
        if not isinstance(PSDDF_run.field_data[field_data_type], list):
            raise TypeError("Field data doesn't exist. Check that it was loaded in")

        # Plot the field data
        for data in PSDDF_run.field_data[field_data_type]:
            ax.plot(data.iloc[0,:], data["Settlement"].iloc[0,:], label = "Field Data")
    
    # If layers are to be plotted
    if isinstance(layers, list) or layers == "All":
        # Check that the PSDDF layers data exists
        if not isinstance(PSDDF_run.layer_settlements[file_type], list):
            raise TypeError("The layer settlements isn't type list. Type is {}. Check that the layer settlements have been calculated".format(PSDDF_run.layer_settlements[file_type]))
        
        # Plot all of the layer settlements
        if layers == "All":
            i = 0
            for layer in PSDDF_run.layer_settlements[file_type]:
                ax.plot(layer["Time"], layer["Settlement"], label = "Layer {}".format(i+1))
                i+=1
        # Plot the selected layers
        else:
            for layer in layers:
                ax.plot(PSDDF_run.layer_settlements[file_type][layer-1]["Time"], PSDDF_run.layer_settlements[file_type][layer-1]["Settlement"],
                label = "Layer {}".format(layer))
    
    # If something other than a list, "All", or "None" is entered throw an error
    elif layers != "None":
        raise ValueError("layers must equal: \"All\", \"None\" or be a list ")
    
    # If the total material settlement is to be plotted
    if plot_total:
        # Check that the total settlements exist
        if not isinstance(PSDDF_run.tot_settlements[file_type], pd.DataFrame):
            raise TypeError("The total settlements don't exist. Check that the total settlements have been calculated")
        
        #Plot the data
        ax.plot(PSDDF_run.tot_settlements[file_type]["Time"], PSDDF_run.tot_settlements[file_type]["Settlement"], label = "Total Settlement")

    # Label x and y axes
    ax.set_xlabel("Time [{}]".format(PSDDF_run.units["t"]))
    ax.set_ylabel("Settlement [{}]".format(PSDDF_run.units["L"]))

    # If a legend should be shown
    if legend:
        ax.legend(loc = leg_loc)

    # If hold should be turned off
    if not hold_on:
        plt.tight_layout()
        plt.show()
        
def plot_Layer_data(PSDDF_run, xProps, yProps, fig, layers = "All", times = "All", legend = True, 
                    file_type = "pgd", leg_loc = "best", set_xlabel = True, set_ylabel = True, hold_on = True, 
                    input_cmps = ["Blues", "OrRd", "Greens", 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 
                                    'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']):
    # PSDDF_run: is a PSDDF_run object
    ## Note: xProps and yProps should have the same length
    # xProps: List of properties that should go on the x-axis. These labels correspond to the column headers of the layer_dfs
    # yProps: List of properties that should go on the y-axis. These labels correspond to the column headers of the layer dfs
    # fig: Fig object that holds the exes that the data should be plotted on
    # layers: Controls which layer data (eff_stress, void ratio, pore pressure) are plotted. Options are:
        # "All": plots the data for all layers
        # list of integers (eg. [1,2,3]): plots the selected layers
    # times: Controls which times should be plotted
        # "All": plots the data for all times
        # list of times PSDDF print times (eg. [100.00, 200.00, 300.00]): plots the data at selected times
    # legend: Control whether a legend is shown. True -> show legend, False -> don't show legend
    # file_type: set to "pgd" for dredged material or "pgc" for foundation
    # leg_loc: Allows specification of the legend. 
        # "best" enables the plot to put the legend where it thinks is best
        # Google matplotlib.pyplot.legend and look at the loc section for more options
    # set_xlabel: controls whether x labels should be shown on the plots
        # True: turns on the xlabels for all plots
        # list of booleans: Turns on the xlabels for the elements in the list set to True
    # set_ylabel: controls whether y labels should be shown on the plots
        # True: turns on the ylabels for all plots
        # lsit of booleans: Turns on ylabels for the lements in the list set to True
    # hold_on: Determines if the ax elements should still be avaible after this function finishes plotting
        # True: The plots can be editted after running this function
        # False: The plots cannot be editted after running this function
    # colormapsL List of colormaps, colormaps are

    # Store the list of axes
    axes = fig.axes

    # Check that the user inputted enough ax elements for the properties that they wanted plotted
    if len(xProps) > len(axes):
        raise IndexError("Mismatch of properties to plot and number of subplots provided. Number of subplots provided: {}. \
                         Number of properties {}".format(len(axes), len(xProps)))

    # Check that the user inputted the same dimension for xProps and yProps
    if len(xProps) != len(yProps):
        raise IndexError("xProps and yProps do not have the same length. Length of xProps: {}. Length of yProps: {}.".format(len(xProps), len(yProps)))
    
    # If the x_label is a bool
    if isinstance(set_xlabel, bool):
        # Create a list of booleans to facilitate plot labelling
        set_xlabel = [set_xlabel] * len(xProps)

    elif isinstance(set_xlabel, list) and not len(set_xlabel) >= len(xProps):
        # Check that the length of the input list is correct
        raise IndexError("Mismatch between number of properties to plot [{}] and set_xlabel length [{}]. ".format(len(xProps), len(set_xlabel)))
    elif not isinstance(set_xlabel, (list, bool)):
        raise TypeError("set_xlabel must a list the length of the number of parameters or True/False")

    # Check length and 
    if isinstance(set_ylabel, bool):
        set_ylabel = [set_xlabel] * len(xProps)

    elif isinstance(set_ylabel, list) and not len(set_ylabel) >= len(xProps):
        # Check that the length of the input list is correct
        raise IndexError("Mismatch between number of properties to plot [{}] and set_ylabel length [{}]. ".format(len(xProps), len(set_ylabel)))

    elif not isinstance(set_ylabel, (list, bool)):
        raise TypeError("set_ylabel must a list the length of the number of parameters or True/False")

    # Check that hold is a boolean
    if not isinstance(hold_on, bool):
        raise TypeError("hold must be a boolean.")

    # Get the list of layer dfs
    layer_dfs = PSDDF_run.layer_dfs[file_type]

     # Check that the PSDDF layers data exists
    if not isinstance(layer_dfs, list):
        raise TypeError("The layer dfs aren't type list. Type is {}. Check that the layer dfs have been formed".format(layer_dfs))

     # If layers are to be plotted
    if isinstance(layers, list) or layers == "All":
        # Define the color map
        num_times = len(times)

        # Plot all of the layer settlements
        if layers == "All":
            layer_num = 1
            # For each layer df
            for df in layer_dfs:
                # For the user specified data
                for i, (xProp, yProp, ax) in enumerate(zip(xProps, yProps, axes)):

                    # Continuously loop through the color maps
                    cmap = mpl.colormaps[input_cmps[i]]
                    start_color = 0.3
                    end_color = 1.0

                    # Get the number of times
                    num_times = len(times)

                    # Select each time
                    for j, t in enumerate(times):
                        # For the seleted time grab the corresponding data, and store in dummy df
                        dummy_df = df.loc[df["Time"] == t]

                        normalized_j = j/(num_times-1)
                        normalized_color = start_color + (end_color - start_color) * normalized_j

                        # Get the length of the df
                        # If it's the first time 
                        if j==0:
                            # Plot the data and create the legend label
                            
                            ax.plot(dummy_df[xProp], dummy_df[yProp], color = cmap(normalized_color), label = "Layer: {}".format(layer_num))
                        else:
                            # Otherwise just plot the data
                            ax.plot(dummy_df[xProp], dummy_df[yProp], color = cmap(normalized_color))

                    # show legend
                    if legend:
                        ax.legend(loc = leg_loc)

                    # Set x and y labels
                    if set_xlabel[i]:
                        ax.set_xlabel(xProp)
                    if set_ylabel[i]:
                        ax.set_ylabel(yProp)     
                # Increment the layer counter
                layer_num+=1
                          
        # Plot the selected layers
        else:
            # For each of the selected layers
            for layer in layers:
                # Select the corresponding df of data
                df = layer_dfs[layer-1]
                for i, (xProp, yProp, ax) in enumerate(zip(xProps, yProps, axes)):
                    
                    # Continuously loop through the color maps
                    cmap = mpl.colormaps[input_cmps[i]]
                    start_color = 0.3
                    end_color = 1.0
                    
                    # Get the number of times
                    num_times = len(times)
                    
                    for j, t in enumerate(times):

                        normalized_j = j/(num_times-1)
                        normalized_color = start_color + (end_color - start_color) * normalized_j

                        # Store the selected times in a dummy df 
                        dummy_df = df.loc[df["Time"] == t]
                        if j==0:
                            ax.plot(dummy_df[xProp], dummy_df[yProp],color = cmap(normalized_color), label = "Layer: {}".format(layer))
                        else:
                            ax.plot(dummy_df[xProp], dummy_df[yProp], color = cmap(normalized_color))
                    
                    # Set x and y labels
                    if set_xlabel[i]:
                        ax.set_xlabel(xProp)

                    if set_ylabel[i]:
                        ax.set_ylabel(yProp)  

                    # show legend
                    if legend:
                        ax.legend(loc = leg_loc)
    else:
        raise ValueError("layers must be a numeric list or \"All\"")
    
    # If hold is set to false
    if not hold_on:
        # Show the plot and disable editting of the figure
        plt.tight_layout()