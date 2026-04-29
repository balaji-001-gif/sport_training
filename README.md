# Sports Training - ERPNext v15+ Application

A comprehensive **Sports & Performance Training Institute Management System** built on Frappe/ERPNext v15+.

## 🏆 Features

- **Athlete Management** – Complete profile, medical, sport details
- **Coach Management** – Specializations, schedule, compensation
- **Training Programs** – Multi-week, multi-module structured programs
- **Training Sessions** – Schedule, attendance, performance ratings
- **Performance Assessment** – Multi-dimensional scoring
- **Injury Tracking** – Treatment, recovery, restrictions
- **Nutrition Plans** – Daily targets, meals, supplements
- **Membership Plans** – Auto-billing with ERPNext Sales Invoice
- **Attendance Logs** – Auto-generated from sessions
- **Competition Tracking** – Tournaments, results, medals
- **Equipment & Facility** – Inventory + booking
- **Fitness Tests** – VO2 max, strength, agility benchmarks
- **5+ Reports** – Performance, attendance, revenue, coach utilization, injuries
- **Dashboard** – Live charts on workspace
- **Role-based Permissions** – Sports Manager, Coach, Athlete, Physio

## 📋 Prerequisites

- Frappe Framework v15+
- ERPNext v15+
- Python 3.10+
- MariaDB 10.6+ / Postgres 14+

## ⚙️ Installation

```bash
cd ~/frappe-bench
bench get-app https://github.com/yourorg/sports_training.git
bench --site yoursite.local install-app sports_training
bench --site yoursite.local migrate
bench build --app sports_training
bench restart
```

## 👥 Default Roles

| Role | Permissions |
|------|------------|
| Sports Manager | Full access to all modules |
| Coach | Manage assigned athletes, sessions, assessments |
| Athlete | View own data |
| Physio | Manage injury records |

## 📄 License
MIT License
