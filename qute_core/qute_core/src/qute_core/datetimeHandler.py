import datetime


class DatetimeHandler(object):
    command_datetime = "%Y{0}%m{0}%d %H:%M:%S"
    command_date = "%Y{0}%m{0}%d"

    def datetime_now(self):
        return datetime.datetime.now()

    def datetime_strf(self, mark='-'):
        return self.datetime_now().strftime(self.command_datetime.format(mark))

    def datetime_strf_date(self, mark='-'):
        return self.datetime_now().strftime(self.command_date.format(mark))

    def datetime_delta(self, days=0, seconds=0, hours=0, weeks=0, mark='-', flag=True):
        new_date = self.datetime_now() + datetime.timedelta(days=days, seconds=seconds, hours=hours, weeks=weeks)
        return self.datetime_format(new_date, mark, flag)

    def datetime_format(self, date, mark, flag):
        if flag:
            return date.strftime(self.command_datetime.format(mark))
        else:
            return date.strftime(self.command_date.format(mark))
