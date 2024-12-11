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
        self.tutoring = None

    def update(self, attributes):
        """Update the user's attributes
            kwargs should have a JSON object with each attribute and its extracted value:
            -If the value is an empty string, then the LLM did not extract any value for it and we want to keep it as None.
            -Else, we assign the extracted value to its attribute.
        """
    
        self.name = attributes.name
        self.age = attributes.age
        self.gender = attributes.gender
        self.study_hours_per_week = attributes.study_hours_per_week
        self.sleep_hours_per_night = attributes.sleep_hours_per_night
        self.previous_exam_scores = attributes.previous_exam_scores
        self.motivation_level = attributes.motivation_level
        self.class_attendance = attributes.class_attendance
        self.teacher_quality = attributes.teacher_quality
        self.resource_access = attributes.resource_access
        self.extracurricular_activities = attributes.extracurricular_activities
        self.school_type = attributes.school_type
        self.peer_influence = attributes.peer_influence
        self.learning_disabilities = attributes.learning_disabilities
        self.distance_from_home = attributes.distance_from_home
        self.physical_activity = attributes.physical_activity
        self.tutoring = attributes.tutoring
        
        print("\n\nupdated user attributes: ", self.data())


    # TODO: Add tutoring attribute 
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
        
    def prediction_attributes(self):
        
        if self.class_attendance != None:
            return {'study_hours_per_week': self.study_hours_per_week,
                    'class_attendance': ((100 - self.class_attendance)/100) * 32,
                    'tutoring_sessions': self.tutoring,
                    'extracurricular_activities': self.extracurricular_activities,
                    'physical_activity': self.physical_activity}
            
        else:
            return {'study_hours_per_week': self.study_hours_per_week,
                    'class_attendance': self.class_attendance,
                    'tutoring_sessions': self.tutoring,
                    'extracurricular_activities': self.extracurricular_activities,
                    'physical_activity': self.physical_activity}


if __name__ == "__main__":
    u = User()
