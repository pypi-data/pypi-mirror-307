import pandas as pd

# the path of the orignal file 
original_flight_data = r'C:\Users\taiya\anaconda3\envs\SOAR\Lib\site-packages\MAPLEAF\Examples\Simulations\zack1_Run28\FirstStage_derivativeEvaluationLog.csv'

# set the same folder in which it was ran in                                                   NOTE ensure paths are correct
final_destination = r'C:\Users\taiya\anaconda3\envs\SOAR\Lib\site-packages\MAPLEAF\Examples\Simulations\zack1_Run28\filtered_FirstStage_derivativeEvaluationLog.csv'
second_destination = r'C:\Users\taiya\anaconda3\envs\SOAR\Lib\site-packages\MAPLEAF\Examples\Simulations\zack1_Run28\maximasofdarocket.csv'

# read the dataset (ds) 
ds = pd.read_csv(original_flight_data)

# Filter columns containing "(N)" or "(Nm)"
filtered_columns = [col for col in ds.columns if "(N)" in col or "(Nm)" in col]


# Create a new DataFrame with only the filtered columns
filtered_ds = ds[filtered_columns]

#combine abs of maxes and mins and find the max between both and add it to the list 
maxes = abs(filtered_ds.max()).combine(abs(filtered_ds.min()),max)

totalforce = []

for i in range(0,len(maxes),3):
    tv = ((maxes[i]**2)+(maxes[i+1]**2)+(maxes[i+2]**2))**(1/2)
    totalforce.append("")
    totalforce.append("")
    totalforce.append(tv)

#print(totalforce)


#create a dataset of maxes list
maxima = pd.DataFrame({"part X,Y,Z" : filtered_columns, "Forces & Moments" : maxes, "Magnitude Vectors of Forces and Moments" : totalforce})

# save the maximas to a csv file in second destiantion
maxima.to_csv(second_destination,index=False)

# save the filtered Dataset to the same run folder
filtered_ds.to_csv(final_destination, index=False) #since i want time as my index i put index to false


print(f"Filtered data saved to {final_destination}")