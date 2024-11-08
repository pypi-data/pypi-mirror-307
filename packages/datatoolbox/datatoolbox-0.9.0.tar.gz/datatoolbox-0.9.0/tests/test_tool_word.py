#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 13:57:45 2024

@author: ageiges
"""

import datatoolbox as dt
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

wt = dt.tools.word

# %%

data = pd.DataFrame(
    index=[2018, 2017], columns=["Coal", "Oil", "Gas", "Nuclear", "Renewables"]
)
data.loc[2018, :] = [88.9, 0.1, 0, 4.5, 6.6]
data.loc[2017, :] = [89.9, 0.1, 0, 3.5, 6.6]
# data.loc[2016,: ] = [85.9,0.1, 0, 3.5, 9.6]


# %%
def test_word_doc_creation_and_save():
    doc = wt.Document()

    doc.add_heading("Test document", level=1)

    doc.save("test.docx")

    assert os.path.exists("test.docx")
    os.remove("test.docx")


def test_word_structure_elements():
    doc = wt.Document()

    doc.add_heading("Test document", level=1)
    para = doc.add_paragraph(
        "This document is generated automatically by datatoolbox using the python package docx.",
    )

    para = doc.add_to_paragraph(
        para, "This is an additional scentence in the same paragraph."
    )

    expected_text = "This document is generated automatically by datatoolbox using the python package docx. This is an additional scentence in the same paragraph. "
    assert para.text == expected_text

    doc.add_page_break()

    doc.add_bullet_list(["one", "two", "three"])


def test_word_table():
    doc = wt.Document()

    table = doc.add_table(data, "Power generation shares")

    assert len(doc.doc.tables) == 1


def test_word_table_syles():
    doc = wt.Document()

    table = doc.add_table(data, "Power generation shares")
    wt.set_cell_background(table, 1, 2, color="2a6099")

    wt.change_font_size(table, 8)
    # doc.open_word()


def test_word_figure():
    doc = wt.Document()

    fig = plt.figure()
    plt.clf()
    plt.bar(list(range(len(data.columns))), data.loc[2018, :])
    plt.xticks(list(range(len(data.columns))), data.columns)

    doc.add_figure(fig, relative_width=0.7, crop=True, caption="Figure caption")

    doc = wt.Document(numbering_figures=True)
    doc.add_figure(fig, relative_width=0.7, crop=False, caption="Figure caption")

    plt.close("all")


def test_word_text_styles():
    doc = wt.Document()
    para = doc.add_paragraph("New paragraph.")
    doc.add_to_paragraph(para, text="bold", style="bold")
    doc.add_to_paragraph(para, text="italic", style="italic")
    doc.add_to_paragraph(para, text="italic", style="italic", highlight_color=True)

    doc.font_color_runs(para, hexcolor="2a6099")
    para = doc.add_paragraph("Second paragraph")
    doc.highlight_runs(para)
    # doc.save('test.docx')
    # doc.open_word()
