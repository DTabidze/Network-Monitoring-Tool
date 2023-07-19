import sqlite3
import threading
import time
import ping3
from datetime import datetime
from Log import Log
import colorama
from colorama import Fore

DB_URL = "monitoring.db"


class Hostname:
    # running_thread = True

    @classmethod
    def create_table(cls):
        query = """
                    CREATE TABLE IF NOT EXISTS hostnames(
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        hostname TEXT NOT NULL,
                        type TEXT NOT NULL,
                        user_id INTEGER,
                        log_id INTEGER,
                        status TEXT,
                        notification TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(log_id) REFERENCES logs(id)
                    );
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.close()

    def __init__(self, name, hostname, type, id=None):
        self.name = name
        self.hostname = hostname
        self.type = type

    def add_host(self, user):
        query = """
                    INSERT INTO hostnames(name,hostname,type,user_id) values(?,?,?,?);
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(query, (self.name, self.hostname, self.type, user.id))
        conn.commit()
        self.id = result.lastrowid
        print("Host Added Succesfully!")
        conn.close()

    @classmethod
    def remove_host(cls, user, name):
        if threading.active_count() > 1:
            print("Waiting for the ping check process to complete...")
            time.sleep(60)
        query = """
            DELETE FROM hostnames WHERE name == ? and user_id == ?;
        """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query, (name, user.id))
        rows_deleted = cursor.rowcount
        conn.commit()
        conn.close()
        if rows_deleted > 0:
            print(f"Host '{name}' removed successfully!")
        else:
            print(f"No host found with name '{name}' for the user.")

    @staticmethod
    def ping_check():
        while True:
            # Retrieve hostnames associated with the user from the database
            query = """
                        SELECT * FROM hostnames;
                    """
            conn = sqlite3.connect(DB_URL)
            cursor = conn.cursor()
            result = cursor.execute(query).fetchall()
            # print(result)
            hostnames = [row[2] for row in result]
            types = [row[3] for row in result]
            ids = [row[0] for row in result]
            # print(ids, hostnames, types)
            conn.close()

            query = """
                        INSERT INTO logs(hostname_id,time,status,ms,old_status) values(?,?,?,?,?);
                    """
            conn = sqlite3.connect(DB_URL)
            cursor = conn.cursor()

            for id, hostname, type in zip(ids, hostnames, types):
                # get previous status for host
                old_query = """
                                SELECT status
                                FROM logs
                                WHERE hostname_id = ?
                                ORDER BY time DESC
                                LIMIT 1;
                            """
                cursor.execute(old_query, (id,))
                result = cursor.fetchone()
                previous_status = result[0] if result else None

                # print(id, hostname, type)
                if type == "ICMP":
                    try:
                        response_time = ping3.ping(hostname)
                        # print(response_time)
                        if isinstance(response_time, (float, int)):
                            if previous_status == "OFFLINE" and previous_status != None:
                                print(f"HOST {hostname} STATUS BECAME ONLINE")

                            current_datetime = datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                            cursor.execute(
                                query,
                                (
                                    id,
                                    current_datetime,
                                    "ONLINE",
                                    "%.4f" % response_time,
                                    previous_status,
                                ),
                            )
                        else:
                            if previous_status != "OFFLINE" and previous_status != None:
                                print(f"HOST {hostname} WENT DOWN!!!")
                            cursor.execute(
                                query,
                                (
                                    id,
                                    current_datetime,
                                    "OFFLINE",
                                    None,
                                    previous_status,
                                ),
                            )
                            # print(f"No response from {hostname}")
                    except OSError as e:
                        # print(f"Error pinging host: {hostname} - {str(e)}")
                        if previous_status != "OFFLINE" and previous_status is not None:
                            print(f"HOST {hostname} WENT DOWN!!!")
                        cursor.execute(
                            query,
                            (id, current_datetime, "OFFLINE", None, previous_status),
                        )
                else:
                    print(f"Unsupported type for {hostname}")
                conn.commit()
            # # Sleep for 60 seconds between checks
            conn.close()
            time.sleep(60)

    @classmethod
    def start_ping_check(cls):
        # Start the ping_check method as a background thread
        # cls.running_thread = True
        thread = threading.Thread(target=cls.ping_check)
        thread.daemon = True  # Set the thread as a daemon thread
        thread.start()

    # @classmethod
    # def kill_thread(cls):
    #     cls.running_thread = False

    @classmethod
    def select_host(cls, user, host_name):
        query = """
                    SELECT * FROM hostnames WHERE hostnames.name == ? and hostnames.user_id == ?;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(query, (host_name, user.id)).fetchone()
        if result is None:
            print("Invalid Host Name!!!")
        else:
            Log.display_logs(result[0])

    @classmethod
    def display_hosts(cls, user):
        colorama.init()
        query = """
                    SELECT * FROM hostnames WHERE hostnames.user_id == ?;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        hosts_results = cursor.execute(query, (user.id,)).fetchall()
        print(
            " _________________________________________________________________________________________________________________"
        )
        print(
            "|             Nname              |          Hostname         |  TYPE  |   Last Online Time  |  Last Offline Time  |"
        )
        print(
            "|_________________________________________________________________________________________________________________|"
        )
        for host in hosts_results:
            query = """
                        SELECT time,status 
                        FROM logs 
                        WHERE hostname_id == ?
                        ORDER BY time DESC;
                    """
            log_result = cursor.execute(query, (host[0],)).fetchall()
            counter = 0
            if log_result:
                last_active_time = None
                last_inactive_time = None
                for log in log_result:
                    status = log[1]
                    if status == "ONLINE" and not last_active_time:
                        if counter == 0:
                            last_active_time = (
                                "\033[32m" + "ONLINE".ljust(19) + "\033[0m"
                            )
                            # last_active_time = f"{Fore.GREEN}ONLINE{Fore.RESET}"
                        else:
                            last_active_time = log[0]
                    elif status == "OFFLINE" and not last_inactive_time:
                        if counter == 0:
                            last_inactive_time = (
                                "\033[31m" + "OFFLINE".ljust(19) + "\033[0m"
                            )
                            # last_inactive_time = f"{Fore.RED}OFFLINE{Fore.RESET}"
                        else:
                            last_inactive_time = log[0]
                        # last_inactive_time = log[0]
                    counter += 1
                    if last_active_time and last_inactive_time:
                        break
                if last_active_time == None:
                    last_active_time = "NO DATA"
                if last_inactive_time == None:
                    last_inactive_time = "NO DATA"
                print(
                    "| {:<30} | {:<25} | {:<6} | {:<19} | {:<19} |".format(
                        host[1],
                        host[2],
                        host[3],
                        last_active_time.ljust(19, " ")
                        if last_active_time != "ONLINE"
                        else last_active_time,
                        last_inactive_time.ljust(19, " ")
                        if last_inactive_time != "NO DATA"
                        else last_inactive_time,
                    )
                )

        print(
            "|_________________________________________________________________________________________________________________|"
        )
