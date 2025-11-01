# Requirements Document

## Introduction

A modern, responsive gaming cafe booking system built with Django and Supabase as a SaaS solution by TapNex Technologies for a single gaming cafe establishment. The system enables customers to book gaming slots exclusively online (no walk-in bookings) and provides comprehensive management tools for cafe owners and TapNex administrators. The system features a sleek UI/UX design with Tailwind CSS, integrates Google OAuth for customer authentication, custom dashboards for all user roles, payment gateway integration, and commission tracking. The application is optimized for Vercel deployment with focus on performance and user experience.

## Glossary

- **Gaming_Cafe_System**: The complete Django-based SaaS booking platform for a single gaming cafe
- **Customer**: End users who book games exclusively online through the web interface
- **Cafe_Owner**: The gaming cafe proprietor who manages games, settings, and daily operations through custom dashboard
- **TapNex_Superuser**: TapNex Technologies administrator who manages commission settings, revenue tracking, and cafe owner account
- **Gaming_Slot**: A bookable time period for a specific game automatically generated based on game schedule and duration
- **Game**: Bookable gaming resource (8-ball pool, table tennis, PS4 Console 1, etc.) with defined capacity, schedule, and pricing
- **Auto_Generated_Slots**: Time slots automatically created by the system based on game opening/closing times and slot duration
- **Custom_Slots**: Additional temporary slots manually added by cafe owner for specific games and dates
- **Hybrid_Booking**: Booking system allowing customers to book either private (full capacity) or shared (individual spots) for multi-player games
- **Private_Booking**: Booking the entire game capacity for a group at private rate
- **Shared_Booking**: Booking individual spots in multi-player games to play with other customers
- **Game_Capacity**: Maximum number of players that can use a game simultaneously
- **Commission_Model**: TapNex Technologies' revenue sharing structure from booking transactions
- **Payment_Gateway**: Third-party service for processing customer payments
- **Google_OAuth**: Google's authentication service for customer login
- **Custom_Dashboard**: Role-specific responsive interface replacing Django admin panel
- **Supabase_Database**: PostgreSQL database service for data storage and real-time features
- **Tailwind_CSS**: Utility-first CSS framework for responsive design
- **Vercel_Platform**: Deployment platform for the Django application

## Requirements

### Requirement 1

**User Story:** As a customer, I want to authenticate using my Google account, so that I can quickly access the booking system without creating separate credentials.

#### Acceptance Criteria

1. WHEN a customer visits the login page, THE Gaming_Cafe_System SHALL display a prominently styled Google authentication button with clear visual hierarchy
2. WHEN a customer clicks the Google authentication button, THE Gaming_Cafe_System SHALL show a loading indicator and redirect to Google OAuth service
3. WHEN Google OAuth returns successful authentication, THE Gaming_Cafe_System SHALL create or update the customer account automatically with smooth transition animation
4. WHEN authentication fails, THE Gaming_Cafe_System SHALL display a user-friendly error message with retry option and return to the login page
5. THE Gaming_Cafe_System SHALL store customer profile information received from Google OAuth and display welcome message with user avatar

### Requirement 2

**User Story:** As a cafe owner, I want to use manual login credentials, so that I can securely access administrative functions with controlled access.

#### Acceptance Criteria

1. WHEN a cafe owner visits the admin login page, THE Gaming_Cafe_System SHALL display username and password fields with professional styling
2. WHEN valid credentials are entered, THE Gaming_Cafe_System SHALL authenticate the user and redirect to the cafe owner dashboard
3. WHEN invalid credentials are entered, THE Gaming_Cafe_System SHALL display an error message and remain on the login page
4. THE Gaming_Cafe_System SHALL enforce password complexity requirements for cafe owner accounts
5. THE Gaming_Cafe_System SHALL implement session timeout for security

### Requirement 3

**User Story:** As a customer, I want to book games with flexible private or shared options, so that I can choose between booking the entire game for my group or joining other players at a lower cost.

#### Acceptance Criteria

