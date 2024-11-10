"""Module to plot predicition, etc.

This file regroups all functions used to plot the input data or the regression results
"""

import base64
import os
from io import BytesIO
from typing import Union
from xml.etree import ElementTree as ET

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable

mpl.use("agg")

CM_PER_INCH = 1 / 2.54
CONSTANT_TIME_STEP = "constant"


def extract_svg_dimensions(svg_content):
    """Extract dimensions from SVG content."""

    def _strip_unit(dimension):
        if (
            dimension.endswith("pt")
            or dimension.endswith("in")
            or dimension.endswith("cm")
            or dimension.endswith("mm")
            or dimension.endswith("px")
        ):
            return float(dimension[:-2])
        elif dimension.endswith("%"):
            return float(dimension[:-1])
        else:
            return float(dimension)

    root = ET.fromstring(svg_content)
    width = root.get("width")
    height = root.get("height")
    if width is None:
        raise ValueError("Width attribute is missing in the SVG content.")
    if height is None:
        raise ValueError("Height attribute is missing in the SVG content.")

    return _strip_unit(width.strip()), _strip_unit(height.strip())


def convert_plt_to_base64(plt):
    """Convert matplotlib plot to dimensions and base64 encoded image."""
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="svg", bbox_inches="tight")
    plt.close()
    img_buffer.seek(0)
    svg_content = img_buffer.getvalue().decode()
    content = base64.b64encode(img_buffer.read()).decode()
    width, height = extract_svg_dimensions(svg_content)

    return (width, height, content)


def plot_selection(rfo_model, plot_input=True, plot_results=True):
    """
    Plot visualizations defined by the input selection.

    Parameters:
    - rfo_model (object): Random forest regression model and results.

    This function plots various visualizations based on the input selection
    defined in the rfo_model object. It plots predictors, prediction correlation
    matrix, measurements, model predictions, and predictor importance for each
    time step if specified in what_to_plot attribute of rfo_model. Additionally,
    it can plot predictor importance across all days if specified.
    """
    output_dir = rfo_model.work_dir
    what_to_plot = rfo_model.parameters.what_to_plot

    if rfo_model.input_data.all_predictors_constant():
        predictor_time_steps = [CONSTANT_TIME_STEP]
    else:
        predictor_time_steps = rfo_model.input_data.soil_moisture_data.time_steps

    for time_step in predictor_time_steps:
        if what_to_plot.predictors and plot_input:
            plot_predictors(
                rfo_model,
                time_step,
                output_dir,
                add_measurments=True,
                show_mask=True,
            )

        if what_to_plot.pred_correlation and plot_results:
            prediction_correlation_matrix(rfo_model, time_step, output_dir)

    for time_step in rfo_model.input_data.soil_moisture_data.time_steps:
        if what_to_plot.day_measurements and plot_input:
            plot_measurements(
                rfo_model,
                time_step,
                output_dir,
            )
        if what_to_plot.day_prediction_map and plot_results:
            plot_rfo_model(
                rfo_model,
                time_step,
                output_dir,
            )
        if what_to_plot.day_predictor_importance and plot_results:
            plot_predictor_importance(
                rfo_model,
                time_step,
                output_dir,
            )
    if what_to_plot.alldays_predictor_importance and plot_results:
        predictor_importance_along_days(rfo_model, output_dir)


