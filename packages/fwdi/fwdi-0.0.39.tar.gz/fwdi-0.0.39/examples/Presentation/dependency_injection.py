from fwdi.WebApp.web_application import WebApplication
from Presentation.Endpoints.dumps_endpoints import DumpEndpoint
from Presentation.Endpoints.parse_and_create_db_endpoints import ParseEndpoint
from Presentation.Endpoints.questions_endpoints import QuestionEndpoint

class DependencyInjection():
    
    from fwdi.WebApp.web_application_builder import WebApplicationBuilder

    def AddEndpoints(app:WebApplication):
        app.map_get(f'/api/v1.0/question', QuestionEndpoint.search)
        app.map_get(f'/api/v1.0/answer', QuestionEndpoint.answer)
        app.map_get(f'/api/v1.0/dumps_list', DumpEndpoint.dumps_list)
        app.map_get(f'/api/v1.0/dump_detail', DumpEndpoint.dump)
        app.map_get(f'/api/v1.0/parse', ParseEndpoint.parse)

    def AddScope(builder:WebApplicationBuilder):
        scopes = {
            "admin": "Administration access.", 
            "question": "Question LLM access"
            }
        builder.add_scope(scopes)