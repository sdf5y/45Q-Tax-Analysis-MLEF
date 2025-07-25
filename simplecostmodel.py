import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

cost_df = pd.read_excel('CostReport_copypaste.xlsx', sheet_name = 1)

#amount of electricity generated MWh per year
def Annual_EG(capacity, cap_factor):
  gen_MWh = capacity * cap_factor * 8760
  return gen_MWh

cost_df["Elecricity MWh/year"] = Annual_EG(cost_df['Plant Size (net MW)'], cost_df['Capacity factor'])

#enter in individual number for Shift hours (ex: 12)
def Labor_costs(S_Op, Op, Foreman, Lab_Tech, shift_hours,
                S_Op_wages, Op_wages, Foreman_wages, Lab_Tech_wages,capacity):
  if shift_hours == 12:
    daily_cost = (2*(S_Op* S_Op_wages) + 2*(Op * Op_wages) + 2*(Foreman * Foreman_wages) + 2*(Lab_Tech * Lab_Tech_wages)) * 2*shift_hours
    yearly_cost = daily_cost * 365

  elif shift_hours == 24:
    daily_cost = (2*(S_Op* S_Op_wages) + 2*(Op * Op_wages) + 2*(Foreman * Foreman_wages) + 2*(Lab_Tech * Lab_Tech_wages)) *shift_hours
    yearly_cost = daily_cost * 365

  adj_yearly_cost = yearly_cost * (capacity/100)

  return adj_yearly_cost

labor = pd.DataFrame()
labor = Labor_costs(cost_df['Skilled Operator'], cost_df['Operator'], cost_df['Foreman'], cost_df['Lab Techs'], 12,
                    cost_df['SO Wage ($)'], cost_df['OP Wage ($)'], cost_df['For Wage ($)'], cost_df['LT Wage ($)'], cost_df['Capacity factor'])

cost_df['Annual Labor Costs'] = labor

#Removed labor from FC
FixedCost = (cost_df.loc[:,"Fixed Operating Costs"] -
 (cost_df.loc[:,"Annual Operating Labor"] +
  cost_df.loc[:,"Maintenance Labor"] +
  cost_df.loc[:,"Administrative & Support Labor"]))

LaborCost = (cost_df['Annual Labor Costs'] +
             cost_df.loc[:,"Maintenance Labor"] +
             cost_df.loc[:,"Administrative & Support Labor"])

VariableCost = (cost_df.loc[:,"Variable Operating Costs"] +
                cost_df.loc[:,"Total Fuel Cost"])

inflation_rate = 0.0293 #from 2018 to 2023 from BLS
names = cost_df.iloc[:,0].astype(str).str[:6]

names = []
for i in range(0, len(cost_df['Name'])):
  test = cost_df['Name']
  jk = test[i].split('–', 1)[0].strip(" ")
  jk = jk.split(' ', 1)[0].strip(" ")
  names.append(jk)

sim_cost_df = pd.DataFrame()

sim_cost_df = pd.DataFrame([names, FixedCost, LaborCost, VariableCost, cost_df["Elecricity MWh/year"]]).T

sim_cost_df = sim_cost_df.set_axis(["Name", "FC", "LC", "VC", "Elecricity MWh/year"], axis=1)

def include_inflation(var, inflation_rate):
  new_var = var * (1+inflation_rate)
  return new_var

def calculate_cost(r, KC, LC, FC):

    VC_all = (r * KC) + KC + LC
    TC = VC_all + FC
    return TC

TC_cost = calculate_cost(cost_df['Capital Depreciation'], sim_cost_df["VC"], sim_cost_df["LC"], sim_cost_df["FC"])
#TC_cost = include_inflation(TC_cost, 0.0293)

cost_df['Sim TC'] = TC_cost

def iterate_ratios(numerator_df, divisor_df):
  for i in range(0, len(sim_cost_df)):
    if i == 0:
      ratio_list = []
    X = divisor_df[i]
    Y = numerator_df[i]
    ratio_list.append(Y / X)
  return ratio_list

labor_ratios =  iterate_ratios(sim_cost_df['LC'], sim_cost_df['Elecricity MWh/year'])
capital_ratios =  iterate_ratios(sim_cost_df['VC'], sim_cost_df['Elecricity MWh/year'])

sim_ratio_df = pd.DataFrame()
sim_ratio_df = pd.DataFrame(zip(names, capital_ratios, labor_ratios), columns=['Names', 'Capital_ratio', 'Labor_ratio'])

sim_cost_df_sorted = sim_cost_df.sort_values("Elecricity MWh/year")

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle('Annual Firm Costs and Electrical Production')
ax1.bar(names, TC_cost)
ax1.tick_params(axis='y', labelrotation = 0)
ax1.set_ylabel('hundred Mil ($)')
#ax1.grid()

ax2.bar(names, sim_cost_df_sorted['Elecricity MWh/year'])
ax2.tick_params(axis='x', labelrotation = 75)
ax2.set_ylabel('Electricity MWh/yr')
#ax2.grid()
fig.show()
fig.savefig('Prod_Costs.png')

sim_ratio_df_sorted = sim_ratio_df.sort_values("Capital_ratio")

plt.scatter(sim_ratio_df_sorted['Names'], sim_ratio_df_sorted['Capital_ratio'], label = "K")
plt.scatter(sim_ratio_df_sorted['Names'], sim_ratio_df_sorted['Labor_ratio'], label = 'L')
plt.xticks(rotation=75)
plt.legend()
plt.title("Capital and Labor Cost Ratios")
plt.xlabel("Firms")
plt.ylabel("Ratio")
#plt.grid()
plt.show()
plt.savefig('K_L_ratios.png')

from google.colab import data_table
data_table.enable_dataframe_formatter()

sim_ratio_df

#include 45Q tax Credit
#include column for captured emissions, the price/tonne of carbon, if there is no multiplier label as 1

def include45Q(captured_emissions, TC, pricepertonne, multiplier):
  profit_l = []
  profit = []
  fort_Q = captured_emissions * pricepertonne * multiplier
  new_TC = TC - (fort_Q)
  for i in range(0, len(new_TC)):
    cell = new_TC[i]
    if cell > 0:
      profit.append(cell)
    elif cell < 0:
      #cell = cell*-1
      profit.append(cell)
  return profit

cost_df['TC_17_45Q'] = include45Q(cost_df['Carbon Capture (tonne/year)'], TC_cost, 17, 1)
cost_df['TC_12_45Q'] = include45Q(cost_df['Carbon Capture (tonne/year)'], TC_cost, 12, 1)
cost_df['TC_85_45Q'] = include45Q(cost_df['Carbon Capture (tonne/year)'], TC_cost, 17, 5)
cost_df['TC_60_45Q'] = include45Q(cost_df['Carbon Capture (tonne/year)'], TC_cost, 12, 5)

cost_df.iloc[:,31:35] =  include_inflation(cost_df.iloc[:,31:35], 0.293)

def socialcostcarbon(Total_em, Cap_em, SCC):
  #residual_em = Total_em - Cap_em
  res_cost = SCC * Total_em
  return res_cost

cost_df['Residual SCC'] = socialcostcarbon(cost_df['Carbon Emissions (tonne/year)'], cost_df['Carbon Capture (tonne/year)'], 51)

from google.colab.data_table import DataTable
DataTable.max_columns = 48
cost_df
