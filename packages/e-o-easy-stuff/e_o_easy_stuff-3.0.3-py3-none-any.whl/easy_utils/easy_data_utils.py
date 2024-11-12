class EasyDataUtils:
    def __init__(self):
        pass

    @staticmethod
    def name_to_pascal_case(name: str) -> str:
        return (name[0].upper() + name[1:]).strip()

    @staticmethod
    def name_to_pascal_case_between_dots(name: str) -> str:
        return '.'.join([EasyDataUtils.name_to_pascal_case(x) for x in name.split('.')])

    @staticmethod
    def names_to_pascal_case_from_dict(record: dict) -> dict:
        return {EasyDataUtils.name_to_pascal_case_between_dots(key): value for key, value in record.items()}

    @staticmethod
    def flatten_record(record: dict):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '.')
            else:
                out[name[:-1]] = x

        flatten(record)

        return out
