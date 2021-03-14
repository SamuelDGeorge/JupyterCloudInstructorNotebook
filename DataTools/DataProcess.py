import pandasql as ps
import pandas as pd
import datetime

class DataProcess:
    
    def __init__(self, event_frame):
        self.event_frame = event_frame

    def userActivity(self):
        event_table = self.event_frame.copy()
        sql = """
            SELECT 
                user as USER,
                COUNT(activity) as USER_EVENTS
            from event_table
            GROUP BY user
            ORDER BY USER_EVENTS DESC
        """
        out = ps.sqldf(sql, locals())
        return out

    def eventFrequency(self):
        event_table = self.event_frame.copy()
        sql = """
        SELECT 
            activity as ACTIVITY,
            COUNT(*) as TOTAL_VISITS
        from event_table
        GROUP BY activity
        ORDER BY TOTAL_VISITS DESC
        """
        out = ps.sqldf(sql, locals())
        return out

    def eventUserFrequency(self):
        event_table = self.event_frame.copy()
        sql = """
            SELECT 
                activity as ACTIVITY,
                COUNT(DISTINCT user) as DISTINCT_USERS_TO_VISIT
            from event_table
            GROUP BY activity
            ORDER BY DISTINCT_USERS_TO_VISIT DESC
        """
        out = ps.sqldf(sql, locals())
        return out

    def userAverageTimeBetweenEvents(self):
        event_table = self.event_frame.copy()
        all_users = []
        users = pd.unique(event_table['user'])
        for i in users:
            user_table = event_table.loc[event_table['user'] == i]
            sql = """
                SELECT 
                    *
                from user_table
                ORDER BY timestamp ASC
            """
            out = ps.sqldf(sql, locals())
            out['timestamp'] = pd.to_datetime(out['timestamp'], 
                                        format="%Y-%m-%d %H:%M:%S")
            time_array = []
            for j in range(0,out.shape[0]):
                v = out.iloc[j]
                current_timestamp = v['timestamp']
                if j + 1 < out.shape[0]:
                    next_timestamp = out.iloc[j + 1]['timestamp']
                    distance = next_timestamp - current_timestamp
                    time_array.append(distance)
            
            if len(time_array) > 0:
                avg = sum(time_array,datetime.timedelta())/len(time_array)
                all_users.append(
                    {'USER': i,
                    'AVERAGE_TIME_BETWEEN_ACTIVITIES': avg}
                )
        to_return = pd.DataFrame.from_dict(all_users)
        to_return = to_return.sort_values(by='AVERAGE_TIME_BETWEEN_ACTIVITIES', ascending=False)
        return to_return

    def userTotalTimeOnEvents(self):
        event_table = self.event_frame.copy()
        all_users = []
        users = pd.unique(event_table['user'])
        for i in users:
            user_table = event_table.loc[event_table['user'] == i]
            sql = """
                SELECT 
                    *
                from user_table
                ORDER BY timestamp ASC
            """
            out = ps.sqldf(sql, locals())
            out['timestamp'] = pd.to_datetime(out['timestamp'], 
                                        format="%Y-%m-%d %H:%M:%S")
            time_array = []
            for j in range(0,out.shape[0]):
                v = out.iloc[j]
                current_timestamp = v['timestamp']
                if j + 1 < out.shape[0]:
                    next_timestamp = out.iloc[j + 1]['timestamp']
                    distance = next_timestamp - current_timestamp
                    time_array.append(distance)
            
            if len(time_array) > 0:
                s = sum(time_array,datetime.timedelta())
                all_users.append(
                    {'USER': i,
                    'TOTAL_TIME_ON_ACTIVITIES': s}
                )
        to_return = pd.DataFrame.from_dict(all_users)
        to_return = to_return.sort_values(by='TOTAL_TIME_ON_ACTIVITIES', ascending=False)
        return to_return