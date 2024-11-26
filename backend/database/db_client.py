import os

import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

config = {
    'host': os.environ['AZURE_HOST'],
    'user': os.environ['AZURE_USER'],
    'password': os.environ['AZURE_PWD'],
    'database': os.environ['AZURE_DB']
}


class DBClient:
    def __init__(self):
        """
        Initialize the DBController class with the given database configuration.
        """
        self.config = config
        self.connection = None
        self.connect()

        cur_file_dir = os.path.dirname(os.path.abspath(__file__))
        ssl_args = {
            "ssl_ca": f"{cur_file_dir}/DigiCertGlobalRootCA.crt.pem"
        }
        self.engine = create_engine(
            f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}",
            connect_args={"ssl": ssl_args}
        )

    def connect(self):
        """
        Establish a database connection.
        """
        if not self.connection or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(**self.config)
                print("Connection established")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.connection = None

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")

    def add_user_and_academics(self, user, academics):
        """
        Add a user and their academics to the database.
        """
        cursor = self.connection.cursor()
        try:
            # Insert user
            cursor.execute("""
                INSERT INTO User (name, age, gender) 
                VALUES (%s, %s, %s)
            """, (user.get('Name'), user.get('age'), user.get('gender')))
            user_id = cursor.lastrowid

            # Insert academics
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
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                academics.get('study_hours_per_week'),
                academics.get('sleep_hours_per_night'),
                academics.get('previous_exam_scores'),
                academics.get('motivation_level'),
                academics.get('class_attendance'),
                academics.get('teacher_quality'),
                academics.get('resource_access'),
                academics.get('extracurricular_activities'),
                academics.get('school_type'),
                academics.get('peer_influence'),
                academics.get('learning_disabilities'),
                academics.get('distance_from_home'),
                academics.get('physical_activity')
            ))

            self.connection.commit()
            print("User and academics added successfully.")
            return user_id
        finally:
            cursor.close()

    def update_user_and_academics(self, user_id, user, academics):
        """
        Update user and academic details for a specific user.
        """
        cursor = self.connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE User
                SET name = %s, age = %s, gender = %s
                WHERE user_id = %s
                """,
                (
                    user.get("name"),
                    user.get("age"),
                    user.get("gender"),
                    user_id,
                ),
            )

            # Update Academics table
            cursor.execute(
                """
                UPDATE Academics
                SET 
                    study_hours_per_week = %s,
                    sleep_hours_per_night = %s,
                    previous_exam_scores = %s,
                    motivation_level = %s,
                    class_attendance = %s,
                    teacher_quality = %s,
                    resource_access = %s,
                    extracurricular_activities = %s,
                    school_type = %s,
                    peer_influence = %s,
                    learning_disabilities = %s,
                    distance_from_home = %s,
                    physical_activity = %s
                WHERE user_id = %s
                """,
                (
                    academics.get("study_hours_per_week"),
                    academics.get("sleep_hours_per_night"),
                    academics.get("previous_exam_scores"),
                    academics.get("motivation_level"),
                    academics.get("class_attendance"),
                    academics.get("teacher_quality"),
                    academics.get("resource_access"),
                    academics.get("extracurricular_activities"),
                    academics.get("school_type"),
                    academics.get("peer_influence"),
                    academics.get("learning_disabilities"),
                    academics.get("distance_from_home"),
                    academics.get("physical_activity"),
                    user_id,
                ),
            )
            self.connection.commit()
            print(f"User with user_id {user_id} and their academic details updated successfully!")
        finally:
            cursor.close()

    def add_chat_history(self, user_id, role, message_content):
        """
        Add a chat history record.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO ChatHistory (user_id, role, message_content) 
                VALUES (%s, %s, %s)
            """, (user_id, role, message_content))
            self.connection.commit()
            print("Chat history added successfully.")
            return user_id
        finally:
            cursor.close()

    def read_chat_history(self, user_id):
        """
        Read chat history for a specific user.
        """
        query = "SELECT * FROM ChatHistory WHERE user_id = %s"
        return pd.read_sql(query, self.engine, params=(user_id,))

    def read_training_data(self):
        """
        Read training data from the TrainingDataView.
        """
        return pd.read_sql("SELECT * FROM TrainingDataView", self.engine)


if __name__ == "__main__":
    # Example 3shan tefham el data types w shakl el dict

    academics = {
        "study_hours_per_week": 10,  # FLOAT
        "sleep_hours_per_night": 7,  # FLOAT
        "previous_exam_scores": 85,  # FLOAT
        "motivation_level": 3,  # INT
        "class_attendance": 90,  # INT
        "teacher_quality": 4,  # INT
        "resource_access": 3,  # INT
        "extracurricular_activities": 1,  # INT
        "school_type": "Public",  # VARCHAR(50)
        "peer_influence": 1,  # INT
        "learning_disabilities": 0,  # INT
        "distance_from_home": 1,  # INT
        "physical_activity": 2  # FLOAT
    }

    user = {
        "name": "hamada",  # VARCHAR(50)
        "age": 18,  # FLOAT
        "gender": 1,  # INT
    }

    db = DBClient(config)
    # db.add_chat_history(4000,"System","Hello")
    # print(db.read_chat_history(4000))
    db.update_user_and_academics(3145, user, academics)
    print(db.read_training_data())
    db.close_connection()
