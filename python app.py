import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Constants
NUM_RECORDS = 10000
CURRENT_YEAR = 2024

# Departments and roles with job levels
departments = {
    'HR': {
        'roles': ['HR Specialist', 'HR Manager', 'HR Director'],
        'levels': [1, 3, 5]
    },
    'R&D': {
        'roles': ['Research Scientist', 'Senior Researcher', 'R&D Manager', 'Director of R&D'],
        'levels': [1, 2, 4, 5]
    },
    'Sales': {
        'roles': ['Sales Executive', 'Sales Manager', 'Sales Director'],
        'levels': [1, 3, 5]
    }
}

education_fields = [
    'Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Other'
]

marital_statuses = ['Single', 'Married', 'Divorced']

business_travel_options = ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']

work_life_balance_scores = [1, 2, 3, 4]

satisfaction_scores = [1, 2, 3, 4]

performance_ratings = [1, 2, 3, 4, 5]

# Helper Functions

def weighted_choice(choices, weights):
    return np.random.choice(choices, p=weights)

def generate_gender():
    return weighted_choice(['Female', 'Male', 'Non-Binary'], [0.45, 0.53, 0.02])

def generate_department():
    # Rough realistic distribution of employees
    return weighted_choice(list(departments.keys()), [0.2, 0.5, 0.3])

def generate_job_role_and_level(dept):
    roles = departments[dept]['roles']
    levels = departments[dept]['levels']
    
    # Generate descending preference scores (e.g. more weight to entry roles)
    raw_probs = np.linspace(0.5, 0.1, len(roles))[::-1]
    probs = raw_probs / raw_probs.sum()  # Normalize to sum to 1
    
    role = np.random.choice(roles, p=probs)
    idx = roles.index(role)
    level = levels[idx]
    return role, level


def generate_hire_date():
    # Higher probability for recent years (2010-2024)
    years = list(range(2010, CURRENT_YEAR + 1))
    weights = np.array([0.03] * len(years))
    # Increase weight for recent years exponentially
    weights = weights * np.exp(np.linspace(0, 3, len(years)))
    weights /= weights.sum()
    year = weighted_choice(years, weights)
    # Random month/day
    month = np.random.randint(1, 13)
    day = np.random.randint(1, 29)  # To avoid invalid dates
    return datetime(year, month, day)

def generate_termination_date(hire_date, attrition):
    if not attrition:
        return None
    
    min_term_date = hire_date + timedelta(days=180)
    max_term_date = datetime(2024, 12, 31)

    # If employee was hired too late (e.g., in Dec 2024), they can't be terminated within data range
    if min_term_date >= max_term_date:
        return None
    
    delta_days = (max_term_date - min_term_date).days

    # Safety check to avoid ValueError
    if delta_days <= 0:
        return None

    term_date = min_term_date + timedelta(days=np.random.randint(0, delta_days))
    return term_date