def plot_predictors(
    rfo_model,
    time_step,
    output_dir: Union[str, None],
    add_measurments=True,
    show_mask=True,
):
    """
    Plot all predictors as color maps.

    Parameters:
    - output_dir (str/None): Directory path to save the plot image file. If None
     return the plot image as a base64 string.

    This function plots all predictors as color maps, with predictor name and
    unit displayed. It automatically adjusts the layout based on the number
    of predictors and shares the same axes for all subplots.
    """
    if show_mask:
        transparency = 0.6
    else:
        transparency = 0

    n_cols = np.ceil(len(rfo_model.input_data.predictors) / 2).astype(int)
    xaxis, yaxis = rfo_model.input_data.soil_moisture_data.geometry.get_axis()

    if CONSTANT_TIME_STEP == time_step:
        x = (
            np.concatenate(list(rfo_model.input_data.soil_moisture_data.x.values()))
            / 1000
        )
        y = (
            np.concatenate(list(rfo_model.input_data.soil_moisture_data.y.values()))
            / 1000
        )
    else:
        x = rfo_model.input_data.soil_moisture_data.x[time_step] / 1000
        y = rfo_model.input_data.soil_moisture_data.y[time_step] / 1000

    fig, ax = plt.subplots(
        nrows=2,
        ncols=n_cols,
        sharex=True,
        sharey=True,
        figsize=(17 * CM_PER_INCH, 9 * CM_PER_INCH),
    )

    fig.subplots_adjust(wspace=0.4)
    plt.rcParams.update({"font.size": 5})
    axes_count = 0

    nan_mask = rfo_model.input_data.get_nan_mask(time_step)

    for pred_name, pred_data in rfo_model.input_data.predictors.items():
        values_on_nodes = pred_data.values_on_nodes[time_step]

        im = ax.flat[axes_count].pcolormesh(
            xaxis,
            yaxis,
            values_on_nodes,
            shading="auto",
            cmap="viridis",
            edgecolors="k",
            linewidths=0.5,
            alpha=1 - nan_mask.astype(float) * transparency,
        )
        if add_measurments:
            ax.flat[axes_count].scatter(x, y, color="black", s=1, alpha=0.5)

        ax.flat[axes_count].set_title(pred_name)
        ax.flat[axes_count].set_aspect(1)

        divider = make_axes_locatable(ax.flat[axes_count])
        cax = divider.append_axes("right", size="5%", pad=0.15)
        cbar = plt.colorbar(im, cax=cax)
        cbar.ax.set_title(pred_data.information.unit)
        axes_count += 1

    # Hide any remaining empty subplots
    for i in range(axes_count, ax.size):
        fig.delaxes(ax.flat[i])

    if output_dir is None:
        return convert_plt_to_base64(plt)

    if time_step == CONSTANT_TIME_STEP:
        fig_file_path = os.path.join(output_dir, "predictors.svg")
    else:
        fig_file_path = os.path.join(output_dir, f"predictors_{time_step}.svg")

    plt.savefig(fig_file_path, dpi=300)
    plt.close()


def prediction_correlation_matrix(rfo_model, time_step, output_dir: Union[str, None]):
    """Plot the correlation matrix between all predictors, 2 by 2.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - output_dir (str/None): Directory path to save the plot image file. If None
     return the plot image as a base64 string.

    This function plots the correlation matrix between all predictors as a heatmap.
    Each cell represents the correlation coefficient between two predictors.
    The x-axis and y-axis labels show the names of the predictors.
    The color intensity indicates the strength and direction of correlation,
    ranging from -1 (strong negative correlation) to 1 (strong positive correlation).
    """
    ticks = list(rfo_model.input_data.predictors.keys())
    plt.figure(figsize=(12 * CM_PER_INCH, 9 * CM_PER_INCH))
    plt.rcParams.update({"font.size": 5})
    correlation_matrix = rfo_model.input_data.compute_correlation_matrix(time_step)
    annot_array = np.vectorize(lambda x: "NaN" if np.isnan(x) else f"{x:.2f}")(
        correlation_matrix
    )
    correlation_matrix = np.nan_to_num(correlation_matrix)  # Replace NaNs with zeros

    sns.heatmap(
        correlation_matrix,
        annot=annot_array,
        fmt="",
        cmap="seismic",
        vmin=-1,
        vmax=1,
        xticklabels=ticks,
        yticklabels=ticks,
        cbar_kws={"label": "Correlation coefficient"},
    )

    if output_dir is None:
        return convert_plt_to_base64(plt)

    if time_step == CONSTANT_TIME_STEP:
        fig_file_path = os.path.join(output_dir, "correlation_matrix.svg")
    else:
        fig_file_path = os.path.join(output_dir, f"correlation_matrix_{time_step}.svg")

    plt.savefig(fig_file_path, dpi=300)
    plt.close()


