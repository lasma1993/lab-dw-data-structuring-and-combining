import pandas as pd

def preprocess_data(df):
    # Step 1: Rename columns
    df = rename_columns(df)
    
    # Step 2: Map gender values
    df = map_gender(df)
    
    # Step 3: Map state abbreviations to full names
    df = map_state(df)
    
    # Step 4: Map education values
    df = map_education(df)
    
    # Step 5: Clean customer lifetime value
    df = clean_customer_lifetime_value(df)
    
    # Step 6: Map vehicle class
    df = map_vehicle(df)
    
    # Step 7: Convert open complaints format
    df = convert_open_complaints(df)
    
    # Step 8: Drop rows with all null values
    df = drop_nulls(df)
    
    # Step 9: Fill missing values
    df = fill_na(df)
    
    # Step 10: Drop fully duplicated rows
    df = drop_duplicates(df)
    
    return df


def rename_columns(df):
    df.rename(columns={
        "Customer": "customer",
        "ST": "state",
        "GENDER": "gender",
        "Education": "education",
        "Customer Lifetime Value": "customer_lifetime_value",
        "Income": "income",
        "Monthly Premium Auto": "monthly_premium_auto",
        "Number of Open Complaints": "number_of_open_complaints",
        "Policy Type": "policy_type",
        "Vehicle Class": "vehicle_class",
        "Total Claim Amount": "total_claim_amount"
    }, inplace=True)
    return df

def map_gender(df):

    gender_mapping = {
    'F': 'F',
    'Femal': 'F',
    'female': 'F',
    'M': 'M',
    'Male': 'M'
}

    df['gender'] = df['gender'].replace(gender_mapping)
    df.gender.unique()
    return df

def map_state(df):

    state_mapping = {
    "AZ": "Arizona",
    "CA": "California",
    "WA": "Washington",
    "Cali": "California",
    "OR": "Oregon"
}
    df['state'] = df['state'].replace(state_mapping)

    return df


#Using replace function to fix value in education column
def map_education(df):

    df['education'] = df['education'].replace("Bachelors", "Bachelor")
    df.education.unique()

    return df

#Removing % symbol from customer_lifetime_value column
def clean_customer_lifetime_value(df):
    df['customer_lifetime_value'] = df['customer_lifetime_value'].astype(str) #convert to string
    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%', '') #use the str method to remove the '%' character
    df['customer_lifetime_value'] = df['customer_lifetime_value'].astype(float) #convert to float
    return df

#Using map function to fix inconsistencies in vehicle_class column
def map_vehicle(df):
    car_mapping = {
    'Luxury Car': 'Luxury',
    'Sports Car': 'Luxury',
    'Luxury SUV': 'Luxury',
}

    df['vehicle_class'] = df['vehicle_class'].replace(car_mapping)
    df.vehicle_class.unique()
    return df


#Editing the number_of_open_complaints string and converting it to numeric
def convert_open_complaints(df):
    df['number_of_open_complaints'].unique()
    df["number_of_open_complaints"] = df["number_of_open_complaints"].str.split('/').str[1]
    df['number_of_open_complaints'] = pd.to_numeric(df['number_of_open_complaints'], errors='coerce')
    df['number_of_open_complaints'].unique()
    return df


def drop_nulls(df):
    df = df.dropna(how='all')
    return df

def fill_na(df):
    df['gender'] = df['gender'].fillna('Unknown')
    df['state'] = df['state'].fillna('Unknown')
    df.gender.unique()
    customer_mean = df.customer_lifetime_value.mean()
    df['customer_lifetime_value'] = df['customer_lifetime_value'].fillna(customer_mean)
    open_complaints_mean = df.number_of_open_complaints.mean()
    open_complaints_mean
    df['number_of_open_complaints'] = df['number_of_open_complaints']. fillna(open_complaints_mean)

    return df

def drop_duplicates(df):
    df.drop_duplicates(subset=['customer'])
    return df