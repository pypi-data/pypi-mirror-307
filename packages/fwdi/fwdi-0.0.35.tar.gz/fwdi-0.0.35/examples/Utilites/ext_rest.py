from pydantic import BaseModel

class RestResponse():
    def __init__(self) -> None:
        pass

    def make_response(self, message:str):
        return {
            'Message':message
        }, 200


    def response_200(m_base:BaseModel):
        if m_base == None:
            return {'result': 'OK'}
        else:
            return m_base, 200
    
    def abort_400():
        return {
            'result':'error'
        }, 400
    
    def make_error_response(error):
        return error, 404
    
    def make_response_200(text:str, key:str|None = None):
        if key == None:
            return {'Message':text}
        else:
            return {
                key: text
            }, 200