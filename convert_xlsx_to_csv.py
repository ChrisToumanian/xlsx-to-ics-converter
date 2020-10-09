#!/usr/bin/python3

import sys
import pandas as pd

print("test!")
filename = sys.argv[1]
csv_filename = filename.split(".")[0] + ".csv"
read_file = pd.read_excel(filename)
read_file.to_csv(csv_filename, index = None, header=True)
print("done")
