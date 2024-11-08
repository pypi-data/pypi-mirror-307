#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:25:15 2019

@author: Andreas Geiges
"""

import os
import sys
import networkx as nx
from functools import reduce
from operator import and_

import pandas as pd
import numpy as np
from typing import Union, Iterable

import logging

import datatoolbox as dt
from datatoolbox import mapping as mapp
from datatoolbox import core
from datatoolbox import config
from datatoolbox import data_structures

import matplotlib.pylab as plt

import tqdm


logger = logging.getLogger(__name__)


# used  in __init__
try:
    from hdx.location.country import Country

    def getCountryISO(string):
        # print(string)
        try:
            string = string.replace("*", "")
            results = Country.get_iso3_country_code_fuzzy(string)
            if len(results) > 0:
                return results[0]
            else:
                return None
        except Exception:
            print("error for: " + string)

except Exception:

    def getCountryISO(string):
        print("the package hdx is not installed, thus this function is not available")
        print('use: "pip install hdx-python-country" to install')
        return None


# used by Datatable.clean
def cleanDataTable(dataTable):
    if "standard_region" in dataTable.columns:
        dataTable = dataTable.reset_index("region").set_index(
            ["region", "standard_region"]
        )
    dataTable = (
        dataTable.dropna(how="all", axis=1).dropna(how="all", axis=0).astype(float)
    )

    # clean meta data
    keysToDelete = list()
    for key in dataTable.meta.keys():
        if np.any(pd.isna(dataTable.meta[key])):
            if key not in config.ID_FIELDS:
                keysToDelete.append(key)
            else:
                dataTable.meta[key] = ""
    for key in keysToDelete:
        del dataTable.meta[key]

    # ensure time colums to be integer
    dataTable.columns = dataTable.columns.astype(int)

    dataTable = dataTable.loc[:, dataTable.columns.sort_values()]
    return dataTable


# used by indexing.convert_idx_string_to_iso
def identifyCountry(string):
    # numeric ISO code

    try:
        numISO = float(string)
        mask = numISO == mapp.countries.codes["numISO"]
        if mask.any():
            return mapp.countries.codes.index[mask][0]
    except Exception:
        pass

    if len(str(string)) == 2:
        mask = str(string).upper() == mapp.countries.codes["alpha2"]
        if mask.any():
            return mapp.countries.codes.index[mask][0]

    if len(str(string)) == 3:
        if str(string).upper() in mapp.countries.codes.index:
            return string.upper()

    try:
        coISO = dt.getCountryISO(string)
        return coISO
    except Exception:
        print(f"not matching country found for {string}")
        return None


def update_source_from_file(fileName, message=None):
    sourceData = pd.read_csv(fileName)
    for index in sourceData.index:
        dt.core.DB._addNewSource(sourceData.loc[index, :].to_dict())


def update_DB_from_folder(folderToRead, message=None):
    fileList = os.listdir(folderToRead)
    fileList = [file for file in fileList if ".csv" in file[-5:].lower()]

    tablesToUpdate = dict()

    for file in fileList:
        table = dt.read_csv(os.path.join(folderToRead, file))
        source = table.meta["source"]
        if source in tablesToUpdate.keys():
            tablesToUpdate[source].append(table)
        else:
            tablesToUpdate[source] = [table]
    if message is None:
        message = "External data added from external source by " + config.CRUNCHER

    for source in tablesToUpdate.keys():
        sourceMetaDict = dict()
        sourceMetaDict["SOURCE_ID"] = source
        dt.commitTables(
            tablesToUpdate[source],
            message=message,
            sourceMetaDict=sourceMetaDict,
            append_data=True,
            update=True,
        )


def zipExport(fileName, tablesIDs_to_export=None):
    from zipfile import ZipFile

    if tablesIDs_to_export is None:
        tablesIDs_to_export = list(dt.core.DB.inventory.index)

    folder = os.path.join(config.PATH_TO_DATASHELF, "exports/")
    os.makedirs(folder, exist_ok=True)

    #    root = config.PATH_TO_DATASHELF

    sources = dt.get_inventory().loc[tablesIDs_to_export].source.unique()
    sourceMeta = dt.core.DB.sources.loc[sources]
    sourceMeta.to_csv(os.path.join(folder, "sources.csv"))
    zipObj = ZipFile(os.path.join(folder, fileName), "w")
    zipObj.write(os.path.join(folder, "sources.csv"), "./sources.csv")
    for ID in tqdm.tqdm(tablesIDs_to_export):
        # Add multiple files to the zip
        tablePath = dt.core.DB._getTableFilePath(ID)
        csvFileName = os.path.basename(tablePath)

        zipObj.write(tablePath, os.path.join("./data/", csvFileName))
    #        zipObj.write(tablePath, os.path.relpath(os.path.join(root, file), os.path.join(tablePath, '..')))

    # close the Zip File
    zipObj.close()
    print(f"export written to {os.path.join(folder, fileName)}")

    return os.path.join(folder, fileName)


def update_DB_from_zip(filePath):
    from zipfile import ZipFile
    import shutil

    zf = ZipFile(filePath, "r")

    tempFolder = os.path.join(config.PATH_TO_DATASHELF, "temp/")
    shutil.rmtree(tempFolder, ignore_errors=True)
    os.makedirs(tempFolder)
    zf.extractall(tempFolder)
    zf.close()

    update_source_from_file(os.path.join(tempFolder, "sources.csv"))
    update_DB_from_folder(
        os.path.join(tempFolder, "data"),
        message="DB update from " + os.path.basename(filePath),
    )


import csv


def dict_to_csv(dictionary, filePath):
    with open(filePath, "w", newline="") as file:
        writer = csv.writer(file)
        for key, val in dictionary.items():
            writer.writerow([key, val])


def csv_to_dict(filePath):
    with open(filePath, "r", newline="") as file:
        reader = csv.reader(file)
        mydict = dict()
        for row in reader:
            print(row)
            #            v = rows[1]
            mydict[row[0]] = row[1]
    return mydict


def pattern_match(
    data: pd.Series, patterns: Union[str, Iterable[str]], regex: bool = False
):
    """Find matches in `data` for a list of shell-style `patterns`

    Arguments
    ---------
    data : pd.Series
        Series of data to match against
    patterns : Union[str, Iterable[str]]
        One or multiple patterns, which are OR'd together
    regex : bool, optional
        Accept plain regex syntax instead of shell-style, default: False

    Returns
    -------
    matches : pd.Series
        Mask for selecting matched rows
    """

    if not isinstance(patterns, Iterable) or isinstance(patterns, str):
        patterns = [patterns]
    elif not patterns:
        raise ValueError("pattern list may not be empty")

    matches = False
    for pat in patterns:
        if isinstance(pat, str):
            if not regex:
                pat = shell_pattern_to_regex(pat) + "$"
            matches |= data.str.match(pat, na=False)
        else:
            matches |= data == pat

    return matches


def shell_pattern_to_regex(s):
    """Escape characters with specific regexp use"""
    return (
        str(s)
        .replace("|", r"\|")
        .replace(".", r"\.")  # `.` has to be replaced before `*`
        .replace("**", "__starstar__")  # temporarily __starstar__
        .replace("*", r"[^|]*")
        .replace("__starstar__", r".*")
        .replace("+", r"\+")
        .replace("(", r"\(")
        .replace(")", r"\)")
        .replace("$", r"\$")
    )


# open files
openers = dict()

operation_systems_supported = ["Linux", "Darwin"]
# excel
openers["xlsx"] = dict()
openers["xlsx"]["Linux"] = "libreoffice"
openers["xlsx"]["Darwin"] = 'open -a "Microsoft Excel"'

openers["docx"] = dict()
openers["docx"]["Linux"] = "libreoffice"
openers["docx"]["Darwin"] = 'open -a "Microsoft Word"'


def open_file(path):
    suffix = path.split(".")[-1]

    if config.OS not in operation_systems_supported:
        print(
            "OS not supported. Currently support is restriced to "
            + str(operation_systems_supported)
        )
        return

    if suffix not in openers.keys():
        print("no suiable file opener found ")
        return

    os.system(" ".join([openers[suffix][config.OS], path]))
    # elif dt.config.OS == 'Darwin':
    #     os.system('open -a "Microsoft Excel" ' + self.setup.MAPPING_FILE)


def shorten_find_output(dataframe):
    return dataframe.reset_index(drop=True).drop(
        [
            "scenario",
            "model",
            "category",
            "entity",
            "source_year",
            "source_name",
            "unit",
        ],
        axis=1,
    )


# def get_data_trees(**kwargs):
#     findc = core.DB.findc
#     results = findc(**kwargs)
#     return _process_query(results)


def _process_query(results):
    # Initialize graphs for different data heads
    heads, graphs = [], {}

    if len(results.scenario.unique()) > 1:
        raise ValueError(
            "Multiple scenarios were detected, ensure that the"
            + " scenario name/ model/ data source etc. specify a unique scenario"
        )
    if len(results.scenario.unique()) == 0:
        raise ValueError(
            "Specified kwargs point to an empty list of scenarios. "
            + "Change kwargs or update your database."
        )
    scenario = list(results.scenario.unique())[0]

    # Iterate through data inventory
    for ix in results.index:
        # Remove scenario and model name
        ix = ix.split("__")[0]
        nodes = ix.split("|")

        # If first time occurrence of data head, update graphs
        if nodes[0] not in heads:
            heads.append(nodes[0])
            graph = nx.DiGraph()
            attr = {"label": nodes[0]}
            graph.add_node(nodes[0], **attr)
            graphs.update({nodes[0]: graph})

        # Fetch correct graph/  dict/ list
        graph = graphs[nodes[0]]

        # Add branches to tree
        root = nodes[0]
        for i, name_short in enumerate(nodes[1:]):
            # Get unique node name
            name_long = "|".join(nodes[1 : i + 2])
            # Add node to graph if it does not exist already
            if name_long not in graph.nodes:
                # Mark with "*"" if it point to a data table
                label = name_short
                # Add a short label for better visualization
                attr = {"label": label}
                graph.add_node(name_long, **attr)
            if i == len(nodes[1:]) - 1:
                graph.nodes[name_long]["label"] = name_short + "*"
            # Add edge
            graph.add_edge(root, name_long)
            root = name_long

    return graphs, scenario


def get_positions(graph, x_offset=1):
    """Get positions of nodes for horizontally aligned tree visualization

    Args:
        graph (networkx DiGraph): directed graph which is a tree
        x_offset (int, optional): Offset between horizontal spacing. Defaults to 1.

    Raises:
        TypeError: if not networkx DiGraph or tree

    Returns:
        dict: dictionary, mapping nodes to xy positions
    """

    # Check if tree
    if not isinstance(graph, nx.DiGraph):
        raise TypeError("Has to be a networkx DiGraph")

    if not nx.is_tree(graph):
        raise TypeError("Has to be a tree")

    # Determine root node
    root = next(iter(nx.topological_sort(graph)))

    # Determine number of subbranches
    out_degrees = graph.out_degree()

    def nb_leafs_in_subtree(root):
        """Recursive function for getting the number of leafs attached to root (root inclusive)

        Args:
            root (networkx node): root of subtree

        Returns:
            int: number of leafs in subtree
        """
        if out_degrees[root] == 0:
            nb_children = 1
        else:
            nb_children = sum(
                nb_leafs_in_subtree(child) for child in graph.neighbors(root)
            )

        return nb_children

    def set_positions(
        root_,
        x_spacing={},
        depth=0,
        pos={root: (0, nb_leafs_in_subtree(root) / 2)},
    ):
        """Sets positions of nodes in a tree for horizontally aligned tree in a recursive fashion

        Args:
            root_ (networkx node): root of subtree
            x_spacing (dict, optional): Dictionary for keeping track of required horizontal spacing. Defaults to {}.
            depth (int, optional): Current tree depth. Defaults to 0.
            pos (dict, optional): [description]. Defaults to {root: (0, nb_leafs_in_subtree(root) / 2)}.

        Returns:
            (dict, dict): Returns  x_spacing and pos
        """

        # Consider length of root for x-spacing
        x_spacing.setdefault(depth, len(graph.nodes[root_]["label"]))
        x_spacing[depth] = max(x_spacing[depth], len(graph.nodes[root_]["label"]))

        if out_degrees[root_] == 0:
            return

        # Distribute children of root_ across the y-axis
        offset = 0
        depth += 1
        x_spacing.setdefault(depth, 0)

        for child in graph.neighbors(root_):
            y_pos = (
                pos[root_][1]
                - nb_leafs_in_subtree(root_) / 2
                + nb_leafs_in_subtree(child) / 2
                + offset
            )
            pos.update({child: (depth, y_pos)})
            offset += nb_leafs_in_subtree(child)

            set_positions(child, x_spacing, depth=depth, pos=pos)

        return pos, x_spacing

    # Determine positions of nodes
    pos, x_spacing = set_positions(root)
    # Re-adjust x-spacing
    pos = {
        key: (sum(x_spacing[i] + x_offset for i in range(pos_[0])), pos_[1])
        for key, pos_ in pos.items()
    }

    return pos, x_spacing


def plot_tree(
    graph,
    scenario,
    x_offset=3,
    fontsize=12,
    figsize=None,
    savefig_path=None,
    dpi=100,
):
    """Plots a tree indicating available data of a scenario

    Parameters
    ----------
    graph : networkx.DiGraph
        tree in digraph format (obtained via get_data_trees function)
    scenario : str
        scenario name
    x_offset : int, optional
        x offset between nodes, by default 3
    fontsize : int, optional
        fontsize of the node labels (either fontsize or figsize can be specified not
        both), by default 12
    figsize : 2-dim tuple or None, optional
        figure size (either fontsize or figsize can be specified not
        both), by default None
    savefig_path : str or None, optional
        path to save figure to (e.g savefig_path = os.path.join(os.getcwd(), "fig.png") ),
        by default None
    dpi : int, optional
        dots per inches used in savefig, by default 100
    """

    pos, x_spacing = get_positions(graph, x_offset=x_offset)

    if figsize is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = plt.subplots(figsize=figsize)

    # Draw the graph
    nx.draw(graph, pos=pos, with_labels=False, ax=ax, node_color="none")

    # Set xlim and ylim
    x_max = (
        sum(x + x_offset for level, x in x_spacing.items() if isinstance(level, int))
        - x_offset
    )
    y_max = max(pos_[1] for pos_ in pos.values()) + 1
    ax.set_xlim([0, x_max]), ax.set_ylim([0, y_max])

    # Get fontsize or reset figsize to avoid overlaps
    if fontsize is None:
        x_fig, y_fig = fig.get_size_inches() * fig.dpi
        fontsize = min(x_fig / (x_max / 1.5), y_fig / (y_max * 2.5))
    else:
        x_fig = 2 + (fontsize * (x_max / 1.5) / fig.dpi)
        y_fig = 2 + (fontsize * y_max * 2.5 / fig.dpi)
        fig.set_size_inches(x_fig, y_fig, forward=True)

    # Add node labels
    for node, xy in pos.items():
        text = graph.nodes[node]["label"]
        ax.annotate(
            text,
            xy,
            bbox=dict(pad=0.2, fc="gainsboro", ec="k", boxstyle="round"),
            family="monospace",
            fontsize=fontsize,
            verticalalignment="center",
            horizontalalignment="left",
        )

    # Add legend
    ax.annotate(
        "*: data available\nscenario: {}".format(scenario),
        (x_max, y_max),
        family="monospace",
        fontsize=fontsize,
        verticalalignment="top",
        horizontalalignment="right",
    )

    # Plot and save
    plt.tight_layout()

    if savefig_path is not None:
        plt.savefig(savefig_path, dpi=dpi)

    plt.show()


def plot_query_as_graph(results, savefig_path=None):
    graphs, scenario = _process_query(results)
    for gKey in graphs.keys():
        plot_tree(
            graphs[gKey],
            scenario,
            #                 figsize=[5,6],
            savefig_path=savefig_path,
        )


def to_pyam(results, native_regions=False, disable_progress=None):
    """
    Load resuls as pyam IDateFrame.

    Parameters
    ----------
    results : pandas Dataframe with datatoolbox query results
        Results from find.
    native_regions : bool, optional
        Load native region defintions if available. The default is False.
    disable_progress : bool, optional
        Disable displaying of progressbar. The default None hides the
        progressbar on non-tty outputs.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return core.DB.getTables(
        results.index, native_regions, disable_progress=disable_progress
    ).to_pyam()