def draw_error_band_path(x, y, error):
    """
    Calculate normals via centered finite differences.

    Parameters:
    - x (numpy.ndarray): Array of x-coordinates.
    - y (numpy.ndarray): Array of y-coordinates.
    - error (numpy.ndarray): Array of error values corresponding to each point.

    Returns:
    - matplotlib.path.Path: Path object representing the error band.

    This function calculates the normals of a path using centered finite differences.
    It computes the components of the normals and extends the path in both directions
    based on the error values. The resulting path forms an error band around the
    original path.
    """
    dist_to_next_point_x_component = np.concatenate(
        [[x[1] - x[0]], x[2:] - x[:-2], [x[-1] - x[-2]]]
    )
    dist_to_next_point_y_component = np.concatenate(
        [[y[1] - y[0]], y[2:] - y[:-2], [y[-1] - y[-2]]]
    )
    dist_to_next_point = np.hypot(
        dist_to_next_point_x_component, dist_to_next_point_y_component
    )
    normal_x_component = dist_to_next_point_y_component / dist_to_next_point
    normal_y_component = -dist_to_next_point_x_component / dist_to_next_point

    scale_error_vector = 3
    x_error_end_point = x + normal_x_component * error * scale_error_vector
    y_error_end_point = y + normal_y_component * error * scale_error_vector

    vertices = np.block([[x_error_end_point, x[::-1]], [y_error_end_point, y[::-1]]]).T
    codes = np.full(len(vertices), Path.LINETO)
    codes[0] = Path.MOVETO
    return Path(vertices, codes)


def plot_measurements(rfo_model, time_step, output_dir: Union[str, None]):
    """
    Plot measurements as scatter on a x-y map.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - time_step (int): Index of the time step for which measurements are plotted.
    - output_dir (str/None): Directory path to save the plot image file. If None
     return the plot image as a base64 string.

    This function plots measurements as a scatter plot on an x-y map. It uses
    the soil moisture measurements from the specified time step of the input
    data. The measurements are colored according to their corresponding soil
    moisture values. If Monte Carlo simulations are enabled, error bands
    representing the standard deviations are overlaid on the scatter plot.
    """
    plt.figure()
    plt.gca().set_aspect(1)
    soil_moisture_data = rfo_model.input_data.soil_moisture_data
    x = soil_moisture_data.x[time_step] / 1000
    y = soil_moisture_data.y[time_step] / 1000
    sc = plt.scatter(
        x,
        y,
        c=soil_moisture_data.soil_moisture[time_step],
        cmap="Spectral",
        s=5,
        vmin=0.1,
        vmax=0.6,
        zorder=2,
        label="Measurements",
    )
    if soil_moisture_data.uncertainty:
        plt.gca().add_patch(
            PathPatch(
                draw_error_band_path(
                    x,
                    y,
                    -soil_moisture_data.soil_moisture_dev_low[time_step],
                ),
                alpha=0.3,
                color="purple",
                label="Lower/upper SD",
            )
        )
        plt.gca().add_patch(
            PathPatch(
                draw_error_band_path(
                    x,
                    y,
                    soil_moisture_data.soil_moisture_dev_high[time_step],
                ),
                alpha=0.3,
                color="purple",
            )
        )
    plt.xlabel("Easting (km)")
    plt.ylabel("Northing (km)")
    plt.legend(loc="upper left")
    cbar = plt.colorbar(sc, shrink=0.55)
    cbar.set_label("Gravimetric soil moisture (g/g)")

    if output_dir is None:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, f"measurements_{time_step}.svg")
    plt.savefig(fig_file_path, dpi=300)
    plt.close()


def plot_rfo_model(rfo_model, time_step, *args, **kwargs):
    """Plot random forest prediction as a color map."""
    if (
        rfo_model.parameters.monte_carlo_soil_moisture
        or rfo_model.parameters.monte_carlo_predictors
    ):
        return plot_rfo_model_with_dispersion(rfo_model, time_step, *args, **kwargs)
    else:
        return plot_rfo_model_no_dispersion(rfo_model, time_step, *args, **kwargs)


