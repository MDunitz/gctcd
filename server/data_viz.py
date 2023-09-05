import bokeh.io
from bokeh import plotting
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, ColorBar, LinearColorMapper
from bokeh.palettes import Spectral6, Inferno256
from bokeh.transform import jitter

import pandas as pd
import numpy as np



def get_methane_df(df):
    methane_df = df[(df['peak_compound'] == 'CH4') & (df['is_std'] == False) & (df['sample_id']!="DROP_ME")]
    return methane_df


def get_CO2_df(df):
    CO2_df = df[(df['peak_compound'] == 'CO2') & (df['is_std'] == False) & (df['sample_id']!="DROP_ME")]
    return CO2_df


def create_co2_chart(df):
    CO2_df = get_CO2_df(df)
    plot = create_conc_v_salt_ratio_with_annotated_treatments_chart("CO2 conc", CO2_df)
    return plot

def create_methane_chart(df):
    methane_df = get_methane_df(df)
    plot = create_conc_v_salt_ratio_with_annotated_treatments_chart("Methane conc v Salt:Organic Matter", methane_df)
    plot.line(x=1)
    return plot


# bokeh.io.output_notebook()


def create_conc_v_salt_ratio_with_annotated_treatments_chart(title, df):
    incubation_length_max = int(df["incubation_length"].max())
    wet_df = ColumnDataSource(df[df["treatment"]=="Wet"])
    dry_df = ColumnDataSource(df[df["treatment"]=="Dry"])
    ratios = ["1:0", "16:1", "1:1", "1:5"]

    TOOLTIPS = [
    ("sample_id", "@sample_id"),
    ("calculated_conc", "@calculated_conc")
        ]
    
    exp_cmap = LinearColorMapper(palette=Inferno256, low=incubation_length_max, high=0)
    p = plotting.figure(
        title=title,
        x_axis_label = "Organic Matter:Salt",
        y_axis_label = "Calculated Conc (ppm)",
        x_range=ratios,
        y_axis_type="log",
        y_range=[10e-2, 10e5],
        toolbar_location='above',
        tooltips = TOOLTIPS,
        sizing_mode="stretch_width"
    )
   
    p.triangle(
        source=wet_df,
        x = jitter("salt_ratio", width=0.3, range=p.x_range),
        y = "calculated_conc",
        color={"field":"incubation_length", "transform":exp_cmap},
        size=10,
        legend_label="Wet"
    )
    p.plus(
        source=dry_df,
        x = jitter("salt_ratio", width=0.3, range=p.x_range),
        y = "calculated_conc",
        color={"field":"incubation_length", "transform":exp_cmap},
        size=10,
        legend_label="Dry"
    )
    p.x_range.range_padding = 0

    p.add_layout(bokeh.models.Legend(), "right")
    p.legend.click_policy = "hide"
    bar = ColorBar(color_mapper=exp_cmap, location=(0,0))
    p.add_layout(bar, "right")
    return p




def create_salt_ratio_v_conc_chart(title, df):
    df = ColumnDataSource(df)
    ratios = ["1:0", "16:1", "1:1", "1:5"]

    TOOLTIPS = [("sample_id", "@sample_id")]
    exp_cmap = LinearColorMapper(palette=Inferno256, low=60, high=0)
    p = plotting.figure(
        title=title,
        x_axis_label = "Organic Matter:Salt",
        y_axis_label = "Calculated Conc (ppm)",
        x_range=ratios,
        y_axis_type="log",
        y_range=[10e0, 10e5],
        toolbar_location='above',
        tooltips = TOOLTIPS,
        sizing_mode="stretch_width"
    )
    p.circle(
        source=df,
        x = jitter("salt_ratio", width=0.6, range=p.x_range),
        # x = "calculated_conc",
        y = "calculated_conc",
        color={"field":"incubation_length", "transform":exp_cmap},
        size=10,
        )
    bar = ColorBar(color_mapper=exp_cmap, location=(0,0))
    p.add_layout(bar, "right")
    return p
