Battery
Battery_id: int, pk
capacity (kwh): numeric 
location: Text
max_charging_rate: numeric
max_discharging_rate: numeric

History
(battery_id, timestamp): idk_what_type (tuple?), pk
battery_id: int, fk
timestamp: timestamptz
power_kw: numeric
temperature: numeric
soc_percent: numeric


Build the API and database

[X] Create the repository and Python environment
[X] Design your PostgreSQL tables yourself
[X] Build your first FastAPI endpoint
[X] Store and retrieve a single battery event


Saturday afternoon
Handle large amounts of data

[ ] Write a Python battery-data simulator
[ ] Generate 100,000 events, then scale toward 1 million
[ ] Implement batch ingestion without loading everything into memory
[ ] Measure ingestion throughput and add database indexes


Sunday morning
Implement the core algorithm

[ ] Write the charge/discharge planning algorithm
[ ] Enforce state-of-charge and backup-reserve constraints
[ ] Add fleet-level summaries and alert rules
[ ] Write tests for edge cases


Sunday afternoon
Break it, fix it, ship it

[ ] Test duplicate, invalid, and out-of-order events
[ ] Investigate slow queries and benchmark API latency
[ ] Add Docker Compose to run the system reproducibly
[ ] Write a README explaining architecture and tradeoffs