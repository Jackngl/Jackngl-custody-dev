# 📖 Configuration Guide - School Holidays

This guide explains how to configure **school holidays** in the Custody application.

> ⚠️ **Important**: 
> - This guide concerns **school holidays only**
> - **School holidays have absolute priority** over regular custody (weekends/weeks)
> - **Public holidays** do not apply during school holidays
> - For regular custody, see `README_CONFIG_GARDE.md`

---

## 📋 Table of Contents

1. [Separation of regular custody / school holidays](#separation-of-regular-custody--school-holidays)
2. [School Holiday API](#school-holiday-api)
3. [School Zones](#school-zones)
4. [Available Holiday Rules](#available-holiday-rules)
5. [Basic Configuration](#basic-configuration)
6. [Detailed Holiday Rules](#detailed-holiday-rules)
7. [Special Summer Rules](#special-summer-rules)
8. [Date and Time Calculation](#date-and-time-calculation)
9. [Configuration Examples](#configuration-examples)

---

## 🔀 Separation of Regular Custody / School Holidays

The application clearly separates **two independent custody systems**:

### 1. **Regular Custody** (see `README_CONFIG_GARDE.md`)
- **Configuration**: "Regular custody (weekends/weeks)" input form
- **Period**: Outside school holidays only
- **Features**:
  - Alternate weekends, alternate weeks, 2-2-3 patterns, etc.
  - Automatic extension with public holidays (Friday/Monday)
  - Based on cycles or ISO week parity

### 2. **School Holidays** (this guide)
- **Configuration**: "School holidays" input form
- **Period**: During school holidays only
- **Features**:
  - Automatic date retrieval from French Ministry of Education API
  - Rules by half, by week, by year parity
  - Automatic calculation of exact holiday midpoint
  - Absolute priority over regular custody

### ⚠️ Priority Rule

```
School holidays > Public holidays > Regular custody
```

- **During holidays**: Only holiday rules apply
- **Outside holidays**: Regular custody applies, with holiday extension if applicable
- **Public holidays during holidays**: Ignored (holidays already take priority)

---

## 🌐 School Holiday API

The application uses the **official French Ministry of Education API** to automatically retrieve school holiday dates.

### Data Source

- **API**: `https://data.education.gouv.fr/api/records/1.0/search/`
- **Dataset**: `fr-en-calendrier-scolaire`
- **Format**: JSON
- **Update**: Automatic (15-minute cache)

### How It Works

1. **Automatic retrieval**: The application queries the API for your school zone
2. **Cache**: Data is cached to avoid repeated calls
3. **School years**: The API uses format "2024-2025" (September to June)
4. **Filtering**: Only future or current holidays are displayed

### Supported Zones

| Zone | Code | Main Cities |
|------|------|-------------|
| **Zone A** | `A` | Besançon, Bordeaux, Clermont-Ferrand, Dijon, Grenoble, Limoges, Lyon, Poitiers |
| **Zone B** | `B` | Aix-Marseille, Amiens, Lille, Nancy-Metz, Nantes, Nice, Normandy, Orléans-Tours, Reims, Rennes, Strasbourg |
| **Zone C** | `C` | Créteil, Montpellier, Paris, Toulouse, Versailles |
| **Corsica** | `Corse` | Corsica |
| **DOM-TOM** | `DOM-TOM` | Guadeloupe, Martinique, French Guiana, Réunion, Mayotte |

### Holiday Types Retrieved

The API provides the following periods:
- **All Saints' Day Holidays** (October)
- **Christmas Holidays** (December-January)
- **Winter Holidays** (February-March)
- **Spring Holidays** (April-May)
- **Summer Holidays** (July-August)
- **Ascension Bridge** (May)

### Manual Corrections

Some dates may be manually corrected in the code if the API is incomplete or incorrect (e.g., Zone C winter 2025-2026).

---

## ⚙️ Basic Configuration

### Required Fields

#### 1. **School Zone** (`zone`)
- **Description**: Geographic zone for school holidays
- **Values**: `"A"`, `"B"`, `"C"`, `"Corse"`, `"DOM-TOM"`
- **Example**: `"C"` for Zone C (Paris, Créteil, etc.)

#### 2. **Reference Year for Holidays** (`reference_year_vacations`)
- **Description**: Indicates for which **years (even or odd)** you have school holidays
- **Values**: `"even"` (even), `"odd"` (odd)
- **Configuration**: In the "School holidays" input form (separate from `reference_year_custody` for regular custody)
- **How it works**: The **parity of the current year** determines if you have holidays this year
  - `reference_year_vacations: "odd"` → you have holidays **on odd years**
  - `reference_year_vacations: "even"` → you have holidays **on even years**
- **Examples**:
  - Year 2025 (odd) + `reference_year_vacations: "odd"` → You have holidays
  - Year 2026 (even) + `reference_year_vacations: "even"` → You have holidays
- **Note**: 
  - This logic applies to **all holidays** (Christmas, Winter, Spring, All Saints' Day)
  - For summer, use `july_rule` and `august_rule` to independently choose July or August based on years
  - `reference_year_vacations` for holidays is **independent** of `reference_year_custody` for regular custody

#### 3. **Half Distribution** (`vacation_split_mode`)
- **Description**: Defines **which half** of holidays you have based on year parity
- **Values**:
  - `"odd_first"`: **odd years = 1st half**, even years = 2nd half (default)
  - `"odd_second"`: **odd years = 2nd half**, even years = 1st half
- **Examples**:
  - Year 2025 (odd) + `odd_first` → 1st half
  - Year 2026 (even) + `odd_first` → 2nd half
  - Year 2025 (odd) + `odd_second` → 2nd half (inverse)
  - Year 2026 (even) + `odd_second` → 1st half (inverse)

#### 4. **School Level** (`school_level`)
- **Description**: Child's school level (affects dismissal times)
- **Values**: `"primary"` (primary), `"middle"` (middle school), `"high"` (high school)
- **Impact**:
  - **Primary**: Holiday start = Friday 16:15 (school dismissal)
  - **Middle/High School**: Holiday start = Saturday morning (according to API)

### Optional Fields

#### 5. **Summer Rule** (`summer_rule`)
- **Description**: Special rule for summer holidays (July-August)
- **Values**: See [Special Summer Rules](#special-summer-rules)
- **Example**: `"summer_half_parity"` for half sharing based on year parity

---

## 🎯 Available Holiday Rules

### Simplified System Based on `reference_year_vacations` + `vacation_split_mode`

The application uses an **automatic system** based on:
- `reference_year_vacations` → **which years** (even/odd) you have holidays
- `vacation_split_mode` → **which half** of holidays applies this year

- **`reference_year_vacations: "odd"` (odd)** → you have holidays **on odd years**

- **`reference_year_vacations: "even"` (even)** → you have holidays **on even years**

### Examples

**Parent A Configuration**: `reference_year_vacations: "odd"`, `vacation_split_mode: "odd_first"`
- **2025 (odd)**: ✅ Parent A has the **1st half**
- **2026 (even)**: ❌ No custody (even year, parent B)

**Parent B Configuration**: `reference_year_vacations: "even"`, `vacation_split_mode: "odd_first"`
- **2024 (even)**: ✅ Parent B has the **2nd half**
- **2025 (odd)**: ❌ No custody (odd year, parent A)

> **Note**: Both parents have complementary configurations. `vacation_split_mode` allows the inverse (odd years = 2nd half).

### Special Summer Rules

#### Rules for July and August (Full Months)

| Rule | Code | Description |
|------|------|-------------|
| **July (even years)** | `july_even` | Full July in even years only |
| **July (odd years)** | `july_odd` | Full July in odd years only |
| **August (even years)** | `august_even` | Full August in even years only |
| **August (odd years)** | `august_odd` | Full August in odd years only |

> **Note**: 
> - These rules are configured via `july_rule` and `august_rule` fields in the "School holidays" form
> - Each parent can independently choose July or August, and for which years (even or odd)
> - This allows complete flexibility: a parent can have July in odd years and August in even years, or vice versa

#### Rules for Fortnights (Month Halves)

| Rule | Code | Description |
|------|------|-------------|
| **July - 1st half** | `july_first_half` | July 1-15<br>- `reference_year_vacations: "even"`: odd years only<br>- `reference_year_vacations: "odd"`: even years only |
| **July - 2nd half** | `july_second_half` | July 16-31<br>- `reference_year_vacations: "even"`: even years only<br>- `reference_year_vacations: "odd"`: odd years only |
| **August - 1st half** | `august_first_half` | August 1-15<br>- `reference_year_vacations: "even"`: odd years only<br>- `reference_year_vacations: "odd"`: even years only |
| **August - 2nd half** | `august_second_half` | August 16-31<br>- `reference_year_vacations: "even"`: even years only<br>- `reference_year_vacations: "odd"`: odd years only |

> **Note**: 
> - Fortnight rules are used via the `summer_rule` field and apply only to summer holidays
> - They use `reference_year_vacations` to automatically determine if they apply based on year parity

---

## 📅 Detailed Holiday Rules

### Automatic System Based on `reference_year_vacations` + `vacation_split_mode`

The application automatically determines:
- **which years** you have holidays (via `reference_year_vacations`)
- **which half** you have this year (via `vacation_split_mode`)

#### 1. Years Concerned (`reference_year_vacations`)
- `reference_year_vacations: "odd"` → you have holidays **on odd years**
- `reference_year_vacations: "even"` → you have holidays **on even years**

#### 2. Half Distribution (`vacation_split_mode`)
- `odd_first`: odd years = **1st half**, even years = **2nd half**
- `odd_second`: odd years = **2nd half**, even years = **1st half**

#### Example (Default Mode)
```yaml
zone: "C"
reference_year_vacations: "odd"
vacation_split_mode: "odd_first"
school_level: "primary"
```

#### Example (Inverse)
```yaml
zone: "C"
reference_year_vacations: "odd"
vacation_split_mode: "odd_second"
school_level: "primary"
```

> **Note**: The calculation of the **exact midpoint** remains identical (midpoint = (start + end) / 2).

### Exact Midpoint Calculation

For half-sharing rules, the midpoint is automatically calculated:

- **Effective period**: Friday 16:15 → Sunday 19:00 (official end)
- **Midpoint** = (start + end) / 2 (with precise hours and minutes)
- **Example**: 19/12/2025 16:15 → 05/01/2026 19:00 → Midpoint = 27/12/2025 17:37:30

---

## ☀️ Special Summer Rules

Summer rules allow you to specifically configure summer holidays (July-August). They are configured in the "School holidays" input form.

### ✅ Choose Between **Full Months** and **Fortnights**

For summer, you have **two distinct approaches**:

1) **Full Months** (recommended if you share July/August)
- Use **`july_rule`** and/or **`august_rule`**
- Each rule gives **a full month** (July or August) based on parity
- You can **enable one, the other, or both**

2) **Fortnights** (1-15 / 16-31 sharing)
- Use **`summer_rule`** (e.g., `july_first_half`, `august_second_half`)
- The half is determined by **`vacation_split_mode`**

> ⚠️ **Priority**: if `july_rule` or `august_rule` is defined, the `summer_rule` is **not** used for summer.

### July (Even Years) (`july_even`)

**How it works**:
- Custody of full July in even years only
- Odd years: no custody in July (other parent may have July or August)

**Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # or "odd", for other holidays
july_rule: "july_even"  # July in even years
school_level: "primary"
```

**Result**:
- 2024 (even): ✅ Full July 2024
- 2025 (odd): ❌ No custody in July
- 2026 (even): ✅ Full July 2026

---

### July (Odd Years) (`july_odd`)

**How it works**:
- Custody of full July in odd years only
- Even years: no custody in July

**Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # or "odd", for other holidays
july_rule: "july_odd"  # July in odd years
school_level: "primary"
```

**Result**:
- 2024 (even): ❌ No custody in July
- 2025 (odd): ✅ Full July 2025
- 2026 (even): ❌ No custody in July

---

### August (Even Years) (`august_even`)

**How it works**:
- Custody of full August in even years only
- Odd years: no custody in August

**Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # or "odd", for other holidays
august_rule: "august_even"  # August in even years
school_level: "primary"
```

**Result**:
- 2024 (even): ✅ Full August 2024
- 2025 (odd): ❌ No custody in August
- 2026 (even): ✅ Full August 2026

---

### August (Odd Years) (`august_odd`)

**How it works**:
- Custody of full August in odd years only
- Even years: no custody in August

**Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # or "odd", for other holidays
august_rule: "august_odd"  # August in odd years
school_level: "primary"
```

**Result**:
- 2024 (even): ❌ No custody in August
- 2025 (odd): ✅ Full August 2025
- 2026 (even): ❌ No custody in August

---

### July - 1st Half (`july_first_half`)

**How it works**:
- Custody of the **1st fortnight of July** (July 1-15)
- Uses `reference_year_vacations` to determine if the rule applies based on year parity
- **`reference_year_vacations: "even"`**: applies only on odd years
- **`reference_year_vacations: "odd"`**: applies only on even years

**Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # or "odd", determines when rule applies
summer_rule: "july_first_half"
school_level: "primary"
```

**Result with `reference_year_vacations: "even"`**:
- 2024 (even): ❌ Does not apply
- 2025 (odd): ✅ July 1-15, 2025
- 2026 (even): ❌ Does not apply

**Result with `reference_year_vacations: "odd"`**:
- 2024 (even): ✅ July 1-15, 2024
- 2025 (odd): ❌ Does not apply
- 2026 (even): ✅ July 1-15, 2026

---

### July - 2nd Half (`july_second_half`)

**How it works**:
- Custody of the **2nd fortnight of July** (July 16-31)
- Uses `reference_year_vacations` to determine if the rule applies based on year parity
- **`reference_year_vacations: "even"`**: applies only on even years
- **`reference_year_vacations: "odd"`**: applies only on odd years

**Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # or "odd", determines when rule applies
summer_rule: "july_second_half"
school_level: "primary"
```

**Result with `reference_year_vacations: "even"`**:
- 2024 (even): ✅ July 16-31, 2024
- 2025 (odd): ❌ Does not apply
- 2026 (even): ✅ July 16-31, 2026

**Result with `reference_year_vacations: "odd"`**:
- 2024 (even): ❌ Does not apply
- 2025 (odd): ✅ July 16-31, 2025
- 2026 (even): ❌ Does not apply

---

### August - 1st Half (`august_first_half`)

**How it works**:
- Custody of the **1st fortnight of August** (August 1-15)
- Uses `reference_year_vacations` to determine if the rule applies based on year parity
- **`reference_year_vacations: "even"`**: applies only on odd years
- **`reference_year_vacations: "odd"`**: applies only on even years

**Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # or "odd", determines when rule applies
summer_rule: "august_first_half"
school_level: "primary"
```

**Result with `reference_year_vacations: "even"`**:
- 2024 (even): ❌ Does not apply
- 2025 (odd): ✅ August 1-15, 2025
- 2026 (even): ❌ Does not apply

**Result with `reference_year_vacations: "odd"`**:
- 2024 (even): ✅ August 1-15, 2024
- 2025 (odd): ❌ Does not apply
- 2026 (even): ✅ August 1-15, 2026

---

### August - 2nd Half (`august_second_half`)

**How it works**:
- Custody of the **2nd fortnight of August** (August 16-31)
- Uses `reference_year_vacations` to determine if the rule applies based on year parity
- **`reference_year_vacations: "even"`**: applies only on even years
- **`reference_year_vacations: "odd"`**: applies only on odd years

**Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # or "odd", determines when rule applies
summer_rule: "august_second_half"
school_level: "primary"
```

**Result with `reference_year_vacations: "even"`**:
- 2024 (even): ✅ August 16-31, 2024
- 2025 (odd): ❌ Does not apply
- 2026 (even): ✅ August 16-31, 2026

**Result with `reference_year_vacations: "odd"`**:
- 2024 (even): ❌ Does not apply
- 2025 (odd): ✅ August 16-31, 2025
- 2026 (even): ❌ Does not apply

---

## 🕐 Date and Time Calculation

### Effective Holiday Period

The application automatically adjusts API dates to match custody times:

#### Effective Start
- **Primary**: Previous Friday at 16:15 (school dismissal)
- **Middle/High School**: Saturday morning (according to API)

#### Effective End
- **Always**: Sunday 19:00 (even if API indicates "resume Monday")

### Date Calculation

Dates are automatically calculated based on the selected rule, year parity (`reference_year_vacations`), and half distribution (`vacation_split_mode`).

---

## 📝 Configuration Examples

### Example 1: Half Sharing (All Holidays)

**Situation**: Fair sharing of all holidays (Christmas, Winter, Spring, All Saints' Day, Summer) by half based on year parity.

**Parent A Configuration**:
```yaml
zone: "C"
reference_year_vacations: "odd"  # 1st part (1st half) in odd years
vacation_split_mode: "odd_first"
school_level: "primary"
```

**Parent B Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # 2nd part (2nd half) in even years
vacation_split_mode: "odd_first"
school_level: "primary"
```

**Parent A Result** (all holidays):
- **2025 (odd)**: ✅ 1st half of all holidays
  - Christmas 2025: 19/12/2025 16:15 → 27/12/2025 17:37:30
  - Winter 2025: 1st half
  - Spring 2025: 1st half
  - All Saints' Day 2025: 1st half
- **2026 (even)**: ❌ No custody (because it's the 2nd part, parent B has custody)

**Parent B Result** (all holidays):
- **2025 (odd)**: ❌ No custody (because it's the 1st part, parent A has custody)
- **2026 (even)**: ✅ 2nd half of all holidays
  - Christmas 2026: 27/12/2026 17:37:30 → 03/01/2027 19:00
  - Winter 2026: 2nd half
  - Spring 2026: 2nd half
  - All Saints' Day 2026: 2nd half
```

> **Note**: This logic applies to **all school holidays** (Christmas, Winter, Spring, All Saints' Day, Summer). The `reference_year_vacations` field determines **the years concerned**, and `vacation_split_mode` determines **the half**.

**Inverse Variant** (odd years = 2nd half):
```yaml
zone: "C"
reference_year_vacations: "odd"
vacation_split_mode: "odd_second"
school_level: "primary"
```

---

### Example 2: July/August Sharing with Separate Rules

**Situation**: Using `july_rule` and `august_rule` to fairly share July and August.

**Parent A Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # For other holidays (Christmas, Winter, Spring, All Saints' Day)
july_rule: "july_odd"  # July in odd years
august_rule: "august_even"  # August in even years
school_level: "primary"
```

**Parent B Configuration**:
```yaml
zone: "C"
reference_year_vacations: "odd"  # For other holidays (Christmas, Winter, Spring, All Saints' Day)
july_rule: "july_even"  # July in even years
august_rule: "august_odd"  # August in odd years
school_level: "primary"
```

**Parent A Result**:
- 2024 (even): ✅ Full August 2024
- 2025 (odd): ✅ Full July 2025
- 2026 (even): ✅ Full August 2026
- 2027 (odd): ✅ Full July 2027

**Parent B Result**:
- 2024 (even): ✅ Full July 2024 (complementary to parent A)
- 2025 (odd): ✅ Full August 2025 (complementary to parent A)
- 2026 (even): ✅ Full July 2026 (complementary to parent A)
- 2027 (odd): ✅ Full August 2027 (complementary to parent A)

> **Note**: Each parent independently configures `july_rule` and `august_rule`. This allows complete flexibility: a parent can have July in odd years and August in even years, or any other combination. Both parents get different months each year, ensuring fair alternation.

---

### Example 3: July Fortnight with `reference_year_vacations`

**Situation**: Sharing the 1st fortnight of July based on year parity.

**Parent A Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # Determines when rule applies
summer_rule: "july_first_half"  # 1st half of July
school_level: "primary"
```

**Parent B Configuration**:
```yaml
zone: "C"
reference_year_vacations: "odd"  # Determines when rule applies
summer_rule: "july_first_half"  # 1st half of July
school_level: "primary"
```

**Parent A Result** (`reference_year_vacations: "even"`):
- 2024 (even): ❌ Does not apply
- 2025 (odd): ✅ July 1-15, 2025
- 2026 (even): ❌ Does not apply

**Parent B Result** (`reference_year_vacations: "odd"`):
- 2024 (even): ✅ July 1-15, 2024 (complementary to parent A)
- 2025 (odd): ❌ Does not apply (parent A has custody)
- 2026 (even): ✅ July 1-15, 2026 (complementary to parent A)

> **Note**: Both parents use the same `july_first_half` rule, but with different `reference_year_vacations`. In 2025 (odd year), only parent A has custody. In 2024 and 2026 (even years), only parent B has custody.

---

### Example 4: August Fortnight with `reference_year_vacations`

**Situation**: Sharing the 2nd fortnight of August based on year parity.

**Parent A Configuration**:
```yaml
zone: "C"
reference_year_vacations: "even"  # Determines when rule applies
summer_rule: "august_second_half"  # 2nd half of August
school_level: "primary"
```

**Parent B Configuration**:
```yaml
zone: "C"
reference_year_vacations: "odd"  # Determines when rule applies
summer_rule: "august_second_half"  # 2nd half of August
school_level: "primary"
```

**Parent A Result** (`reference_year_vacations: "even"`):
- 2024 (even): ✅ August 16-31, 2024
- 2025 (odd): ❌ Does not apply
- 2026 (even): ✅ August 16-31, 2026

**Parent B Result** (`reference_year_vacations: "odd"`):
- 2024 (even): ❌ Does not apply (parent A has custody)
- 2025 (odd): ✅ August 16-31, 2025 (complementary to parent A)
- 2026 (even): ❌ Does not apply (parent A has custody)

> **Note**: Both parents use the same `august_second_half` rule, but with different `reference_year_vacations`. In 2024 and 2026 (even years), only parent A has custody. In 2025 (odd year), only parent B has custody.

---

## 🔧 Troubleshooting

### API Returns No Data

1. **Check zone**: Make sure the zone is correct (A, B, C, Corsica, DOM-TOM)
2. **Check school year**: The API uses format "2024-2025"
3. **Test connection**: Use the `test_holiday_api` service in Home Assistant
4. **Check logs**: Check logs for API errors

### Dates Don't Match

1. **School level**: Verify that `school_level` is correct (primary = Friday 16:15)
2. **Zone**: Verify that the zone matches your academy
3. **Year**: Verify that the reference year is correct for parity-based rules

### Rules Don't Apply Correctly

1. **reference_year_vacations**: Verify that you selected the concerned years (even / odd)
2. **vacation_split_mode**: Verify if you chose the 1st or 2nd half for odd years
3. **july_rule / august_rule / summer_rule**: Check summer rules
4. **Logs**: Check logs to see calculated dates

---

## 📚 Resources

- **French Ministry of Education API**: https://data.education.gouv.fr/explore/dataset/fr-en-calendrier-scolaire
- **Regular custody documentation**: `README_CONFIG_GARDE.md`
- **School zones**: https://www.education.gouv.fr/les-zones-de-vacances-12073

---

## ✅ Summary

### Rule Priority

```
School holidays > Public holidays > Regular custody
```

### Key Points

- ✅ Holidays are automatically retrieved from the API
- ✅ Dates are adjusted to match custody times
- ✅ Midpoint is automatically calculated for sharing rules
- ✅ Holidays completely replace regular custody during their duration
- ✅ Public holidays do not apply during holidays
