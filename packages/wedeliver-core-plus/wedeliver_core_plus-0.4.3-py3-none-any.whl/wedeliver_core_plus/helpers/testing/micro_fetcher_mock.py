from unittest.mock import MagicMock
from enum import Enum


# Placeholder exception classes
class AppMicroFetcherError(Exception):
    pass


class AppFetchServiceDataError(Exception):
    pass


# Utility functions for getting and setting values in nested objects
def get_obj_value(obj, key):
    keys = key.split('.')
    for k in keys:
        if isinstance(obj, dict):
            obj = obj.get(k)
        else:
            obj = getattr(obj, k, None)
        if obj is None:
            return None
    return obj


def set_obj_value(obj, key, value, append_if_exists=False):
    keys = key.split('.')
    for k in keys[:-1]:
        if isinstance(obj, dict):
            obj = obj.setdefault(k, {})
        else:
            if not hasattr(obj, k):
                setattr(obj, k, {})
            obj = getattr(obj, k)
    last_key = keys[-1]

    if isinstance(obj, dict):
        if append_if_exists and last_key in obj:
            if not isinstance(obj[last_key], list):
                obj[last_key] = [obj[last_key]]
            obj[last_key].append(value)
        else:
            obj[last_key] = value
    else:
        if append_if_exists and hasattr(obj, last_key):
            existing_value = getattr(obj, last_key)
            if not isinstance(existing_value, list):
                existing_value = [existing_value]
            existing_value.append(value)
            setattr(obj, last_key, existing_value)
        else:
            setattr(obj, last_key, value)


class QueryTypes(Enum):
    SIMPLE_TABLE = 'SIMPLE_TABLE'
    FUNCTION = 'FUNCTION'
    SEARCH = 'SEARCH'


class MockMicroFetcher:
    def __init__(self, data_mapping=None):
        self.data_mapping = data_mapping or {}
        self.instances = []

    def __call__(self, service_name):
        instance = MockMicroFetcherInstance(service_name, self.data_mapping)
        self.instances.append(instance)
        return instance


