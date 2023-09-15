import bokeh.io
from bokeh import plotting
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, ColorBar, LinearColorMapper, Span, CategoricalColorMapper, Label, Whisker
from bokeh.palettes import Spectral6, Inferno256
from bokeh.transform import jitter
from GCPDFReader.server.constants import COMPOUNDS
from bokeh.colors import RGB

import pandas as pd
import numpy as np

from cmcrameri import cm as scm
TAB10 = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
         "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"]


def get_methane_df(df):
    methane_df = df[(df['peak_compound'] == 'CH4') & (df['is_std'] == False) & (df['sample_id']!="DROP_ME")]
    return methane_df


def get_CO2_df(df):
    CO2_df = df[(df['peak_compound'] == 'CO2') & (df['is_std'] == False) & (df['sample_id']!="DROP_ME")]
    return CO2_df


def create_co2_chart(df):
    CO2_df = get_CO2_df(df)
    plot = create_conc_v_organic_matter_percent_with_annotated_treatments_chart("CO2 Concentration v Percent Organic Matter", CO2_df, COMPOUNDS["CO2"]["atm_conc"], y_range=[10e0, 10e5], atm_conc_offset=150)
    plot.height = 600
    plot.width = 800
    return plot

def create_methane_chart(df):
    methane_df = get_methane_df(df)
    plot = create_conc_v_organic_matter_percent_with_annotated_treatments_chart("Methane", methane_df, COMPOUNDS["CH4"]["atm_conc"], y_range=[10e-2, 10e2], atm_conc_offset=1)
    plot.width=1000
    return plot

def create_methane_incubation_length_chart(df):
    methane_df = get_methane_df(df)
    plot = time_v_conc("Methane", methane_df, COMPOUNDS["CH4"]["atm_conc"], y_range=[10e-2, 10e2], atm_conc_offset=1)
    plot.height = 600
    plot.width = 800
    return plot


def create_co2_incubation_length_chart(df):
    co2_df = get_CO2_df(df)
    plot = time_v_conc("CO2", co2_df, COMPOUNDS["CO2"]["atm_conc"],  y_range=[10e0, 10e5], atm_conc_offset=150)
    return plot



def create_salt_ratio_co2_chart(df):
    CO2_df = get_CO2_df(df)
    plot = create_conc_v_salt_ratio_with_annotated_treatments_chart("CO2", CO2_df, COMPOUNDS["CO2"]["atm_conc"], y_range=[10e0, 10e5], atm_conc_offset=150)
    return plot

def create_salt_ratio_methane_chart(df):
    methane_df = get_methane_df(df)
    plot = create_conc_v_salt_ratio_with_annotated_treatments_chart("Methane", methane_df, COMPOUNDS["CH4"]["atm_conc"], y_range=[10e-2, 10e2], atm_conc_offset=1)
    return plot



def create_2mL_co2_chart(df):
    CO2_df = get_CO2_df(df)
    two_mL_df = CO2_df[CO2_df["Sample_Name"].str.startswith("2ML")]
    plot = create_conc_v_organic_matter_percent_with_annotated_treatments_chart("CO2 (2mL)", two_mL_df, COMPOUNDS["CO2"]["atm_conc"], y_range=[10e0, 10e5], atm_conc_offset=150)
    return plot

def create_2mL_methane_chart(df):
    methane_df = get_methane_df(df)
    two_mL_df = methane_df[methane_df["Sample_Name"].str.startswith("2ML")]
    plot = create_conc_v_organic_matter_percent_with_annotated_treatments_chart("Methane (2mL)", two_mL_df, COMPOUNDS["CH4"]["atm_conc"], y_range=[10e-2, 10e2], atm_conc_offset=1)
    plot.height = 600
    plot.width = 800
    return plot

