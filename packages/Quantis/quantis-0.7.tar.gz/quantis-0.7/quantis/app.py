"""The Quantis app layout and Dash callbacks

Copyright 2024 Daniil Pomogaev
SPDX-License-Identifier: Apache-2.0
"""

# from . import log_setup
from dash import Dash, dcc, callback, Input, Output, State, html, no_update, dash_table, ctx
import dash_bootstrap_components as dbc
# import dash_uploader as du
from dash_daq.ColorPicker import ColorPicker
from pathlib import Path
import pandas as pd
import numpy as np
import atexit
import re
from traceback import format_exc

import argparse as argp

from typing import Any, TYPE_CHECKING

import webview
import webbrowser

from .ncbi_species_parser import fetch_species_name
from .cash_or_new import hash_parameters, check_existing_data, save_data
from .string_request import get_string_svg, get_annotations, get_string_ids
from .open_tsv_files_dialog import open_tsv_files_dialog, save_csv_file_dialog, open_exe_files_dialog
from .utils import *
from .ms1diffacto import *
from .filetypes import descriptions as FTD


FILES_PATH = Path(__file__).parent / "user_files"
CACHE_PATH = Path(__file__).parent / "data_cache"
ASSETS_PATH = Path(__file__).parent / "assets"

def resource_path(relative_path):
    """get absolute path to resource"""
    import sys
    import os
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = Path(__file__).parent
    return os.path.join(base_path, relative_path)




def reinstantiate():
    global app, window
    app = Dash(
        "Quantis", title="Quantis", assets_folder=str(resource_path("assets")),
        external_stylesheets=[str(resource_path("assets/css/dragula.css")), dbc.themes.BOOTSTRAP]
    )
    window = webview.create_window(app.title, app.server, width=1200, height=800)  # type: ignore


# ======== Callbacks ========

# Show proper div for currently chosen input format
@callback(
    Output("single_input_div", "style"),
    Output("multi_input_div", "style"),
    Output("maxquant_table_div", "style"),
    Input("input_format", "value")
)
def hide_show_divs(value):
    if value == "Scavager" or value == "s+d":
        return {"display": "none"}, {"display": "grid"}, {"display": "none"}
    elif value == "MaxQuant":
        return {"display": "grid"}, {"display": "none"}, {"display": "grid"}
    elif value == "DirectMS1Quant" or value == "Diffacto":
        return {"display": "grid"}, {"display": "none"}, {"display": "none"}
    else:
        raise ValueError("File type `{}` is not supported".format(value))

@callback(
    Output("executable_div", "style"),
    Output("diffacto_div", "style"),
    Output("main_header", "children"),
    Input("input_format", "value")
)
def hide_show_diffacto(value):
    if value == "s+d":
        return {"display": "grid"}, {"display": "grid"}, "ms1todiffacto.py"
    else:
        return {"display": "none"}, {"display": "none"}, "Quantis"

@callback(
    Output("file_type_description", "children"),
    Input("input_format", "value")
)
def show_file_type_description(value):
    if value in FTD:
        ret = FTD[value]
        if value == "s+d":
            return [html.P(ret), html.P("You can get diffacto here:"), html.P("https://github.com/statisticalbiotechnology/diffacto", style={'user-select': 'all', 'color': 'var(--color-primary)'})]
        return FTD[value]
    else:
        return "No description available"
    

# Fill Column table with ibaq labels on table input
@callback(
    Output("column_DT", "data"),
    Input("single_file_path", "value"),
    Input("col_prefix", "value"),
    Input("btn_prefix", "n_clicks"),
    State("input_format", "value"),
    State("k_prefix", "value"),
    State("a_prefix", "value"),
)
def fill_col_table(path: str, prefix: str, _, input_format: str, k_prefix, a_prefix):
    if input_format != "MaxQuant":
        return no_update
    if not path:
        return no_update
    with open(path) as f:
        fline = f.readline()
    cols = fline.split("\t")
    iBAQ_cols = [col for col in cols if prefix in col and col != prefix]
    labels = [col.strip(prefix+" ") for col in iBAQ_cols]
    return [{"col": col, "kan": (
        "K" if k_prefix and k_prefix in col else (
            "A" if a_prefix and a_prefix in col else "N"
        )
    )} for col in labels]


# Disable threshold type and sliders for DirectMS1Quant
@callback(
    Output("threshold_calculation", "disabled"),
    Output("threshold_calculation", "value"),
    Input("input_format", "value")
)
def disable_threshold(value):
    if value == "DirectMS1Quant":
        return True, "ms1"
    else:
        return False, "static"

# Disable imputation for DirectMS1Quant (and MaxQuant -- restored) and Diffacto
@callback(
    Output("imputation", "disabled"),
    Output("imputation", "value"),
    Input("input_format", "value")
)
def disable_imputation(value):
    if value in ("DirectMS1Quant", "Diffacto"):
        return True, "Min"
    else:
        return False, "Min"


