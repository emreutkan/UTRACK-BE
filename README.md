# UTrack Backend

A Django REST API for tracking workouts, exercises, and fitness progress.

## Features

### User Management
- Email-based authentication (no username required)
- User profiles with customizable preferences
- Security features: login attempt tracking & account lockout
- User preferences: rest timers, unit system (metric/imperial), auto warm-up sets

### Exercise Library
- Comprehensive exercise database
- Muscle group targeting (primary & secondary)
- Equipment type classification (barbell, dumbbell, machine, bodyweight, etc.)
- Support for images and video URLs

### Workout Tracking
- Create and organize workouts
- Track workout duration and intensity
- Add notes to workouts
- Mark workouts as complete

### Exercise Sets
- Record reps and weight for each set
- Track Reps In Reserve (RIR)
- Custom rest times per set
- Warm-up set indicators

## Tech Stack

- **Framework**: Django 5.2.7
- **REST API**: Django REST Framework 3.16.1
- **Database**: SQLite (development)
- **Python**: 3.14+

## Installation

1. Clone the repo
```bash
git clone https://github.com/yourusername/UTrack-BE.git
cd UTrack-BE
```

2. Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run server
```bash
python manage.py runserver
```

## Project Structure

```
UTrack-BE/
├── user/          # User auth, profiles, preferences
├── exercise/      # Exercise library & templates
├── workout/       # Workouts, sets, tracking
├── core/          # Shared models & utilities
└── utrack/        # Project settings & config
```

## MVP Status

This is the MVP (Minimum Viable Product) version with core functionality:
- ✅ User authentication system
- ✅ Exercise library with muscle groups
- ✅ Workout creation and tracking
- ✅ Set/rep/weight logging
- ✅ User preferences
- 🚧 API endpoints (coming soon)
- 🚧 Frontend integration (coming soon)

## Contributing

Pull requests welcome! For major changes, open an issue first.

## License

MIT

