import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# -------------------------------------------------------
# Comprehensive Simulation Script
#   - Weighted day-of-week & time-of-day visits
#   - Active members skip day passes
#   - Use customer_id in [1..num_customers] for all Sales rows
#   - member_id=0 if not a member (never 0 for customer_id!)
# -------------------------------------------------------

# CONFIGURATIONS
num_members = 1000
num_customers = 10000

american_first_names = ["James", "Michael", "Emma", "Olivia", "William", "Sophia", "Ethan", "Ava",
                        "Benjamin", "Charlotte", "Bill", "Marshall", "Audrey", "Julia"]
chinese_first_names = ["Xiao", "Wei", "Jing", "Li", "Zhang", "Chen", "Hao", "Mei", "Yuan", "Wen", "Xia"]
international_first_names = ["Mateo", "Isabella", "Liam", "Santiago", "Amara", "Johannes", "Fatima",
                             "Omar", "Anya", "Ivan", "Lux"]
last_names = ["Smith", "Johnson", "Lee", "Chen", "Garcia", "Schmidt", "Patel", "Nguyen",
              "Brown", "Takahashi", "Skleegore", "Banks", "Gates", "Aeterna"]

def generate_unique_names(num_people):
    fn = (
        american_first_names * (num_people // 3) +
        chinese_first_names  * (num_people // 6) +
        international_first_names * (num_people // 6)
    )
    ln = last_names * (num_people // len(last_names) + 1)
    random.shuffle(fn)
    random.shuffle(ln)
    return [f"{fn[i]} {ln[i]}" for i in range(num_people)]

# 1. CREATE CUSTOMERS
customer_names = generate_unique_names(num_customers)
customers = [
    {
        "customer_id": i,
        "name": customer_names[i - 1],
        "age": random.randint(5, 60)
    }
    for i in range(1, num_customers + 1)
]
df_customers = pd.DataFrame(customers)

# 2. CREATE MEMBERS
members = []
for i in range(1, num_members + 1):
    join_date_obj = datetime.today() - timedelta(days=random.randint(30, 730))
    membership_length_days = random.randint(90, 365)
    end_date_obj = join_date_obj + timedelta(days=membership_length_days)
    is_active_flag = 1 if end_date_obj > datetime.today() else 0
    members.append({
        "member_id": i,
        "customer_id": i,  # guaranteed valid in [1..num_members]
        "name": customers[i - 1]["name"],
        "age": customers[i - 1]["age"],
        "join_date": join_date_obj.strftime('%Y-%m-%d'),
        "is_active": is_active_flag
    })
df_members = pd.DataFrame(members)

# 3. DAY-OF-WEEK & TIME-OF-DAY WEIGHTS FOR VISITS
dow_weights = {
    0: 0.9,  # Monday
    1: 0.9,  # Tuesday
    2: 1.0,  # Wednesday (Kids Club)
    3: 0.9,  # Thursday
    4: 1.2,  # Friday
    5: 2.0,  # Saturday busiest
    6: 0.6   # Sunday slower
}
total_dow_weight = sum(dow_weights.values())

time_distributions = {
    0: {  # Monday
        "morning":   (range(6, 10), 0.2),
        "afternoon": (range(10,17), 0.3),
        "evening":   (range(17,23), 0.5)
    },
    1: {  # Tuesday
        "morning":   (range(6, 10), 0.1),
        "afternoon": (range(10,17), 0.4),
        "evening":   (range(17,23), 0.5)
    },
    2: {  # Wednesday
        "morning":   (range(6, 10), 0.05),
        "afternoon": (range(10,15), 0.25),
        "kidsclub":  (range(15,20), 0.45),
        "evening":   (range(20,23), 0.25)
    },
    3: {  # Thursday
        "morning":   (range(6, 10), 0.1),
        "afternoon": (range(10,17), 0.4),
        "evening":   (range(17,23), 0.5)
    },
    4: {  # Friday
        "morning":   (range(6, 10), 0.1),
        "afternoon": (range(10,16), 0.3),
        "evening":   (range(16,23), 0.6)
    },
    5: {  # Saturday
        "morning":   (range(7, 11), 0.3),
        "afternoon": (range(11,18), 0.4),
        "evening":   (range(18,23), 0.3)
    },
    6: {  # Sunday
        "early":     (range(7, 12), 0.5),
        "afternoon": (range(12,15), 0.3),
        "evening":   (range(15,19), 0.2)
    },
}

def pick_day_of_week():
    rnd = random.random() * total_dow_weight
    cumulative = 0
    for wday, w in dow_weights.items():
        cumulative += w
        if rnd <= cumulative:
            return wday
    return 6

def pick_hour_for_day(wday):
    distribution = time_distributions[wday]
    sub_total = sum(v[1] for v in distribution.values())
    r = random.random() * sub_total
    c = 0.0
    for label, (hours_range, sub_weight) in distribution.items():
        c += sub_weight
        if r <= c:
            return random.choice(list(hours_range))
    return 12

# 4. VISITS
visits = []
visit_id = 1
start_date = datetime.today() - timedelta(days=730)

for m in members:
    total_visits = random.randint(50, 250)
    for _ in range(total_visits):
        wday = pick_day_of_week()
        while True:
            candidate_date = start_date + timedelta(days=random.randint(0, 729))
            if candidate_date.weekday() == wday:
                break
        chosen_hour = pick_hour_for_day(wday)
        visits.append({
            "visit_id": visit_id,
            "member_id": m["member_id"],
            "date": candidate_date.strftime('%Y-%m-%d'),
            "time": f"{chosen_hour}:00",
            "duration": random.randint(30, 180)
        })
        visit_id += 1
df_visits = pd.DataFrame(visits)

# 5. DAY PASS PURCHASES (Skip if membership is active)
day_passes = []
day_pass_id = 1
for _ in range(random.randint(5000, 15000)):
    purchaser = random.choice(customers)
    cust_id = purchaser["customer_id"]  # always 1..num_customers
    if cust_id <= num_members:
        if members[cust_id - 1]["is_active"] == 1:
            continue
    num_passes = random.randint(1, 6)
    group_ages = [purchaser["age"]] + [random.randint(5, 60) for _ in range(num_passes - 1)]
    purchase_date = datetime.today() - timedelta(days=random.randint(1, 730))
    day_passes.append({
        "day_pass_id": day_pass_id,
        "purchaser_id": cust_id,  # valid in [1..num_customers]
        "date": purchase_date.strftime('%Y-%m-%d'),
        "pass_type": random.choice(["Single", "Family", "Student"]),
        "group_ages": ",".join(map(str, group_ages))
    })
    day_pass_id += 1
df_day_passes = pd.DataFrame(day_passes)

# 6. SALES
items = ['Chalk Bag', 'Shoes Rental', 'Protein Bar', 'Water Bottle', 'T-Shirt', 'Gatorade', 'Celsius']
sales_list = []
sale_id = 1
for _ in range(random.randint(3000, 7000)):
    # pick a valid customer
    cust = random.choice(customers)
    # if they are a member, store that ID, else 0
    if cust["customer_id"] <= num_members:
        mid = cust["customer_id"]
    else:
        mid = 0
    sales_list.append({
        "sale_id": sale_id,
        "customer_id": cust["customer_id"],  # always valid
        "member_id": mid,
        "date": (datetime.today() - timedelta(days=random.randint(1, 730))).strftime('%Y-%m-%d'),
        "item": random.choice(items),
        "price": "{:.2f}".format(random.uniform(5, 50))
    })
    sale_id += 1
df_sales = pd.DataFrame(sales_list)

# Convert to proper numeric & handle infinities
df_sales.replace({np.inf: np.nan, -np.inf: np.nan}, inplace=True)
df_sales["price"] = pd.to_numeric(df_sales["price"], errors="coerce").fillna(0).round(2)

# Optional: Ensure no blank strings in member_id
df_sales["member_id"] = df_sales["member_id"].astype(int)

# 7. SAVE CSVs
df_customers.to_csv("customers.csv", index=False)
df_members.to_csv("members.csv", index=False)
df_visits.to_csv("visits.csv", index=False)
df_day_passes.to_csv("day_passes.csv", index=False)
df_sales.to_csv("sales.csv", index=False)

print("✅ Data generation complete, guaranteed valid customer_id references. No foreign key conflicts.")