# Disable bonferonni correction for dynamic threshold calculation
@callback(
    Output("correction", "options"),
    Output("correction", "value"),
    Input("threshold_calculation", "value")
)
def disable_bonferroni(value):
    correction_options: list[dict[str, Any]] = [
        {"label": "Bonferroni", "value": "bonferroni"},
        {"label": "Holm", "value": "holm"},
        {"label": "Benjamini-Hochberg", "value": "fdr_bh"},
        {"label": "Simes-Hochberg", "value": "sh"},
        {"label": "None", "value": "none"}
    ]
    if value in ("dynamic", "ms1"):
        correction_options[0]["disabled"] = True
    return correction_options, "fdr_bh"
    


# Add files to tables
@callback(
    Output("lastfiles_K", "value"),
    Output("input_error", "children", allow_duplicate=True),
    Output("input_error", "is_open", allow_duplicate=True),
    Input("control_btn_input", "n_clicks"),
    State("input_format", "value"),
    prevent_initial_call=True
)
def write_control_files(_, format):
    files = open_tsv_files_dialog(window, True) or []
    if format != "s+d":
        return ";".join(files), no_update, no_update
    failed_files = []
    passed_files = []
    for file in files:
        if are_files_present(file):
            passed_files.append(file)
        else:
            failed_files.append(file)
    retfiles = ";".join(passed_files)
    if failed_files:
        error_message = html.Div([
            html.H3("Import failure!"),
            html.P(
                "To successfully add files for this input type, make sure that files "
                +"with suffixes '_proteins.tsv', '_PFMs_ML.tsv', '_PFMs.tsv' are present in the same folder."
            ),
            html.P("Files that didn't pass the check:"),
            html.Ul([html.Li(file) for file in failed_files])
        ])
        return retfiles, error_message, True
    return retfiles, "", False

@callback(
    Output("lastfiles_A", "value"),
    Output("input_error", "children", allow_duplicate=True),
    Output("input_error", "is_open", allow_duplicate=True),
    Input("test_btn_input", "n_clicks"),
    State("input_format", "value"),
    prevent_initial_call=True
)
def write_test_files(_, format):
    files = open_tsv_files_dialog(window, True) or []
    if format != "s+d":
        return ";".join(files), no_update, no_update
    failed_files = []
    passed_files = []
    for file in files:
        if are_files_present(file):
            passed_files.append(file)
        else:
            failed_files.append(file)
    retfiles = ";".join(passed_files)
    if failed_files:
        error_message = html.Div([
            html.H3("Import failure!"),
            html.P(
                "To successfully add files for this input type, make sure that files "
                +"with suffixes '_proteins.tsv', '_PFMs_ML.tsv', '_PFMs.tsv' are present in the same folder."
            ),
            html.P("Files that didn't pass the check:"),
            html.Ul([html.Li(file) for file in failed_files])
        ])
        return retfiles, error_message, True
    return retfiles, "", False

@callback(
    Output("single_file_path", "value"),
    Input("single_input_btn", "n_clicks"),
    prevent_initial_call=True
)
def write_single_file(_):
    path = open_tsv_files_dialog(window, False)
    if path:
        return path[0]
    return ""

# Select executable file
@callback(
    Output("executable_path", "value"),
    Input("executable_btn", "n_clicks"),
    prevent_initial_call=True
)
def write_exceutable_file(_):
    path = open_exe_files_dialog(window, False)
    if path:
        return path[0]
    return ""


@callback(
    Output("control_files_table", "data"),
    Input("lastfiles_K", "value"),
    State("control_files_table", "data")
)
def append_control_files(lastfiles: str, data: list[dict] | None):
    if data is None: # Prevents error when data is None
        data = []
    if not lastfiles:
        return no_update
    lfl = lastfiles.split(";")
    
    all_paths = set(row["path"] for row in data)

    for file in lfl:
        if file not in all_paths:
            data.append({"path": file})
    
    return data

@callback(
    Output("test_files_table", "data"),
    Input("lastfiles_A", "value"),
    State("test_files_table", "data"),
)
def append_test_files(lastfiles: str, data: list[dict] | None):
    if data is None: # Prevents error when data is None
        data = []
    if not lastfiles:
        return no_update
    lfl = lastfiles.split(";")
    
    all_paths = set(row["path"] for row in data)

    for file in lfl:
        if file not in all_paths:
            data.append({"path": file})
    
    return data

# Remove files from tables

@callback(
    Output("control_files_table", "data", allow_duplicate=True),
    Input("rm_K_sel_btn", "n_clicks"),
    State("control_files_table", "selected_rows"),
    State("control_files_table", "data"),
    prevent_initial_call=True
)
def rm_sel_K(_, selected_rows: list[int], data: list[dict]):
    # for i, row in enumerate(data):
    #     if i in selected_rows:
    #         FILES_PATH.joinpath(row["path"]).unlink()
    return [row for i, row in enumerate(data) if i not in selected_rows]

