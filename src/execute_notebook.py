import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import time

notebook_path = "d:/Data Analysis project/IPL-Data-Analysis/notebooks/IPL_Analysis.ipynb"

print(f"Loading notebook: {notebook_path}...")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

print("Initializing ExecutePreprocessor...")
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

start_time = time.time()
print("Executing all cells in the notebook... This will run data cleaning, generate insights, and save plots to the 'images/' folder. Please wait, as processing 283k rows takes a few moments...")

try:
    ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})
    print(f"Execution completed successfully in {time.time() - start_time:.2f} seconds!")
except Exception as e:
    print(f"Error during notebook execution: {e}")
    raise e

print(f"Saving the executed notebook back to: {notebook_path}...")
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook execution and saving completed!")
