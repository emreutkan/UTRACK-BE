# Database Structure

## Overview
UTrack uses a relational database with four main modules: User, Exercise, Workout, and Core.

---

## Core Models

### TimestampedModel (Abstract Base)
Used by all models to track creation and modification times.

**Fields:**
- `created_at` - DateTime (auto)
- `updated_at` - DateTime (auto)

---

## User Module

### CustomUser
Email-based authentication without username.

**Fields:**
- `id` - UUID (primary key)
- `email` - Email (unique, used for login)
- `password` - Hashed string
- `is_verified` - Boolean (default: False)
- `is_active` - Boolean
- `is_staff` - Boolean
- `is_superuser` - Boolean
- `first_name` - String
- `last_name` - String
- `last_login` - DateTime
- `date_joined` - DateTime
- `created_at` - DateTime
- `updated_at` - DateTime

**Relationships:**
- One-to-One → UserProfile
- One-to-One → SecurityStatus
- One-to-One → Preferences
- One-to-Many → Workout

### UserProfile
Extended user information.

**Fields:**
- `user` - OneToOne → CustomUser
- `created_at` - DateTime
- `updated_at` - DateTime

### SecurityStatus
Login attempt tracking and account lockout.

**Fields:**
- `user` - OneToOne → CustomUser
- `failed_login_attempts` - Integer (default: 0)
- `locked_until` - DateTime (nullable)
- `created_at` - DateTime
- `updated_at` - DateTime

### Preferences
User workout preferences.

**Fields:**
- `user` - OneToOne → CustomUser
- `auto_warmup_set` - Boolean (default: False)
- `rest_time` - Integer (seconds, default: 90)
- `units` - Choice: 'metric' or 'imperial' (default: 'metric')
- `created_at` - DateTime
- `updated_at` - DateTime

---

## Exercise Module

### Exercise
Exercise templates/library.

**Fields:**
- `id` - Integer (auto, primary key)
- `name` - String (max 255)
- `description` - Text (optional)
- `instructions` - Text (optional)
- `image` - ImageField (optional)
- `video_url` - URL (optional)
- `primary_muscle` - Choice (see below)
- `secondary_muscles` - JSON array (optional)
- `equipment_type` - Choice (see below)
- `created_at` - DateTime
- `updated_at` - DateTime

**Muscle Groups:**
- Chest: chest
- Shoulders: shoulders
- Arms: biceps, triceps, forearms
- Back: lats, traps, lower_back
- Legs: quads, hamstrings, glutes, calves
- Core: abs, obliques

**Equipment Types:**
- bodyweight, barbell, dumbbell, machine, cable
- resistance_band, kettlebell, treadmill, other

**Relationships:**
- One-to-Many → WorkoutExercise

---

## Workout Module

### Workout
Individual workout sessions.

**Fields:**
- `id` - Integer (auto, primary key)
- `title` - String (max 255)
- `user` - ForeignKey → CustomUser
- `date` - Date
- `duration` - Integer (seconds, default: 0)
- `intensity` - Choice: 'low', 'medium', 'high'
- `notes` - Text (optional)
- `is_done` - Boolean (default: False)
- `created_at` - DateTime
- `updated_at` - DateTime

**Relationships:**
- Many-to-One → CustomUser
- One-to-Many → WorkoutExercise

### WorkoutExercise
Links exercises to workouts with ordering.

**Fields:**
- `id` - Integer (auto, primary key)
- `workout` - ForeignKey → Workout
- `exercise` - ForeignKey → Exercise
- `order` - Integer (default: 0)
- `created_at` - DateTime
- `updated_at` - DateTime

**Relationships:**
- Many-to-One → Workout
- Many-to-One → Exercise
- One-to-Many → ExerciseSet

**Ordering:** By `order` field (ascending)

### ExerciseSet
Individual sets within an exercise.

**Fields:**
- `id` - Integer (auto, primary key)
- `workout_exercise` - ForeignKey → WorkoutExercise (related_name='sets')
- `set_number` - Integer
- `reps` - Integer (default: 0)
- `weight` - Decimal (6 digits, 2 decimals, default: 0)
- `rest_time_before_set` - Integer (seconds, default: 0)
- `is_warmup` - Boolean (default: False)
- `reps_in_reserve` - Integer (RIR, default: 0)
- `created_at` - DateTime
- `updated_at` - DateTime

**Relationships:**
- Many-to-One → WorkoutExercise

**Ordering:** By `set_number` (ascending)

---

## Entity Relationship Diagram

```
CustomUser
    ├─ (1:1) UserProfile
    ├─ (1:1) SecurityStatus
    ├─ (1:1) Preferences
    └─ (1:M) Workout
              └─ (1:M) WorkoutExercise
                        ├─ (M:1) Exercise
                        └─ (1:M) ExerciseSet
```

---

## Data Flow Example

**Creating a workout:**

1. User creates Workout (title, date, intensity)
2. Add exercises via WorkoutExercise (links Exercise template to Workout)
3. Log sets via ExerciseSet (reps, weight, RIR for each WorkoutExercise)
4. Mark Workout as `is_done=True` when complete

**Example:**
```
User: john@example.com
  └─ Workout: "Leg Day" (2025-11-18, intensity: high)
        ├─ WorkoutExercise #1: Squat (order: 0)
        │     ├─ Set 1: 5 reps @ 135 lbs (warmup)
        │     ├─ Set 2: 5 reps @ 185 lbs
        │     └─ Set 3: 5 reps @ 225 lbs (RIR: 2)
        └─ WorkoutExercise #2: Leg Press (order: 1)
              ├─ Set 1: 12 reps @ 200 lbs
              └─ Set 2: 10 reps @ 250 lbs (RIR: 1)
```