@callback(
    Output("test_files_table", "data", allow_duplicate=True),
    Input("rm_A_sel_btn", "n_clicks"),
    State("test_files_table", "selected_rows"),
    State("test_files_table", "data"),
    prevent_initial_call=True
)
def rm_sel_A(_, selected_rows: list[int], data: list[dict]):
    # for i, row in enumerate(data):
    #     if i in selected_rows:
    #         FILES_PATH.joinpath(row["path"]).unlink()
    return [row for i, row in enumerate(data) if i not in selected_rows]

@callback(
    Output("control_files_table", "data", allow_duplicate=True),
    Input("rm_K_all_btn", "n_clicks"),
    State("control_files_table", "data"),
    prevent_initial_call=True
)
def rm_all_K(_, data):
    # for file in data:
    #     FILES_PATH.joinpath(file["path"]).unlink()
    return []

@callback(
    Output("test_files_table", "data", allow_duplicate=True),
    Input("rm_A_all_btn", "n_clicks"),
    State("test_files_table", "data"),
    prevent_initial_call=True
)
def rm_all_A(_, data):
    # for file in data:
    #     FILES_PATH.joinpath(file["path"]).unlink()
    return []

# Generate sample file from table data
@callback(
    Output("download_sample", "data"),
    Input("sample_gen_btn", "n_clicks"),
    State("control_files_table", "data"),
    State("test_files_table", "data"),
    prevent_initial_call=True
)
def generate_sample_file(_, k_data, a_data):
    if not k_data or not a_data:
        return no_update
    k_files = pd.DataFrame(k_data)
    a_files = pd.DataFrame(a_data)
    k_files["Sample"] = "K"
    a_files["Sample"] = "A"
    sample = pd.concat([k_files, a_files], ignore_index=True)
    sample = sample.rename(columns={"path": "Path"})
    path = save_csv_file_dialog(window)
    if path:
        sample.to_csv(str(path), index=False)
    return None


# Select files with sample file
# @du.callback(
#     [Output("control_files_table", "data", allow_duplicate=True),
#     Output("test_files_table", "data", allow_duplicate=True)],
#     id="sample_input"
# )
# def load_sample_file(status: du.UploadStatus):
#     if not status.uploaded_files:
#         return no_update, no_update
    
#     # Load the sample file
#     sdf = pd.read_csv(FILES_PATH / status.uploaded_files[0].name)
#     k_files = [{"path": f} for f in sdf[sdf["Sample"] == "K"]["Path"].tolist()]
#     a_files = [{"path": f} for f in sdf[sdf["Sample"] == "A"]["Path"].tolist()]
#     return k_files, a_files

# Enable/disable custom species input
@callback(
    Output("custom_species", "disabled"),
    Output("custom_species", "value"),
    Input("species", "value")
)
def disable_custom_species(value):
    if value == -1:
        return False, no_update
    else:
        return True, ""


# Display custom species name
@callback(
    Output("species_name", "children"),
    Input("custom_species", "value"),
    prevent_initial_call=True
)
def custom_species_name(taxid: str):
    if taxid == "":
        return ""
    try:
        return fetch_species_name(taxid)
    except ValueError:
        return "Species not found"


# Sync fold change slider and input
@callback(
    Output("fold_change_input_left", "value", allow_duplicate=True),
    Output("fold_change_input_right", "value", allow_duplicate=True),
    Output("fold_change_slider", "value"),
    Input("fold_change_input_left", "value"),
    Input("fold_change_input_right", "value"),
    Input("fold_change_slider", "value"),
    prevent_initial_call=True
)
def fc_sync(input_val_l, input_val_r, slider_val):
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger in ["fold_change_input_left", "fold_change_input_right"]:
        return input_val_l, input_val_r, [input_val_l, input_val_r]
    else:
        return slider_val[0], slider_val[1], slider_val

# Sync p-value slider and input
@callback(
    Output("pvalue_input", "value", allow_duplicate=True),
    Output("pvalue_slider", "value"),
    Input("pvalue_input", "value"),
    Input("pvalue_slider", "value"),
    prevent_initial_call=True
)
def pvalue_sync(input_val, slider_val):
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger == "pvalue_input":
        return input_val, round(np.log10(input_val), 2)
    else:
        return 10**slider_val, slider_val


# Block sliders on dynamic threshold calculation
@callback(
    Output("pvalue_slider", "disabled"),
    Output("pvalue_input", "disabled"),
    Output("fold_change_slider", "disabled"),
    Output("fold_change_input_left", "disabled"),
    Output("fold_change_input_right", "disabled"),
    Input("threshold_calculation", "value"),
)
def disable_sliders(value):
    if value == "dynamic" or value == "ms1":
        return True, True, True, True, True
    elif value == "semi-dynamic":
        return True, True, False, False, False
    else:
        return False, False, False, False, False

# Block start if no files are provided
@callback(
    Output("start_button", "disabled"),
    # Output("start_button", "className"),
    Input("control_files_table", "data"),
    Input("test_files_table", "data"),
    Input("single_file_path", "value"),
    Input("input_format", "value")
)
def disable_start(c_data, t_data, sfp, fmt):
    mf_fmts = ["s+d", "Scavager"]
    if fmt in mf_fmts:
        res = not bool(c_data and t_data)
    else:
        res = not bool(sfp)
    return res


