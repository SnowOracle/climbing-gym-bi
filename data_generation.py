# Corrected Data Simulation Script with Defined `visits`

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np


# Configurations
num_members = 1000  # Total members
num_customers = 10000  # Total unique customers (members + non-members)
num_non_members = num_customers - num_members

# Expanded Name Pools
american_first_names = ["James", "Michael", "Emma", "Olivia", "William", "Sophia", "Ethan", "Ava", "Benjamin", "Charlotte", "Bill", "Marshall", "Audrey", "Julia"]
chinese_first_names = ["Xiao", "Wei", "Jing", "Li", "Zhang", "Chen", "Hao", "Mei", "Yuan", "Wen", "Xia"]
international_first_names = ["Mateo", "Isabella", "Liam", "Santiago", "Amara", "Johannes", "Fatima", "Omar", "Anya", "Ivan", "Lux"]
last_names = ["Smith", "Johnson", "Lee", "Chen", "Garcia", "Schmidt", "Patel", "Nguyen", "Brown", "Takahashi", "Skleegore", "Banks", "Gates", "Aeterna"]

# Function to generate unique names
def generate_unique_names(num_people):
    first_names = (
        random.sample(american_first_names, len(american_first_names)) * (num_people // 3) +
        random.sample(chinese_first_names, len(chinese_first_names)) * (num_people // 6) +
        random.sample(international_first_names, len(international_first_names)) * (num_people // 6)
    )
    last_names_shuffled = random.sample(last_names, len(last_names)) * (num_people // len(last_names) + 1)

    random.shuffle(first_names)
    random.shuffle(last_names_shuffled)

    return [f"{first_names[i]} {last_names_shuffled[i]}" for i in range(num_people)]

# Generate Unique Customers
customer_names = generate_unique_names(num_customers)
customers = [{"customer_id": i, "name": customer_names[i - 1], "age": random.randint(5, 60)} for i in range(1, num_customers + 1)]
df_customers = pd.DataFrame(customers)

# Generate Members
members = [{"member_id": i, "customer_id": i, "name": customers[i - 1]["name"], "age": customers[i - 1]["age"],
            "join_date": (datetime.today() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
            "is_active": int(random.choices([1, 0], weights=[0.8, 0.2])[0])}
           for i in range(1, num_members + 1)]
df_members = pd.DataFrame(members)

# Generate Visits
visits = []
visit_id = 1  # Ensuring unique sequential IDs
for member in members:
    visit_count = random.randint(20, 300)  # Random visits per member
    for _ in range(visit_count):
        visits.append({
            "visit_id": visit_id,
            "member_id": member["member_id"],
            "date": (datetime.today() - timedelta(days=random.randint(1, 730))).strftime('%Y-%m-%d'),
            "time": f"{random.randint(6, 22)}:00",
            "duration": random.randint(30, 180)
        })
        visit_id += 1  # Increment visit ID
df_visits = pd.DataFrame(visits)

# Generate Day Pass Purchases
day_passes = []
day_pass_id = 1
for _ in range(random.randint(5000, 15000)):
    purchaser = random.choice(customers)
    num_passes = random.randint(1, 6)
    group_ages = [purchaser["age"]] + [random.randint(5, 60) for _ in range(num_passes - 1)]
    day_passes.append({"day_pass_id": day_pass_id, "purchaser_id": purchaser["customer_id"],
                       "date": (datetime.today() - timedelta(days=random.randint(1, 730))).strftime('%Y-%m-%d'),
                       "pass_type": random.choice(["Single", "Family", "Student"]),
                       "group_ages": ','.join(map(str, group_ages))})
    day_pass_id += 1
df_day_passes = pd.DataFrame(day_passes)

# Generate Sales
items = ['Chalk Bag', 'Shoes Rental', 'Protein Bar', 'Water Bottle', 'T-Shirt', 'Gatorade', 'Celsius']
sales = [{"sale_id": sale_id, "customer_id": customer["customer_id"],
          "member_id": next((m["member_id"] for m in members if m["customer_id"] == customer["customer_id"]), None),
          "date": (datetime.today() - timedelta(days=random.randint(1, 730))).strftime('%Y-%m-%d'),
          "item": random.choice(items), "price":"{:.2f}".format(random.uniform(5, 50))}
         for sale_id, customer in enumerate(random.choices(customers, k=random.randint(3000, 7000)), start=1)]
df_sales = pd.DataFrame(sales)
df_sales["member_id"] = df_sales["member_id"].astype("Int64")


df_sales.replace({np.inf: np.nan, -np.inf: np.nan}, inplace=True)
df_sales = df_sales.fillna(0)
# df_sales['price'] = df_sales['price'].fillna(0)  # only fill price
# but do NOT fillna() on df_sales['member_id']


# Save to CSV
df_customers.to_csv('customers.csv', index=False)
df_members.to_csv('members.csv', index=False)
df_visits.to_csv('visits.csv', index=False)
df_day_passes.to_csv('day_passes.csv', index=False)
df_sales.to_csv("sales.csv", index=False)

# # Display sample data for validation
# import ace_tools as tools
# tools.display_dataframe_to_user(name="Updated Visits Data Sample", dataframe=df_visits)

print("✅ Data generation complete: Customers, Members, Visits, Sales, and Day Passes generated.")
