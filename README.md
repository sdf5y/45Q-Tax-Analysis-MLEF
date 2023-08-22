# 45Q-Tax-Analysis-MLEF
Summer 2023 MLEF Scripts to Analyze the Operational Costs from the 45Q Carbon Sequestration Tax credits
    Wage Effects on 45Q Tax Credit Participation:
        The Carbon Oxide Sequestration (i.e., Section 45Q) tax credit offers a per-unit tax credit to companies including electric generating units (EGUs) that build and operate projects to capture and then either utilize or store (i.e., sequester) carbon dioxide (CO2).  For eligible EGUs who meet the prevailing wage and apprenticeship (PWA) requirements established by the Inflation Reduction Act (IRA) a 5x multiplier is applied to the base rate of the tax credit. PWA requirements stipulate the wages that laborers, mechanics, contractors, and sub-contractors must be paid, and the percentage of total labor hours for construction, alteration, or repair work that must be performed by a qualified apprentice. The PWA requirements could influence the economics of an EGU’s decision to implement carbon capture technologies. To explore how so, scenario and other analysis were performed using data from NETL’s Baseline Studies for Fossil Energy Plants, which provide estimates for the cost and performance of combustion- and gasification-based EGUs. We use these data to build a framework that permits assessments of how the operating costs of 45Q eligible EGUs could be influenced by the IRA’s PWA requirements. In other words, how meeting or not meeting PWQ requirements could impact an EGU’s decision to implement carbon capture technologies. 
    Getting Started:
        In your python environment, make sure to install the libraries as stated in the preamble of the python scripts, and make sure to load the NETL Bituminous baseline report (as linked in the scripts for data collection).
    Usage:
        datacollect.py is a script to collect the data from the Bituminous baseline report, and simplecostmodel.py performs the simulation of firm operating costs. These estimation of firm operating costs are "back of the envelope" calculations and should be viewed as such.
        License:
    Creative Commons Zero v1.0 Universal
    Author:
        Sean Franco, and Dr.Harker Steele for conducting this inquiry.
    Acknowledgments:
        Much gratitude is for the MLEF, DOE/NETL, and ORISE organizations and Dr.Harker Steele for supporting this summer research project. 