NULL_PLOT = {"layout": {
    "xaxis": {"visible": False},
    "yaxis": {"visible": False},
    "annotations": [{
        "text": "No data to display",
        "xref": "paper",
        "yref": "paper",
        "showarrow": False,
        "font": {"size": 28}
    }]
}}

# Start analysis
@callback(
    Output("volcano_plot", "figure"),
    Output("result_proteins_table", "data"),
    Output("save_proteins_button", "disabled"),
    Output("run_error", "children"),
    Output("run_error", "is_open"),
    Output("fold_change_input_left", "value"),
    Output("fold_change_input_right", "value"),
    Output("pvalue_input", "value"),
    Input("start_button", "n_clicks"),
    State("executable_path", "value"),
    State("fold_change_input_left", "value"),
    State("fold_change_input_right", "value"),
    State("pvalue_input", "value"),
    State("regulation", "value"),
    State("correction", "value"),
    State("threshold_calculation", "value"),
    State("control_files_table", "data"),
    State("test_files_table", "data"),
    State("single_file_path", "value"),
    State("col_prefix", "value"),
    State("column_DT", "data"),
    State("imputation", "value"),
    State("up_color", "value"),
    State("down_color", "value"),
    State("not_color", "value"),
    State("input_format", "value"),
    State("dif_normalize", "value"),
    State("dif_impute_threshold", "value"),
    State("dif_min_samples", "value"),
    # prevent_initial_call=True,
)
def run_quantis(
    _, exec_str, fc_threshold_l, fc_threshold_r,
    pvalue_threshold, regulation, correction,
    threshold_calculation,
    control_files, test_files, single_file,
    col_prefix, column_DT,
    imputation,
    up_color, down_color, not_color,
    input_format,
    d_norm, d_it, d_ms
):
    try:
        thhs_set = Thresholds(up_fc=fc_threshold_r, down_fc=fc_threshold_l, p_value=-np.log10(pvalue_threshold))
        color_scheme: ColorScheme = {'UP': up_color['hex'], 'DOWN': down_color['hex'], 'NOT': not_color['hex']}

        if input_format == "s+d":
            if not control_files or not test_files:
                return NULL_PLOT, no_update, no_update, "", False, no_update, no_update, no_update
            if not exec_str:
                return NULL_PLOT, no_update, no_update, "No executable file selected", True, no_update, no_update, no_update
            cfl = [f["path"] for f in control_files]
            tfl = [f["path"] for f in test_files]
            _hash = hash_parameters(cfl, tfl, imputation, input_format)
            data = check_existing_data(_hash, str(CACHE_PATH))
            d_input = compile_diffacto_data(cfl, tfl, str(FILES_PATH))
            d_it = d_it or 0.75
            d_ms = d_ms or 3
            single_file = run_diffacto(
                d_input, exec_str,
                DiffactoParameters(normalize=d_norm, impute_threshold=d_it, min_samples=d_ms),
                str(FILES_PATH)
            )
            input_format = "Diffacto"

        if input_format == "Scavager":
            if not control_files or not test_files:
                return NULL_PLOT, no_update, no_update, "", False, no_update, no_update, no_update
            # Turn files into lists
            cfl = [f["path"] for f in control_files]
            tfl = [f["path"] for f in test_files]
            _hash = hash_parameters(cfl, tfl, imputation, input_format)
            data = check_existing_data(_hash, str(CACHE_PATH))
            if data is None:
                tgdf = load_data_scavager(cfl, tfl)
                ogdf = OneGroupDF(tgdf.data, tgdf.K_cols + tgdf.A_cols)
                data = impute_missing_values(ogdf, imputation)
                tgdf = TwoGroupDF(data, tgdf.K_cols, tgdf.A_cols)
                data = calculate_fold_change_p_value(tgdf)
                save_data(data, _hash, str(CACHE_PATH))
            dwt = DFwThresholds(data, thhs_set)
            dwt = apply_mtc_and_log(dwt, correction)
            thhs_calc = calculate_thresholds(dwt.data)

        else:
            if not single_file:
                return NULL_PLOT, no_update, no_update, no_update, no_update, no_update, no_update, no_update

            if input_format == "DirectMS1Quant":
                data = load_data_directms1quant(single_file)
                dwt = DFwThresholds(data, thhs_set)
                dwt = apply_mtc_and_log(dwt, correction)
                thhs_calc = calculate_thresholds_directms1quant(dwt.data)

            elif input_format == "Diffacto":
                data = load_data_diffacto(single_file)
                dwt = DFwThresholds(data, thhs_set)
                dwt = apply_mtc_and_log(dwt, correction)
                thhs_calc = calculate_thresholds(dwt.data)

            elif input_format == "MaxQuant":
                K_cols = [col_prefix+" "+col["col"] for col in column_DT if col["kan"] == "K"]
                A_cols = [col_prefix+" "+col["col"] for col in column_DT if col["kan"] == "A"]
                _hash = hash_parameters(single_file, K_cols+A_cols, "None", input_format)
                data = check_existing_data(_hash, str(CACHE_PATH))
                if data is None:
                    ogdf = load_data_maxquant(single_file, K_cols, A_cols)
                    data = impute_missing_values(ogdf, imputation)
                    tgdf = TwoGroupDF(data, K_cols, A_cols)
                    data = calculate_fold_change_p_value(tgdf)
                    save_data(data, _hash, str(CACHE_PATH))
                dwt = DFwThresholds(data, thhs_set)
                dwt = apply_mtc_and_log(dwt, correction)
                thhs_calc = calculate_thresholds(dwt.data)

            else:
                return NULL_PLOT, no_update, no_update, "", False, no_update, no_update, no_update

        if correction == "bonferroni":
            thhs = dwt.thresholds
        else:
            thhs = replace_thresholds(thhs_set, thhs_calc, threshold_calculation)
        dwt = DFwThresholds(dwt.data, thhs)
        dwt, data_de = apply_thresholds(dwt, regulation)
        if input_format in ("DirectMS1Quant", "Diffacto") or threshold_calculation != "static":
            fctr = round(dwt.thresholds.up_fc, 2)
            fctl = round(dwt.thresholds.down_fc, 2)
            pt = round(0.1**dwt.thresholds.p_value, 3)
        else:
            fctr = no_update
            fctl = no_update
            pt = no_update
        return build_volcano_plot(dwt, color_scheme), data_de.to_dict("records"), False, "", False, fctl, fctr, pt
    except Exception as e:
        return NULL_PLOT, [], True, [
            html.H2("An error has occured!"),
            # *[html.P(line, style={"padding": "0"}) for line in format_exc(limit=3).split("\n")]
            html.Code(format_exc(limit=3), style={"white-space": "pre-wrap"})
        ], True, no_update, no_update, no_update

