%% Main File - Basic Script to access PecanStreet Data

% Author: Ninad Kiran Gaikwad
% Date: July/3/2023
% Description: Basic Script to access Pecan Street Data

% There are 75 data columns in Pecan StreetData Files they may or may not
% be filled up for a given house
% The first four columns are Day-Month-Year-Time(Decimal 24hrs)

% Clearing Workspace
clear all;
clc;
close all;

% Adding relevant paths for accessing functionality
addpath('Utils')

%% Inputs

% File resolution in minutes
FileRes = 10; % Currently only 10min resolution is available in the database

% Region Name
Region_Name = 'austin'; % austin , newyork, california

% House Number
House_Number = 1; % austin: 1-25 , newyor: 1-25 , california: 1-23

% Start Date
StartMonth=1;      % User Defined
StartDay=1;         % User Defined
StartTime=0;        % User Defined

% End Date
EndMonth=12;        % User Defined
EndDay=30;          % User Defined
EndTime=24-(FileRes/60);%24-(FileRes/60); 

% Folder Path upto Data folder in the repo
Data_FolderPath = 'C:\Users\ninad\Dropbox (Personal)\NinadGaikwad_PhD\Gaikwad_Research\Gaikwad_Research_Work\NSF_CPS_BuildingsControl\Data';

% MAT File Name to be saved
Save_FileName = 'Austin_House1.mat';

Save_FileName_Priority = 'Austin_House1_Prioritized.mat';

%% Processing Pecan Street Data based on user input

% Creating PecanStreet file path
PecanStreet_Data_FilePath = strcat(Data_FolderPath,'\PecanStreetData','\10minute_data_',Region_Name,'_HouseWise','\House_',num2str(House_Number),'_15minTo_10min.csv');

% Creating Struct for Time Period
TimePeriod = [];

TimePeriod.StartMonth=StartMonth;
TimePeriod.StartDay=StartDay;
TimePeriod.StartTime=StartTime;
TimePeriod.EndMonth=EndMonth;
TimePeriod.EndDay=EndDay;
TimePeriod.EndTime=EndTime;

% Calling external function to get desired PecanStreet Data
[PecanStreet_Data_Output] = PecanStreet_Data_Extractor(TimePeriod,FileRes,PecanStreet_Data_FilePath,Save_FileName);

%% Converting 75 Energy Usage columns to 8 categories of priorities

% This priority list can be changed from within PecanStreet_Data_Extractor

% Getting Renewable Source Data
SolarGen_Data=PecanStreet_Data_Output(:,4+1:6);

Battery_ChargerDischarge_Data=PecanStreet_Data_Output(:,7);

EVCharging_Data=PecanStreet_Data_Output(:,7+1:9);

E_LoadData=PecanStreet_Data_Output(:,:);

% Making Negatives (-) = 0 in LoadData
E_LoadData(E_LoadData(:,9+1:end)<0)=0;

% Creating 8 Level Priority Load Data

% Level 1 Priority - Fridge, Freezer, Kitchen
E_Load_P1=sum(E_LoadData(:,9+1:9+12),2); % Priority Level1 Sum 

% Level 2 Priority - Bedrooms
E_Load_P2=sum(E_LoadData(:,21+1:21+5),2); % Priority Level2 Sum

% Level 3 Priority - Living Rooms, Office Room
E_Load_P3=sum(E_LoadData(:,26+1:26+3),2); % Priority Level3 Sum

% % Level 4 Priority Clothes, Garbage Disposal, P{umps
E_Load_P4=sum(E_LoadData(:,29+1:29+7),2); % Priority Level4 Sum

% Level 5 Priority - Security, Bathrooms, Dinning Room, Dishwasher
E_Load_P5=sum(E_LoadData(:,36+1:36+6),2); % Priority Level5 Sum

% Level 6 Priority - Remaining Rooms, Outside Lights
E_Load_P6=sum(E_LoadData(:,42+1:42+6),2); % Priority Level6 Sum

% Level 7 Priority - Aquarium, Lawn Sprinklers, Wine Cooler
E_Load_P7=sum(E_LoadData(:,48+1:48+3),2); % Priority Level7 Sum

% Level 8 Priority - Pool, Jacuzzi, Water Heater 
E_Load_P8=sum(E_LoadData(:,51+1:51+6),2); % Priority Level8 Sum

E_LoadData=[E_LoadData(:,1:9)...
            E_Load_P1 E_Load_P2 E_Load_P3 E_Load_P4...
            E_Load_P5 E_Load_P6 E_Load_P7 E_Load_P8];
        
% Saving Prioritized Load
save(Save_FileName_Priority,'E_LoadData')