1. WHEN a customer browses available games, THE Gaming_Cafe_System SHALL display games with available time slots showing both private and shared booking options where applicable
2. WHEN a game slot is completely available, THE Gaming_Cafe_System SHALL show both private booking option (full capacity at private rate) and shared booking option (individual spots at shared rate) for hybrid games
3. WHEN a customer books a private slot, THE Gaming_Cafe_System SHALL mark the entire slot as unavailable and prevent any shared bookings for that time
4. WHEN a customer books a shared spot, THE Gaming_Cafe_System SHALL remove the private booking option and show remaining shared spots available for that time slot
5. THE Gaming_Cafe_System SHALL prevent overbooking by tracking capacity and updating availability in real-time using Supabase real-time features

### Requirement 4

**User Story:** As a cafe owner, I want to create games with automatic slot generation and flexible booking options, so that I can efficiently manage game schedules and maximize revenue through different booking types.

#### Acceptance Criteria

1. WHEN a cafe owner creates a new game, THE Gaming_Cafe_System SHALL require game name, description, capacity, opening time, closing time, slot duration (in minutes), available days of week, and booking type (single or hybrid)
2. WHEN booking type is single, THE Gaming_Cafe_System SHALL require only private booking price for the full game capacity
3. WHEN booking type is hybrid, THE Gaming_Cafe_System SHALL require both private booking price (full capacity) and shared booking price (per individual spot)
4. WHEN a game is created, THE Gaming_Cafe_System SHALL automatically generate time slots based on opening/closing times and slot duration for all selected days of the week
5. THE Gaming_Cafe_System SHALL allow the cafe owner to add custom temporary slots for specific games on particular dates outside regular operating hours

### Requirement 5

**User Story:** As a TapNex superuser, I want to manage commission settings, revenue tracking, and cafe owner account through a custom dashboard, so that I can oversee the SaaS business operations and financial aspects.

#### Acceptance Criteria

1. WHEN a TapNex superuser logs in, THE Gaming_Cafe_System SHALL display the superuser dashboard with commission overview and revenue analytics
2. THE Gaming_Cafe_System SHALL allow TapNex superusers to configure commission rates and platform fees
3. THE Gaming_Cafe_System SHALL allow TapNex superusers to view detailed revenue reports including gross revenue, commission amounts, and net payouts
4. THE Gaming_Cafe_System SHALL allow TapNex superusers to manage the cafe owner account including password resets and account modifications
5. THE Gaming_Cafe_System SHALL allow TapNex superusers to access system-wide analytics and financial calculations through custom dashboard interface

### Requirement 6

**User Story:** As a system architect, I want all administrative functions handled through custom dashboards only, so that business operations are streamlined and user experience is consistent across all roles.

#### Acceptance Criteria

1. THE Gaming_Cafe_System SHALL provide all administrative functions through role-specific custom dashboards
2. THE Gaming_Cafe_System SHALL disable Django admin panel access for all user types
3. THE Gaming_Cafe_System SHALL redirect any admin URL attempts to the appropriate role-based login page
4. THE Gaming_Cafe_System SHALL ensure cafe owner management functions are available through TapNex superuser dashboard
5. THE Gaming_Cafe_System SHALL maintain system security through custom authentication and authorization in dashboards

### Requirement 7

**User Story:** As a user of any role, I want to access a custom dashboard tailored to my permissions, so that I can efficiently perform my role-specific tasks without using Django admin interface.

#### Acceptance Criteria

1. WHEN a customer logs in, THE Gaming_Cafe_System SHALL display the customer dashboard with booking history and browse interface showing available games
2. WHEN a cafe owner logs in, THE Gaming_Cafe_System SHALL display the owner dashboard with game management, booking overview, and analytics tools
3. WHEN a TapNex superuser logs in, THE Gaming_Cafe_System SHALL display the superuser dashboard with commission management, revenue analytics, and cafe owner account management
4. THE Gaming_Cafe_System SHALL prevent users from accessing dashboards outside their role permissions
5. THE Gaming_Cafe_System SHALL provide role-appropriate navigation and functionality in each custom dashboard with emphasis on simple game booking flow

