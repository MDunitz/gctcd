import bokeh.io
from bokeh import plotting
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, ColorBar, LinearColorMapper, Span, CategoricalColorMapper
from bokeh.palettes import Spectral6, Inferno256
from bokeh.transform import jitter
from GCPDFReader.server.constants import COMPOUNDS

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
    plot = create_conc_v_salt_ratio_with_annotated_treatments_chart("CO2 conc", CO2_df, COMPOUNDS["CO2"]["atm_conc"])
    return plot

def create_methane_chart(df):
    methane_df = get_methane_df(df)
    plot = create_conc_v_salt_ratio_with_annotated_treatments_chart("Methane conc v Salt:Organic Matter", methane_df, COMPOUNDS["CH4"]["atm_conc"])
    plot.line(x=1)
    return plot


# bokeh.io.output_notebook()


def create_conc_v_salt_ratio_with_annotated_treatments_chart(title, df, atmospheric_conc):
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

    if atmospheric_conc:
        atm_conc_line = Span(location=atmospheric_conc, dimension='width', line_color='red', line_width=2)
        p.add_layout(atm_conc_line)

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



def time_v_conc(title, df):
    incubation_length_max = int(df["incubation_length"].max())
    wet_df = ColumnDataSource(df[df["treatment"]=="Wet"])
    dry_df = ColumnDataSource(df[df["treatment"]=="Dry"])
    
    
    clr_mapper = CategoricalColorMapper(palette=["red", "blue", "green", "purple"], factors=["1:0", "16:1", "1:1", "1:5"])


    TOOLTIPS = [
    ("sample_id", "@sample_id"),
    ("calculated_conc", "@calculated_conc")
        ]
    
    p = plotting.figure(
        title=title,
        x_axis_label = "Incubation Length",
        y_axis_label = "Measured Concentration(ppm)",
        y_axis_type="log",
        y_range=[10e-2, 10e5],
        x_range=[0, incubation_length_max],
        toolbar_location='above',
        tooltips = TOOLTIPS,
        sizing_mode="stretch_width"
    )
    p.triangle(
        source=wet_df,
        x = jitter("incubation_length", width=0.5, range=p.x_range),
        y = "calculated_conc",
        color={"field":"salt_ratio", "transform":clr_mapper},
        size=10,
        legend_label="Wet Treatment"
        )
    p.circle(
        source=dry_df,
                x = jitter("incubation_length", width=0.5, range=p.x_range),
        y = "calculated_conc",
        color={"field":"salt_ratio", "transform":clr_mapper},
        size=10,
        legend_label="Dry Treatment"
        )
    dst_end = Span(location=1.922, dimension='width',
               line_color='red', line_width=2)
   
    p.add_layout(dst_end)

    p.add_layout(bokeh.models.Legend(), "above")
    p.legend.click_policy = "hide"
    return p
    