# Show StringDB network
@callback(
    Output("string_svg", "src"),
    Output("annotations_table", "data"),
    Output("run_error", "children", allow_duplicate=True),
    Output("run_error", "is_open", allow_duplicate=True),
    Input("result_proteins_table", "data"),
    State("input_format", "value"),
    State("req_score", "value"),
    State("species", "value"),
    State("custom_species", "value"),
    prevent_initial_call=True
)
def show_string_network(data, inpf: str, rs, sp, csp):
    try:
        if sp == -1:
            sp = csp
        if not data:
            return no_update
        if inpf == "MaxQuant":
            import re
            template = re.compile(r"sp\|([A-Z0-9]+)")
            proteins = [re.findall(template, row["dbname"])[0] for row in data]
        else:
            proteins = [row["dbname"].split("|")[1] for row in data]
        rs = rs or None
        ids = get_string_ids(proteins, sp)
        svg = get_string_svg(ids, sp, rs)
        annots = get_annotations(ids, sp)
        d_a = annots.to_dict("records")
        return svg, d_a, no_update, False
    except Exception as e:
        return no_update, no_update, [
            html.H2("An error has occured!"),
            html.Code(format_exc(limit=3), style={"white-space": "pre-wrap"})
        ], True


# Save DE proteins
@callback(
    Output("download_proteins", "data"),
    Input("save_proteins_button", "n_clicks"),
    State("result_proteins_table", "data"),
    prevent_initial_call=True
)
def save_proteins(_, data):
    df = pd.DataFrame(data)
    path = save_csv_file_dialog(window)
    if path:
        df.to_csv(str(path), index=False)
    return None

# On DE proteins table click, open Uniprot in browser with protein ID
@callback(
    Output("result_proteins_table", "active_cell"),
    Input("result_proteins_table", "active_cell"),
    State("result_proteins_table", "data"),
    prevent_initial_call=True
)
def open_uniprot_browser(active_cell, data):
    if active_cell is None:
        return no_update
    dbname = data[active_cell["row"]]["dbname"]
    uniprot_id = re.findall(r"sp\|([A-Z0-9]+)", dbname)[0]
    if uniprot_id:
        webbrowser.open(f"https://www.uniprot.org/uniprot/{uniprot_id}")
    return None

# On DE proteins graph click, open Uniprot in browser with protein ID
@callback(
    Input("volcano_plot", "clickData"),
    prevent_initial_call=True
)
def open_uniprot_browser_graph(data):
    if not data:
        return no_update
    points = data["points"]
    if not points:
        return no_update
    point = points[0]
    dbname = point["customdata"][0]
    uniprot_id = re.findall(r"sp\|([A-Z0-9]+)", dbname)[0]
    if uniprot_id:
        webbrowser.open(f"https://www.uniprot.org/uniprot/{uniprot_id}")
    return None

# On scipt exit remove uploaded files
def remove_files():
    for file in FILES_PATH.iterdir():
        file.unlink()
    for file in CACHE_PATH.iterdir():
        file.unlink()