def generate_years_diff(start_date, end_date):
    if end_date is None:
        end_date = datetime.now()
    return max(0, (end_date - start_date).days // 365)

def generate_education(level):
    # Higher job level correlates to higher education
    # Level 1: mostly bachelors or less; Level 5: mostly masters/PhD
    ed_probs = {
        1: [0.5, 0.3, 0.1, 0.1, 0.0],  # High School to PhD
        2: [0.3, 0.4, 0.15, 0.1, 0.05],
        3: [0.1, 0.3, 0.4, 0.15, 0.05],
        4: [0.05, 0.2, 0.4, 0.25, 0.1],
        5: [0.0, 0.1, 0.2, 0.4, 0.3]
    }
    levels_education = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD']
    return weighted_choice(levels_education, ed_probs.get(level, [0.2]*5))

def generate_salary(dept, level, gender, education_level):
    # Base salary ranges by department and job level (in thousands)
    base_salary_ranges = {
        'HR': [(30, 50), (50, 70), (70, 90)],
        'R&D': [(40, 70), (70, 100), (90, 130), (130, 160)],
        'Sales': [(35, 60), (60, 85), (85, 120)]
    }
    role_idx = departments[dept]['levels'].index(level) if level in departments[dept]['levels'] else 0
    low, high = base_salary_ranges[dept][role_idx]

    # Convert to actual salary number in USD *1000
    salary = np.random.uniform(low, high) * 1000

    # Adjust salary based on education level: roughly +5% per level above Bachelor
    ed_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD']
    ed_idx = ed_levels.index(education_level)
    bachelor_idx = ed_levels.index('Bachelor')
    edu_bonus_pct = max(0, ed_idx - bachelor_idx) * 0.05
    salary *= (1 + edu_bonus_pct)

    # Mild gender bias: Women earn 95%-98% of male salary at same level, except Non-Binary get 97%-100%
    if gender == 'Female':
        salary *= np.random.uniform(0.95, 0.98)
    elif gender == 'Non-Binary':
        salary *= np.random.uniform(0.97, 1.0)

    return int(salary)

def generate_performance_rating():
    # More 3 and 4 ratings, few 5 and 1
    ratings = [1, 2, 3, 4, 5]
    weights = [0.05, 0.1, 0.5, 0.25, 0.1]
    return weighted_choice(ratings, weights)

def generate_satisfaction():
    # Uniform distribution 1-4
    return np.random.randint(1, 5)

def generate_work_life_balance():
    # Slightly skewed to 3-4
    return weighted_choice([1, 2, 3, 4], [0.1, 0.2, 0.4, 0.3])

def generate_attrition():
    # 16% attrition rate
    return weighted_choice(['Yes', 'No'], [0.16, 0.84]) == 'Yes'

def generate_boolean(p_true):
    return 'Yes' if np.random.rand() < p_true else 'No'

def generate_employee_record(emp_num):
    gender = generate_gender()
    dept = generate_department()
    role, level = generate_job_role_and_level(dept)
    hire_date = generate_hire_date()
    attrition = generate_attrition()
    termination_date = generate_termination_date(hire_date, attrition)

    years_at_company = generate_years_diff(hire_date, termination_date)
    years_in_current_role = np.random.randint(0, years_at_company + 1) if years_at_company > 0 else 0
    years_since_promotion = np.random.randint(0, years_in_current_role + 1) if years_in_current_role > 0 else 0
    years_with_manager = np.random.randint(0, years_at_company + 1)

    education = generate_education(level)
    first_name = fake.first_name_female() if gender == 'Female' else fake.first_name_male() if gender == 'Male' else fake.first_name()
    last_name = fake.last_name()

    age = np.random.randint(22 + level * 2, 60)  # Higher levels have older employees on average

    # Employee demographics
    marital_status = weighted_choice(marital_statuses, [0.4, 0.5, 0.1])
    education_field = weighted_choice(education_fields, [0.25, 0.15, 0.2, 0.3, 0.1])
    business_travel = weighted_choice(business_travel_options, [0.6, 0.3, 0.1])
    training_last_year = np.random.randint(0, 7)
    stock_option_level = np.random.choice([0, 1, 2, 3], p=[0.6, 0.25, 0.1, 0.05])

    employee_count = 1
    standard_hours = 40
    overtime = generate_boolean(0.3)

    hourly_rate = np.random.randint(20, 60)
    daily_rate = hourly_rate * 8
    monthly_income = generate_salary(dept, level, gender, education)
    monthly_rate = monthly_income * 1.1
    percent_salary_hike = np.random.randint(11, 26)

    performance_rating = generate_performance_rating()

    job_involvement = generate_satisfaction()
    job_satisfaction = generate_satisfaction()
    environment_satisfaction = generate_satisfaction()
    relationship_satisfaction = generate_satisfaction()
    work_life_balance = generate_work_life_balance()

    num_companies_worked = np.random.randint(0, 11)

    employee = {
        'EmployeeNumber': emp_num,
        'EmployeeID': f"EMP{emp_num:05d}",
        'FirstName': first_name,
        'LastName': last_name,
        'Gender': gender,
        'Age': age,
        'MaritalStatus': marital_status,
        'Education': education,
        'EducationField': education_field,
        'Department': dept,
        'JobRole': role,
        'JobLevel': level,
        'HireDate': hire_date.strftime('%Y-%m-%d'),
        'YearsAtCompany': years_at_company,
        'YearsInCurrentRole': years_in_current_role,
        'YearsSinceLastPromotion': years_since_promotion,
        'YearsWithCurrManager': years_with_manager,
        'Attrition': 'Yes' if attrition else 'No',
        'TerminationDate': termination_date.strftime('%Y-%m-%d') if termination_date else None,
        'BusinessTravel': business_travel,
        'DailyRate': daily_rate,
        'DistanceFromHome': np.random.randint(1, 50),
        'EmployeeCount': employee_count,
        'HourlyRate': hourly_rate,
        'JobInvolvement': job_involvement,
        'JobSatisfaction': job_satisfaction,
        'MaritalStatus': marital_status,
        'MonthlyIncome': monthly_income,
        'MonthlyRate': monthly_rate,
        'NumCompaniesWorked': num_companies_worked,
        'Over18': 'Y',
        'OverTime': overtime,
        'PercentSalaryHike': percent_salary_hike,
        'PerformanceRating': performance_rating,
        'RelationshipSatisfaction': relationship_satisfaction,
        'StandardHours': standard_hours,
        'StockOptionLevel': stock_option_level,
        'TotalWorkingYears': years_at_company + num_companies_worked,  # Rough estimate
        'TrainingTimesLastYear': training_last_year,
        'WorkLifeBalance': work_life_balance,
    }
    return employee


def generate_dataset(n=NUM_RECORDS):
    data = []
    for i in range(1, n + 1):
        data.append(generate_employee_record(i))
    return pd.DataFrame(data)


if __name__ == '__main__':
    print("Generating dataset, please wait...")
    df = generate_dataset()
    print("Dataset generated. Saving to 'hr_synthetic_dataset.csv' ...")
    df.to_csv('hr_synthetic_dataset.csv', index=False)
    print("Done!")
