
from Application.DTO.Request.custom_prompt_view_model import CustomPromptViewModel
from Domain.Enums.enumTypeInference import TypeInference


class ExtPrompt():
    def create_prompt_update_question(question):
        default_prompt = "[INST]Ты эксперт-аналитик по вопросам. Изучи приведенный ниже вопрос:"
        lst_arg:list[dict] = []
        lst_arg.append({
            'type':'system',
            "arg_prompt": "Вопрос: {question}", 
            "arg_name":"question",
            "arg_value": question
        })
        lst_arg.append({
            "type": "system", 
            "arg_prompt": "Изучи текст и сформулируй на основе этого предложения вопрос и ничего больше. Ответ должен быть лаконичным, кратким и только на русском языке. Если текст в вопросительной форме и  не содержит ошибок, то ответом будет служить заданный текст. Формат ответа: 'Правильный вопрос:' ответ.[/INST]### Ответ:",
            "arg_name":"",
            "arg_value": ""
        })

        req_custom_prompt = CustomPromptViewModel(TypeInference.RAG, 'alitrix', 1000, default_prompt, lst_arg)

        return req_custom_prompt