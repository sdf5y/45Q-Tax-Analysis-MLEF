setwd("")
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
CostReport_copypaste <- read_excel("CostReport_copypaste.xlsx", 
                                   sheet = "Firm Attributes")

#Firm size and production attributes ----
firm_type_df <- CostReport_copypaste[c(1:4, 11:14, 25)]

firm_type_df$Name <- gsub("\\ .*", "", firm_type_df$Name)

firm_type_df <- firm_type_df %>% 
  arrange(firm_type_df$`Fuel Type`)

firm_type_df$`Carbon Capture` <- ifelse(is.na(firm_type_df$`Carbon Capture`) == TRUE, "No", "Yes")

#end result
stargazer(firm_type_df, summary = FALSE)

#Firm Costs----

firm_final_cost_df <- CostReport_copypaste[c(1, 5, 9, 30:35)]

firm_final_cost_df$Name <- gsub("\\ .*", "", firm_final_cost_df$Name)

firm_final_cost_df$`Carbon Capture` <- ifelse(is.na(firm_final_cost_df$`Carbon Capture`) == TRUE, "No", "Yes")

colnames(firm_final_cost_df)[7:10] <- c("$17/t Baserate", "$12/t Baserate", "$85/t PWA", "$60/t PWA")

firm_final_cost_df[-c(1,4)] <- firm_final_cost_df[-c(1,4)]*1.0293

#end result
stargazer(firm_final_cost_df, summary = FALSE, digits = 0)

firm_final_cost_df %>% 
  xtable(digits=0) %>% 
  print(include.rownames=FALSE, 
        format.args=list(big.mark=","))

#Plotting Prep -----

cbPalette <- c("skyblue", "orange", "green","black")

options(scipen=100)

firm_final_cost_df <- CostReport_copypaste[c(1, 5, 9, 11, 30:35)]

firm_final_cost_df$Name <- gsub("\\ .*", "", firm_final_cost_df$Name)

#PLotting All Firms in 45Q----

long_df <- data.frame(rep(firm_final_cost_df$Name, 8), 
                      unlist(c(firm_final_cost_df[7], firm_final_cost_df[8], 
                               firm_final_cost_df[9], firm_final_cost_df[10],
                               firm_final_cost_df[6], firm_final_cost_df[6],
                               firm_final_cost_df[6], firm_final_cost_df[6]), use.names = FALSE),
                      rep(c(rep("Operating Costs", 88), rep("SCC", 88))), 
                      c(rep("$17/t Scenario", 22), rep("$12/t Scenario", 22), 
                        rep("$85/t Scenario", 22), rep("$60/t Scenario", 22))) 

colnames(long_df) <- c("Name", "Value", "Condition", "Group")

ggplot(data = long_df,
       aes(x = reorder(Name, Value),
           y = Value,
           fill = `Condition`)) +
  geom_histogram(stat = "identity", position = 'stack') + 
  theme(axis.text.x=element_text(angle=55, size = 9, hjust = 1))+
  labs(title = "Total Costs after 45Q Scenarios and SCC ($51/t)",
       x = "Firm", 
       y = "Dollars $ Mil",
       fill = "Costs")+
  scale_y_continuous(labels = unit_format(unit = "$ Mil", scale = 1e-6))+
  facet_wrap(~`Group`) +
  scale_fill_manual(values=cbPalette)

#Plotting CC Firms----

firm_final_cost_df <- subset(firm_final_cost_df, `Carbon Capture` == '1')

long_df <- data.frame(rep(firm_final_cost_df$Name, 8), 
                      unlist(c(firm_final_cost_df[7], firm_final_cost_df[8], 
                               firm_final_cost_df[9], firm_final_cost_df[10],
                               firm_final_cost_df[6], firm_final_cost_df[6],
                               firm_final_cost_df[6], firm_final_cost_df[6]), use.names = FALSE),
                      rep(c(rep("Operating Costs", 60), rep("SCC", 60))), 
                      c(rep("$17/t Scenario", 15), rep("$12/t Scenario", 15), 
                        rep("$85/t Scenario", 15), rep("$60/t Scenario", 15))) 

colnames(long_df) <- c("Name", "Value", "Condition", "Group")

ggplot(data = long_df,
       aes(x = reorder(Name, Value),
           y = Value,
           fill = `Condition`)) +
  geom_histogram(stat = "identity", position = 'stack') + 
  theme(axis.text.x=element_text(angle=55, size = 9, hjust = 1))+
  labs(title = "Total Costs after 45Q Scenarios and SCC ($51/t)",
       x = "Firm", 
       y = "Dollars $ Mil",
       fill = "Costs")+
  scale_y_continuous(labels = unit_format(unit = "$ Mil", scale = 1e-6))+
  facet_wrap(~`Group`) +
  scale_fill_manual(values=cbPalette)
