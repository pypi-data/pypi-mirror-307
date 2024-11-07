import os
from datetime import datetime

from Application.DTO.Request.rag_question_project import RequestToLLM
from Utilites.ext_path import ExtPath


class ExtDump():

    def dump_relevan_search(text, method: str):

        datetime_now = datetime.now().strftime('%d.%m.%y_%H.%M.%S')
        if ExtPath.exists_or_create_path('Dumps'):
            with open(f'Dumps/res_{method}_{datetime_now}.txt', 'w', encoding="utf-8") as fl:
                fl.write(text)

        ExtDump.check_and_delete_dumps()

    def formated_result(question_pack: RequestToLLM, lst_answer: list, method: str):
        lst_answer = ExtDump.create_list_dump(lst_answer)
        text_for_dump = f'Method: {method}\n' \
                        f'### question: {question_pack.question}\n' \
                        f'### k-top: {question_pack.k_top}\n' \
                        f'### prompt: {question_pack.prompt}\n' \
                        f'### result_search:\n\n'

        for index, item in enumerate(lst_answer):
            text_for_dump += f"{index + 1}.\n" \
                         f"### name: {item['name']}\n" \
                         f"### url: {item['url']}\n" \
                         f"### distance: {item['distance']}\n"

            ExtDump.dump_relevan_search(text_for_dump, method)

    def check_and_delete_dumps():
        dumps = os.listdir("Dumps")
        if len(dumps) >= 100:
            for dump in dumps[0:50:1]:
                os.remove(f"Dumps/{dump}")

    def create_list_dump(lst):
        lst_answer_dumps = [{'id': item['id'],
            'name': item['name'],
            'context': item['context'],
            'url': item['url'],
            'distance': item['distance']} for item in lst]
    
        return lst_answer_dumps