def plot_rfo_model_no_dispersion(
    rfo_model,
    time_step,
    output_dir: Union[str, None],
):
    """
    Plot soil moisture prediction as a color map.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - time_step (int): Index of the time step for which predictions are plotted.
    - output_dir (str/None): Directory path to save the plot image file. If None
     return the plot image as a base64 string.
    """
    if not output_dir:
        output_dir = rfo_model.work_dir

    xaxis, yaxis = rfo_model.geometry.get_axis()
    time_index = rfo_model.input_data.soil_moisture_data.time_steps.index(time_step)

    plt.rcParams.update({"font.size": 6})
    fig, ax = plt.subplots(figsize=(16 * CM_PER_INCH, 14 * CM_PER_INCH))
    im = plt.pcolormesh(
        xaxis,
        yaxis,
        rfo_model.RF_prediction[0, time_index, :, :],
        vmin=0.1,
        vmax=0.45,
        cmap="Spectral",
    )

    plt.scatter(
        rfo_model.input_data.soil_moisture_data.x[time_step] / 1000,
        rfo_model.input_data.soil_moisture_data.y[time_step] / 1000,
        c="black",
        s=0.5,
    )
    ax.set_title(time_step)
    ax.set_aspect(1)
    cbar = plt.colorbar(im)
    cbar.ax.tick_params(labelsize=14)
    if output_dir is None:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "RF_prediction_" + time_step + ".svg")
    plt.savefig(fig_file_path, dpi=300)
    plt.close()


def plot_rfo_model_with_dispersion(
    rfo_model,
    time_step,
    output_dir: Union[str, None],
):
    """
    Plot soil moisture mean prediction and coefficient of dispersion maps.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - time_step (int): Index of the time step for which predictions are plotted.
    - output_dir (str/None): Directory path to save the plot image file. If None
     return the plot image as a base64 string.

    This function plots the mean prediction and coefficient of dispersion maps
    for soil moisture predictions. It uses the data from the specified time
    step of the random forest model. Measurement locations are overlaid on the
    plots. The first subplot displays the mean prediction map, while the second
    subplot displays the coefficient of dispersion map.
    """
    xaxis, yaxis = rfo_model.geometry.get_axis()
    time_index = rfo_model.input_data.soil_moisture_data.time_steps.index(time_step)

    plt.rcParams.update({"font.size": 7})

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16 / 2.54, 10 / 2.54))
    axes[0].set_aspect(1)
    axes[1].set_aspect(1)

    divider = make_axes_locatable(axes[0])
    cax = divider.append_axes("right", size="5%", pad=0.15)
    im = axes.flat[0].pcolormesh(
        xaxis,
        yaxis,
        rfo_model.MC_mean[time_index],
        shading="auto",
        vmin=0.1,
        vmax=0.45,
        cmap="Spectral",
    )
    axes.flat[0].scatter(
        rfo_model.input_data.soil_moisture_data.x[time_step] / 1000,
        rfo_model.input_data.soil_moisture_data.y[time_step] / 1000,
        c="black",
        s=1,
    )
    axes.flat[0].set_title("Mean")
    plt.colorbar(im, cax=cax)

    im1 = axes.flat[1].pcolormesh(
        xaxis,
        yaxis,
        rfo_model.dispersion_coefficient[time_index],
        shading="auto",
        vmin=0,
        vmax=0.15,
        cmap="Reds",
    )
    axes.flat[1].set_title("Coefficient of dispersion")
    axes.flat[1].tick_params(axis="y", left=False, labelleft=False)
    divider = make_axes_locatable(axes[1])
    cax = divider.append_axes("right", size="5%", pad=0.15)
    plt.colorbar(im1, cax=cax)

    fig.suptitle(time_step)

    if output_dir is None:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "RF_prediction_" + time_step + ".svg")
    plt.savefig(fig_file_path, dpi=300)
    plt.close()


def plot_monte_carlo_iteration(
    rfo_model,
    time_step,
    iteration_index,
    output_dir: Union[str, None],
):
    """Plot the Monte Carlo itration for the given RFO model and time step.

    Parameters:
    - rfo_model (object): The RFO model containing prediction data.
    - time_step (int): The time step index for plotting.
    - iteration_index (int): The iteration index for Monte Carlo simulation.
    - output_dir (str/None): Directory path to save the plot image file. If None
     return the plot image as a base64 string.
    """
    xaxis, yaxis = rfo_model.geometry.get_axis()
    time_step = rfo_model.input_data.soil_moisture_data.time_steps[time_step]

    plt.rcParams.update({"font.size": 6})
    fig, ax = plt.subplots(figsize=(16 * CM_PER_INCH, 14 * CM_PER_INCH))
    im = plt.pcolormesh(
        xaxis,
        yaxis,
        rfo_model.RF_prediction[iteration_index, time_step, :, :],
        vmin=0.1,
        vmax=0.45,
        cmap="Spectral",
    )
    plt.scatter(
        rfo_model.input_data.soil_moisture_data.x[time_step] / 1000,
        rfo_model.input_data.soil_moisture_data.y[time_step] / 1000,
        c="black",
        s=0.5,
    )
    ax.set_title(time_step)
    ax.set_aspect(1)
    cbar = plt.colorbar(im)
    cbar.ax.tick_params(labelsize=14)

    if output_dir is None:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(
        output_dir,
        "RF_prediction_" + time_step + "_iteration_" + iteration_index + ".svg",
    )
    plt.savefig(fig_file_path, dpi=300)
    plt.close()