def create_40mL_co2_chart(df):
    CO2_df = get_CO2_df(df)
    forty_mL_df = CO2_df[CO2_df["Sample_Name"].str.startswith("40ML")]
    plot = create_conc_v_organic_matter_percent_with_annotated_treatments_chart("CO2 (40mL)", forty_mL_df, COMPOUNDS["CO2"]["atm_conc"], y_range=[10e0, 10e5], atm_conc_offset=150)
    plot.height = 600
    return plot

def create_40mL_methane_chart(df):
    methane_df = get_methane_df(df)
    forty_mL_df = methane_df[methane_df["Sample_Name"].str.startswith("40ML")]
    plot = create_conc_v_organic_matter_percent_with_annotated_treatments_chart("Methane (40mL)", forty_mL_df, COMPOUNDS["CH4"]["atm_conc"], y_range=[10e-2, 10e2], atm_conc_offset=1)
    plot.height = 600
    plot.width = 800

    return plot



def create_2mL_methane_incubation_length_chart(df):
    methane_df = get_methane_df(df)
    two_mL_df = methane_df[methane_df["Sample_Name"].str.startswith("2ML")]
    plot = time_v_conc("Methane (2mL)", two_mL_df, COMPOUNDS["CH4"]["atm_conc"], y_range=[10e-2, 10e2], atm_conc_offset=1)
    plot.height = 600
    plot.width = 800
    return plot


def create_2mL_co2_incubation_length_chart(df):
    co2_df = get_CO2_df(df)
    two_mL_df = co2_df[co2_df["Sample_Name"].str.startswith("2ML")]
    plot = time_v_conc("CO2 (2mL)", two_mL_df, COMPOUNDS["CO2"]["atm_conc"], y_range=[10e0, 10e5], atm_conc_offset=150)
    return plot

def create_40mL_methane_incubation_length_chart(df):
    methane_df = get_methane_df(df)
    forty_mL_df = methane_df[methane_df["Sample_Name"].str.startswith("40ML")]
    plot = time_v_conc("Methane (40mL)", forty_mL_df, COMPOUNDS["CH4"]["atm_conc"], y_range=[10e-2, 10e2], atm_conc_offset=0.4)
    plot.height = 600
    plot.width = 800
    return plot


def create_40mL_co2_incubation_length_chart(df):
    co2_df = get_CO2_df(df)
    forty_mL_df = co2_df[co2_df["Sample_Name"].str.startswith("40ML")]
    plot = time_v_conc("CO2 (40mL)", forty_mL_df, COMPOUNDS["CO2"]["atm_conc"], y_range=[10e0, 10e5], atm_conc_offset=150)
    plot.height = 600
    plot.width = 800    
    return plot

# bokeh.io.output_notebook()


def create_log10_conc_v_salt_ratio_with_annotated_treatments_chart(title, df, atmospheric_conc):
    # incubation_length_max = int(df["incubation_length"].max())
    wet_df = ColumnDataSource(df[df["treatment"]=="Wet"])
    dry_df = ColumnDataSource(df[df["treatment"]=="Dry"])
    ratios = ["1:0", "16:1", "1:1", "1:5"]

    TOOLTIPS = [
    ("sample_id", "@sample_id"),
    ("Measured Concentration", "@calculated_conc")
        ]
    
    # exp_cmap = LinearColorMapper(palette=Inferno256, low=incubation_length_max, high=0)
    p = plotting.figure(
        title=title,
        x_axis_label = "Organic Matter:Salt",
        y_axis_label = "Log10 of Measured Conc (ppm)",
        x_range=ratios,
        # y_axis_type="log",
        # y_range=[10e-2, 10e5],
        toolbar_location=None,  # 'above',
        tooltips = TOOLTIPS,
        # sizing_mode="stretch_width"
    )
   
    p.triangle(
        source=wet_df,
        x = jitter("salt_ratio", width=0.3, range=p.x_range),
        y = "log10_calc_conc",
        color=TAB10[0],
        # color={"field":"incubation_length", "transform":exp_cmap},
        size=30,
        legend_label="Wet"
    )
    p.scatter(marker="inverted_triangle",
        source=dry_df,
        x = jitter("salt_ratio", width=0.3, range=p.x_range),
        y = "log10_calc_conc",
        color=TAB10[2],
        # color={"field":"incubation_length", "transform":exp_cmap},
        size=30,
        legend_label="Dry"
    )
    p.x_range.range_padding = 0

    if atmospheric_conc:
        atm_conc_line = Span(location=np.log10(atmospheric_conc), dimension='width', line_color='red', line_width=2)
        p.add_layout(atm_conc_line)

    my_label = Label(x=0, y=np.log10(atmospheric_conc), text='Atmospheric Conc')
    p.add_layout(my_label)
    p.add_layout(bokeh.models.Legend(), "right")
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "20pt"
    # bar = ColorBar(color_mapper=exp_cmap, location=(0,0))
    # p.add_layout(bar, "right")
    return p


