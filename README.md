# UTrack Backend

A comprehensive Django REST API for tracking workouts, exercises, body measurements, supplements, and fitness progress with AI-powered recommendations.

## Features

### User Management
- Email-based authentication (no username required)
- JWT token authentication
- Social login (Google, Apple)
- User profiles with customizable preferences
- Security features: login attempt tracking & account lockout
- User preferences: rest timers, unit system (metric/imperial), auto warm-up sets
- Profile management: height, weight, gender tracking

### Exercise Library
- Comprehensive exercise database
- Muscle group targeting (primary & secondary)
- Equipment type classification (barbell, dumbbell, machine, bodyweight, etc.)
- Support for images and video URLs
- Exercise search and filtering

### Workout Tracking
- Create and organize workouts
- Template workouts for quick start
- Track workout duration and calories burned
- Add notes to workouts
- Mark workouts as complete
- Active workout management
- Exercise ordering and reordering
- Calendar view with workout history
- Rest day tracking
- Rest timer functionality

### Exercise Sets & Tracking
- Record reps and weight for each set
- Track Reps In Reserve (RIR)
- One-rep max (1RM) calculation and history
- Custom rest times per set
- Warm-up set indicators
- Volume analysis
- Set update and deletion

### Body Measurements
- Track body measurements over time
- Body fat percentage calculation
- Measurement history and trends

### Supplements
- Track daily supplement intake
- Manage supplement inventory
- Record dosages and timing
- Bioavailability scoring
- Supplement logging

### AI-Powered Recommendations
- Recovery recommendations based on training volume
- Rest period recommendations
- Training frequency recommendations
- Muscle recovery status tracking
- Relevant research articles
- Volume analysis

## Tech Stack

- **Framework**: Django 5.2.7
- **REST API**: Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt), dj-rest-auth
- **Social Auth**: django-allauth
- **Database**: SQLite (development)
- **Python**: 3.14+
- **Image Processing**: Pillow
- **CORS**: django-cors-headers

## Quick Start

### Option 1: Using the Startup Script (Recommended)

The easiest way to get started is using the provided startup script:

**Windows:**
```bash
.\start.bat
```

**Linux/Mac:**
```bash
./start.sh
```

The script will:
- Check if virtual environment exists, create it if not
- Activate the virtual environment
- Run the Django server
  - Windows: `192.168.1.7:8000` (accessible on local network)
  - Linux: `127.0.0.1:8000` (localhost)

### Option 2: Manual Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/UTrack-BE.git
cd UTrack-BE
```

2. **Set up virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Run server**
```bash
# Windows (accessible on local network)
python manage.py runserver 192.168.1.7:8000

# Linux/Mac
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/user/register/` - Register new user
- `POST /api/user/login/` - Login (get JWT tokens)
- `POST /api/user/refresh/` - Refresh JWT token
- `POST /auth/google/` - Google OAuth login
- `POST /auth/apple/` - Apple OAuth login

### User Profile
- `GET /api/user/me/` - Get current user profile
- `PUT /api/user/me/` - Update user profile
- `POST /api/user/height/` - Update user height
- `POST /api/user/gender/` - Update user gender

### Exercises
- `GET /api/exercise/` - List all exercises
- `GET /api/exercise/<id>/` - Get exercise details

### Workouts
- `POST /api/workout/create/` - Create new workout
- `GET /api/workout/list/` - List all workouts
- `GET /api/workout/list/<id>/` - Get specific workout
- `GET /api/workout/active/` - Get active workout
- `POST /api/workout/<id>/add_exercise/` - Add exercise to workout
- `POST /api/workout/exercise/<id>/add_set/` - Add set to exercise
- `PUT /api/workout/<id>/update/` - Update workout
- `POST /api/workout/<id>/complete/` - Complete workout
- `DELETE /api/workout/<id>/delete/` - Delete workout
- `GET /api/workout/calendar/` - Get calendar view
- `GET /api/workout/calendar/stats/` - Get calendar statistics
- `GET /api/workout/years/` - Get available years

### Exercise Sets
- `PUT /api/workout/set/<id>/update/` - Update exercise set
- `DELETE /api/workout/set/<id>/delete/` - Delete exercise set
- `GET /api/workout/exercise/<id>/1rm-history/` - Get 1RM history

### Templates
- `POST /api/workout/template/create/` - Create workout template
- `GET /api/workout/template/list/` - List workout templates
- `POST /api/workout/template/start/` - Start workout from template

### Recommendations
- `GET /api/workout/recommendations/recovery/` - Get recovery recommendations
- `GET /api/workout/recommendations/frequency/` - Get training frequency recommendations
- `GET /api/workout/recovery/status/` - Get muscle recovery status
- `GET /api/workout/research/` - Get relevant research articles
- `GET /api/workout/volume-analysis/` - Get volume analysis

### Body Measurements
- `POST /api/measurements/` - Create body measurement
- `GET /api/measurements/` - Get body measurements
- `POST /api/measurements/calculate-body-fat-men/` - Calculate body fat (men)
- `POST /api/measurements/calculate-body-fat-women/` - Calculate body fat (women)

### Supplements
- `GET /api/supplements/` - List all supplements
- `GET /api/supplements/user/` - Get user supplement logs
- `POST /api/supplements/user/` - Log supplement intake

## Project Structure

```
UTrack-BE/
├── user/              # User authentication, profiles, preferences
├── exercise/          # Exercise library & management
├── workout/           # Workouts, sets, tracking, recommendations
├── supplements/       # Supplement tracking & inventory
├── body_measurements/ # Body measurement tracking
├── core/              # Shared models & utilities
├── utrack/            # Project settings & configuration
├── media/             # Uploaded media files
├── logs/              # Application logs
├── start.py           # Cross-platform startup script
├── start.bat          # Windows startup script
├── start.sh           # Linux/Mac startup script
└── manage.py          # Django management script
```

## Development

### Running Management Commands

The project includes several management commands for data population:

```bash
# Populate exercises
python manage.py populate_exercises

# Populate supplements
python manage.py populate_supplements

# Add measurement tips
python manage.py add_measurement_tips

# Import workout research
python manage.py import_research

# Recalculate calories
python manage.py recalculate_calories
```

### Environment Variables

Create a `.env` file in the project root for environment-specific settings:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
```

## Database

The project uses SQLite for development. See `DATABASE.md` for detailed database schema documentation.

## Logging

Application logs are stored in the `logs/` directory:
- `errors.log` - Error logs
- `info.log` - Info logs
- `requests.log` - Request logs

## Contributing

Pull requests welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
