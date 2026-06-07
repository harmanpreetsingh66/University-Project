# University Project Student Intake-################################
# Python script student_report_v2.py
# This will create:  student_report_v2.pdf  in this same folder.
####################################################################

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
import os

# --- LOAD DATA ---
script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "students_v2.csv"))
print(f"Loaded {len(df)} student records.\n")

# --- OPEN PDF ---
pdf = pdf_backend.PdfPages(os.path.join(script_dir, "student_report_v2.pdf"))

def save_chart():
    plt.tight_layout()
    pdf.savefig()
    plt.close()

years  = sorted(df["Year"].unique())
colors = ["#3498DB","#2ECC71","#E67E22","#9B59B6","#E74C3C"]


# CHART 1: How many students enrolled each year? 
yearly = df.groupby("Year").size()

plt.figure(figsize=(8, 5))
bars = plt.bar(yearly.index.astype(str), yearly.values, color=colors)
plt.bar_label(bars, padding=3, fontsize=11)
plt.title("How Many International Students Enrolled Each Year? (2021–2025)",
          fontsize=13, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Students Enrolled")
save_chart()


# CHART 2: Which department is most popular each year? (line per dept) 
dept_year = df.groupby(["Year","Department"]).size().unstack(fill_value=0)

plt.figure(figsize=(10, 6))
for dept in dept_year.columns:
    plt.plot(dept_year.index.astype(str), dept_year[dept],
             marker="o", linewidth=2, label=dept)
plt.title("Department Intake Trend Year by Year (2021–2025)",
          fontsize=13, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Students")
plt.legend(title="Department", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
save_chart()


# CHART 3: Online vs Offline applications – has it changed over years?
app_year = df.groupby(["Year","ApplicationMode"]).size().unstack(fill_value=0)

plt.figure(figsize=(9, 5))
app_year.plot(kind="bar", ax=plt.gca(),
              color=["#E74C3C","#2ECC71"], edgecolor="white", width=0.6)
plt.title("Online vs Offline Applications Each Year (2021–2025)",
          fontsize=13, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Number of Applications")
plt.xticks(rotation=0)
plt.legend(title="Application Mode")
save_chart()


# CHART 4: English level of students across all years (bar) 
eng_order = ["A2","B1","B2","C1","C2"]
eng_year  = df.groupby(["Year","EnglishLevel"]).size().unstack(fill_value=0)
eng_year  = eng_year.reindex(columns=eng_order, fill_value=0)

plt.figure(figsize=(10, 6))
eng_year.plot(kind="bar", ax=plt.gca(),
              color=["#E74C3C","#E67E22","#F1C40F","#2ECC71","#3498DB"],
              edgecolor="white", width=0.7)
plt.title("English Language Levels of Students Each Year (2021–2025)",
          fontsize=13, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)
plt.legend(title="English Level")
save_chart()


# CHART 5: Male vs Female each year 
gender_year = df.groupby(["Year","Gender"]).size().unstack(fill_value=0)

plt.figure(figsize=(9, 5))
gender_year.plot(kind="bar", ax=plt.gca(),
                 color=["#E87C7C","#4C9BE8"], edgecolor="white", width=0.6)
plt.title("Male vs Female Students Each Year (2021–2025)",
          fontsize=13, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)
plt.legend(title="Gender")
save_chart()


# CHART 6: Top 10 countries sending students (all years combined)
top_countries = df["Country"].value_counts().head(10)

plt.figure(figsize=(10, 5))
bars = plt.bar(top_countries.index, top_countries.values,
               color="#3498DB", edgecolor="white")
plt.bar_label(bars, padding=3, fontsize=9)
plt.title("Top 10 EU Countries Sending International Students (2021–2025)",
          fontsize=13, fontweight="bold")
plt.xlabel("Country")
plt.ylabel("Total Students")
plt.xticks(rotation=30, ha="right")
save_chart()


# CHART 7: Scholarship rate per year 
schol_year = df.groupby(["Year","Scholarship"]).size().unstack(fill_value=0)
schol_year["Rate_%"] = (schol_year["Yes"] /
                        (schol_year["Yes"] + schol_year["No"]) * 100).round(1)

plt.figure(figsize=(8, 5))
bars = plt.bar(schol_year.index.astype(str), schol_year["Rate_%"],
               color="#2ECC71", edgecolor="white")
for bar, val in zip(bars, schol_year["Rate_%"]):
    plt.text(bar.get_x() + bar.get_width() / 2, val + 0.3,
             f"{val}%", ha="center", fontsize=10)
plt.title("What % of Students Received a Scholarship Each Year?",
          fontsize=13, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Scholarship Rate (%)")
plt.ylim(0, schol_year["Rate_%"].max() + 8)
save_chart()


# CHART 8: Average GPA per department per year (heatmap-style table)
avg_gpa = df.groupby(["Department","Year"])["GPA"].mean().unstack()

fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(avg_gpa.values, cmap="YlGn", aspect="auto",
               vmin=2.8, vmax=3.8)
ax.set_xticks(range(len(avg_gpa.columns)))
ax.set_xticklabels(avg_gpa.columns.astype(str))
ax.set_yticks(range(len(avg_gpa.index)))
ax.set_yticklabels(avg_gpa.index)
for i in range(len(avg_gpa.index)):
    for j in range(len(avg_gpa.columns)):
        ax.text(j, i, f"{avg_gpa.values[i,j]:.2f}",
                ha="center", va="center", fontsize=10, fontweight="bold")
plt.colorbar(im, ax=ax, label="Average GPA")
ax.set_title("Average GPA by Department and Year (2021–2025)",
             fontsize=13, fontweight="bold")
save_chart()


# CLOSE PDF
pdf.close()
print("Done! Report saved: student_report_v2.pdf")
print("Open it to see all 8 charts.")
