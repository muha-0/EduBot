class User:
    def __init__(self) -> None:
        self.name = None
        self.age = None
        self.gender = None
        self.study_hours_per_week = None
        self.sleep_hours_per_night = None
        self.previous_exam_scores = None
        self.motivation_level = None
        self.class_attendance = None
        self.teacher_quality = None
        self.resource_access = None
        self.extracurricular_activities = None
        self.school_type = None
        self.peer_influence = None
        self.learning_disabilities = None
        self.distance_from_home = None
        self.physical_activity = None

    def update(self, **kwargs):
        """Update the user's attributes
            kwargs should have a JSON object with each attribute and its extracted value:
            -If the value is an empty string, then the LLM did not extract any value for it and we want to keep it as None.
            -Else, we assign the extracted value to its attribute.
        """
        for attribute, value in kwargs.items():
            if (value != ''):
                if attribute.__contains__("name"):
                    self.name = value

                elif attribute.__contains__("age"):
                    self.age = value

                elif attribute.__contains__("gender"):
                    self.gender = value

                elif attribute.__contains__("study"):
                    self.study_hours_per_week = value

                elif attribute.__contains__("sleep"):
                    self.sleep_hours_per_night = value

                elif attribute.__contains__("exam"):
                    self.previous_exam_scores = value

                elif attribute.__contains__("motivation"):
                    self.motivation_level = value

                elif attribute.__contains__("attendance"):
                    self.class_attendance = value

                elif attribute.__contains__("teacher"):
                    self.teacher_quality = value

                elif attribute.__contains__("resource"):
                    self.resource_access = value

                elif attribute.__contains__("extracurricular"):
                    self.extracurricular_activities = value

                elif attribute.__contains__("school"):
                    self.school_type = value

                elif attribute.__contains__("peer") or attribute.__contains__("influence"):
                    self.peer_influence = value

                elif attribute.__contains__("learning") or attribute.__contains__("disabilities"):
                    self.learning_disabilities = value

                elif attribute.__contains__("distance") or attribute.__contains__("home"):
                    self.distance_from_home = value

                elif attribute.__contains__("physical"):
                    self.physical_activity = value

    def data(self):
        return {
            "user": {
                "name": self.name,
                "age": self.age,
                "gender": self.gender
            },
            "academics": {
                "study_hours_per_week": self.study_hours_per_week,
                "sleep_hours_per_night": self.sleep_hours_per_night,
                "previous_exam_scores": self.previous_exam_scores,
                "motivation_level": self.motivation_level,
                "class_attendance": self.class_attendance,
                "teacher_quality": self.teacher_quality,
                "resource_access": self.resource_access,
                "extracurricular_activities": self.extracurricular_activities,
                "school_type": self.school_type,
                "peer_influence": self.peer_influence,
                "learning_disabilities": self.learning_disabilities,
                "distance_from_home": self.distance_from_home,
                "physical_activity": self.physical_activity
            }
        }


if __name__ == "__main__":
    u = User()