def create_create_log10conc_v_organic_matter_percent_with_annotated_treatments_chart(title, df, atmospheric_conc, include_errors=False, atm_conc_offset=0):
    wet_df = ColumnDataSource(df[df["treatment"]=="Wet"])
    dry_df = ColumnDataSource(df[df["treatment"]=="Dry"])
    x_range = ["100%", "94%", "50%", "20%"]

    TOOLTIPS = [
    ("sample_id", "@sample_id"),
    ("Measured Concentration", "@calculated_conc")
        ]
    
    # exp_cmap = LinearColorMapper(palette=Inferno256, low=incubation_length_max, high=0)
    p = plotting.figure(
        title=title,
        x_axis_label = "Percent Organic Matter",
        y_axis_label = "Log10 of Measured Conc (ppm)",
        x_range=x_range,
        toolbar_location=None,  # 'above',
        tooltips = TOOLTIPS,
        # sizing_mode="stretch_width"
    )
    p.axis.major_label_text_font_size = "30pt"
    p.axis.axis_label_text_font_size = "25pt"
    p.title.text_font_size = "40pt"

    if include_errors is False:
        p.triangle(
            source=wet_df,
            x = jitter("percent_organic_matter", width=0.3, range=p.x_range),
        y = "log10_calc_conc",
            color=TAB10[0],
            size=30,
            legend_label="Wet"
        )
        p.scatter(marker="inverted_triangle",
            source=dry_df,
            x = jitter("percent_organic_matter", width=0.3, range=p.x_range),
        y = "log10_calc_conc",
            color=TAB10[2],
            size=30,
            legend_label="Dry"
        )
    p.x_range.range_padding = 0

    # if include_errors==True:
        # p.triangle(
        #     source=wet_df,
        #     x="percent_organic_matter",
        #     y = "calculated_conc",
        #     color=TAB10[0],
        #     size=30,
        #     legend_label="Wet"
        # )
        # p.scatter(marker="inverted_triangle",
        #     source=dry_df,
        #     x="percent_organic_matter",
        #     y = "calculated_conc",
        #     color=TAB10[2],
        #     size=30,
        #     legend_label="Dry"
        # )
        # p.segment(
        #     source=wet_df,
        #     x0="percent_organic_matter",
        #     y0='lower',
        #     x1="percent_organic_matter",
        #     y1='upper',
        #     line_width=2,
        #     color=TAB10[0],
        #     legend_label="Wet Error Bars"
        # )
        # p.segment(
        #     source=dry_df,
        #     x0="percent_organic_matter",
        #     y0='lower',
        #     x1="percent_organic_matter",
        #     y1='upper',
        #     line_width=2,
        #     color=TAB10[2],
        #     legend_label="Dry Error Bars"
        # )
    if atmospheric_conc:
        atm_conc_line = Span(location=np.log10(atmospheric_conc), dimension='width', line_color='grey', line_width=2)
        p.add_layout(atm_conc_line)

        my_label = Label(x=0, y=np.log10(atmospheric_conc) - 0.1, text='Atmospheric Concentration')
        p.add_layout(my_label)
    p.add_layout(bokeh.models.Legend(), "right")
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "20pt"
    # bar = ColorBar(color_mapper=exp_cmap, location=(0,0))
    # p.add_layout(bar, "right")
    return p