def filterp(df, level=None, regex=False, **filters):
    """
    Future defaulf find method that allows for more
    sophisticated syntax in the filtering

    Usage:
    -------
    filters : Union[str, Iterable[str]]
        One or multiple patterns, which are OR'd together
    regex : bool, optional
        Accept plain regex syntax instead of shell-style, default: False

    Returns
    -------
    matches : pd.Series
    Mask for selecting matched rows
    """

    # filter by columns and list of values
    keep = True

    for field, pattern in filters.items():
        # treat `col=None` as no filter applied
        if pattern is None:
            continue

        if field not in df:
            raise ValueError(f"filter by `{field}` not supported")

        keep &= pattern_match(df[field], pattern, regex=regex)

    if level is not None:
        keep &= df["variable"].str.count(r"\|") == level

    return df if keep is True else df.loc[keep]


def yearsColumnsOnly(index):
    """
    Extracts from any given index only the index list that can resemble
    as year

    e.g. 2001
    """

    import re

    REG_YEAR = re.compile("^[0-9]{4}$")

    newColumns = []
    for col in index:
        if REG_YEAR.search(str(col)) is not None:
            newColumns.append(col)
        else:
            try:
                if ~np.isnan(col) and REG_YEAR.search(str(int(col))) is not None:
                    #   test float string
                    newColumns.append(col)
            except Exception:
                pass
    return newColumns


