setwd("C:/Users/FRANCOS/Documents/Modeling")
#install.packages("readr")
#install.packages("ggplot2")
#install.packages("dplyr")
#install.packages("stargazer")
#install.packages("readxl", "formattable")
#install.packages('scales')
#install.packages("xtable")
library(readr)
library(ggplot2)
library(readxl)
library(stargazer)
library(dplyr)
library(scales)
library(xtable)

#import dataset
Operational_Data_2021 <- read_excel("Operational_Data_2021.xlsx", 
                                                            skip = 2)

EIA923_Schedules <- read_excel("EIA923_Schedules_2_3_4_5_M_12_2021_Final_Revision.xlsx", 
                                                               skip = 5)

EIA923_Schedules <- read_excel("EIA923_Schedules_6_7_NU_SourceNDisposition_2021_Final_Revision.xlsx", 
                                                                             skip = 4)