def create_conc_v_salt_ratio_with_annotated_treatments_chart(title, df, atmospheric_conc, include_errors=False):
    # incubation_length_max = int(df["incubation_length"].max())
    wet_df = ColumnDataSource(df[df["treatment"]=="Wet"])
    dry_df = ColumnDataSource(df[df["treatment"]=="Dry"])
    df = ColumnDataSource(df)


    ratios = ["1:0", "16:1", "1:1", "1:5"]

    TOOLTIPS = [
    ("sample_id", "@sample_id"),
    ("Measured Concentration", "@calculated_conc")
        ]
    
    # exp_cmap = LinearColorMapper(palette=Inferno256, low=incubation_length_max, high=0)
    p = plotting.figure(
        title=title,
        x_axis_label = "Organic Matter:Salt",
        y_axis_label = "Measured Concentration (ppm)",
        x_range=ratios,
        y_axis_type="log",
        y_range=[10e0, 10e5],
        toolbar_location=None,  # 'above',
        tooltips = TOOLTIPS,
        # sizing_mode="stretch_width"
    )
    p.axis.major_label_text_font_size = "30pt"
    p.axis.axis_label_text_font_size = "25pt"
    p.triangle(
        source=wet_df,
        # x = jitter("salt_ratio", width=0.3, range=p.x_range),
        x="salt_ratio"
,        y = "calculated_conc",
        color=TAB10[0],
        # color={"field":"incubation_length", "transform":exp_cmap},
        size=30,
        legend_label="Wet"
    )
    p.scatter(marker="inverted_triangle",
        source=dry_df,
        # x = jitter("salt_ratio", width=0.3, range=p.x_range),
        x="salt_ratio",
        y = "calculated_conc",
        color=TAB10[2],
        # color={"field":"incubation_length", "transform":exp_cmap},
        size=30,
        legend_label="Dry"
    )
    p.x_range.range_padding = 0

    if include_errors:
        p.segment(
            source=wet_df,
            x0="salt_ratio",
            y0='lower',
            x1="salt_ratio",
            y1='upper',
            line_width=2,
            color=TAB10[0],
            legend_label="Wet Error Bars"
        )
        p.segment(
            source=dry_df,
            x0="salt_ratio",
            y0='lower',
            x1="salt_ratio",
            y1='upper',
            line_width=2,
            color=TAB10[2],
            legend_label="Dry Error Bars"
        )
    if atmospheric_conc:
        atm_conc_line = Span(location=atmospheric_conc, dimension='width', line_color='grey', line_width=2)
        p.add_layout(atm_conc_line)

        my_label = Label(x=0, y=atmospheric_conc-200, text='Atmospheric Concentration')
        p.add_layout(my_label)
    p.add_layout(bokeh.models.Legend(), "right")
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "20pt"
    # bar = ColorBar(color_mapper=exp_cmap, location=(0,0))
    # p.add_layout(bar, "right")
    return p



