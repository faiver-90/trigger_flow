from src.modules.api_source.api.v1.source.services.data_source_service import CRUDDataSourceService
from src.modules.api_source.api.v1.source.data_source_repo import DataSourceRepo
from src.shared.services.base_get_service import base_get_service
from src.shared.services.fernet_service import FernetService

get_data_source_service = base_get_service(CRUDDataSourceService, DataSourceRepo, FernetService())
