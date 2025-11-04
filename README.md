# 🎮 Forge Gaming Cafe - Booking Platform

A comprehensive gaming cafe booking platform built with Django, powered by TapNex Technologies.

## 📋 Overview

This platform enables customers to book gaming slots at Forge Gaming Cafe with integrated payment processing, real-time availability management, and multi-role dashboard support.

## 🚀 Features

- **Multi-Role System**
  - Customer Dashboard: Book gaming slots, view bookings, manage profile
  - Cafe Owner Dashboard: Manage games, slots, view bookings and revenue
  - TapNex Superuser: Platform analytics, commission management, system settings

- **Booking Management**
  - Real-time slot availability
  - Multiple game stations support
  - Flexible time slot generation
  - Booking confirmation and notifications

- **Payment Integration**
  - Razorpay payment gateway
  - Secure payment processing
  - Commission tracking

- **Authentication**
  - Email/Password authentication
  - Google OAuth integration
  - Role-based access control
  - Session management

## 🛠️ Technology Stack

- **Backend:** Django 5.2.7, Python 3.9+
- **Database:** PostgreSQL (Supabase)
- **Frontend:** Tailwind CSS v4
- **Payment:** Razorpay
- **Authentication:** Django Allauth, Google OAuth
- **Hosting:** Vercel (Serverless)
- **Real-time:** Supabase Realtime

## 📦 Project Structure

```
FGC/
├── authentication/          # User authentication and roles
│   ├── models.py           # Customer, CafeOwner, TapNexSuperuser models
│   ├── views.py            # Login, registration, dashboard views
│   └── management/         # Management commands
├── booking/                # Booking system
│   ├── models.py           # Game, Slot, Booking models
│   ├── views.py            # Booking flow views
│   └── services/           # Business logic
├── gaming_cafe/            # Django project settings
│   ├── settings.py         # Configuration
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI application
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS)
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
├── vercel.json             # Vercel configuration
└── manage.py               # Django management script
```

## 🚦 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL (or Supabase account)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/prabhavjain2004/FCB.git
   cd FCB
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**
   ```bash
   npm install
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Build CSS**
   ```bash
   npm run build-css
   npm run build-css-prod
   ```

7. **Run migrations**
   ```bash
   python manage.py migrate
   python manage.py makemigrations
   python manage.py collectstatic

   ```

8. **Create test users (development only)**
   ```bash
   python manage.py create_test_users --password YourPassword123
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit http://localhost:8000

## 🌐 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

### Quick Deploy to Vercel

1. Fork/clone this repository
2. Sign up at https://vercel.com
3. Import your repository
4. Set environment variables (see [VERCEL_ENV_SETUP.md](VERCEL_ENV_SETUP.md))
5. Deploy!

## 🔐 Environment Variables

Required environment variables:

```bash
SECRET_KEY=              # Django secret key
DEBUG=False              # Set to False in production
DATABASE_URL=            # PostgreSQL connection string
SUPABASE_URL=            # Supabase project URL
SUPABASE_KEY=            # Supabase anon key
RAZORPAY_KEY_ID=         # Razorpay API key
RAZORPAY_KEY_SECRET=     # Razorpay secret
GOOGLE_OAUTH_CLIENT_ID=  # Google OAuth client ID
GOOGLE_OAUTH_CLIENT_SECRET=  # Google OAuth secret
```

See [.env.example](.env.example) for complete list.

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [Deployment Checklist](DEPLOYMENT_CHECKLIST.md) - Pre-deployment checklist
- [Vercel Environment Setup](VERCEL_ENV_SETUP.md) - Environment variables guide
- [Razorpay Integration](RAZORPAY_APPLICATION_DATA.md) - Payment setup
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical details

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

## 👥 User Roles

### Customer
- Browse available games and slots
- Make bookings
- View booking history
- Manage profile

### Cafe Owner
- Manage games and gaming stations
- Configure slot timings
- View all bookings
- Access revenue reports

### TapNex Superuser
- Platform-wide analytics
- Commission management
- Cafe owner management
- System configuration

## 🔒 Security Features

- Environment-based configuration
- Secure password hashing
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure cookie handling
- HTTPS enforcement (production)

## 📄 License

Proprietary - TapNex Technologies

## 👨‍💻 Development Team

**TapNex Technologies**
- Website: https://forge.tapnex.tech
- Email: support@tapnex.tech

## 🤝 Contributing

This is a private project. For bug reports or feature requests, please contact support@tapnex.tech

## 📞 Support

- Email: support@tapnex.tech
- Documentation: See /docs folder
- Issues: Contact the development team

## 🎯 Roadmap

- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Loyalty program
- [ ] Multi-cafe support
- [ ] Tournament management
- [ ] Social features

## ⚙️ Configuration

### Database

The project uses PostgreSQL via Supabase. Configure the connection string in `DATABASE_URL`.

### Payment Gateways

- **Razorpay:** Primary payment processor

### OAuth Providers

- Google OAuth for social login
- Configurable via Django Allauth

## 🐛 Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings

2. **Database connection error**
   - Verify DATABASE_URL is correct
   - Check Supabase connection limits

3. **OAuth not working**
   - Verify redirect URIs match
   - Check OAuth credentials

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for more troubleshooting tips.

---

**Built with ❤️ by TapNex Technologies**