def _create_sandbox_tables(sourceID, random_seed):
    #    import datatoolbox as dt
    import numpy as np

    np.random.seed(1)

    tables = list()
    source_meta = {
        "SOURCE_ID": sourceID,
        "collected_by": "Hard worker 1",
        "date": core.get_date_string(),
        "source_url": "www.www.www",
        "licence": "open access",
    }

    meta = {
        "entity": "Emissions|CO2",
        "category": "Total",
        "model": None,
        "scenario": "Historic",
        "source": sourceID,
        "unit": "Mt CO2",
    }

    table = data_structures.Datatable(
        np.random.randint(0, 20, [3, 21]),
        columns=list(range(2000, 2021)),
        index=["World", "Asia", "ZAF"],
        meta=meta,
    ).astype(float)
    tables.append(table)

    meta = {
        "entity": "Emissions|CO2",
        "category": "Total",
        "scenario": "Medium",
        "model": "Projection",
        "source": sourceID,
        "unit": "Mt CO2",
    }

    table = data_structures.Datatable(
        np.random.randint(20, 30, [3, 31]),
        columns=list(range(2020, 2051)),
        index=["World", "Asia", "ZAF"],
        meta=meta,
    ).astype(float)
    tables.append(table)

    meta = {
        "entity": "Emissions|CO2",
        "category": "Total_excl_LULUCF",
        "scenario": None,
        "model": "Historic",
        "source_name": sourceID,
        "unit": "Mt CO2",
    }

    table = data_structures.Datatable(
        np.random.randint(0, 15, [3, 21]),
        columns=list(range(2000, 2021)),
        index=["World", "Asia", "ZAF"],
        meta=meta,
    ).astype(float)
    tables.append(table)
    return tables, source_meta


