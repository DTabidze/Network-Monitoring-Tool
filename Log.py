import sqlite3

DB_URL = "monitoring.db"


class Log:
    @classmethod
    def create_table(cls):
        query = """
                    CREATE TABLE IF NOT EXISTS logs(
                        id INTEGER PRIMARY KEY,
                        hostname_id INTEGER,
                        time TEXT NOT NULL,
                        status TEXT NOT NULL,
                        ms REAL,
                        old_status TEXT
                    );
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.close()

    def __init__(self, time, status):
        self.time = time
        self.status = status

    @classmethod
    def display_logs(self, host_name_id):
        query = """
                    SELECT time, status, ms
                    FROM logs
                    WHERE hostname_id = ?
                    ORDER BY time DESC;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        results = cursor.execute(query, (host_name_id,)).fetchall()
        if results == None:
            print("No Logs for this Hostname")
        else:
            # Print table header
            print(" ________________________________________________ ")
            print("|         Time         |    Status    |    MS    |")
            print("|______________________|______________|__________|")

            # Print table rows
            for row in results:
                time_str = row[0]
                status_str = row[1]
                ms_str = str(row[2]) if row[2] else "None"  # Convert float to string
                print(
                    "| {}  | {}   | {} |".format(
                        time_str.ljust(14), status_str.ljust(10), ms_str.ljust(8)
                    )
                )

                # Print table footer
            print("|________________________________________________|")

    @classmethod
    def display_current_alarms(cls, user):
        counter = False
        query = """
                    SELECT id,name,hostname FROM hostnames WHERE user_id == ?;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        hosts = cursor.execute(query, (user.id,)).fetchall()
        # print(hosts)
        print(
            " ____________________________________________________________________________________"
        )
        print(
            "|              Name              |         HostName          |         ALARM         |"
        )
        print(
            "|________________________________|___________________________|_______________________|"
        )
        for host in hosts:
            # print(host[0])
            log_query = """
                            SELECT * FROM logs 
                            WHERE hostname_id == ? 
                            ORDER BY time DESC 
                            LIMIT 1;
                        """
            alarm = cursor.execute(log_query, (host[0],)).fetchone()
            if alarm[3] == "OFFLINE":
                counter = True
                print("| {:<30} | {:<25} | {:<21} |".format(host[1], host[2], alarm[3]))
            # print(alarm)
        if not counter:
            print(
                "|                                NO CURRENT ALARMS!                                  |"
            )
        print(
            "|________________________________|___________________________|_______________________|"
        )