def create_conc_v_organic_matter_percent_with_annotated_treatments_chart(title, df, atmospheric_conc, include_errors=False, y_range=[10e-2, 10e5], atm_conc_offset=0):
    wet_df = ColumnDataSource(df[df["treatment"]=="Wet"])
    dry_df = ColumnDataSource(df[df["treatment"]=="Dry"])
    x_range = ["100%", "94%", "50%", "20%"]
    
    TOOLTIPS = [
    ("sample_id", "@sample_id"),
    ("Measured Concentration", "@calculated_conc")
        ]
    
    # exp_cmap = LinearColorMapper(palette=Inferno256, low=incubation_length_max, high=0)
    p = plotting.figure(
        title=title,
        x_axis_label = "Percent Organic Matter",
        y_axis_label = "Measured Concentration (ppm)",
        x_range=x_range,
        y_axis_type="log",
        y_range=y_range,
        toolbar_location=None,  # 'above',
        tooltips = TOOLTIPS,
        # sizing_mode="stretch_width"
    )
    p.axis.major_label_text_font_size = "30pt"
    p.axis.axis_label_text_font_size = "25pt"
    p.title.text_font_size = "40pt"

    if include_errors is False:
        p.triangle(
            source=wet_df,
            x = jitter("percent_organic_matter", width=0.2, range=p.x_range),
            y = "calculated_conc",
            color=TAB10[0],
            size=30,
            legend_label="Wet"
        )
        p.scatter(marker="inverted_triangle",
            source=dry_df,
            x = jitter("percent_organic_matter", width=0.2, range=p.x_range),
            y = "calculated_conc",
            color=TAB10[2],
            size=30,
            legend_label="Dry"
        )
    p.x_range.range_padding = 0

    if include_errors==True:
        p.triangle(
            source=wet_df,
            x="percent_organic_matter",
            y = "calculated_conc",
            color=TAB10[0],
            size=30,
            legend_label="Wet"
        )
        p.scatter(marker="inverted_triangle",
            source=dry_df,
            x="percent_organic_matter",
            y = "calculated_conc",
            color=TAB10[2],
            size=30,
            legend_label="Dry"
        )
        p.segment(
            source=wet_df,
            x0="percent_organic_matter",
            y0='lower',
            x1="percent_organic_matter",
            y1='upper',
            line_width=2,
            color=TAB10[0],
            legend_label="Wet Error Bars"
        )
        p.segment(
            source=dry_df,
            x0="percent_organic_matter",
            y0='lower',
            x1="percent_organic_matter",
            y1='upper',
            line_width=2,
            color=TAB10[2],
            legend_label="Dry Error Bars"
        )
    if atmospheric_conc:
        atm_conc_line = Span(location=atmospheric_conc, dimension='width', line_color='grey', line_width=2)
        p.add_layout(atm_conc_line)

        my_label = Label(x=0, y=atmospheric_conc-atm_conc_offset, text='Atmospheric Concentration')
        p.add_layout(my_label)
    p.add_layout(bokeh.models.Legend(), "right")
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "20pt"
    # bar = ColorBar(color_mapper=exp_cmap, location=(0,0))
    # p.add_layout(bar, "right")
    return p



def create_salt_ratio_v_conc_chart(title, df):
    df = ColumnDataSource(df)
    ratios = ["1:0", "16:1", "1:1", "1:5"]

    TOOLTIPS = [("sample_id", "@sample_id")]
    exp_cmap = LinearColorMapper(palette=Inferno256, low=60, high=0)
    p = plotting.figure(
        title=title,
        x_axis_label = "Organic Matter:Salt",
        y_axis_label = "Measured Concentration (ppm)",
        x_range=ratios,
        y_axis_type="log",
        y_range=[10e0, 10e5],
        toolbar_location=None,  # 'above',
        tooltips = TOOLTIPS,
        # sizing_mode="stretch_width"
    )
    p.circle(
        source=df,
        x = jitter("salt_ratio", width=0.6, range=p.x_range),
        # x = "calculated_conc",
        y = "calculated_conc",
        color={"field":"incubation_length", "transform":exp_cmap},
        size=30,
        )
    bar = ColorBar(color_mapper=exp_cmap, location=(0,0))
    p.add_layout(bar, "right")
    return p



# def time_v_conc(title, df, atmospheric_conc):
#     incubation_length_max = int(df["incubation_length"].max())
#     wet_df = ColumnDataSource(df[df["treatment"]=="Wet"])
#     dry_df = ColumnDataSource(df[df["treatment"]=="Dry"])
    
    
#     clr_mapper = CategoricalColorMapper(palette=["red", "blue", "green", "purple"], factors=["1:0", "16:1", "1:1", "1:5"])


#     TOOLTIPS = [
#     ("sample_id", "@sample_id"),
#     ("Measured Concentration", "@calculated_conc")
#         ]
    
