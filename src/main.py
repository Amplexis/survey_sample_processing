import codecs
import pandas as pd
from datetime import datetime
import os

def insert_into_access_and_answers(project, identifier, survey, subgroup, batch, master_string):
    string = (
        "INSERT INTO {0}.Access (identifier, survey, subgroup, batch_number)\n"
        "   VALUES ('{1}', '{2}', '{3}', '{4}');\n"
        "INSERT INTO {0}.Answers (identifier, batch_number)\n"
        "   VALUES ('{1}', '{4}');\n\n"
    ).format(project, identifier, survey, subgroup, batch)

    master_string = master_string + string
    return master_string

# Project name
PROJECT_NAME = "marad"

now = datetime.now()
BATCH = now.strftime("%y%m%d")

infile = "example_input_sample_file.xlsx"
outfile = "sample_" + BATCH + ".sql"

# Establish file structure
base_dir = os.path.dirname(os.path.dirname(__file__))
filepath_out = os.path.join(base_dir, "output/", outfile)

master_string = "USE {};\n\n".format(PROJECT_NAME)


with pd.ExcelFile((infile)) as xlsx:
    sample = pd.read_excel(xlsx)

    for i in sample.index:
        id = (sample["id"][i])
        survey = (sample["survey"][i])
        subgroup = (sample["subgroup"][i])
        master_string = insert_into_access_and_answers(PROJECT_NAME, id, survey, subgroup, BATCH, master_string)


with codecs.open((filepath_out), 'w', 'utf8') as sqlfile:
    sqlfile.write(master_string)
