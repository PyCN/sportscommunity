# coding=utf-8
import _env  # noqa
import datetime
import os
from solo.config import TEMP_FILE_PATH


class DateTime(object):

    date_format = '%Y-%m-%d'
    time_format = '%Y-%m-%d %H:%M:%S'

    @property
    def current_time(self):
        return datetime.datetime.now().strftime(DateTime.time_format)

    @property
    def today(self):
        return datetime.date.today().strftime(DateTime.date_format)

    @classmethod
    def get_day(cls, days):
        return (datetime.date.today() - datetime.timedelta(days=int(days))).strftime(cls.date_format)

    @classmethod
    def get_day_date(cls, days):
        return datetime.date.today() - datetime.timedelta(days=int(days))

    @staticmethod
    def datetime_str(date, format):
        return datetime.datetime.strftime(date, format)

    @staticmethod
    def str_datetime(date, format):
        return datetime.datetime.strptime(date, format)


class ChoiceMapping(object):
    """
      DisplayString  StoreInt mapping
      Those choices named by <FIELD_NAME>_CHOICE
    """

    def get_choice_to_store(self, choice_name, choice_string):
        name  = choice_name.upper()
        if hasattr(self, name):
            try:
                value = getattr(self, name)[choice_string]
            except KeyError:
                return None
            return value


    def get_choice_to_display(self, choice_name, choice_key):
        name  = choice_name.upper()
        if not choice_key:
            return None
        if hasattr(self, name):
            keys = getattr(self, name)
            for i in keys:
                if keys[i] == choice_key:
                    return i
            return None


class EnumMap(object):

    @staticmethod
    def enum(*sequential, **named):
        enums = dict(zip(sequential, range(1, (len(sequential)+1))), **named)
        reverse_enums = dict((value, key) for key, value in enums.iteritems())
        enums['display'] = reverse_enums
        return type('Enum', (), enums)


class Tools(object):

    @staticmethod
    def str_to_class(class_name):
        return globals()[class_name]

    @staticmethod
    def report_tmp_file(file_name, cookie):
        file_floder = os.path.join(TEMP_FILE_PATH, 'temporary')
        if not os.path.isdir(file_floder):
            os.mkdir(file_floder)
        return '{0}/{1}_{2}.csv'.format(file_floder, cookie, file_name)

    @staticmethod
    def report_tmp_file_delete(f):
        if os.path.exists(f):
            os.remove(f)
        return True
