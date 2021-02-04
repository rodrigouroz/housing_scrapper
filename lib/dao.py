import logging
import time
import sqlite3

class Dao:
    def __init__(self):
        self.connection = sqlite3.connect('properties.db')
        self.connection.row_factory = self.__row_factory

    def __row_factory(self, cursor, row):
        output = {}
        for index, column in enumerate(cursor.description):
            output[column[0]] = row[index]
        return output

    def __run_select(self, stmt, params):
        cursor = self.connection.cursor()
        cursor.execute(stmt, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_property(self, property):
        stmt = 'SELECT * FROM properties WHERE internal_id=:internal_id AND provider=:provider LIMIT 1'
        result = self.__run_select(stmt, {'internal_id': property['internal_id'], 'provider': property['provider']})
        return next(iter(result), None)

    def register_property(self, property):
        stmt = 'INSERT INTO properties (internal_id, provider, url, title) VALUES (:internal_id, :provider, :url, :title)'
        try:
            self.connection.execute(stmt, property)
            self.connection.commit()
        except Exception as e:
            logging.error(e)
            self.connection.rollback()

    def get_today(self):
        stmt = "SELECT * FROM properties WHERE captured_date >= datetime(:today_date, 'unixepoch')"
        last_day_epoch = time.time() - 24 * 3600
        return self.__run_select(stmt, {"today_date": last_day_epoch})

    def get_pending_to_notify(self):
        stmt = "SELECT * FROM properties WHERE notified_date IS NULL ORDER BY captured_date DESC LIMIT 10;"
        return self.__run_select(stmt, {})

    def mark_as_notified(self, prop):
        current_timestamp = time.time()
        stmt = "UPDATE properties SET notified_date = :current_timestamp WHERE internal_id = :internal_id AND provider = :provider;"
        try:
            self.connection.execute(stmt, {
                'internal_id': prop['internal_id'],
                'provider': prop['provider'],
                'current_timestamp': current_timestamp
            })
            self.connection.commit()
        except Exception as e:
            logging.error(e)
            self.connection.rollback()

    def delete(self, prop):
        stmt = 'DELETE FROM properties WHERE internal_id = :internal_id AND provider = :provider;'
        try:
            self.connection.execute(stmt, {'internal_id': prop['internal_id'], 'provider': prop['provider']})
            self.connection.commit()
        except Exception as e:
            logging.error(e)
            self.connection.rollback()

    def close(self):
        self.connection.close()