def plot_predictor_importance(
    rfo_model,
    time_step,
    output_dir: Union[str, None],
):
    """
    Plot predictor importance from the random forest model.

    This function plots the predictor importance from the random forest model
    for the specified time step. It displays the importance values as bars for
    each predictor. If Monte Carlo simulations were performed, the function
    shows the 5th, 50th (median), and 95th quantiles of the importance values.
    Otherwise, it displays the raw importance values. The x-axis represents the
    predictors, and the y-axis represents the importance values.
    """
    time_index = rfo_model.input_data.soil_moisture_data.time_steps.index(time_step)

    plt.rcParams.update({"font.size": 7})
    x = np.arange(len(rfo_model.input_data.predictors))
    plt.figure(figsize=(16 / 2.54, 7 / 2.54))
    if (
        rfo_model.parameters.monte_carlo_soil_moisture
        or rfo_model.parameters.monte_carlo_predictors
    ):
        plt.bar(
            rfo_model.input_data.predictors.keys(),
            np.percentile(
                rfo_model.predictor_importance[:, time_index, :],
                95,
                axis=0,
            ),
            color="deepskyblue",
            label="q95",
        )
        plt.bar(
            rfo_model.input_data.predictors.keys(),
            np.percentile(
                rfo_model.predictor_importance[:, time_index, :],
                50,
                axis=0,
            ),
            color="blue",
            label="median",
        )
        plt.bar(
            rfo_model.input_data.predictors.keys(),
            np.percentile(
                rfo_model.predictor_importance[:, time_index, :],
                5,
                axis=0,
            ),
            color="navy",
            label="q5",
        )
        plt.legend()
    else:
        plt.bar(
            rfo_model.input_data.predictors.keys(),
            rfo_model.predictor_importance[0, time_index, :],
        )
    plt.xticks(x, rfo_model.input_data.predictors.keys())
    plt.title(time_step)

    if output_dir is None:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, f"predictor_importance_{time_step}.svg")
    plt.savefig(fig_file_path, dpi=300)
    plt.close()


def predictor_importance_along_days(
    rfo_model,
    output_dir: Union[str, None],
):
    """
    Plot predictor importance from the RF model along the days.

    This function plots the predictor importance from the random forest model
    over the days. It displays the mean importance values for each predictor
    across all days. The x-axis represents the days, and the y-axis
    represents the importance values.
    """
    number_predictors = len(rfo_model.input_data.predictors)
    time_steps = rfo_model.input_data.soil_moisture_data.time_steps
    predictor_importance = rfo_model.predictor_importance
    predictors = rfo_model.input_data.predictors

    plt.rcParams.update({"font.size": 7})
    fig, ax = plt.subplots(
        number_predictors,
        sharex=True,
        figsize=(17 / 2.54, 16 / 2.54),
    )
    if number_predictors == 1:
        ax.plot(
            range(len(time_steps)),
            np.mean(predictor_importance[:, :, 0], axis=0),
            label=list(predictors.keys())[0],
        )
        ax.set_ylim(0, 1)
        ax.legend(loc="right")
    else:
        for pred_index, predictor_name in enumerate(predictors.keys()):
            ax[pred_index].plot(
                range(len(time_steps)),
                np.mean(predictor_importance[:, :, pred_index], axis=0),
                label=predictor_name,
            )
            ax[pred_index].set_ylim(0, 1)
            ax[pred_index].legend(loc="right")

    if output_dir is None:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "predictor_importance_vs_days.svg")
    plt.savefig(fig_file_path, dpi=300)
    plt.close()
