import sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0,str(Path(sys.path[0]).parent))

start_service_time = datetime.now()
#======= Package library ============================
from fwdi.WebApp.web_application import WebApplication
from fwdi.WebApp.web_application_builder import WebApplicationBuilder
#----------------------------------------------------
from Application.dependency_injection import DependencyInjection as ApplicationDependencyInjection
from Persistance.dependency_injection import DependencyInjection as PersistanceDependencyInjection
from Presentation.dependency_injection import DependencyInjection as PresentationDependencyInjection
from Utilites.dependency_injection import DependencyInjection as UtilitesDependencyInjection
from Infrastructure.dependency_injection  import DependencyInjection as InfrastructureDependencyInjection
stop_module_service_load = datetime.now()
#----------------------------------------------------
def start_web_service():
    server_param = {
        'name':'Rest Inference service',
        'debug':'False'
    }
    builder:WebApplicationBuilder = WebApplication.create_builder(**server_param)
    #------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------
    ApplicationDependencyInjection.AddConfig(builder.services)
    UtilitesDependencyInjection.AddUtils(builder.services)
    InfrastructureDependencyInjection.AddConfigs(builder.services)
    InfrastructureDependencyInjection.AddInfrastructure(builder.services)
    ApplicationDependencyInjection.AddApplicationInteractors(builder.services)
    PersistanceDependencyInjection.AddPersistance(builder.services)
    #------------------------------------------------------------------------------------------
    PresentationDependencyInjection.AddScope(builder)
    stop_env_service_load = datetime.now()

    app:WebApplication = builder.build()
    #------------------------------------------------------------------------------------------
    PresentationDependencyInjection.AddEndpoints(app)
    stop_endpoint_load = datetime.now()
    #------------------------------------------------------------------------------------------
    kwargs = {
            'host': "0.0.0.0",
            'port': 5000
        }
    print(f"\n============================================================")
    print(f"Start service at :{start_service_time}")
    print(f"    1.Module service load ellapsed time: :{stop_module_service_load - start_service_time}")
    print(f"    1.Env service load ellapsed timet :{stop_env_service_load - stop_module_service_load}")
    print(f"    1.Create endpoints and build service load ellapsed time :{stop_endpoint_load - stop_env_service_load}")
    print(f"\n============================================================")

    app.run(**kwargs)

if __name__ == "__main__":
    start_web_service()