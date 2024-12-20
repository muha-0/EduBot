import json
import os
from typing import Optional

from groq import Groq
from pydantic import BaseModel

from .user import User
from ..MLM import MlModel


class ChatModel:
    """**ChatModel Class Description:**
    *This class does the main functionality of:*  
        1-Communication with the LLM.  
        2-Context Analysis.  
        3-Sentiment Analysis.  
        4-Feature Extraction.  
        5-Saving the chat history and the chat context.  
        6-All in-code prompts are featured here.  
    
    It uses a user object to store the user's attributes and an MlModel object to get score predictions
    """

    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.history = []
        self.user = User()
        self.mlmodel = MlModel()
        self.client = Groq(
            api_key=os.environ['GROQ_API_KEY'],
        )

        # Make a flag that tells whether there was an initial prediction request that made us go to extraction or not.
        # This flag should be used only when the user input is directed for extraction.
        self.wanted_prediction = False
        
        start_system_message = """
                                You are the best model to assist students in improving their productivity, study habits, and helping them in their studies.
                                you are the best at doing the following:
                                1- Making recommendations: you provide effective suggestions and assistance in their studies and productivity and your suggestions with the information you know about them if provided.
                                2- Sometimes you will be provided with an exam score prediction, you need to explain possible reasons behind such score given what you know about them and how they can improve or what to do next.
                                
                                when you are asked for recommendation, you must be specific for the studying or productivity techniques you might suggest them, citing where you know such techniques from if possible, and maybe suggesting that they check the source themselves.
                                
                                Here are some possible books, authors and people who provide advices on productivity and studying:
                                
                                1- Atomic Habits Book, by James Clear.
                                
                                2- The Slight Edge, by Jeff Olson.
                                
                                3- The 7 Habits of Highly Effective People, by Stephen Covey.
                                
                                4- Eat That Frog!: 21 Great Ways to Stop Procrastinating and Get More Done in Less Time, by Brian Tracy.
                                
                                5- Huberman's Lab, a podcast by Andrew Huberman.
                                
                                You do not have to use these examples all the time or even mention all of them, but get an idea on what you might suggest from them or similar books you know of.
                            """
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": 'system',
                    "content": start_system_message
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        

        self.history.append({
            "role": 'system',
            "content": start_system_message
        })

    def context_analysis(self, user_input):
        """Given user input, it decides the best course of action given the context and return the appropriate response
        
        1-It calls the extraction function to extract any relevant information if the response is recommendation (I found it to give wrong information if the request is prediction)
        2-Ask the LLM to decide the Context/Intent of the user's input
        If Recommendation, respond directly
        If Prediction, call for validation and then respond
        If Extraction, call for extraction and then check the state for the next step
        """

        # We will make the context analysis message stand alone for the LLM without giving giving him the chat history

        # Append the user's message to the chat history to keep the LLM in context 
        self.history.append({
            "role": 'user',
            "content": user_input
        })

        messege = f"""Given the following text, say prediction if the user wants to get a prediction, 
        say extraction if the user is providing information or a self report about themself, say recommendation for any other context: \n
        User input: \"{user_input}\"
        
        Follow these rules:
        1-For prediction, be sure that the user actually wants you to predict something, grade, score, test, etc.
        2-For extraction, the user should be providing some information about themselves, like their name, gender, age, academic information about them, etc.
        3-For recommendation, the user should either want a recommendation from you to help them at something, or a general message which you can handle yourself with no need for extraction or making a prediction. 
        4-you must only respond with 1 word of the three indicated above.
        
        Check the following messages and the intent behind them as an example to what you should recognize as what where 'In' is the input message and 'Out' is the Intent recognized from the message:
        
        (1)
        In: Hello, my name shady ali, I'm 24
        Out: extraction
        
        (2)
        In: What do you think my next score will be?
        Out: prediction
        
        (3)
        In: I am really at loss of what to do to improve my study habits and grades, what can I do?
        Out: recommendation
        
        (4)
        In: Hello
        Out: recommendation
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": 'user',
                    "content": messege
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        # Get the LLM's response, he should answer with yes or no
        response = chat_completion.choices[0].message.content
        response = response.rstrip(r'.|;|:|,').lower()

        # test
        # print("in-code prompt to analyze context and user's intent:\n", messege, "\n\n")
        # print("LLM response to the analysis request:\n", response, "\n\n")
        # print(self.history, "\n\n")

        '''
        We want to check the response, 
            -If prediction, then we need to validate that we have all attributes needed before we make the prediction,
            
            -If recommendation, then we should simply let the LLM handle the response,
            
            -If extraction, it should mean that the user has requested a prediction before but we needed them to provide more attributes,
                so we extract the information, double check that we have everything, and make a prediction.
        '''

        # Not a prediction request
        if response == 'recommendation':
            # Retreive a JSON Object containing all extracted relevant information
            user_info = self.extract(user_input=user_input)

            # Update the extracted information into the user object's attributes
            try:
                self.user.update(user_info)

            except Exception as e:
                print("Execption while inputing extracted data during a recommendation: ", e)

            # Save the LLM's response to the actual user input while giving him context using chat history
            chat_completion = self.client.chat.completions.create(
                messages=self.history,
                model="llama-3.2-90b-vision-preview",
            )

            in_context_response = chat_completion.choices[0].message.content

            # Append the LLM's response to the chat history
            self.history.append({
                "role": "assistant",
                "content": in_context_response
            })

            # test
            # print("in-context response that we will make a recommendation:\n", in_context_response, "\n\n")
            # print(self.history, "\n\n")
            return in_context_response

        # It is a prediction request
        if response == 'prediction':
            return self.validate_and_output()

        # It is an extraction request
        if response == 'extraction':
            # Retreive a JSON Object containing all extracted information
            user_info = self.extract(user_input=user_input)

            # Update the extracted information into the user object's attributes
            try:
                self.user.update(user_info)

            except Exception as e:
                print("Execption while inputing extracted data during an extraction: ", e)

            # Test
            # print("User Current Attributes and values:\n", self.user.__dict__, "\n")

            # Check if the there was an initial prediction request to process
            if self.wanted_prediction == True:
                # Reset the flag
                self.wanted_prediction == False

                return self.validate_and_output()

            # If no initial prediction request, then let LLM reply
            elif self.wanted_prediction == False:

                # Save the LLM's response to the actual user input while giving him context using chat history
                chat_completion = self.client.chat.completions.create(
                    messages=self.history,
                    model="llama-3.3-70b-versatile",
                )

                in_context_response = chat_completion.choices[0].message.content

                # Append the LLM's response to the chat history
                self.history.append({
                    "role": "assistant",
                    "content": in_context_response
                })

                # test
                # print("in-context response that we made an extraction with no prior prediction request:\n",
                #       in_context_response, "\n\n")
                # print(self.history, "\n\n")
                return in_context_response

    def validate_and_output(self):
        """
        We start by handling problems and missing values
        - Make a list of the missing values
        
        If missing values:
            LLM -> Ask user to provide missing values
            
        If no missing values:
            prediction <- Predict(user)
            Let the LLM wrap the prediction in a message along with recommendations and tips given the chat history and the user's attributes
        """
        # Let's check which attributes are still missing
        missing_attributes = []

        for attribute, value in self.user.prediction_attributes().items():  # or obj.__dict__.items()
            # If the attribute is missing add it to the missing list
            if value == None or value == "" or value == []:
                missing_attributes.append(attribute)
            # print(f"{attribute}: {value}\n", "\n\n")

        # We can manage things and make predictions if 0-2 attributes are missing
        # Tell the user we need more info if more than 2 attributes are missing
        if len(missing_attributes) > 0:
            # Turn the wanted prediction flag to true
            # After validation, the user input should make an extraction request which when done,
            # we need to know whether if there was an initial prediction request that led us to this point or otherwise
            self.wanted_prediction = True

            message = f"""
            Can you write a message stating that you need them (the user) to provide following attributes to be able to make a prediction:
            {missing_attributes}
            """
            # Save the LLM's response to the actual user input while giving him context using chat history
            chat_completion = self.client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": message
                }],
                model="llama-3.3-70b-specdec",
            )

            in_context_response = chat_completion.choices[0].message.content

            # Append the LLM's response to the chat history
            self.history.append({
                "role": "assistant",
                "content": in_context_response
            })

            # print("in-code prompt: \n", message, "\n\n")
            # print("in-context response for that we found missing values:\n", in_context_response, "\n\n")
            # print(self.history, "\n\n")
            return in_context_response

        # Now we can provide a prediction
        prediction = self.mlmodel.predict(self.user.prediction_attributes())

        # Wrap up the prediction in a message
        message = f"""
        given the chat history so far and the user's following information along with this exam score prediction ({prediction}) for them: \n
        user's attributes: {self.user.__dict__} \n
        
        can you announce the prediction to the user provided along with specific tips and recommendations to improve themselves more given their history and what you know so far?
        """

        # get a copy of the chat history because we don't want to append the in-code prompt to the actual user's chat history
        chat_history = self.history.copy()
        chat_history.append({
            "role": "system",
            "content": message
        })

        # print("chat history to announce with the prediction: \n", chat_history)
        chat_completion = self.client.chat.completions.create(
            messages=chat_history,
            model="llama-3.3-70b-specdec",
        )

        in_context_response = chat_completion.choices[0].message.content

        # Append the LLM's response to the chat history
        self.history.append({
            "role": "assistant",
            "content": in_context_response
        })

        # print("in-code prompt: \n", message, "\n\n")
        # print("in-context response for announcing predictions:\n", in_context_response, "\n\n")
        # print(self.history)
        return in_context_response


    def predict(self):
        attributes = [
            self.user.study_hours_per_week,
            self.user.class_attendance,
            self.user.resource_access,
            self.user.extracurricular_activities,
            self.user.sleep_hours_per_night,
            self.user.previous_exam_scores,
            self.user.motivation_level,
            self.user.teacher_quality,
            self.user.school_type,
            self.user.peer_influence,
            self.user.physical_activity,
            self.user.learning_disabilities,
            self.user.distance_from_home
        ]

        try:
            prediction = self.mlmodel.predict(attributes=attributes)
            return prediction
        except Exception as e:
            print("Exception during calling ml model for a prediction: ", e, "\n")

        # If an error happened, return this message instead
        return 'could not predict exam score'




# This is a class template for the JSON Object which we want to retrieve from the LLM in extract()
    class user_attributes(BaseModel):
        name: Optional[str]
        age: Optional[int]
        gender: Optional[str]
        study_hours_per_week: Optional[int]
        sleep_hours_per_night: Optional[int]
        previous_exam_scores: Optional[int]
        motivation_level: Optional[str]
        class_attendance: Optional[int]
        teacher_quality: Optional[str]
        resource_access: Optional[str]
        extracurricular_activities: Optional[int]
        school_type: Optional[str]
        peer_influence: Optional[str]
        learning_disabilities: Optional[str]
        distance_from_home: Optional[str]
        physical_activity: Optional[int]
        tutoring: Optional[int]

    def extract(self, user_input):

        """
        We will use Few-Shot Prompting to insure the LLM:
        1-Has a specific rules & structure to follow
        2-Has "few" examples and the output to learn from
        """

        # Few-Shot Prompt
        prompt = f"""
                You are the best model to extract data from raw texts to desired Json format. you will be provided user messages that you need to extract specfic information from it into JSON format. 
                You are tasked with converting the given text into a JSON object with the specified structure. 
                Please follow these guidelines:

                1. - If the provided text is empty or does not contain any relevant information, return the JSON structure with all values as an None.
                - If the provided text contains multiple instances of the same information (e.g., multiple names), use the one that relates to the user the most and not anyone else's.
                - If the provided text contains conflicting information (e.g., different ages), use the one that relates to the user the most and not anyone else's.

                2. Extract relevant information from the provided text and map it to the corresponding keys in the JSON structure.

                3. If a particular key's value is not found in the given text, leave the value as an None.

                4. Do not include any additional information or formatting beyond the requested JSON object.
                
                5. Make sure to transform each of "motivation_level", "teacher_quality", "resource_access" values into (low, medium, high) categories.

                6. You must follow the given JSON structure exactly, including the key names.
                
                7. remember to specify the gender.
                
                8. Make sure to make the values of "age", "study_hours_per_week", "sleep_hours_per_night", "previous_exam_scores", "class_attendance" as numbers only.
                
                9. If values of "age" or "sleep_hours_per_night" are zero, leave the value as an empty string.
                
                10. Make sure to transform the values of "extracurricular_activities", "tutoring", "physical_activity", into (0, 1) categories such that 0 means 'no' and 1 means 'yes'.
                
                11. Make sure to transform the values of "school_type" into (private, public) categories.
                
                12. Make sure to transform the values of "peer_influence" into (positive, negative, neutral) categories.
                
                13. Make sure to transform the values of "distance_from_home" into (near, moderate, far) categories.
                
                14. Make sure to stick to the given format and value categories.
                
                15. Make sure to transform the values of "learning_disabilities" into (yes, no) Categories.
                
                
                
                Here are some examples, I'm gonna provide you the raw_texts and json structure.
                raw_texts: 
                1-Hey, I’m Shady, 21, male. I go to a private school and study about 20 hours a week. I usually get 6 hours of sleep a night, and my last exam score was 85. My motivation level is medium, and I attend 90% of my classes. Teachers are great, and resource access is decent. I’m involved in extracurricular activities and do about 6 hours of physical activity weekly. The school is far from home, but I manage. Peer influence is neutral, and thankfully, I don’t have any learning disabilities. I take tutoring sessions yes.
                2-Resources are decent—nothing fancy, but they work. I get about 6 hours of sleep most nights, which isn’t ideal but manageable. My last exam score was 85%.
                3-Classes are alright! I attend regularly, maybe 85-90%. My study schedule’s flexible, but I squeeze in a few hours daily. Sleep’s hit-or-miss—usually 5-6 hours.
                4-Hi, I’m Shady, a 21-year-old male. I study around 25 hours weekly, get 6 hours of sleep nightly, and scored 87 in my last exam. Motivation is at 8/10, with decent teacher support and 92% attendance.
                5-I’ve been trying to study consistently (about 3-4 hours a day), and motivation’s not bad! Teachers are okay, and I sleep about 6 hours. Last exam? 83%.
                6-Hey, I’ve been studying around 20 hours weekly—pretty manageable. Ahmed says he studies way less, but his motivation is crazy high! My last exam score was 85%.
                7-Classes are alright. I think Salma mentioned she’s getting better sleep—like 7 hours nightly. Me? Still around 6. Teachers are supportive, though!
                json_structure:{json.dumps(self.user_attributes.model_json_schema(), indent=2)}""",
            

        messages = [{
            "role": "system",
            "content": str(prompt)
        },
            {
                "role": "user",
                "content": str(user_input)
            }]

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0,
            # Streaming is not supported in JSON mode
            stream=False,
            # Enable JSON mode by setting the response format
            response_format={"type": "json_object"},
        )


        try:
            extracted_data = self.user_attributes.model_validate_json(chat_completion.choices[0].message.content)
            # print(extracted_data, "\n\n")
        except Exception as e:
            print("Error while validating the JSON Output after an extraction attempt: ", e, "\n")
        return extracted_data


if __name__ == "__main__":
    chatty = ChatModel("787")

    chatty.context_analysis(input())
