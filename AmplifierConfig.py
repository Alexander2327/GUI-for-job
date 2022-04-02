import copy
from math import log
import os.path


class AmplifierConfig:
    def __init__(self, modification, sn):
        self.__file_name = '__Config_Write_XXX_'
        self.mod = modification
        self.sn = sn
        self.u_drv = 30
        self.i_op = 650
        self.i_eol = 661
        self.nf = 4.35
        self.u_drv_corr = 0

    def found_error(self):
        """Функция проверки наличия
                файла в директории"""
        is_exist = os.path.exists(
            fr"C:\Users\danil\OneDrive\Документы\ZOC7 Files\ComSet_for_UI\{self.__file_name[0:15]}{self.sn}.txt")
        return is_exist

    def delete_file(self):
        """Функция удаления файла,
                если он есть в директории"""
        if self.found_error:
            os.remove(
                fr"C:\Users\danil\OneDrive\Документы\ZOC7 Files\ComSet_for_UI\{self.__file_name[0:15]}{self.sn}.txt")
            print('Файл успешно удален')

    @staticmethod
    def open_for_read(mod):
        """Функция открытия и чтения конфиг файлов 15 и 19,
                при создании файлов конфигурации"""
        config_dict1 = {}
        with open(
                fr"C:\Users\danil\OneDrive\Документы\ZOC7 Files\ComSet_for_UI\__Config_Write_XXX_{mod}.txt",
                encoding='UTF-8') as config_file:
            for row in config_file:
                (key, val) = row.split(' ')
                try:
                    config_dict1[key] = int(val)
                except ValueError:
                    config_dict1[key] = val.strip()
            return config_dict1

    def read_config_file(self):
        """Функция считывания файла
                конфигурации в словарь"""
        config_dict = {}
        if self.mod == 15 and self.found_error() is False:
            return self.open_for_read(self.mod)
        elif self.mod == 19 and self.found_error() is False:
            return self.open_for_read(self.mod)
        elif self.mod in (15, 19) and self.sn is not None and self.found_error() is True:
            with open(
                    fr'C:\Users\danil\OneDrive\Документы\ZOC7 Files\ComSet_for_UI\{self.__file_name[0:15]}{self.sn}.txt',
                    encoding='UTF-8') as config_file:
                for row in config_file:
                    (key, val) = row.split(' ')
                    try:
                        config_dict[key] = int(val)
                    except ValueError:
                        config_dict[key] = val.strip()
                return config_dict
        else:
            print('Некорректно указана модификация изделия.')

    def get_config_value(self, key):
        """Функция возвращает значение
                            файла по ключу"""
        return self.read_config_file()[key]

    def new_config_dict(self, **kwargs):
        """Функция считывает файл и
            переписывает значения по ключу,
                и возвращает новый словарь"""
        old_config_dict = self.read_config_file()
        new_config_dict = copy.deepcopy(old_config_dict)
        for key, value in kwargs.items():
            for old_key in old_config_dict.keys():
                if key == old_key:
                    new_config_dict[key] = value
        return new_config_dict

    def write_config_file(self, new_dict):
        """Функция создает новый файл, если его нет
                            или пересохраняет старый"""
        with open(
                fr'C:\Users\danil\OneDrive\Документы\ZOC7 Files\ComSet_for_UI\{self.__file_name[0:15]}{self.sn}.txt',
                'w', encoding='UTF-8') as new_config_file:
            for key, value in new_dict.items():
                if key == 'SN':
                    new_config_file.write(f'{key} {f"{value:03d}"}\n')
                elif key == 'AMPSETUP':
                    new_config_file.write(f'{key} {value}\n')
                    new_config_file.write('AMPSETUP 3278\n')
                else:
                    new_config_file.write(f'{key} {value}\n')
            new_config_file.write('AMPSETUP OFF\n')

    def dacsp_calc(self):
        """Функция расчета ошибки драйвера"""
        DACSP = int(2650 - self.u_drv / 0.8 + 0.5)
        return DACSP

    def dacsp_corr(self, u_drv_corr):
        if u_drv_corr > 0.4:
            new_DACSP = self.get_config_value('DACSP') - int(u_drv_corr / 0.8 + 0.5)
            self.write_config_file(self.new_config_dict(DACSP=new_DACSP))
        elif u_drv_corr < -0.4:
            new_DACSP = self.get_config_value('DACSP') - int(u_drv_corr / 0.8 - 0.5)
            self.write_config_file(self.new_config_dict(DACSP=new_DACSP))

    def eol_calc(self):
        """Функция расчета максиального тока"""
        if self.i_eol < 758:
            EOL = int(round(self.i_eol / 0.185033 - 6.396, 0))
            return EOL
        elif self.i_eol >= 758:
            EOL = 4090
            return EOL

    def nf_calc(self):
        """Функция расчета уровня шума"""
        NF = int(round(10 ** (self.nf / 10) * 10000, 0))
        return NF


