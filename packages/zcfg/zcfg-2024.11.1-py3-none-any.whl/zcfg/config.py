import os
import configparser
from loguru import logger


class CaseSensitiveConfigParser(configparser.RawConfigParser):

    def optionxform(self, optionstr):
        # 不转换选项名称
        return optionstr


def calculate_file_hash(file_path):
    md5_hash = round(os.path.getmtime(file_path))
    return md5_hash


class Config:

    def __init__(self, config_file: str = 'config.ini') -> None:
        if not os.path.exists(config_file):
            logger.error("config file {} is not exists", config_file)
            raise ValueError("config file {} is not exists".format(config_file))
        self.config_file_name = config_file
        cfp = CaseSensitiveConfigParser()
        cfp.read(config_file, encoding='utf-8')
        self._cfp = cfp
        self.md5_hash = calculate_file_hash(config_file)
        self.md5_dict = {}

    def file_changed(self, watch_file):
        modified_time = round(os.path.getmtime(watch_file))
        if modified_time <= self.md5_dict.get(watch_file, 0):
            return False
        self.md5_dict[watch_file] = modified_time
        return True

    def update_config(self):
        md5_hash = calculate_file_hash(self.config_file_name)
        if md5_hash == self.md5_hash:
            return False

        self.md5_hash = md5_hash
        cfp = CaseSensitiveConfigParser()
        cfp.read(self.config_file_name, encoding='utf-8')
        self._cfp = cfp
        return True

    def sections(self):
        return self._cfp.sections()

    def get_options(self, section):
        if self._cfp.has_section(section):
            return self._cfp.options(section)
        return []

    def get(self, key, default_value="") -> any:
        str_v = self.get_value(key, default_value)
        if isinstance(default_value, int):
            try:
                return int(str_v)
            except ValueError:
                logger.error("`{}` value:`{}` is not int", key, str_v)
                return default_value
        if isinstance(default_value, float):
            try:
                return float(self.get_value(key, repr(default_value)))
            except ValueError:
                logger.error("`{}` value:`{}` is not float", key, str_v)
                return default_value
        if isinstance(default_value, str):
            return str_v
        logger.error("{} type is {} not supported!", default_value, type(default_value))
        return default_value

    def get_value(self, key: str, default_value: str = None) -> str:
        """
        key的格式: section.option

        [section]
        option=value
        """
        if '.' in key:
            ll = key.split('.', maxsplit=1)
            section = ll[0]
            option = ll[1]
            if self._cfp.has_option(section, option):
                val = self._cfp.get(section, option)
                if "~" in val:
                    return os.path.expanduser(val)
                return val
            return default_value
        return default_value

    def get_intvalue(self, key: str, default_value: int = None) -> int:
        """
        key的格式: section.option

        [section]
        option=value
        """
        if '.' in key:
            ll = key.split('.', maxsplit=1)
            section = ll[0]
            option = ll[1]
            if self._cfp.has_option(section, option):
                return self._cfp.getint(section, option)
            return default_value
        return default_value

    def get_floatvalue(self, key: str, default_value: float = None) -> float:
        """
        key的格式: section.option

        [section]
        option=value
        """
        if '.' in key:
            ll = key.split('.', maxsplit=1)
            section = ll[0]
            option = ll[1]
            if self._cfp.has_option(section, option):
                return self._cfp.getfloat(section, option)
            return default_value
        return default_value

    def get_booleanvalue(self, key: str, default_value: bool = None) -> bool:
        """
        [section]
        option=value

        key的格式: section.option
        """
        if '.' in key:
            ll = key.split('.', maxsplit=1)
            section = ll[0]
            option = ll[1]
            if self._cfp.has_option(section, option):
                return self._cfp.getboolean(section, option)
            return default_value
        return default_value

    def get_list(self, key: str, default_value: list = []) -> list:
        """
        key的格式: section.option

        [section]
        option=v1,v2,v3,v4
        @return [v1, v2, v3, v4]
        """
        str_val = self.get_value(key, "")
        if not str_val:
            return default_value
        str_list = [i.strip() for i in str_val.split(",") if i.strip()]
        return str_list

    def get_floatlist(self, key: str, default_value: list = []) -> list:
        """
        key的格式: section.option

        [section]
        option=v1,v2,v3,v4
        @return [v1, v2, v3, v4]
        """
        str_val = self.get_value(key, "")
        if not str_val:
            return default_value
        str_list = [float(i.strip()) for i in str_val.split(",") if i.strip()]
        return str_list

    def get_intlist(self, key: str, default_value: list = []) -> list:
        """
        key的格式: section.option

        [section]
        option=v1,v2,v3,v4
        @return [v1, v2, v3, v4]
        """
        str_val = self.get_value(key, "")
        if not str_val:
            return default_value
        str_list = [int(i.strip()) for i in str_val.split(",") if i.strip()]
        return str_list
