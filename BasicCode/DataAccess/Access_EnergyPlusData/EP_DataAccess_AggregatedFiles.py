# -*- coding: utf-8 -*-
"""
Created on Tue July 3 16:56:16 2023

@author: sninad kiran ghaikwad
"""

# =============================================================================
# Import Required Modules
# =============================================================================

# External Modules
import os
import pandas as pd
import numpy as np
import pickle
import datetime
import copy

# Custom Modules


# =============================================================================
# User Inputs
# =============================================================================
Simulation_Name = "DOE_SmallOffice_Seattle"

Aggregation_File_Name = 'Aggregation_Dict_1Zone.pickle'

## User Input: Aggregation Unit Number ##
Aggregation_UnitNumber_Total = 1

# Aggregation Zone NameStem Input
Aggregation_Zone_NameStem = 'Aggregation_Zone'

## User Input: User Defined Testing DateTime Range List ##
DataExtraction_Time_Range_List = [('01/25/2013', '01/31/2013'),('02/22/2013', '02/28/2013'),('03/25/2013', '03/31/2013'),('04/24/2013', '04/30/2013'),('05/25/2013', '05/31/2013'),('06/24/2013', '06/30/2013'),('07/25/2013', '07/31/2013'),('08/25/2013', '08/31/2013'),('09/24/2013', '09/30/2013'),('10/25/2013', '10/31/2013'),('11/24/2013', '11/30/2013'),('12/25/2013', '12/31/2013')]

## Extraction File name

Aggregation_DF_Extract_File_Name1 = 'Aggregation_DF_Extract'

## List of all the variables present in each Dataframe per Aggregated Zone
Aggregation_VariableNames_List = ['Schedule_Value_',
                                  'Facility_Total_HVAC_Electric_Demand_Power_',
                                  'Site_Diffuse_Solar_Radiation_Rate_per_Area_',
                                  'Site_Direct_Solar_Radiation_Rate_per_Area_',
                                  'Site_Outdoor_Air_Drybulb_Temperature_',
                                  'Site_Solar_Altitude_Angle_',
                                  'Surface_Inside_Face_Internal_Gains_Radiation_Heat_Gain_Rate_',
                                  'Surface_Inside_Face_Lights_Radiation_Heat_Gain_Rate_',
                                  'Surface_Inside_Face_Solar_Radiation_Heat_Gain_Rate_',
                                  'Surface_Inside_Face_Temperature_',
                                  'Zone_Windows_Total_Transmitted_Solar_Radiation_Rate_',
                                  'Zone_Air_Temperature_',
                                  'Zone_People_Convective_Heating_Rate_',
                                  'Zone_Lights_Convective_Heating_Rate_',
                                  'Zone_Electric_Equipment_Convective_Heating_Rate_',
                                  'Zone_Gas_Equipment_Convective_Heating_Rate_',
                                  'Zone_Other_Equipment_Convective_Heating_Rate_',
                                  'Zone_Hot_Water_Equipment_Convective_Heating_Rate_',
                                  'Zone_Steam_Equipment_Convective_Heating_Rate_',
                                  'Zone_People_Radiant_Heating_Rate_',
                                  'Zone_Lights_Radiant_Heating_Rate_',
                                  'Zone_Electric_Equipment_Radiant_Heating_Rate_',
                                  'Zone_Gas_Equipment_Radiant_Heating_Rate_',
                                  'Zone_Other_Equipment_Radiant_Heating_Rate_',
                                  'Zone_Hot_Water_Equipment_Radiant_Heating_Rate_',
                                  'Zone_Steam_Equipment_Radiant_Heating_Rate_',
                                  'Zone_Lights_Visible_Radiation_Heating_Rate_',
                                  'Zone_Total_Internal_Convective_Heating_Rate_',
                                  'Zone_Total_Internal_Radiant_Heating_Rate_',
                                  'Zone_Total_Internal_Total_Heating_Rate_',
                                  'Zone_Total_Internal_Visible_Radiation_Heating_Rate_',
                                  'Zone_Air_System_Sensible_Cooling_Rate_',
                                  'Zone_Air_System_Sensible_Heating_Rate_',
                                  'System_Node_Temperature_',
                                  'System_Node_Mass_Flow_Rate_']

# LOOP: For Each Aggregated Sub-Zone
Aggregation_DF_Extract_List = []  # Initialization

