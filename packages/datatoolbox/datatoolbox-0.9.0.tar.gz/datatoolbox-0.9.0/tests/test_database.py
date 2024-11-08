#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 19:56:03 2020

@author: ageiges
"""

import os
import copy
import pytest
import datatoolbox as dt
import pandas as pd
from util_for_testing import df, df2, sourceMeta, df_empty

os.environ["PYTEST_VERSION"] = "1"

dt.admin.switch_database_to_testing()


def test_unique():
    res = dt.findp()
    list(res.loc[:, "source"].unique()) == ["Numbers_2020"]


def test_create_empty_datashelf():
    _path = os.path.abspath("./test_db")
    dt.core.DB.create_empty_datashelf(_path)
    import shutil

    shutil.rmtree(_path)


def test_validate():
    dt.core.DB._validateRepository()


def test_commit_new_table():
    df.loc["ARG", 2012] = 10
    dt.commitTable(df, "add first table", sourceMeta)


def test_validate_ID():
    assert dt.validate_ID(list(dt.findc().index)[0])

    dt.validate_ID("Numbers|Three__Historic__Numbers_2020")


def test_update_value_table():
    df.loc["ARG", 2012] = 20
    print(df.ID)
    dt.updateTable(df.ID, df, "update value in table")


def test_update_meta():
    df.meta["unit"] = "Mt CO2"
    df.meta["entity"] = "Emissions|CO2|transport"
    oldID = copy.copy(df.ID)
    df.generateTableID()
    dt.updateTable(oldID, df, "update meta data of table")

    assert "Emissions|CO2|transport__Historic__XYZ_2020" in dt.core.DB.inventory.index


def test_delete_table():
    dt.removeTable("Emissions|CO2|transport__Historic__XYZ_2020")

    assert not dt.table_exists(df.ID)


def test_commit_mutliple_tables():
    dt.commitTables([df, df2, df_empty], "adding set of table", sourceMeta)

    dt.commitTables([df2], "woverwrite_table", overwrite=True)

    df2_ext = df2.copy()
    df2_ext.loc["USA", :] = 1, 2, 2, 3

    dt.commitTables([df2_ext], "appending additional data", append_data=True)

    # check extended size
    assert dt.getTable(df2.ID).shape == (5, 4)


def test_delete_mutliple_tables():
    dt.removeTables([df.ID, df2.ID])

    assert not dt.table_exists(df.ID)
    assert not dt.table_exists(df.ID)


def test_delete_source():
    dt.core.DB.remove_source("XYZ_2020")


def test_findp():
    inv = dt.findp(variable="Numbers|Ones", source="Numbers_2020")

    assert len(inv.variable.unique()) == 1

    inv = dt.findp(variable="Numbers**", source="Numbers_2020")

    assert len(inv.variable.unique()) == 2


def test_as_wide_table():
    inv = dt.findp(variable="Numbers|Ones", source="Numbers_2020")

    wdf = inv.as_wide_dataframe()
    assert all(
        [
            x in ["variable", "region", "scenario", "model", "source", "unit"]
            for x in wdf.index.names
        ]
    )


def test_table_logging():
    # create tempory table in DB
    table = dt.getTable("Numbers|Ones__Historic__Numbers_2020")
    tableNew = table * 2
    tableNew.meta.update(table.meta)
    tableNew.meta.update({"category": "Twos"})
    dt.commitTable(tableNew, "test table")

    def test_analysis():
        table = dt.getTable("Numbers|Twos__Historic__Numbers_2020")
        print(table.sum())

    # run to save all required table for the analysis
    dt.core.DB.startLogTables()
    test_analysis()
    dt.core.DB.stopLogTables()
    dt.core.DB.save_logged_tables()

    # remove table form database
    dt.removeTable("Numbers|Twos__Historic__Numbers_2020")

    # run analysis with missing table, but locally stored
    test_analysis()

    # cleanup
    import shutil

    shutil.rmtree("data")


def test_index_operations():
    table = dt.getTable("Numbers|Ones__Historic__Numbers_2020")

    mi_table = table.to_multi_index_dataframe()

    # check index is multiindex
    # check that all meta data levels are in index
    assert isinstance(mi_table.index, pd.MultiIndex)
    assert mi_table.index.names == [
        "region",
        "category",
        "entity",
        "pathway",
        "scenario",
        "source",
        "unit",
        "variable",
    ]

    si_table = mi_table.squeeze_index_to_attrs()

    # check that back-converted table is equivalent to the original table
    assert si_table.equals(table)


def test_selected_meta_to_index():
    table = dt.getTable("Numbers|Ones__Historic__Numbers_2020")

    mi_table = table.to_multi_index_dataframe(
        meta_keys=["variable", "pathway", "source", "unit"]
    )

    # check index is multiindex
    # check that all meta data levels are in index
    assert isinstance(mi_table.index, pd.MultiIndex)
    assert sorted(mi_table.index.names) == sorted(
        ["region", "variable", "pathway", "source", "unit"]
    )


def test_table_logging():
    assert not dt.config.logTables
    dt.core.DB.startLogTables()
    assert dt.config.logTables

    tables = dt.getTables(dt.core.DB.inventory.index)

    dt.core.DB.stopLogTables()

    logged_tables = dt.core.DB.get_logged_tables()

    dt.core.DB.clearLogTables()


def test_aux_stuff_db():
    assert dt.core.DB._checkTablesOnDisk() == []
    dt.core.DB.info()
    dt.core.DB.sourceInfo()

    info = dt.core.DB.sourceInfo(show_number_of_table=True)
    assert "n_tables" in info.columns

    dt.core.DB.get_inventory()

    assert len(dt.core.DB.findc(variable="Numbers|O")) == 1

    dt.findp(None)

    assert len(dt.finde(variable="Numbers|Fives")) == 1


def test_gitManager():
    manager = dt.core.DB.gitManager


def test_inconsitency_error():
    dt.commitTable(df, message="add correct table", sourceMetaDict=sourceMeta)

    # make manual change
    df.iloc[0, 0] = 12

    # datatable.meta["creator"] = config.CRUNCHER
    sourcePath = os.path.join("database", df.source())
    file_path = os.path.join(
        dt.config.PATH_TO_DATASHELF, sourcePath, "tables", df.getTableFileName()
    )

    gitm = dt.core.DB.gitManager

    # test validity
    gitm._validateRepository("XYZ_2020")

    # introduce manual change
    df.to_csv(file_path)

    # test error raised
    with pytest.raises(Exception):
        gitm._validateRepository("XYZ_2020")

    # fix
    dt.admin.fix_brocken_DB("XYZ_2020", how="commmit_source_changes")
    gitm._validateRepository("XYZ_2020")


def test_fix_inconsitency_error():
    dt.commitTable(df, message="add correct table", sourceMetaDict=sourceMeta)

    # make manual change
    df.iloc[0, 0] = 12

    # datatable.meta["creator"] = config.CRUNCHER
    sourcePath = os.path.join("database", df.source())
    file_path = os.path.join(
        dt.config.PATH_TO_DATASHELF, sourcePath, "tables", df.getTableFileName()
    )

    gitm = dt.core.DB.gitManager

    # test validity
    gitm._validateRepository("XYZ_2020")

    # introduce manual change
    df.to_csv(file_path)

    # test error raised
    with pytest.raises(Exception):
        gitm._validateRepository("XYZ_2020")

    # fix
    dt.admin.fix_brocken_DB(sourceID="XYZ_2020", how="reset_source_revision")
    gitm._validateRepository("XYZ_2020")


def test_fix_updated_source_error():
    dt.commitTable(df, message="add correct table", sourceMetaDict=sourceMeta)
    sourceID = "XYZ_2020"
    # make manual change
    df.iloc[0, 0] = 12

    # datatable.meta["creator"] = config.CRUNCHER
    # sourcePath = os.path.join("database", df.source())

    gitm = dt.core.DB.gitManager

    # test validity
    gitm._validateRepository(sourceID)

    repo = gitm[sourceID]
    repo_path = repo.working_dir
    # introduce manual change

    # df.meta["category"] = "Industrial_processes"
    # df.generateTableID()
    file_path = os.path.join(repo_path, "tables", df.getTableFileName())
    df.to_csv(file_path)

    # sourceInventory = dt.inventory().loc[dt.inventory().source == sourceID, :]
    # sourceInventory.to_csv(os.path.join(repo_path, "source_inventory.csv"))
    # gitm.gitAddFile(
    #     sourceID, os.path.join(repo_path, "source_inventory.csv")
    # )
    repo.index.add([file_path])
    commit = repo.index.commit("Add new revison in source")
    new_hash = commit.hexsha

    # test error raised
    with pytest.raises(Exception):
        gitm._validateRepository(sourceID)

    # fix
    dt.admin.fix_brocken_DB(sourceID=sourceID, how="fix_sources_inventory")
    gitm._validateRepository(sourceID)

    assert dt.sourceInfo().loc[sourceID, "git_commit_hash"] == new_hash


def test_inventory_tables_compare():
    dt.admin.compare_source_inventory_to_main("XYZ_2020")


def test_source_log():
    dt.admin.get_source_log()


def test_unique_for_db():
    dt.database.unique(dt.get_inventory())


def test_force_remote_update_not_executed_in_pytest():
    assert not dt.core.DB.gitManager.check_for_new_remote_data(force_check=True)


def test_checkout_specific_source_version():
    dt.admin.switch_database_to_testing()
    source_ID = "Numbers_2020"
    # dt.core.DB.gitManager._update_remote_sources(source_ID)

    dt.core.DB.gitManager.create_new_source_tag(source_ID)
    table = dt.getTable(dt.findp(source=source_ID).index[0])

    new_table = table.copy()
    # changing table data
    new_table.loc["ARG", 2016] = 12.0
    new_table.meta["category"] = "mixed"
    new_table.generateTableID()
    print(f"New table {new_table.ID} created that will be added to source")
    dt.commitTable(new_table, message="added new table")
    dt.core.DB.gitManager.create_new_source_tag(source_ID)

    repo = dt.core.DB.gitManager._get_git_repo(source_ID)

    assert len(dt.core.DB.list_source_versions(source_ID)) == 2
    repo_status_before = repo.git.status()

    dt.core.DB.checkout_source_version(source_ID, tag="v1.0")
    assert "v1.0" in repo.git.status()

    assert new_table.ID not in dt.core.DB.inventory.index

    dt.core.DB.checkout_source_version(source_ID, tag="latest")
    assert repo.git.status() == repo_status_before

    assert new_table.ID in dt.core.DB.inventory.index


def test_list_tags():
    source_ID = "Numbers_2020"
    dt.core.DB.list_source_versions(source_ID)
