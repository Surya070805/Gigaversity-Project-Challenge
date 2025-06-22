# 👥 Gender Bias in Hiring or Promotions — HR Analytics Project

This project analyzes a synthetic HR dataset to identify gender-based disparities in hiring, promotion, compensation, and employee turnover. It uses the full data analytics pipeline—from problem framing and statistical modeling to prescriptive recommendations and Power BI storytelling.

---

## 🧩 Problem Statement

Identify any gender-based bias influencing the company's decisions regarding:
- Hiring
- Promotions
- Compensation (salary, hikes)
- Attrition (voluntary/involuntary exits)

---

## 🎯 Project Goal

To assess whether gender impacts decisions related to:
- Hiring patterns
- Compensation practices
- Performance review outcomes
- Attrition rates

---

## 📊 Key Performance Indicators (KPIs)

- Promotion Rate by Gender  
- Salary Distribution by Gender (adjusted by role/level)  
- Attrition Rate by Gender  
- Performance Ratings by Gender  
- Time to Promotion / Years in Role by Gender  

---

## 📚 Hypotheses

- **H1**: Males and females are not promoted at the same rate.  
- **H2**: There is a statistically significant salary difference between genders after controlling for job role and education.  
- **H3**: Females have a higher attrition rate due to work-life imbalance.  

---

## 🧾 Dataset Overview

A synthetic HR dataset with 89+ attributes, simulating real-world employee data.

### Key Features:
- **Demographics**: Gender, Age, MaritalStatus, Education  
- **Job Info**: Department, JobRole, JobLevel, Manager ID  
- **Compensation**: MonthlyIncome, HourlyRate, Incentives, SalaryHike  
- **Performance**: Ratings, Promotions, Attrition  
- **Work Patterns**: Overtime, ExtraHoursWorked, WorkLifeBalance  
- **Engagement**: JobSatisfaction, EnvironmentSatisfaction, Training  

---

## 🔍 Descriptive & Diagnostic Analysis

### Explored:
- Hiring rate by `JobRole` and `Gender`  
- Average `PercentSalaryHike` by gender  
- Years since last promotion by gender  
- Manager–Employee Gender pair trends  
- Turnover rate by gender  

---

## 🧪 Predictive & Inferential Analysis

### 📈 Independent T-Test
- Compares male vs female salary per job role  
- Found statistically significant gaps in roles like Manager, Senior Developer, and Project Lead  
- p-values < 0.05 indicate real gender-based disparities

### 🤖 Logistic Regression
- Predicts recent promotion likelihood  
- **Gender Coefficient > 0** → being male increases the chance of promotion  
- **Model Score = 0.7** → Acceptable performance on a balanced classification task  

---

## ✅ Recommendations

1. **Standardize Compensation Bands**
   - Set fixed ranges for salary by `JobRole` and `JobLevel`

2. **Transparent Promotion Criteria**
   - Create a measurable scorecard based on performance, involvement, tenure

3. **Bias-Aware Performance Reviews**
   - Use 360° feedback + manager bias training

4. **Audit the Hike Process**
   - Automate hike logic using objective rules (e.g., `Hike = f(Rating * Involvement * JobLevel)`)

---

## 🧠 Storytelling & Delivery

- Power BI used to deliver stakeholder-ready visuals
- Visuals include:
  - Salary gap dumbbell charts
  - Promotion slope plots
  - Overtime vs hike scatterplots
  - Violin plots for promotion wait time
- Interactive dashboards for HR and executive leadership

---

## 📂 Project Structure

```bash
├── data/
│   └── hr_synthetic_dataset.csv
├── notebooks/
│   ├── Descriptive_Analysis.ipynb
│   ├── Inferential_Analysis.ipynb
├── dashboards/
│   └── GenderBiasDashboard.pbix
├── reports/
│   └── Gigaversity_Findings.pdf
├── README.md