### Requirement 8

**User Story:** As a user accessing the system from any device, I want a responsive and intuitive interface, so that I can easily navigate and complete tasks regardless of screen size.

#### Acceptance Criteria

1. THE Gaming_Cafe_System SHALL render responsively across desktop, tablet, and mobile devices using Tailwind CSS
2. WHEN a user accesses the system on mobile devices, THE Gaming_Cafe_System SHALL provide touch-optimized interface elements
3. THE Gaming_Cafe_System SHALL maintain consistent visual design language across all pages and components
4. THE Gaming_Cafe_System SHALL provide loading states and smooth transitions for enhanced user experience
5. THE Gaming_Cafe_System SHALL ensure accessibility compliance with WCAG 2.1 guidelines

### Requirement 9

**User Story:** As a gaming cafe business owner, I want to enforce online-only bookings with no walk-in options, so that I can ensure proper scheduling, payment processing, and customer management.

#### Acceptance Criteria

1. THE Gaming_Cafe_System SHALL require all customers to book games exclusively through the online platform
2. THE Gaming_Cafe_System SHALL not provide any walk-in booking functionality or manual booking options for cafe staff
3. THE Gaming_Cafe_System SHALL display clear messaging to customers that advance online booking is required
4. THE Gaming_Cafe_System SHALL ensure all game access is tied to confirmed online bookings with payment
5. THE Gaming_Cafe_System SHALL prevent any game usage without a valid online booking confirmation

### Requirement 10

**User Story:** As a cafe owner, I want the system to automatically generate time slots based on my game settings, so that customers can book specific time periods without manual slot creation.

#### Acceptance Criteria

1. WHEN a cafe owner sets game opening time (11 AM), closing time (11 PM), and slot duration (60 minutes), THE Gaming_Cafe_System SHALL automatically generate hourly slots (11-12 PM, 12-1 PM, etc.) for all selected days
2. WHEN a cafe owner updates game schedule or slot duration, THE Gaming_Cafe_System SHALL regenerate slots automatically while preserving existing bookings
3. THE Gaming_Cafe_System SHALL allow cafe owners to add custom temporary slots (like 11 PM - 5 AM on weekends) for specific games and dates
4. THE Gaming_Cafe_System SHALL display both auto-generated and custom slots to customers in a unified booking interface
5. THE Gaming_Cafe_System SHALL prevent slot conflicts and ensure custom slots do not overlap with existing bookings

### Requirement 11

**User Story:** As a customer booking a hybrid game, I want clear visibility of booking options and remaining capacity, so that I can make informed decisions about private vs shared bookings.

#### Acceptance Criteria

1. WHEN a customer views a hybrid game slot with full availability, THE Gaming_Cafe_System SHALL display both private booking option with full capacity price and shared booking option with per-spot price
2. WHEN shared spots are partially booked, THE Gaming_Cafe_System SHALL show only shared booking option with remaining spots count and hide private booking option
3. WHEN a customer books a shared spot, THE Gaming_Cafe_System SHALL immediately update the display to show reduced available spots for other customers
4. THE Gaming_Cafe_System SHALL clearly indicate the difference between private (exclusive use) and shared (play with others) booking options
5. THE Gaming_Cafe_System SHALL prevent customers from booking more shared spots than the remaining capacity

### Requirement 12

**User Story:** As a system operator, I want the application deployed on Vercel with Supabase integration, so that the system is scalable, performant, and maintainable.

#### Acceptance Criteria

1. THE Gaming_Cafe_System SHALL be deployed on Vercel platform with optimized build configuration
2. THE Gaming_Cafe_System SHALL connect to Supabase PostgreSQL database for data persistence
3. THE Gaming_Cafe_System SHALL utilize Supabase real-time features for live booking updates and capacity tracking
4. THE Gaming_Cafe_System SHALL implement proper environment variable management for different deployment stages
5. THE Gaming_Cafe_System SHALL achieve page load times under 3 seconds on standard internet connections