#     p = plotting.figure(
#         title=title,
#         x_axis_label = "Incubation Length (Days)",
#         y_axis_label = "Measured Concentration(ppm)",
#         y_axis_type="log",
#         y_range=[10e-2, 10e5],
#         x_range=[30, incubation_length_max+10],
#         toolbar_location=None,  # 'above',
#         tooltips = TOOLTIPS,
#         sizing_mode="stretch_width"
#     )
#     p.triangle(
#         source=wet_df,
#         x = jitter("incubation_length", width=0.5, range=p.x_range),
#         y = "calculated_conc",
#         color={"field":"salt_ratio", "transform":clr_mapper},
#         size=30,
#         legend_label="Wet Treatment"
#         )
#     p.scatter(marker="inverted_triangle",
#         source=dry_df,
#                 x = jitter("incubation_length", width=0.5, range=p.x_range),
#         y = "calculated_conc",
#         color={"field":"salt_ratio", "transform":clr_mapper},
#         size=30,
#         legend_label="Dry Treatment"
#         )
#     if atmospheric_conc:
#         atm_conc_line = Span(location=atmospheric_conc, dimension='width', line_color='red', line_width=2)
#         p.add_layout(atm_conc_line)
   
#     p.add_layout(bokeh.models.Legend(), "above")
#     p.legend.click_policy = "hide"
#     p.legend.label_text_font_size = "20pt"
#     return p
    


def time_v_conc(title, df, atmospheric_conc, connect_samples=False, y_range=[10e-2, 10e5], atm_conc_offset=0):
    incubation_length_max = int(df["incubation_length"].max())
    wet_df = ColumnDataSource(df[df["treatment"]=="Wet"])
    dry_df = ColumnDataSource(df[df["treatment"]=="Dry"])
    
    
    clr_mapper = CategoricalColorMapper(palette=[RGB(*(np.array(scm.bamako(i)[:3])*255).tolist()) for i in [0.1, 0.3, 0.5, 0.7]], factors=["1:0", "16:1", "1:1", "1:5"])


    TOOLTIPS = [
    ("sample_id", "@sample_id"),
    ("Measured Concentration", "@calculated_conc")
        ]
    
    p = plotting.figure(
        title=title,
        x_axis_label = "Incubation Length (Days)",
        y_axis_label = "Measured Concentration (ppm)",
        y_axis_type="log",
        y_range=y_range,
        x_range=[20, incubation_length_max+10],
        toolbar_location=None,  # 'above',
        tooltips = TOOLTIPS,
        # sizing_mode="stretch_width"
    )
    p.axis.major_label_text_font_size = "30pt"
    p.axis.axis_label_text_font_size = "25pt"
    p.title.text_font_size = "40pt"

    p.triangle(
        source=wet_df,
        x = jitter(field_name="incubation_length", width=0.2),
        y = "calculated_conc",
        color={"field":"salt_ratio", "transform":clr_mapper},
        size=30,
        legend_label="Wet Treatment",
        fill_alpha=0.3
        )
    p.scatter(marker="inverted_triangle",
        source=dry_df,
        x = jitter(field_name="incubation_length", width=0.2),
        y = "calculated_conc",
        color={"field":"salt_ratio", "transform":clr_mapper},
        size=30,
        legend_label="Dry Treatment",
        fill_alpha=0.3
        )
    if connect_samples:
        for id in df['sample_id'].unique():
            print(id)
            sub_df = df[df['sample_id'] == id]
            p.line(
                source = sub_df,
                x = "incubation_length",
                y="calculated_conc"
            )
    if atmospheric_conc:
        atm_conc_line = Span(location=atmospheric_conc, dimension='width', line_color='grey', line_width=2)
        p.add_layout(atm_conc_line)
        my_label = Label(x=20, y=atmospheric_conc-atm_conc_offset, text='Atmospheric Concentration')
        p.add_layout(my_label)


    p.add_layout(bokeh.models.Legend(), "above")
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "20pt"
    return p
    