class LineAmplifierConfig(AmplifierConfig):
    def __init__(self, sn):
        self.sn = sn
        AmplifierConfig.__init__(self, modification=19, sn=self.sn)
        self.tap_in_line = -6.27
        self.tap_out_line = 18.65
        self.pd_in_line = -35.10
        self.pd_out_line = -2.03

    def tap_in_line_calc(self):
        TAP_IN_IL_line = int(
            round((10 ** ((10 * log((71285303 / 10 ** 6), 10) + (-6.1 - self.tap_in_line)) / 10)) * 10 ** 6, 0))
        return TAP_IN_IL_line

    def tap_out_line_calc(self):
        TAP_OUT_IL_line = int(
            round((10 ** ((10 * log(121338885 / 10 ** 6, 10) - (18.97 - self.tap_out_line)) / 10)) * 10 ** 6, 0))
        return TAP_OUT_IL_line

    def pd_in_line_calc(self, dlevel):
        B_PD_IN_line = int(round((10.729691 - (
                10 ** ((-35.1 - 10 * log(dlevel / 10 ** 6, 10)) / 10) - 10 ** (
                (self.pd_in_line - 10 * log(dlevel / 10 ** 6, 10)) / 10)) * 1000000) * 1000000, 0))
        return B_PD_IN_line

    def pd_out_line_calc(self, dlevel):
        B_PD_OUT_line = int(
            round(-(-2624.13 - (10 ** ((-2.03 - 10 * log(dlevel / 10 ** 6, 10)) / 10) - 10 ** (
                    (self.pd_out_line - 10 * log(dlevel / 10 ** 6, 10)) / 10)) * 1000000) * 100, 0))
        return B_PD_OUT_line


class PreAmplifierConfig(AmplifierConfig):
    def __init__(self, sn):
        self.sn = sn
        AmplifierConfig.__init__(self, modification=15, sn=self.sn)
        self.tap_in_pre = -10.27
        self.tap_out_pre = 14.00
        self.pd_in_pre = -35.10
        self.pd_out_pre = -2.03

    def tap_in_pre_calc(self):
        TAP_IN_IL_pre = int(
            round((10 ** ((10 * log((35727283 / 10 ** 6), 10) + (-10.1 - self.tap_in_pre)) / 10)) * 10 ** 6, 0))
        return TAP_IN_IL_pre

    def tap_out_pre_calc(self):
        TAP_OUT_IL_pre = int(
            round((10 ** ((10 * log(60813500 / 10 ** 6, 10) - (14.97 - self.tap_out_pre)) / 10)) * 10 ** 6, 0))
        return TAP_OUT_IL_pre

    def pd_in_pre_calc(self, dlevel):
        B_PD_IN_pre = int(
            round((10.729691 - (10 ** ((-35.1 - 10 * log(dlevel / 10 ** 6, 10)) / 10) - 10 ** (
                    (self.pd_in_pre - 10 * log(dlevel / 10 ** 6, 10)) / 10)) * 1000000) * 1000000, 0))
        return B_PD_IN_pre

    def pd_out_pre_calc(self, dlevel):
        B_PD_OUT_pre = int(
            round(-(-2624.13 - (10 ** ((-2.03 - 10 * log(dlevel / 10 ** 6, 10)) / 10) - 10 ** (
                    (self.pd_out_pre - 10 * log(dlevel / 10 ** 6, 10)) / 10)) * 1000000) * 100, 0))
        return B_PD_OUT_pre
