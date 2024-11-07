import re
from nltk.corpus import stopwords
from spacy import load as spacy_load
from sentence_splitter import SentenceSplitter as Sentence_Splitter
from Application.Abstractions.base_text_tools import BaseTextTools



splitter = Sentence_Splitter(language='ru')
nlp = spacy_load("ru_core_news_lg", disable=['parser', 'ner'])
nlp.add_pipe('sentencizer')

#stopwords.words('russian')
#nltk.download('stopwords')
#nltk.download('punkt')
stop_words = set(stopwords.words('russian'))
stopwords_ru = stopwords.words('russian')


class PostProccessingText():

    def delete_tags_in_answer(self, text: str) -> str:
        stop_words = ['plaintext', 'sql', 'python']
        for word in stop_words:
            text = text.replace(word, '')

        return text



class TextTools(BaseTextTools):
    
    def clear_garbage_v1(text: str) -> str:
        text = text.replace('-', '')
        text = text.replace('\r', ' ')
        text = text.replace('\xa0', ' ')
        text = text.replace('\x03', '')
        text = text.replace('\x89', '')
        text = text.replace('\uf034', '')
        text = text.replace('\u2264', '')
        text = text.replace('\uf0b7', '')

        text = text.replace('\n\n', '\n')
        text = text.replace('-\n', '')
        text = text.replace('-', '')
        text = text.replace('` ', '')
        text = text.replace('  ', ' ')
        text = text.strip()

        return text

    def clear_garbage_v2(text: str) -> str:
        text = TextTools.clear_numerics(text)
        text = text.replace('-', ' ')
        text = text.replace('\r', '')
        text = text.replace('\xa0', '')
        text = text.replace('\x03', '')
        text = text.replace('\x89', '')
        text = text.replace('\uf034', '')
        text = text.replace('\u2264', '')
        text = text.replace('\uf0b7', '')

        text = text.replace('\n\n', '\n')
        text = text.replace('-\n', ' ')
        text = text.replace('(', '')
        text = text.replace(')', '')
        text = text.replace('\n', '')
        text = text.replace('`', '')
        text = text.replace('"', '')
        text = text.replace('"', '')
        text = text.replace('«', '')
        text = text.replace('»', '')
        text = text.replace(':', ' ')
        text = text.replace(';', '')
        text = text.replace('=', '')
        text = text.replace('\\', ' ')
        text = text.replace('/', ' ')
        text = text.replace('“', ' ')
        text = text.replace('”', ' ')
        text = text.replace('.,', '.')
        text = text.replace(',.', '.')
        text = text.replace('  ', ' ')
        text = text.strip()

        return text

    def clear_garbage_hard_v1(text: str) -> str:
        text = TextTools.clear_garbage_v2(text)
        text = re.sub(r'[^\w\s]', '', text)

        return text

    def clear_numerics(text: str) -> str:
        regex = r"\d+\.?"
        text = re.sub(regex, '', text, 0, re.MULTILINE)
        text = text.replace('▪', '')

        return text

    def clear_regex_text(text: str) -> str:
        text = re.sub(r'^\s?(\d(\.\d)*)\s?', '', text)
        text = re.sub(r'^([А-Яа-я]+)\s?\d+\s?([А-Яа-я]+)\s?\d+\s?$', '', text)
        text = re.sub(r'\uf0a7', '', text)
        text = re.sub(r'Часть\s?\b(?:I{1,3}[VX]?|[VX]|VI{1,3})', '', text)
        text = re.sub(r'Глава\s?\b(?=[XVIΙ])([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?', '', text)
        text = re.sub(r'Часть\s?\b(?=[XVIΙ])([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?', '', text)
        text = re.sub(r'Глава \d', '', text)
        text = re.sub(r'Часть \d', '', text)

        return text

    def clear_other_text(text: str) -> str:
        text = text.replace('\xa0', ' ')
        text = text.replace('\x03', '')
        text = text.replace('\x89', '')
        text = text.replace('\uf034', '')
        text = text.replace('\u2264', '')
        text = text.replace('\uf0b7', '')
        text = text.strip()
        return text

    def clear_garbage_hard_v1(text: str) -> str:
        text = TextTools.clear_garbage_v2(text)
        text = re.sub(r'[^\w\s]', '', text)

        return text
    
    def lemmatize_fn(text: str) -> str:
        doc = nlp(text.lower())
        lemma_text = " ".join([token.lemma_ for token in doc])

        return lemma_text
    
    def delete_stop_word(text: str) -> str:
        text = text.split()
        clear_text = [word for word in text if word not in stop_words]

        clear_text = " ".join(clear_text)

        return clear_text
    
    def parse_responce_llm_question(responce):
        index_end = responce.find('?') + 1
        index = responce.find('Правильный вопрос:') + 19
        text_question = responce[index:index_end:].replace('"', '')
        text_question = (' '.join(text_question.split()))
        return text_question
    
    def clearing_text_fn_v1(text: str) -> str:
        regex = r"\d+\.?"
        text = re.sub(regex, '', text, 0, re.MULTILINE)
        text = text.replace('▪', '')
        text = TextTools.clear_garbage_v1(text)
        text = TextTools.clear_other_text(text)

        return text
    
    def split_fn_v1(text:str, min_len:int=2)->list[str]:
        splited_text = [item.strip() for item in splitter.split(text) if len(item) > min_len]

        return splited_text
    

    def clean_and_repack_text(text:str)->str:
        result_text:str = ''
        splitted_text = TextTools.split_fn_v1(text)
        
        for text in splitted_text:
            cleared_text = TextTools.clear_garbage_hard_v1(text)
            cleared_text = TextTools.lemmatize_fn(cleared_text)
            cleared_text = TextTools.delete_stop_word(cleared_text)
            result_text += f"{' '.join(cleared_text.split())}.\n"
        
        return result_text
    
    def delete_bad_word_v2(test_str: str) -> str:
        result = re.sub(r'((О|о)твет)\s?\.?\:?', '', test_str, 0, re.MULTILINE)
        result = re.sub(r'((К|к)раткий\s?(С|с)одержание)\s?\.?\:?', '', result, 0, re.MULTILINE)
        result = result.replace('\n\n', '')

        return result


