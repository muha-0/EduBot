import os
from LLM.user import User
from groq import Groq
import json
import re

"""ChatModel Class Description:
    This class does the main functionality of
        1-Communication with the LLM.
        2-Context Analysis.
        3-Sentiment Analysis.
        4-Feature Extraction.
        5-Saving the chat history and the chat context.
        6-All in-code prompts are featured here.
    
    It uses a user object to store the user's attributes
"""


class ChatModel:
    def __init__(self) -> None:
        self.history = []
        self.user = User()
        self.client = Groq(
            api_key="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",
        )
        
        # Make a flag that tells whether there was an initial prediction request that made us go to extraction or not.
        # This flag should be used only when the user input is directed for extraction.
        self.wanted_prediction = False
    
    def context_analysis(self, user_input):
        # We will make the context analysis message stand alone for the LLM without giving giving him the chat history
        
        # Append the user's message to the chat history to keep the LLM in context 
        self.history.append({
            "role": 'user',
            "content": user_input
        })
        
        
        messege = f"""Given the following text, say "prediction" if the user wants to get a prediction, 
        say "extraction" if the user is providing information about themself, say "recommendation" for any other context: \n
        \"{user_input}\""""
        
        chat_completion = self.client.chat.completions.create(
            messages= [
                {
                "role": 'user',
                "content": messege
                }
                       ],
            model="llama-3.2-90b-vision-preview",
        )
        
        # Get the LLM's response, he should answer with yes or no
        response = chat_completion.choices[0].message.content
        response = response.rstrip(r'.|;|,').lower()
        
        # test
        print("in-code prompt to analyze context and user's intent:\n", messege, "\n\n")
        print("LLM response to the analysis request:\n", response, "\n\n")
        print(self.history, "\n\n")
        
        '''
        We want to check the response, 
            -If prediction, then we need to validate that we have all attributes needed before we make the prediction,
            
            -If recommendation, then we should simply let the LLM handle the response,
            
            -If extraction, it should mean that the user has requested a prediction before but we needed them to provide more attributes,
                so we extract the information, double check that we have everything, and make a prediction.
        '''
        
        # Not a prediction request
        if response == 'recommendation':
            # Save the LLM's response to the actual user input while giving him context using chat history
            chat_completion = self.client.chat.completions.create(
            messages= self.history,
            model="llama-3.2-90b-vision-preview",
            )
            
            in_context_response = chat_completion.choices[0].message.content
            
            # Append the LLM's response to the chat history
            self.history.append({
                "role": "assistent",
                "content": in_context_response
            })
            
            #test
            print("in-context response that we will make a recommendation:\n", in_context_response, "\n\n")
            print(self.history, "\n\n")
            return in_context_response
            
        # It is a prediction request
        if response == 'prediction':
            return self.validate_and_output()
        
        
        # It is an extraction request
        if response == 'extraction':
            # Retreive a JSON Object containing all extracted files
            user_info = self.extract(user_input = user_input)
            
            # Update the extracted information into the user object's attributes
            self.user.update(**user_info)
            
            
            # Check if the there was an initial prediction request to process
            if self.wanted_prediction == True:
                # Reset the flag
                self.wanted_prediction == False
                
                return self.validate_and_output()
            
            # If no initial prediction request, then let LLM reply
            elif self.wanted_prediction == False:
                
                # Save the LLM's response to the actual user input while giving him context using chat history
                chat_completion = self.client.chat.completions.create(
                messages= self.history,
                model="llama-3.2-90b-vision-preview",
                )
                
                in_context_response = chat_completion.choices[0].message.content
                
                # Append the LLM's response to the chat history
                self.history.append({
                    "role": "assistent",
                    "content": in_context_response
                })
                
                #test
                print("in-context response that we made an extraction with no prior prediction request:\n", in_context_response, "\n\n")
                print(self.history, "\n\n")
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
        
        for attribute, value in self.user.__dict__.items():  # or obj.__dict__.items()
            # If the attribute is missing add it to the missing list
            if value == None:
                missing_attributes.append(attribute)
            print(f"{attribute}: {value}\n", "\n\n")
        
        # We can manage things and make predictions if 0-2 attributes are missing
        # Tell the user we need more info if more than 2 attributes are missing
        if len(missing_attributes) > 2:
            # Turn the wanted prediction flag to true
            # After validation, the user input should make an extraction request which when done,
            # we need to know whether if there was an initial prediction request that led us to this point or otherwise
            self.wanted_prediction = True
            
            
            message = f"""
            Can you write a message stating that you need them to provide following attributes to be able to make a prediction:
            {missing_attributes}
            """
            # Save the LLM's response to the actual user input while giving him context using chat history
            chat_completion = self.client.chat.completions.create(
            messages = [{
                "role": "user", 
                "content" : message
                }],
            model = "llama-3.2-90b-vision-preview",
            )
            
            in_context_response = chat_completion.choices[0].message.content
            
            # Append the LLM's response to the chat history
            self.history.append({
                "role": "assistent",
                "content": in_context_response
            })
            
            print("in-code prompt: \n", message, "\n\n")
            print("in-context response for that we found missing values:\n", in_context_response, "\n\n")
            print(self.history, "\n\n")
            return in_context_response
        
        # Now we can provide a prediction
        prediction = self.predict(**self.user.__dict__) # To-do
        
        # Wrap up the prediction in a message
        message = f"""
        given the chat history so far and the user's following information along with this exam score prediction ({prediction}) for them: \n
        user's attributes: {self.user.__dict__} \n
        
        can you announce to this user the prediction provided along with specific tips and recommendations to improve themselves more given their history and what you know so far?
        """
        
        # get a copy of the chat history because we don't want to append the in-code prompt to the actual user's chat history
        chat_history = self.history.copy()
        chat_history.append({
                "role": "user",
                "content": message
                })
        
        print("chat history to announce with the prediction: \n", chat_history)
        chat_completion = self.client.chat.completions.create(
            messages = chat_history,
            model = "llama-3.2-90b-vision-preview",
            )
            
        in_context_response = chat_completion.choices[0].message.content
        
        # Append the LLM's response to the chat history
        self.history.append({
            "role": "assistent",
            "content": in_context_response
        })
        
        print("in-code prompt: \n", message, "\n\n")
        print("in-context response for announcing predictions:\n", in_context_response, "\n\n")
        print(self.history)
        return in_context_response
        
        
    # TODO: Related to ML Model
    def predict(self, **kwargs):
        pass
        
    def extract(self, user_input):
        
        """
        We will use Few-Shot Prompting to insure the LLM:
        1-Has a specific rules & structure to follow
        2-Has "few" examples and the output to learn from
        """
        
        # JSON Structure the LLM will follow
        json_structure = {
                            "name": "Shady",
                            "age": 21,
                            "gender": "male",
                            "study_hours_per_week": 20,
                            "sleep_hours_per_night": 6,
                            "previous_exam_scores": 85,
                            "motivation_level": "medium",
                            "class_attendance": 90,
                            "teacher_quality": "high",
                            "resource_access": "medium"
                        }
        
        # Few-Shot Prompt
        prompt = """
                You are the best model to extract data from raw texts to desired Json format. you will be provided user messages that you need to extract specfic information from it into JSON format. 
                You are tasked with converting the given text into a JSON object with the specified structure. 
                Please follow these guidelines:

                1. - If the provided text is empty or does not contain any relevant information, return the JSON structure with all values as an empty string.
                - If the provided text contains multiple instances of the same information (e.g., multiple names), use the one that relates to the user the most and not anyone else's.
                - If the provided text contains conflicting information (e.g., different ages), use the one that relates to the user the most and not anyone else's.

                2. Extract relevant information from the provided text and map it to the corresponding keys in the JSON structure.

                3. If a particular key's value is not found in the given text, leave the value as an empty string.

                4. Do not include any additional information or formatting beyond the requested JSON object.
                
                5. Make sure to transform each of "motivation_level", "teacher_quality", "resource_access" values into (low, medium, high) categories.

                6. You must follow the given JSON structure exactly, including the key names.
                
                7. remember to specify the gender.
                
                8. Make sure to make a values of "age", "study_hours_per_week", "sleep_hours_per_night", "previous_exam_scores", "class_attendance" as numbers only.
                
                9. If values of "age" or "sleep_hours_per_night" are zero, leave the value as an empty string.
                
                Here are some examples, I'm gonna provide you the raw_texts and json structure.
                raw_texts: 
                1-Hey! I’m Shady, 21, and I usually study around 20 hours a week. Teachers here are supportive, but I’d say my motivation for this course is around 7/10. Attendance’s been pretty good too, about 90%!
                2-Resources are decent—nothing fancy, but they work. I get about 6 hours of sleep most nights, which isn’t ideal but manageable. My last exam score was 85%.
                3-Classes are alright! I attend regularly, maybe 85-90%. My study schedule’s flexible, but I squeeze in a few hours daily. Sleep’s hit-or-miss—usually 5-6 hours.
                4-Hi, I’m Shady, a 21-year-old male. I study around 25 hours weekly, get 6 hours of sleep nightly, and scored 87 in my last exam. Motivation is at 8/10, with decent teacher support and 92% attendance.
                5-I’ve been trying to study consistently (about 3-4 hours a day), and motivation’s not bad! Teachers are okay, and I sleep about 6 hours. Last exam? 83%.
                6-Hey, I’ve been studying around 20 hours weekly—pretty manageable. Ahmed says he studies way less, but his motivation is crazy high! My last exam score was 85%.
                7-Classes are alright. I think Salma mentioned she’s getting better sleep—like 7 hours nightly. Me? Still around 6. Teachers are supportive, though!
                json_structure: {json_structure}
                """
            
        messages = [{
            "role": "system",
            "content": prompt
        },
                    {
            "role": "user",
            "content": user_input
        }]
        
        
        chat_completion = self.client.chat.completions.create(
            messages = messages,
            model = "llama-3.2-90b-vision-preview",
            )
        extracted_data = chat_completion.choices[0].message.content
        
        
        # Make the LLM validate its output and refine it
        messages.append({
            "role": "assistant",
            "content": extracted_data
        })
        messages.append({
            "role": "user",
            "content": "Could you validate and refine your last answer by making it follow the exact JSON format provided and following the given rules? Output the final JSON only!"
        })
        
        chat_completion = self.client.chat.completions.create(
            messages = messages,
            model = "llama-3.2-90b-vision-preview",
            )
        extracted_data = chat_completion.choices[0].message.content
        
        try:
            # Try removing any text before and after the JSON structure then try formating it into an Object
            pattern = r'(?s)\{.*\}'
            extracted_data = re.search(pattern, extracted_data).group()
            
            # Load into a JSON Object
            extracted_data = json.loads(extracted_data)
            
        except Exception as e:
            print(f"Exception {e}")
        
        print("Extracted Data:\n", extracted_data)
        return extracted_data
        
            


        
        
                
  
        
    
        
            
        
            
            
        

chatty = ChatModel()

chatty.context_analysis(input())
