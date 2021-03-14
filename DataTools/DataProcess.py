import pandasql as ps

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
        pass