class MockMicroFetcherInstance:
    def __init__(self, service_name, data_mapping):
        self.service_name = service_name
        self.data_mapping = data_mapping or {}
        self.app = MagicMock()
        self.base_data = None
        self.query_type = None
        self.output_key = None
        self.fields = []
        self.table_name = None
        self.column_name = None
        self.compair_operator = None
        self.column_values = None
        self.lookup_key = None
        self.module_name = None
        self.function_params = {}
        self.search_list = None
        self.configs = None
        self.global_configs_data = {}
        self.search_configs = {}
        self.function_params = {}
        self.search_configs = {}
        self.search_list = None

    def join(self, base_data, output_key=None):
        self.base_data = base_data
        self.query_type = QueryTypes.SIMPLE_TABLE.value
        if output_key:
            output_key = output_key.split('as ')[1]
        self.output_key = "{}".format(self.service_name.split('_')[0].lower()) if not output_key else output_key
        return self

    def config(self, **configs):
        self.configs = configs
        return self

    def select(self, *args):
        self.fields = list(args)
        return self

    def filter(self, *args):
        against = args[0].split('.')
        self.compair_operator = args[1]
        self.lookup_key = args[2]
        self.column_values = set()
        if isinstance(self.base_data, dict):
            self.column_values.add(get_obj_value(self.base_data, self.lookup_key))
        else:
            data = self.base_data
            if isinstance(data, list):
                for row in data:
                    self.column_values.add(get_obj_value(row, self.lookup_key))
            else:
                self.column_values.add(get_obj_value(data, self.lookup_key))
        self.column_values = list(filter(None, self.column_values))
        if len(self.column_values) == 1:
            self.column_values = self.column_values[0]
        if len(against) != 2:
            self.column_name = against[0]
        else:
            self.table_name = against[0]
            self.column_name = against[1]
            self.fields.append(self.column_name)
        return self

    def fetch(self):
        if self.column_values or self.module_name or self.query_type == QueryTypes.SEARCH.value:
            return self._call_api()
        else:
            return self.base_data

    def execute(self):
        return self.fetch()

    def with_params(self, **kwargs):
        self.function_params = kwargs
        return self

    def from_function(self, module_name):
        self.query_type = QueryTypes.FUNCTION.value
        self.module_name = module_name
        return self

    def global_configs(self, **keywords):
        self.global_configs_data = keywords
        return self

    def feed_list(self, base_data, output_key=None):
        self.join(base_data, output_key)
        self.query_type = QueryTypes.SEARCH.value
        return self

    def search_config(self, configs):
        self.search_configs = configs
        self._prepare_search_list()
        return self

    def _prepare_search_list(self):
        output = dict()
        for index, item in enumerate(self.base_data):
            for search_column in self.search_configs.get("search_priority", []):
                sanitize = None
                if isinstance(search_column, dict):
                    search_column_name = search_column.get('key')
                    operator = search_column.get('operator') or "IN"
                    sanitize = search_column.get('sanitize')
                else:
                    search_column_name = search_column
                    operator = 'IN'

                value = item.get(search_column_name)
                if sanitize and isinstance(sanitize, list):
                    for _san in sanitize:
                        value = _san(value)

                if value:
                    if not output.get(search_column_name):
                        output[search_column_name] = dict(
                            search_key=search_column_name,
                            operator=operator,
                            inputs=dict()
                        )
                    if not output[search_column_name]['inputs'].get(value):
                        output[search_column_name]['inputs'][value] = dict(
                            indexes=[index],
                            search_value=value
                        )
                    else:
                        output[search_column_name]['inputs'][value]["indexes"].append(index)
                    break

        output = list(output.values())
        for item in output:
            item['inputs'] = list(item['inputs'].values())

        self.search_list = output

    def _call_api(self):
        # Use data_mapping to get data to merge

        # Instead of making network calls, we simulate data using data_mapping
        if self.query_type == QueryTypes.SIMPLE_TABLE.value:
            # Simulate data fetching
            # We can use data_mapping to get the data
            key = (self.service_name, self.output_key)
            data_to_merge = self.data_mapping.get(key, [])

            result = data_to_merge  # self.data_mapping.get(self.service_name, [])
        elif self.query_type == QueryTypes.FUNCTION.value:
            key = (self.service_name, self.module_name)
            data_to_merge = self.data_mapping.get(key, [])
            result = data_to_merge
        elif self.query_type == QueryTypes.SEARCH.value:
            # Simulate search
            key = (self.service_name, self.output_key)
            data_to_merge = self.data_mapping.get(key, {})

            if data_to_merge:
                if isinstance(data_to_merge, list):
                    data_to_merge = data_to_merge[0]

                for sl in self.search_list:
                    for inp in sl.get('inputs'):
                        inp.update(dict(matched_id=data_to_merge.get('id')))
                        inp.update(data_to_merge)
            result = self.search_list
        else:
            result = []
        if self.base_data is not None:
            return self._map_base(result)
        return result

    def _map_base(self, result):
        if self.query_type == QueryTypes.SEARCH.value:
            # Map search result with the original object.
            for item in result:
                for _input in item.get('inputs', []):
                    for _index in _input.get('indexes', []):
                        self.base_data[_index][self.output_key] = _input.get('matched_id')
                        append_extra = self.search_configs.get('append_extra') if isinstance(self.search_configs,
                                                                                             dict) else []
                        for _ap_col in append_extra:
                            if _input.get('matched_id'):
                                self.base_data[_index][_ap_col] = _input.get(_ap_col)
                            else:
                                self.base_data[_index][_ap_col] = self.base_data[_index].get(_ap_col)
            validation_result = []
            # for _val in result.get("validation", []):
            #     for _ind in _val.get("indexes", []):
            #         _val.pop("indexes", None)
            #         validation_result.append(dict(
            #             index=_ind,
            #             **_val
            #         ))
            return validation_result
        else:
            if isinstance(self.base_data, dict):
                for rd in result:
                    if self.base_data.get(self.lookup_key) == rd.get(self.column_name):
                        self.base_data[self.output_key] = rd
            else:
                data = self.base_data
                append_if_exists = self.configs.get("append_if_exists", False) if isinstance(self.configs,
                                                                                             dict) else False
                if isinstance(data, list):
                    for row in data:
                        for rd in result:
                            if get_obj_value(row, self.lookup_key) == rd.get(self.column_name):
                                set_obj_value(row, self.output_key, rd, append_if_exists)
                else:
                    for rd in result:
                        if get_obj_value(data, self.lookup_key) == rd.get(self.column_name):
                            set_obj_value(data, self.output_key, rd, append_if_exists)
            return self.base_data