def isin(df=None, **filters):
    """Constructs a MultiIndex selector

    Usage
    -----
    > df.loc[isin(region="World", gas=["CO2", "N2O"])]
    or with explicit df to get boolean mask
    > isin(df, region="World", gas=["CO2", "N2O"])
    """

    def tester(df):
        tests = (df.index.isin(np.atleast_1d(v), level=k) for k, v in filters.items())
        return reduce(and_, tests, next(tests))

    return tester if df is None else tester(df)


# # %%
# if __name__ == "__main__":
#     # %%
#     def calculateTotalBiomass(scenario):
#         source = "IAMC15_2019_R2"
#         tableID = core._createDatabaseID(
#             {
#                 "entity": "Primary_Energy|Biomass|Traditional",
#                 "category": "",
#                 "scenario": scenario,
#                 "source": "IAMC15_2019_R2",
#             }
#         )
#         tratBio = dt.getTable(tableID)

#         tableID = core._createDatabaseID(
#             {
#                 "entity": "Primary_Energy|Biomass|Modern|wo_CCS",
#                 "category": "",
#                 "scenario": scenario,
#                 "source": "IAMC15_2019_R2",
#             }
#         )
#         modernBio = dt.getTable(tableID)

#         tableID = core._createDatabaseID(
#             {
#                 "entity": "Primary_Energy|Biomass|Modern|w_CCS",
#                 "category": "",
#                 "scenario": scenario,
#                 "source": "IAMC15_2019_R2",
#             }
#         )
#         modernBioCCS = dt.getTable(tableID)

