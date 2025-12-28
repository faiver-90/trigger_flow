from src.modules.source.repository.data_source_repo import DataSourceRepo
from src.modules.source.services.data_source_service import (
    CRUDDataSourceService,
)
from src.shared.services.base_get_service import base_get_service
from src.shared.services.fernet_service import FernetService

get_data_source_service = base_get_service(
    CRUDDataSourceService, DataSourceRepo, FernetService()
)
