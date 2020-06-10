import os

import nbformat as nbf
import yaml


def run_builder():
    # *** Read YAML files ***
    print("Reading YAML file list...")
    path = os.getcwd()
    folder_path = f"{path}/hunt_configs/"

    # ** iterate through our YAML config files **
    conf_files = [x for x in os.listdir(folder_path) if x.endswith(".yaml")]
    for f in conf_files:
        filepath = folder_path + '/' + f
        print(f"Opening: {f}")
        yaml_file = yaml.safe_load(open(filepath).read())

        # *** Create Notebook object and add any metadata ***
        print("\tCreating notebook object...")
        nb = nbf.v4.new_notebook(metadata={"hide_input": True})
        nb['cells'] = []

        # ** append code cells to our notebook object **
        nb['cells'].append(nbf.v4.new_code_cell(
            """import ipywidgets as widgets
import numpy as np
import pandas as pd
import qgrid
from IPython.display import HTML, Javascript, Markdown, display

from hunt_tools import hunt as h
from hunt_tools.downselects import Downselects

# Formatting and Notebook Setup:
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 101)
pd.set_option('display.max_columns', 60)
pd.set_option('colheader_justify', 'left')
display(HTML("<style>.container { width:85% !important; }</style>"))
h.disable_scrolling()
""",
            metadata={"init_cell": True, "tags": ["Imports"]}
        ))

        # ** append markdown cell to our notebook object **
        # ** pull in objects from our yaml config file **
        nb['cells'].append(nbf.v4.new_markdown_cell(f"# Hunt Method: {yaml_file['technique_name']}"))

        nb['cells'].append(nbf.v4.new_code_cell(
            f"""hunt = h.Hunt('./sample_data/{yaml_file['notebook_name']}.json')
df = hunt.normalize_hunt_df({yaml_file['column_list']})""",
            metadata={"init_cell": True, "tags": ["DataFrame", "Normalization"]}
        ))

        # Add some technique decision support in to reduce the technique learning curve
        nb['cells'].append(nbf.v4.new_markdown_cell(
            f"""{yaml_file['hunt_description']}"""
        ))

        nb['cells'].append(nbf.v4.new_markdown_cell(
            f"""{yaml_file['technique_details']}"""
        ))

        nb['cells'].append(nbf.v4.new_markdown_cell(
            f"""{yaml_file['triage_tips']}"""
        ))

        # MORE WIDGETS!!!
        nb['cells'].append(nbf.v4.new_code_cell(
            """display(HTML('<br>'))
button = widgets.Button(description="Start Hunt")
button.on_click(h.run_all)
display(button)
display(HTML('<br>'))""",
            metadata={"init_cell": True, "tags": ["Start"]}
        ))

        nb['cells'].append(nbf.v4.new_markdown_cell(
            """## <span style="color:red">Hunt Data</span>"""
        ))

        # Display the data set with sorting and filtering
        nb['cells'].append(nbf.v4.new_code_cell(
            """hunt_size = len(df.index)
hunt_size_string = 'Hunt contains ' + str(hunt_size) + ' rows of data.'

display(HTML(hunt_size_string))
display(HTML("<br>"))

col_defs = {'index': {'width': 50}, 'record_id':{'width': 65}}
qgrid.show_grid(df, grid_options={'forceFitColumns': False, 'defaultColumnWidth': 200}, column_definitions=col_defs, show_toolbar=True)""",
            metadata={"init_cell": True, "tags": ["DataFrame", "Hunt Data"]}
        ))

        # Add in our technique specific downselects to put the right tools infront of our analysts
        nb['cells'].append(nbf.v4.new_code_cell(
            """d = Downselects(df.copy())""",
            metadata={"tags": ["InvestigativeActions", "Downselects"]}
        ))

        print("\tWriting downselects...")
        for i in yaml_file['downselects']:
            nb['cells'].append(nbf.v4.new_markdown_cell(f"""## {i.get('title')}"""))
            nb['cells'].append(nbf.v4.new_markdown_cell(f"""{i.get('desc')}"""))

            # Add in more references and decision support specific to the downselect
            if i.get('obsv') and len(i.get('obsv')) > 0:
                observables = str()
                for o in i.get('obsv'):
                    ostring = f'- {o}\n'
                    observables += ostring
                nb['cells'].append(nbf.v4.new_markdown_cell(f"""**Observables:**\n{observables}"""))

            if i.get('ref') and len(i.get('ref')) > 0:
                references = str()
                for r in i.get('ref'):
                    rstring = f'- {r}\n'
                    references += rstring
                nb['cells'].append(nbf.v4.new_markdown_cell(f"""**Reference:**\n{references}"""))

            # Write in the downselect function
            nb['cells'].append(nbf.v4.new_code_cell(f"""display(qgrid({i.get('func')}))""", metadata={
                               "tags": ["InvestigativeActions", "Downselects"]}))

         # *** Write Notebook to file ***
        print("\tWriting: {}.ipynb".format(yaml_file['notebook_name']))
        nbf.write(nb, "{}.ipynb".format(yaml_file['notebook_name']))


if __name__ == "__main__":
    print("Building Notebooks")
    run_builder()
