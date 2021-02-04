from commands.base_command import BaseCommand
from lib.dao import Dao
from lib.notifier import Notifier

class TodayCommand(BaseCommand):
    def run(self, update, context):
        dao = Dao()
        todays_properties = dao.get_today()
        for prop in todays_properties:
            if 'title' not in prop.keys() or prop['title'] is None:
                prop['title'] = prop['url']
            update.message.reply_markdown(Notifier.get_prop_markdown(prop))
        dao.close()