for ii in range(Aggregation_UnitNumber_Total):

    Aggregation_UnitNumber = ii + 1

    # =============================================================================
    # Creating Result File Names
    # =============================================================================
    
    Aggregation_DF_Extract_File_Name = Aggregation_DF_Extract_File_Name1 + '_' + Aggregation_File_Name.split('.')[0] + '_' + str(Aggregation_UnitNumber) + '.pickle'

    # =============================================================================
    # Getting Required Data from Data Folder
    # =============================================================================

    # Getting Current File Directory Path
    Current_FilePath = os.path.dirname(__file__)

    # Getting desired Simulation Folder Path
    Sim_AggregatedData_FolderPath = os.path.join(Current_FilePath,  '..',  '..', '..', 'Data', 'EnergyPlusData', Simulation_Name)

    ## Loading the Data File ##

    # Getting DF_OutputVariablesFull_DictDF.mat containing all Data and DateTime
    Aggregated_Dict_File = open(os.path.join(Sim_AggregatedData_FolderPath, Aggregation_File_Name), "rb")

    Aggregated_Dict = pickle.load(Aggregated_Dict_File)

    # Getting DateTime List from IDF_OutputVariables_DictDF
    DateTime_List = Aggregated_Dict['DateTime_List']

    # Creating the Correct key based on Aggregation_UnitNumber
    AggregationDf_Key = Aggregation_Zone_NameStem + "_" + str(Aggregation_UnitNumber)

    # Creating Aggregated Zone name 2 : For the Aggregated Equipment
    Aggregated_Equipment_Key = Aggregation_Zone_NameStem + "_Equipment_" + str(Aggregation_UnitNumber)

    # Getting appropriate Aggregation_DF based on AggregationDf_Key
    Aggregation_DF = copy.deepcopy(Aggregated_Dict[AggregationDf_Key])

    # Getting appropriate Aggregation_DF based on AggregationDf_Key
    Aggregation_DF_Equipment = copy.deepcopy(Aggregated_Dict[Aggregated_Equipment_Key])


    # =============================================================================
    # Basic Computation
    # =============================================================================

    Duration = datetime.timedelta(days=1)

    # FOR LOOP: Correcting DateTime_List for 24th Hour Error
    for ii in range(len(DateTime_List)):
        DT = DateTime_List[ii]
        if DT.hour == 0 and DT.minute == 0:
            DT1 = datetime.datetime(DT.year, DT.month, DT.day, 0, 0, 0) + Duration
            DateTime_List[ii] = DT1

    # Getting Start and End Dates for the Dataset
    StartDate_Dataset = DateTime_List[0]
    EndDate_Dataset = DateTime_List[-1]

    # Getting the File Resolution from DateTime_List
    DateTime_Delta = DateTime_List[1] - DateTime_List[0]

    FileResolution_Minutes = DateTime_Delta.seconds/60


    # =============================================================================
    # Adding important computed Variables to the Dataframe
    # =============================================================================

    # Computing GHI
    DNI = np.array(Aggregation_DF['Site_Direct_Solar_Radiation_Rate_per_Area_'])
    Theta = np.array(Aggregation_DF['Site_Solar_Altitude_Angle_'])
    DHI = np.array(Aggregation_DF['Site_Diffuse_Solar_Radiation_Rate_per_Area_'])

    GHI = (DNI * np.abs(np.cos(Theta))) + DHI

    GHI = GHI.tolist()

    Aggregation_DF['GHI'] = GHI

    # Correcting Schedule with Equipment Level
    Schedule_Value_People_Corrected = Aggregation_DF['Schedule_Value_People'] * Aggregation_DF_Equipment['People_Level'].iloc[0]
    Schedule_Value_Lights_Corrected = Aggregation_DF['Schedule_Value_Lights'] * Aggregation_DF_Equipment['Lights_Level'].iloc[0]
    Schedule_Value_ElectricEquipment_Corrected = Aggregation_DF['Schedule_Value_ElectricEquipment'] * Aggregation_DF_Equipment['ElectricEquipment_Level'].iloc[0]

    Aggregation_DF['Schedule_Value_People_Corrected'] = Schedule_Value_People_Corrected
    Aggregation_DF['Schedule_Value_Lights_Corrected'] = Schedule_Value_Lights_Corrected
    Aggregation_DF['Schedule_Value_ElectricEquipment_Corrected'] = Schedule_Value_ElectricEquipment_Corrected

    # Computing HVAC Parameters
    Tz = np.array(Aggregation_DF['Zone_Air_Temperature_'])
    Ts = np.array(Aggregation_DF['System_Node_Temperature_'])
    M_Dot = np.array(Aggregation_DF['System_Node_Mass_Flow_Rate_'])
    Ca = 1.004

    QHVAC_X = Ca * M_Dot * (Ts - Tz)

    QHVAC_X = QHVAC_X.tolist()

    Aggregation_DF['QHVAC_X'] = QHVAC_X

    QHVAC_Y = Aggregation_DF['Zone_Air_System_Sensible_Heating_Rate_'] - Aggregation_DF['Zone_Air_System_Sensible_Cooling_Rate_']

    # QHVAC_Y = Aggregation_DF['Facility_Total_HVAC_Electric_Demand_Power_'] / Aggregation_UnitNumber_Total

    Aggregation_DF['QHVAC_Y'] = QHVAC_Y


    # =============================================================================
    # Separating Aggregation_DF into Test and Train Data
    # =============================================================================

    # Initializing DateRange List
    Extraction_DateRange_Index = []

    # FOR LOOP:
    for DateTime_Tuple in DataExtraction_Time_Range_List:

        # Getting Start and End Date
        StartDate = datetime.datetime.strptime(DateTime_Tuple[0],'%m/%d/%Y')
        EndDate = datetime.datetime.strptime(DateTime_Tuple[1],'%m/%d/%Y')

        # User Dates Corrected
        StartDate_Corrected = datetime.datetime(StartDate.year,StartDate.month,StartDate.day,0,int(FileResolution_Minutes),0)
        EndDate_Corrected = datetime.datetime(EndDate.year,EndDate.month,EndDate.day,23,60-int(FileResolution_Minutes),0)

        Counter_DateTime = -1

        # FOR LOOP:
        for Element in DateTime_List:
            Counter_DateTime = Counter_DateTime + 1

            if (Element >= StartDate_Corrected and Element <= EndDate_Corrected):
                Extraction_DateRange_Index.append(Counter_DateTime)

    # Getting Train and Test Dataset
    Aggregation_DF_Extract = copy.deepcopy(Aggregation_DF.iloc[Extraction_DateRange_Index,:])
    
    # Appending the Aggregation_DF_Extract_List
    Aggregation_DF_Extract_List.append(Aggregation_DF_Extract)

    

# =============================================================================
# Storing Aggregated Extracted Data in a Pickle File
# =============================================================================

# Saving Aggregated TrainingTesting_Dict as a .pickle File in Results Folder
pickle.dump(Aggregation_DF_Extract_List, open(os.path.join(Current_FilePath, Aggregation_DF_Extract_File_Name1), "wb"))