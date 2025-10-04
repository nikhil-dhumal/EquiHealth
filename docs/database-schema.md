# Database Schema (Tentative)

> **Note:** This schema represents the **current phase** of the EquiHealth project, based on the data collected from government sources.  
> It may be expanded in future stages to include additional entities such as subcategories, surgeries, and complaint tracking.

This schema defines the **core structure** of the EquiHealth database — focusing on hospitals, their service categories, and their relationships across districts.

![Database Schema Diagram](images/database-schema-diagram.png)

---

## Overview

The EquiHealth database is designed to capture **healthcare facility information** and enable comparisons across districts.  
At this stage, the schema contains **three main tables**:

1. **Hospital**
2. **Category**
3. **Hospital_Category (Mapping Table)**

These entities form the foundation for analyzing hospital availability and service coverage.

---

## Tables and Relationships

### 🏥 Hospital
Stores details about healthcare facilities across the state.

| Field | Type | Description |
|--------|------|-------------|
| `hospital_id` | INT (PK) | Unique identifier for each hospital |
| `hospital_name` | VARCHAR | Name of the hospital |
| `district` | VARCHAR | District where the hospital is located |
| `hospital_type` | VARCHAR | Type of hospital (e.g., Government, Corporate) |
| `total_beds` | INT | Number of beds available in the hospital |

---

### 🩺 Category
Defines medical service categories (e.g., Cardiology, Pediatrics, ICU).

| Field | Type | Description |
|--------|------|-------------|
| `category_id` | INT (PK) | Unique identifier for each category |
| `category_name` | VARCHAR | Name of the category/service |

---

### 🔗 Hospital_Category
A **many-to-many mapping** between hospitals and categories.  
Each record indicates that a hospital provides a particular service category.

| Field | Type | Description |
|--------|------|-------------|
| `hospital_id` | INT (FK → Hospital.hospital_id) | Reference to hospital |
| `category_id` | INT (FK → Category.category_id) | Reference to category |

**Primary Key:** (`hospital_id`, `category_id`)

---

## Relationships Summary

- **One Hospital → Many Categories**  
  A hospital can offer multiple service categories.

- **One Category → Many Hospitals**  
  A category (e.g., “ICU”) can exist in multiple hospitals.

These relationships enable flexible analysis of service distribution across regions.

---

## Design Decisions

- **Normalized Structure:**  
  The schema follows a **3NF** (Third Normal Form) design to minimize redundancy.

- **Scalability:**  
  Future tables such as `subcategory`, `hospital_subcategory`, or `complaints` can be easily integrated using the same relational structure.

- **Data Integrity:**  
  Foreign key relationships ensure valid references between hospitals and categories.

---

> This schema is **tentative** and represents the project’s **current scraping phase**.  
> Future iterations will extend it to include complaint handling, government dashboards, and citizen feedback modules.
