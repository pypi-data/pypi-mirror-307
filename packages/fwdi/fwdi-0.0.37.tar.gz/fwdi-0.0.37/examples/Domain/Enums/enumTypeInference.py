from enum import Enum

class TypeInference(int, Enum):
    Question = 0
    RAG = 1
    QA = 2
    Translate = 3
    SPR = 4
