from ..LLM import LLM
from ..database import DBClient


class Controller:
    __DB_client = DBClient()
    __chat_instances = []

    @staticmethod
    def generate(message, user_id):
        user_model = Controller.get_user_model(user_id)
        response = user_model.context_analysis(message)
        return response

    @staticmethod
    def create_user_model(user_id):
        user_model = LLM(user_id)
        Controller.__chat_instances.append(user_model)
        return user_model

    @staticmethod
    def get_user_model(user_id):
        for chat_instance in Controller.__chat_instances:
            if chat_instance.user_id == user_id:
                return chat_instance

        print("User model not found, Creating new model")
        return Controller.create_user_model(user_id)

    @staticmethod
    def delete_user_model(user_id):
        for chat_instance in Controller.__chat_instances:
            if chat_instance.user_id == user_id:
                if chat_instance.history:
                    user_data = chat_instance.user.data()
                    Controller.__DB_client.add_user_and_academics(
                        user_id, user_data['user'], user_data['academics']
                    )
                    for message in chat_instance.history:
                        Controller.__DB_client.add_chat_history(
                            user_id, message["role"], message["content"]
                        )
                Controller.__chat_instances.remove(chat_instance)
                del chat_instance


if __name__ == "__main__":
    x = Controller()
