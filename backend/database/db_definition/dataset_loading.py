import mysql.connector
import pandas as pd
from mysql.connector import errorcode

from ..db_client import config

file_path = r"C:\Users\Ahmed sameh\Desktop\StudentPerformanceFactors.csv"  # Replace with your actual file path
data = pd.read_csv(file_path)


def mapData():
    data['Gender'] = data['Gender'].map({'Male': 1, 'Female': 0})

    data['Motivation_Level'] = data['Motivation_Level'].map({'Low': 1, 'Medium': 2, 'High': 3})

    data['Parental_Involvement'] = data['Parental_Involvement'].map({'Low': 1, 'Medium': 2, 'High': 3})

    data['Access_to_Resources'] = data['Access_to_Resources'].map({'Low': 1, 'Medium': 2, 'High': 3})

    data['Extracurricular_Activities'] = data['Extracurricular_Activities'].map({'Yes': 1, 'No': 0})

    data['Internet_Access'] = data['Internet_Access'].map({'Yes': 1, 'No': 0})

    data['Family_Income'] = data['Family_Income'].map({'Low': 1, 'Medium': 2, 'High': 3})

    data['Teacher_Quality'] = data['Teacher_Quality'].map({'Low': 1, 'Medium': 2, 'High': 3})

    data['Peer_Influence'] = data['Peer_Influence'].map({'Negative': -1, 'Neutral': 0, 'Positive': 1})

    data['Learning_Disabilities'] = data['Learning_Disabilities'].map({'Yes': 1, 'No': 0})

    data['Distance_from_Home'] = data['Distance_from_Home'].map({'Far': -1, 'Moderate': 0, 'Near': 1})

    data['Name'] = ["Unknown" for _ in range(len(data))]

    data['Age'] = [0 for _ in range(len(data))]

    print(data.head())


def loadDataSet():
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    for index, row in data.iterrows():
        if (index % 100 == 0):
            print(index)
        # Insert into User table
        cursor.execute("""
              INSERT INTO User (name, age, gender) 
              VALUES (%s, %s, %s)
          """, (row['Name'], row['Age'], row['Gender']))

        # Get the last inserted user_id
        user_id = cursor.lastrowid

        # Insert into Academics table
        cursor.execute("""
              INSERT INTO Academics (
                  user_id, 
                  study_hours_per_week, 
                  sleep_hours_per_night, 
                  previous_exam_scores, 
                  motivation_level, 
                  class_attendance, 
                  teacher_quality, 
                  resource_access, 
                  extracurricular_activities, 
                  school_type, 
                  peer_influence, 
                  learning_disabilities, 
                  distance_from_home, 
                  physical_activity
              ) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          """, (
            user_id,
            row['Hours_Studied'],
            row['Sleep_Hours'],
            row['Previous_Scores'],
            row['Motivation_Level'],
            row['Attendance'],
            row['Teacher_Quality'],
            row['Access_to_Resources'],
            row['Extracurricular_Activities'],
            row['School_Type'],
            row['Peer_Influence'],
            row['Learning_Disabilities'],
            row['Distance_from_Home'],
            row['Physical_Activity']
        ))

        # Insert into ExamScore table
        cursor.execute("""
              INSERT INTO ExamScore (user_id, exam_name, actual_score)
              VALUES (%s, %s, %s)
          """, (user_id, "Exam 1", row['Exam_Score']))

        # Commit the transaction
    conn.commit()
    print("Data inserted successfully!")
