# RSS-Parser
A sample implementation of parsing RSS contents and storing it in an RDBS using BeautifulSoup

## Steps to execute:
    1) Clone the Repository: git clone https://github.com/vintageplayer/RSS-Parser.git
    2) cd RSS-Parser && chmod +x start.sh
    3) ./start.sh
    4) chmod +x check_db_status.sh
    5) ./check_db_status.sh

You can run `./check_db_status.sh` to retrieve the current number of records in the respective tables.
The python scheduler will run every 12 hours and update the new records in the database.

## Requirements
Current Version of docker installed
