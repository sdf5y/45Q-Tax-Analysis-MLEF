#%pip install tabula-py
#%pip install PyMuPDF
#%pip install PyPDF2
import pandas as pd
from pandas.core.missing import clean_interp_method
import numpy as np
import tabula
import fitz
import re
import PyPDF2

def search_pdf_list(pdf_name, Keyword):
  object  = PyPDF2.PdfReader(pdf_name)
  NumPages = len(object.pages)
  String = Keyword
  page_num = []

  # Extract text and do the search
  for i in range(0, NumPages):
      PageObj = object.pages[i]
      Text = PageObj.extract_text()
      if re.search(String,Text):
        print("Pattern Found on Page: " + str(i+1))
        num = ", " + str(i)
        page_num.append(num)

  page_num_cleaned = [num.replace(", ", "") for num in page_num]
  page_num_cleaned = [int(x) for x in page_num_cleaned]
  page_num_cleaned[:]=[x+1 for x in page_num_cleaned]

  return page_num_cleaned

page_num_cleaned = search_pdf_list("CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf", "B11B.99 air emissions")

#Run this to remove queries from table of content
#Verify table of content page number in if statement
def removeTOC (df, end_pg_TOC):
  i = 0
  cell = []
  new_page_num_cleaned = []

  for i in range(0, len(df)):
    cell = df[i]
    if cell >= end_pg_TOC:
      new_page_num_cleaned.append(cell)
  return new_page_num_cleaned

#PDF_HTML needs quotes and an htmp for the pdf.
#Page_list needs to be a list
def Get_page_data (PDF_HTML, Page_list):
  pdf_path = PDF_HTML
  list_df = []
  for i in range(0, len(Page_list)):
    list_df += (tabula.read_pdf(pdf_path, pages = Page_list[i], stream=True))
  return list_df

new_page_num_cleaned = removeTOC(page_num_cleaned, 28)
dfs = (Get_page_data("https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf", new_page_num_cleaned))

def convert_column_table(enter_table, num_output_cols):
    #original table col numbers
    num_columns = len(enter_table.columns)

    #Concatenate the columns
    if num_columns > num_output_cols:
        # Extract the column headers
        headers = enter_table.columns[:26]
        data = enter_table.iloc[:, num_output_cols:]

        # Reshape the data into 5 columns
        merged_data = data.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=(num_output_cols-1))

        # Create table with headers and data
        new_table = pd.DataFrame({headers[0]: merged_data, headers[1]: None})

    # No conversion
    else:
        new_table = enter_table.copy()

    return new_table

#run this individually, with each index
from google.colab import data_table
data_table.enable_dataframe_formatter()

convert_column_table(dfs[0],5) #done

#All Together:
page_num_cleaned = search_pdf_list("CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf",
                                   "initial and annual operating and maintenance costs")

new_page_num_cleaned = removeTOC(page_num_cleaned, 28)

dfs = (Get_page_data("https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf",
                     new_page_num_cleaned))

from google.colab import data_table
data_table.enable_dataframe_formatter()

convert_column_table(dfs[1],5) #done

convert_column_table(dfs[21],5) #done

converted_table.to_excel('CostReport.xlsx', sheet_name = 'New_sheet')
