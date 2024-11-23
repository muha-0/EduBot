import os.path

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from imblearn.over_sampling import RandomOverSampler


class MlModel:
    """**Machine Learning model used for score prediction**
    
    """

    def __init__(self) -> None:
        self.cat = CatBoostClassifier()

        try:
            cur_file_dir = os.path.dirname(os.path.abspath(__file__))
            self.cat.load_model(f'{cur_file_dir}/catboost_ml_model')

        except Exception as e:
            print("Exception while loading ML model: ", e, "\n")

    def predict(self, attributes):
        """**Predict takes the user's attributes and makes a prediction**
        The order of the features and names is as follows:
            
            * 'Hours_Studied'
            
            * 'Attendance'
            
            * 'Access_to_Resources'
            
            * 'Extracurricular_Activities'
            
            * 'Sleep_Hours'
            
            * 'Previous_Scores'
            
            * 'Motivation_Level'
            
            * 'Teacher_Quality'
            
            * 'School_Type'
            
            * 'Peer_Influence'
            
            * 'Physical_Activity'
            
            * 'Learning_Disabilities'
            
            * 'Distance_from_Home'

        # Args:
            * **attributes** (*pandas dataframe*): user attributes, make it into the format above in a pandas dataframe
        """

        attributes = np.array(attributes).reshape(1, -1)
        return self.cat.predict(attributes)

    def optimize(self, dataset):
        """**Optimize makes the model retrain to optimize on new data and saves the new version**  
        The order of the features and names is as follows:
            
            * 'Hours_Studied'
            
            * 'Attendance'
            
            * 'Access_to_Resources'
            
            * 'Extracurricular_Activities'
            
            * 'Sleep_Hours'
            
            * 'Previous_Scores'
            
            * 'Motivation_Level'
            
            * 'Teacher_Quality'
            
            * 'School_Type'
            
            * 'Peer_Influence'
            
            * 'Physical_Activity'
            
            * 'Learning_Disabilities'
            
            * 'Distance_from_Home'
            
            * 'Exam_Score'
            
        # Arguments:
            * **dataset** (*pandas dataframe*): user attributes, make it into the format above in a pandas dataframe
        """
        # Split the data into features and labels
        x, y = dataset[dataset.columns[:-1]], dataset['Exam_Score']

        # Get categorical columns
        categorical = dataset.select_dtypes(include='object')

        # Over sample the data for uniform label distribution to avoid bias
        sampler = RandomOverSampler()
        x, y = sampler.fit_resample(x, y)

        # Fit the model
        self.cat.fit(x, y, cat_features=categorical.columns.tolist())

        # Save the new, optimized model
        try:
            cur_file_dir = os.path.dirname(os.path.abspath(__file__))
            self.cat.save_model(f'{cur_file_dir}/catboost_ml_model', format='cbm')

        except Exception as e:
            print("Exception while saving a newly trained model: ", e, "\n")


if __name__ == '__main__':
    '''The order of the features and names is as follows:
            
            * 'Hours_Studied'
            
            * 'Attendance'
            
            * 'Access_to_Resources'
            
            * 'Extracurricular_Activities'
            
            * 'Sleep_Hours'
            
            * 'Previous_Scores'
            
            * 'Motivation_Level'
            
            * 'Teacher_Quality'
            
            * 'School_Type'
            
            * 'Peer_Influence'
            
            * 'Physical_Activity'
            
            * 'Learning_Disabilities'
            
            * 'Distance_from_Home'
            
            * 'Exam_Score'
            '''
    cat = MlModel()

    vals = [60, np.nan, 'Low', 'Yes', 7, 95, 'Low', 5, 'High', 'Private', 'Positive', 6, 'No', 'Near', np.nan]

    cols = ['Hours_Studied',
            'Attendance',
            'Access_to_Resources',
            'Extracurricular_Activities',
            'Sleep_Hours',
            'Previous_Scores',
            'Motivation_Level',
            'Tutoring_Sessions',
            'Teacher_Quality',
            'School_Type',
            'Peer_Influence',
            'Physical_Activity',
            'Learning_Disabilities',
            'Distance_from_Home',
            'Exam_Score'
            ]

    vals = np.array(vals).reshape(1, -1)

    df = pd.DataFrame(vals, columns=cols)

    print(cat.predict(vals))
