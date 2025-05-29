# Climbing Gym Business Intelligence System

A comprehensive business intelligence system for climbing gyms that simulates and analyzes customer data, membership information, visits, day passes, and sales.

## Overview

This project provides tools for:
1. Generating realistic simulated data for a climbing gym business
2. Managing and inserting data into a SQL Server database
3. Running business intelligence queries for data analysis
4. Visualizing key performance indicators

## Features

- **Data Simulation**: Generate realistic customer, member, visit, day pass, and sales data
- **Database Integration**: Store and manage data in SQL Server
- **Business Intelligence**: SQL queries to extract valuable insights including:
  - Member activity analysis
  - Visit patterns and duration
  - Sales and revenue reporting
  - Customer segmentation
  - Day pass vs. membership usage
- **Sample Data**: Includes pre-generated CSV files as working examples (customers, members, visits, day passes, sales)

## Tech Stack

- Python 3.x
- Pandas for data manipulation
- pyODBC for SQL Server connectivity
- SQL Server database

## Setup

### Prerequisites

- Python 3.x
- SQL Server instance (local or remote)
- Required Python packages: pandas, numpy, pyodbc

### Database Configuration

Configure your database connection in `test_db.py`:

```python
server = '127.0.0.1'  # Your SQL Server instance
port = '1433'
database = 'test_db'  # Target database
username = 'climbing_user'  # SQL Server user
password = 'hoosierheights'  # Password
driver = '/opt/homebrew/lib/libtdsodbc.so'  # Driver path
```

## Usage

### Data Generation

Generate sample data:

```bash
python data_generation_2.py
```

### Database Operations

Insert data into the database:

```bash
python data_insert_handling_2.py
```

Clear tables if needed:

```bash
python truncate_tables.py
```

### Running Queries

The `queries` folder contains various SQL queries for business analysis:

- `active_vs_inactive_members.sql` - Compare active vs. inactive member statistics
- `average_days_between_visits.sql` - Calculate average time between member visits
- `buyers_who_never_visited.sql` - Identify customers who purchased but never visited
- `day_pass_vs_member_usage.sql` - Compare day pass vs. membership usage patterns
- `members_by_age_group.sql` - Segment members by age groups
- `revenue_by_month.sql` - Track monthly revenue
- And more...

## Project Structure

```
climbing_BI/
├── data_generation.py         # Initial data generation script
├── data_generation_2.py       # Enhanced data generation script
├── data_insert_handling.py    # Initial data insertion script
├── data_insert_handling_2.py  # Enhanced data insertion script
├── main.py                    # Entry point
├── query_writer.py            # Utility for writing SQL queries
├── test_db.py                 # Database connection testing
├── truncate_tables.py         # Utility to clear database tables
├── queries/                   # SQL queries for analysis
│   ├── active_vs_inactive_members.sql
│   ├── average_days_between_visits.sql
│   ├── ...
├── *.csv                      # Generated data files
```

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contact

Your Name - [Your Email or LinkedIn] 