def create_user_files_dirs():
    if not FILES_PATH.exists():
        FILES_PATH.mkdir()
    if not CACHE_PATH.exists():
        CACHE_PATH.mkdir()

atexit.register(remove_files)


def set_layout(app: Dash, args: argp.Namespace):
    app.layout = html.Div([
        html.Div(
            html.Header("Quantis", id="main_header"),
            className="header-fullwidth"
        ),
        html.Div([

            html.H2("Input"),
            html.Div([
                html.P("Input file format: ", style={'marginRight': '0.5em'}),
                dcc.Dropdown(
                    id="input_format", options=[
                        {"label": "Scavager", "value": "Scavager"},
                        {"label": "MS1+Diffacto", "value": "s+d"},  # Research on what typo of workflow it can be used in is needed
                        {"label": "MaxQuant", "value": "MaxQuant"},
                        {"label": "DirectMS1Quant", "value": "DirectMS1Quant"},
                        {"label": "Diffacto", "value": "Diffacto"},
                    ], value=args.format,
                    clearable=False, style={'width': '13em'}
                ),
            ], style={'display': 'flex', 'flex-direction': 'row', 'width': '100%'}),
            html.Details([
                html.Summary("File type description", style={'font-size': '12pt'}),
                html.P(id="file_type_description"),
            ]),
            dbc.Alert(id="input_error", color="danger", is_open=False),
            # Div for single file input
            html.Div([
                html.Button("Upload score file", id='single_input_btn', className="upload_button"),
                dcc.Input(id="single_file_path", value=(args.sample or ""), placeholder="No file selected", disabled=True, className="path_input"),
                html.Div([
                    dcc.Dropdown(id="col_prefix", options=["iBAQ", "Intensity", "Sequence coverage", "Unique peptides"], value="iBAQ", clearable=False),
                    html.Div([
                        html.P("Control prefix"),
                        dcc.Input(id="k_prefix", style={"width": "30%"}),
                        html.P("Test prefix"),
                        dcc.Input(id="a_prefix", style={"width": "30%"}),
                        html.Button("Apply", id="btn_prefix", className="exec_button", style={"width": "15%"})
                    ], style={"display": "flex", "justify-content": "space-between"}),
                    dash_table.DataTable(
                    id="column_DT",
                    columns=[
                        {'id': 'col', 'name': 'Label', 'editable': False},
                        {'id': 'kan', 'name': 'Group', 'presentation': 'dropdown'}
                    ],
                    editable=True,
                    dropdown={
                        'kan': {'options':[
                            {'label': 'None', 'value': 'N'},
                            {'label': 'Control', 'value': 'K'},
                            {'label': 'Test', 'value': 'A'},
                        ], 'clearable': False}
                    },
                    page_size=10,
                    page_action='native',
                    page_current=0,
                    cell_selectable=False
                )], style={'display': 'hidden'}, id="maxquant_table_div")
            ], style={"diplay": "hidden"}, id="single_input_div"),
            # Div for multiple files input
            html.Div([
                html.Div([
                    html.P("Select executable file:"),
                    html.Div([
                        dcc.Input(id="executable_path", type="text", placeholder="Path to Executable", disabled=True, style={'width': '100%'}),
                        html.Button("Browse", id="executable_btn", className="exec_button"),
                    ], style={'display': 'flex', 'flex-direction': 'row', "justify-content": "space-between"}),
                ], style={"display": "hidden"}, id="executable_div"),
                html.Div([
                    html.Div([
                        dcc.Input(id="control_name", type="text", placeholder="Control", className="group-title"),
                        # du.Upload(id="control_input", filetypes=['tsv'], text="Upload Control", max_files=10),
                        html.Button("Upload control files", id="control_btn_input", className="upload_button"),
                        dash_table.DataTable(
                            id="control_files_table", columns=[{"id": "path", "name": "File Path"}],
                            editable=False, row_selectable="multi", cell_selectable=False,
                            style_cell={
                                'overflow': 'hidden', 'textOverflow': 'ellipsis',
                                'maxWidth': 0, 'textAlign': 'left', 'direction': 'rtl'}),
                        dcc.Input(id="lastfiles_K", type="hidden", value=";".join(args.s1 or [])),
                        html.Div([
                            html.Button("Remove selected", id="rm_K_sel_btn", className="rm_button"),
                            html.Button("Remove all", id="rm_K_all_btn", className="rm_button"),
                        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between'}),
                    ], style={"padding": 10, 'flex': 1}),
                    html.Div([
                        dcc.Input(id="test_name", type="text", placeholder="Test", className="group-title"),
                        html.Button("Upload test files", id="test_btn_input", className="upload_button"),
                        # du.Upload(id="test_input", filetypes=['tsv'], text="Upload Test", max_files=10),
                        dash_table.DataTable(
                            id="test_files_table", columns=[{"id": "path", "name": "File Path"}],
                            editable=False, row_selectable="multi", cell_selectable=False,
                            style_cell={
                                'overflow': 'hidden', 'textOverflow': 'ellipsis',
                                'maxWidth': 0, 'textAlign': 'left', 'direction': 'rtl'}),
                        dcc.Input(id="lastfiles_A", type="hidden", value=";".join(args.s2 or [])),
                        html.Div([
                            html.Button("Remove selected", id="rm_A_sel_btn", className="rm_button"),
                            html.Button("Remove all", id="rm_A_all_btn", className="rm_button"),
                        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between'}),
                    ], style={"padding": 10, 'flex': 1}),
                ], style={'display': 'flex', 'flex-direction': 'row',  "justify-content": "space-between"}),
                # dcc.Download(id="download_sample"),
                # html.Button("Generate Sample File", id="sample_gen_btn", className="download_button"),
                # html.P("Or use a sample file:"),
                # du.Upload(id="sample_input", filetypes=['csv'], text="Upload Sample File", max_files=1),
                # html.Details([
                #     html.Summary("What is sample file?", style={'font-size': '12pt'}),
                #     html.P(
                #         "Sample file is a csv file, containing informtion about input files. "
                #         + "It is expected to have two columns: Path with absolute paths to files "
                #         + "and Sample, containing letters K and A for control and test files respectfully."
                #     )
                # ]),
            ], style={"diplay": "grid"}, id="multi_input_div"),
            html.Br(),

            # A collapsible div with quantification parameters, collapsed by default
            html.Details([
                html.Summary("Quantification Parameters"),
                html.H3("Statistical processing"),
                html.Table([
                    # First row
                    html.Tr([
                        html.Td("Imputation", style={"width": "25%"}),
                        html.Td("Regulation", style={"width": "25%"}),
                        html.Td("Threshold calculation", style={"width": "25%"}),
                        html.Td("Multiple-testing correction", style={"width": "25%"}),
                    ]),
                    html.Tr([
                        html.Td(dcc.Dropdown(id="imputation", options=["Drop", "Min", "kNN"], value="Min", clearable=False)),  # default: Min
                        html.Td(dcc.Dropdown(id="regulation", options=["UP", "DOWN", "BOTH"], value="BOTH", clearable=False)),  # default: BOTH
                        html.Td(dcc.Dropdown(id="threshold_calculation", options=[
                            {"label": "static", "value": "static"},
                            {"label": "semi-dynamic", "value": "semi-dynamic"},
                            {"label": "dynamic", "value": "dynamic"},
                            {"label": "MS1", "value": "ms1", "disabled": True}
                        ], value="static", clearable=False)),
                        html.Td(dcc.Dropdown(id="correction", clearable=False, value="fdr_bh")),
                    ]),
                ], style={"padding": 10, 'width': '100%'}),
                html.H3("StringDB network"),
                html.Table([
                    html.Tr([
                        html.Td("Required score"),
                        html.Td("Species", colSpan=2),
                    ]),
                    html.Tr([
                        html.Td(dcc.Input(id="req_score", type="number", min=0, max=1000, step=100, placeholder="default"), style={"width": "30%"}),
                        html.Td(dcc.Dropdown(id="species", options=[
                                {"label": "H. sapiens", "value": 9606},
                                {"label": "E. coli", "value": 562},
                                {"label": "M. musculus", "value": 10090},
                                {"label": "S. cerevisiae", "value": 4932},
                                {"label": "Custom...", "value": -1}
                        ], value=9606, clearable=False), style={"width": "25%"}),
                        html.Td(dcc.Input(id="custom_species", type="number", placeholder="NCBI Taxonomy ID", disabled=True, value=9606, debounce=2), style={"width": "25%"}),
                        html.Td(html.P(id="species_name", style={"font-style": "italic", "margin": 0}, children=""), style={"width": "25%"})
                    ]),
                ], style={"padding": 10, 'width': '100%'})
            ], open=True),
            
            html.Details([
                html.Summary("Diffacto Parameters"),
                html.Table([
                    html.Tr([
                        html.Td("Normalize"),
                        html.Td("Impute threshold"),
                        html.Td("Min samples"),
                    ]),
                    html.Tr([
                        html.Td(dcc.Dropdown(id="dif_normalize", options=['average','median','GMM','None'], value="None", clearable=False)),
                        html.Td(dcc.Input(id="dif_impute_threshold", type="number", min=0, max=1, step=0.05, value=0)),
                        html.Td(dcc.Input(id="dif_min_samples", type="number", min=0, max=20, step=1, value=0)),
                    ]),
                ], style={"padding": 10, 'width': '100%'}),
            ], style={'display': 'hidden'}, id="diffacto_div"),

            # Fold change and p-value threshold value sliders with input fields
            # Not collapsible
            html.Div([
                html.H3(["Log", html.Sub("2"), "(FC) threshold"]),
                html.Div([
                    dcc.Input(id="fold_change_input_left", type="number", value=-1, style={"width": "8%"}),
                    html.Div(dcc.RangeSlider(
                        id="fold_change_slider", min=-3, max=3, step=0.1, value=[-1, 1], marks={0.5*i: f"{0.5*i}" for i in range(-6,7)}
                    ), style={"width": "80%"}),
                    dcc.Input(id="fold_change_input_right", type="number", value=1, style={"width": "8%"}),
                ], style={"padding": 10, 'display': 'flex', 'flex-direction': 'row',  "justify-content": "space-between"}),
                html.H3("P-value Threshold"),
                html.Div([
                    dcc.Input(id="pvalue_input", type="number", value=0.01, style={"width": "15%"}),
                    html.Div(dcc.Slider(
                        id="pvalue_slider", min=-5, max=-1, step=0.1,
                        value=-2, marks={i: f"{10**i}" for i in range(-5, 0)}
                    ), style={"width": "80%"}),
                ], style={"padding": 10, 'display': 'flex', 'flex-direction': 'row',  "justify-content": "space-between"}),
            ]),
        
            # A collapsible div with style parameters
            html.Details([
                html.Summary("Style Parameters", style={'font-size': '14pt'}),
                html.Div([
                    ColorPicker(id="up_color", label="UP points", value={'hex': "#890c0c"}),
                    ColorPicker(id="down_color", label="DOWN points", value={'hex': "#42640a"}),
                    ColorPicker(id="not_color", label="Background points", value={'hex': "#129dfc"}),
                ], style={"padding": 10, "display": "flex", "flex-direction": "row", "justify-content": "space-between"})
            ]),

            # Button to start the analysis
            html.Button(
                "Start Analysis", id="start_button", className="start_button",
                style={'margin-left': 'auto', 'margin-right': 'auto'}
            ),
            html.Hr(),
        ], className="container"),
        html.Div([
            # ====== Results ======
            # Error div
            dbc.Alert(id="run_error",color="danger", is_open=False, style={'user-select': 'all'}),
            dcc.Loading(dcc.Graph(id="volcano_plot"), type="graph"),
            dcc.Loading([
                html.Img(
                    id="string_svg",
                    style={"display": "block", "margin-left": "auto", "margin-right": "auto", 'max-width': '100%'}
                ),
                html.H3("Enriched GO annotations"),
                dash_table.DataTable(
                    id="annotations_table",
                    columns=[
                        {"name": "Category", "id": "category"},
                        {"name": "GO Term", "id": "term"},
                        {"name": "FDR", "id": "fdr"}, 
                        {"name": "Description", "id": "description"},
                    ],
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold',
                        'color': '#3a1771'
                    },
                    page_size=20
                ),
            ], type="circle"),
            html.H3("Differentially Expressed Proteins"),
            html.Button("Save DE protens", id="save_proteins_button", disabled=True),
            dcc.Download(id="download_proteins"),
            dash_table.DataTable(
                id="result_proteins_table",
                columns=[
                    {"name": "Protein", "id": "dbname"},
                    {"name": "Fold Change", "id": "FC"},
                    {"name": "p-value", "id": "logFDR"},
                ],
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'color': '#3a1771'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'dbname'},
                        'textAlign': 'left'
                    },
                    {
                        'if': {'filter_query': '{FC} < 0', 'column_id': 'FC'},
                        'backgroundColor': '#c12424', 'color': 'white'
                    },
                    {
                        'if': {'filter_query': '{FC} > 0', 'column_id': 'FC'},
                        'backgroundColor': '#24c1a4',
                    },
                    {
                        'if': {'state': 'selected'},
                        'backgroundColor': '#4b44c5', 'color': 'white'
                    },
                ],
                style_cell={
                    'overflow': 'hidden', 'textOverflow': 'ellipsis','maxWidth': 0,
                }
            ),
        ])
    ])


def start_webview():
    create_user_files_dirs()
    webview.start()


def launch_from_cli():
    parser = argp.ArgumentParser(
        description="Visual Interface for qunatification analysis of MS/MS proteomics data",
        formatter_class=argp.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--format", "-f", help="format of input data. Allowed values: 'Scavager', 's+d', 'MaxQuant', 'DirectMS1Quant', 'Diffacto'", default='Scavager')
    parser.add_argument("--sample", "-s", help="single file input")
    parser.add_argument("-s1", help="control files input", nargs='+')
    parser.add_argument("-s2", help="test files input", nargs='+')
    parser.add_argument("--web", help="launch as browser app", action="store_true")
    args = parser.parse_args()
    reinstantiate()
    set_layout(app, args)
    if args.web:
        app.run(debug=True)
    else:
        start_webview()


def launch_import(s0="", s1="", s2="", fmt="Scavager"):
    args_dict = {"sample": s0, "s1": s1, "s2": s2, "format": fmt}
    args = argp.Namespace(
        **args_dict
    )
    reinstantiate()
    set_layout(app, args)
    start_webview()


def launch():
    args = argp.Namespace(format='Scavager')


if __name__ == "__main__":
    # app.run_server(debug=False)
    launch_from_cli()