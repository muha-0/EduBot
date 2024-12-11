import os.path

import numpy as np
import pandas as pd
import joblib


class MlModel:
    """

    **Machine Learning model used for score prediction**

    """

    def __init__(self) -> None:
        self.model = None
        
        try:
            cur_file_dir = os.path.dirname(os.path.abspath(__file__))
            self.model = joblib.load(f'{cur_file_dir}/Stacking_Regressor')

        except Exception as e:
            print("Exception while loading ML model: ", e, "\n")
            
    
    def predict(self, attributes):
        """**Predict takes the user's attributes and makes a prediction**
        The order of the features and names is as follows:
            
            * StudyTimeWeekly  
            * Absences  
            * Tutoring  
            * Extracurricular  
            * Sports  

        # Args:
            * **attributes** (*pandas dataframe*): user attributes, make it into the format above in a pandas dataframe
        """
        values = []
        for attribute, value in attributes.items():
            values.append(value)
        
        values = [values]
        
        values = np.array(values).reshape(1, -1)
        
        
        try:
            prediction = self.model.predict(values)
            
            if prediction * 25 > 100:
                prediction = 4
                prediction *= 25
                
            else:
                prediction *= 25
            
        except Exception as e:
            print("Error while making a prediction in predict() method in mlmodel module: ", e, '\n')
            prediction = "You were not able to make a prediction, apologize for this"
            
        return prediction

    def optimize(self, dataset):
        """**Optimize makes the model retrain to optimize on new data and saves the new version**  
        The order of the features and names is as follows:
            
            * StudyTimeWeekly  
            * Absences  
            * Tutoring  
            * Extracurricular  
            * Sports  
            * GradeClass  
            
        # Arguments:
            * **dataset** (*pandas dataframe*): user attributes, make it into the format above in a pandas dataframe
        """
        # Split the data into features and labels
        x, y = dataset[dataset.columns[:-1]], dataset['GradeClass']

        # Get categorical columns
        categorical = dataset.select_dtypes(include='object')


        # Fit the model
        self.model.fit(x, y)

        # Save the new, optimized model
        try:
            cur_file_dir = os.path.dirname(os.path.abspath(__file__))
            joblib.dump(self.model, f'{cur_file_dir}/Stacking_Regressor')

        except Exception as e:
            print("Exception while saving a newly trained model: ", e, "\n")


if __name__ == '__main__':
    '''The order of the features and names is as follows:
            
            * StudyTimeWeekly  
            * Absences  
            * Tutoring  
            * Extracurricular  
            * Sports  
            * GradeClass
            '''
    model = MlModel()

    vals = {
        "StudyTimeWeekly": 20,
        "Absences": 7,
        "Tutoring": 1,
        "Extracurricular": 1,
        "Sports": 1, 
    }



    print(model.predict(vals))