#         table = tratBio + modernBio + modernBioCCS

#         table.meta.update(
#             {
#                 "entity": "Primary_Energy|Biomass|Total",
#                 "scenario": scenario,
#                 "source": source,
#                 "calculated": "calculatedTotalBiomass.py",
#                 "author": "AG",
#             }
#         )
#         return table

#     outputTables, success = forAll(calculateTotalBiomass, "scenario")


# def handle_exception(exc_type, exc_value, exc_traceback):
#     if issubclass(exc_type, KeyboardInterrupt):
#         sys.__excepthook__(exc_type, exc_value, exc_traceback)
#         return

#     logger.exception(
#         "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
#     )


# def setup_logging(log_uncaught_exceptions=True, **kwargs):
#     from colorlog import ColoredFormatter

#     kwargs.setdefault("level", "INFO")

#     streamhandler = logging.StreamHandler()
#     streamhandler.setFormatter(
#         ColoredFormatter(
#             "%(name)-12s: %(log_color)s%(levelname)-8s%(reset)s %(message)s",
#             datefmt=None,
#             reset=True,
#         )
#     )

#     kwargs.setdefault("handlers", []).append(streamhandler)

#     if log_uncaught_exceptions:
#         sys.excepthook = handle_exception

#     logging.basicConfig(**kwargs)

#     def add_parent_to_syspath():
#         if ".." not in sys.path:
#             sys.path.insert(
#                 0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#             )
