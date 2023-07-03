function [PecanStreet_Data_Output] = PecanStreet_Data_Extractor(TimePeriod,FileRes,PecanStreet_Data_FilePath,Data_MatFile_Name)

%% Pecan Street Data Extraction : Converting Many Files to 1

% Author: Ninad Kiran Gaikwad
% Date: July/3/2023
% Description: Pecan Street Data Extractor

%% Getting Required data from HEMSWeatherData_Input - Struct

%---------------------- HEMSWeatherData_Input ----------------------------%
StartMonth=TimePeriod.StartMonth;
StartDay=TimePeriod.StartDay;
StartTime=TimePeriod.StartTime;
EndMonth=TimePeriod.EndMonth;
EndDay=TimePeriod.EndDay;
EndTime=TimePeriod.EndTime;

%% Getting All files which have the required DateTime Range

% Read CSV File
Single_DataFile_Matrix=csvread(PecanStreet_Data_FilePath);

% Getting StartYear and EndYear
StartYear=Single_DataFile_Matrix(1,3);
EndYear=StartYear;

% Creating a DateTimeMatrix_ForSlicer
DateTimeMatrixAggregate_ForSlicer=horzcat(Single_DataFile_Matrix(:,1:4),zeros(length(Single_DataFile_Matrix(:,1)),1));

% Computing required Start and End Indices
[ OriginalSeries,StartIndex_Aggregate,EndIndex_Aggregate ] = DateTimeSeriesSlicer_PecanStreetData(DateTimeMatrixAggregate_ForSlicer,1,FileRes,StartYear,EndYear,StartMonth,EndMonth,StartDay,EndDay,StartTime,EndTime);

% Checking if desired Dates were presentin the current file
if (isstring(OriginalSeries)) % Desired Dates not present in the current file

    % Nothing Happens - We skip over the current file
    warning('Desired Dates not found in files')

else % Desired Dates present in the current file

    % Getting the Data for the desired dates
    Data=Single_DataFile_Matrix(StartIndex_Aggregate:EndIndex_Aggregate,:);

    % Storing the Files with correct dates along with DateTime
    AllFiles_CorrectDates_Data_Matrix=Data;

    PecanStreet_Data_Output=[AllFiles_CorrectDates_Data_Matrix(:,1:4)... % Date-Time
                                            AllFiles_CorrectDates_Data_Matrix(:,66+4:67+4) AllFiles_CorrectDates_Data_Matrix(:,13+4) AllFiles_CorrectDates_Data_Matrix(:,14+4:15+4)... % Solar PV, Battery, EV
                                            AllFiles_CorrectDates_Data_Matrix(:,61+4:62+4) AllFiles_CorrectDates_Data_Matrix(:,25+4) AllFiles_CorrectDates_Data_Matrix(:,39+4) AllFiles_CorrectDates_Data_Matrix(:,37+4) AllFiles_CorrectDates_Data_Matrix(:,40+4) AllFiles_CorrectDates_Data_Matrix(:,38+4) AllFiles_CorrectDates_Data_Matrix(:,60+4) AllFiles_CorrectDates_Data_Matrix(:,71+4) AllFiles_CorrectDates_Data_Matrix(:,49+4) AllFiles_CorrectDates_Data_Matrix(:,53+4:54+4) ... Level 1 Priority - Fridge, Freezer, Kitchen
                                            AllFiles_CorrectDates_Data_Matrix(:,8+4:12+4)... % Level 2 Priority - Bedrooms
                                            AllFiles_CorrectDates_Data_Matrix(:,47+4:48+4) AllFiles_CorrectDates_Data_Matrix(:,50+4) ... % Level 3 Priority - Living Rooms, Office Room
                                            AllFiles_CorrectDates_Data_Matrix(:,17+4) AllFiles_CorrectDates_Data_Matrix(:,23+4) AllFiles_CorrectDates_Data_Matrix(:,64+4) AllFiles_CorrectDates_Data_Matrix(:,22+4) AllFiles_CorrectDates_Data_Matrix(:,59+4) AllFiles_CorrectDates_Data_Matrix(:,69+4) AllFiles_CorrectDates_Data_Matrix(:,74+4) ... % Level 4 Priority Clothes, Garbage Disposal, P{umps
                                            AllFiles_CorrectDates_Data_Matrix(:,63+4) AllFiles_CorrectDates_Data_Matrix(:,6+4:7+4) AllFiles_CorrectDates_Data_Matrix(:,19+4:21+4) ... % Level 5 Priority - Security, Bathrooms, Dinning Room, Dishwasher
                                            AllFiles_CorrectDates_Data_Matrix(:,28+4:29+4) AllFiles_CorrectDates_Data_Matrix(:,70+4) AllFiles_CorrectDates_Data_Matrix(:,65+4) AllFiles_CorrectDates_Data_Matrix(:,51+4:52+4) ... % Level 6 Priority - Remaining Rooms, Outside Lights
                                            AllFiles_CorrectDates_Data_Matrix(:,5+4) AllFiles_CorrectDates_Data_Matrix(:,68+4) AllFiles_CorrectDates_Data_Matrix(:,75+4) ... % Level 7 Priority - Aquarium, Lawn Sprinklers, Wine Cooler
                                            AllFiles_CorrectDates_Data_Matrix(:,35+4) AllFiles_CorrectDates_Data_Matrix(:,58+4) AllFiles_CorrectDates_Data_Matrix(:,57+4) AllFiles_CorrectDates_Data_Matrix(:,36+4) AllFiles_CorrectDates_Data_Matrix(:,72+4:73+4)]; % Level 8 Priority - Pool, Jacuzzi, Water Heater

    %% Saving PecanStreet_Data_Output as .mat File

    save(Data_MatFile_Name,'PecanStreet_Data_Output');  

end     

end

