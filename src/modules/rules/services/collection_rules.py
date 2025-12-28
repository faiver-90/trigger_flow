from src.modules.rules.repository.rules_repo import RulesRepo
from src.shared.services.base_crud_service import BaseCRUDService


class ParseRulesService(BaseCRUDService[RulesRepo]):
    def parse_rules(self):
        result = self.repo.parce_rules()
        if result:
            return ...
        return ...
