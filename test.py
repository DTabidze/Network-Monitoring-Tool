import ping3

timeout = 1

iplist = ["8.8.8.8", "8.8.4.4", "www.facebook.com", "www.google.com", "1.2.3.4"]


timeout = 1
ping_count = 1  # Number of pings to send

iplist = ["8.8.8.8", "8.8.4.4", "www.facebook.com", "www.google.com", "1.2.3.4"]


def ping_host():
    for host in iplist:
        total_response_time = 0
        successful_pings = 0

        for _ in range(ping_count):
            response_time = ping3.verbose_ping(host, ping_count)
            if response_time is not None:
                total_response_time += response_time
                successful_pings += 1
        print(response_time)
        if successful_pings > 0:
            average_response_time = total_response_time / successful_pings
            print(
                f"Average ping response time for {host}: {average_response_time:.2f} ms"
            )
        else:
            print(f"No response from {host}")


# Example usage
ping_host()  # Ping Google's public DNS server
|         Time        |    Status  |    MS    |
| 2023-07-18 18:28:08 | ACTIVE     | 0.0725   |

 _________________________________________________________________________________________________________
|              Nname              |        Hostname      | TYPE |  Last Active Time  |   Last Down Time   |
|_________________________________________________________________________________________________________|
|                                 |                      |      |                    |                    |

Google DNS   8.8.8.8    ICMP   2023-07-18 21:36:54   2023-07-18 18:35:49
Flatiron   71.190.177.64   ICMP   2023-07-18 21:36:54   2023-07-18 18:35:49
My Phone   10.129.2.50   ICMP   2023-07-18 18:35:49   2023-07-18 21:36:54
Mordechai   10.129.3.10   ICMP   2023-07-18 21:26:12   2023-07-18 21:36:54
Avi   10.129.3.1   ICMP   2023-07-18 21:33:51   2023-07-18 21:36:54
Alice   10.129.2.51   ICMP   2023-07-18 18:28:08   2023-07-18 21:36:54
MyPhone Home   192.168.1.157   ICMP   2023-07-18 21:37:11   2023-07-18 21:33:51

SELECT * FROM logs WHERE hostname_id == 1 ORDER BY time DESC LIMIT 1;

|______________________|________________________|_____________________|
| FACEBOOK             | www.facebook.com       | OFFLINE             |
|                         NO CURRENT ALARMS!                          |

595, 10, '2023-07-19 15:11:48', 'OFFLINE', None, 'OFFLINE'

| Mordechai                      | 10.129.3.10               | OFFLINE               |
| Avi                            | 10.129.3.1                | OFFLINE               |
| Alice                          | 10.129.2.51               | OFFLINE               |
|________________________________|___________________________|_______________________|