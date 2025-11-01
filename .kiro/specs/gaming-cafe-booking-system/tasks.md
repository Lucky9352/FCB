# Implementation Plan

- [x] 1. Set up Django project structure and core configuration
  - Create Django project with proper directory structure
  - Configure settings for development and production environments
  - Set up Supabase database connection and environment variables
  - Configure Tailwind CSS integration with Django
  - Set up static files handling for Vercel deployment
  - _Requirements: 12.1, 12.4_

- [x] 2. Implement user authentication system
  - [x] 2.1 Set up Django authentication models and views
    - Create custom user model extensions for Customer, CafeOwner, and TapNexSuperuser
    - Implement manual login/logout views with form validation
    - Create password complexity validation and session timeout
    - _Requirements: 2.1, 2.2, 2.4, 2.5_

  - [x] 2.2 Integrate Google OAuth for customer authentication
    - Install and configure django-allauth with Google provider
    - Create Google OAuth login flow with loading indicators and smooth transitions
    - Implement automatic customer profile creation from Google data with avatar display
    - Add comprehensive error handling for authentication failures with retry options
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [x] 2.3 Implement role-based access control and custom dashboards
    - Create permission decorators for different user roles (Customer, CafeOwner, TapNexSuperuser)
    - Set up URL routing with role-based restrictions and dashboard redirects
    - Disable Django admin panel access and redirect to custom dashboards
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 7.4_

- [x] 3. Create core data models for games and hybrid booking system





  - [x] 3.1 Implement Game model with automatic slot generation


    - Create Game model with capacity, booking_type (single/hybrid), schedule settings
    - Add fields: opening_time, closing_time, slot_duration_minutes, available_days
    - Implement pricing fields: private_price, shared_price for hybrid games
    - Add image upload functionality and game status management
    - _Requirements: 4.1, 4.2, 4.3, 10.1_


  - [ ] 3.2 Implement GameSlot and SlotAvailability models
    - Create GameSlot model for both auto-generated and custom slots
    - Implement SlotAvailability model for real-time capacity tracking
    - Add unique constraints and validation for slot conflicts
    - Create automatic slot generation algorithm based on game schedule
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_


  - [ ] 3.3 Implement hybrid booking system models
    - Create Booking model supporting both private and shared booking types
    - Add fields: booking_type, spots_booked, price_per_spot, total_amount
    - Implement booking validation with capacity checking and conflict resolution
    - Create real-time availability updates using Supabase integration

    - _Requirements: 3.2, 3.3, 3.5, 11.1, 11.2, 11.3, 11.5_

  - [ ] 3.4 Set up Supabase real-time integration for capacity tracking
    - Configure Supabase client for real-time subscriptions
    - Implement real-time booking availability updates and capacity broadcasting
    - Add conflict resolution for simultaneous booking attempts with database locking
    - Create booking service with hybrid booking logic and validation
    - _Requirements: 3.5, 12.3, 12.5_

- [ ] 4. Build responsive UI components with Tailwind CSS
  - [ ] 4.1 Create base templates and navigation
    - Design responsive header with role-based navigation menus
    - Implement mobile-friendly hamburger menu with touch optimization
    - Create footer with consistent styling and accessibility compliance
    - _Requirements: 8.1, 8.2, 8.3, 8.5_

  - [ ] 4.2 Design authentication pages
    - Create customer login page with prominently styled Google OAuth button
    - Design cafe owner login page with professional manual form styling
    - Add loading states, smooth transitions, and user-friendly error messages
    - Implement responsive design for all screen sizes with touch optimization
    - _Requirements: 1.1, 1.2, 1.4, 2.1, 8.1, 8.2, 8.4_

  - [ ] 4.3 Build game display components with hybrid booking options
    - Create game cards showing both private and shared booking options
    - Implement availability indicators with real-time capacity updates
    - Add clear pricing display for both booking types with capacity information
    - Design responsive grid layout with mobile-optimized booking interface
    - _Requirements: 3.1, 8.1, 8.2, 11.1, 11.4_

- [ ] 5. Implement customer dashboard and hybrid booking flow
  - [ ] 5.1 Create customer dashboard
    - Build welcome section with user avatar and Google profile information
    - Implement booking history with status indicators and filtering options
    - Add browse games section showing available slots with hybrid options
    - Design responsive layout with touch-optimized elements for mobile
    - _Requirements: 1.5, 7.1, 8.2_

  - [ ] 5.2 Build hybrid booking selection interface
    - Create booking option selector showing private vs shared choices
    - Implement capacity indicators and remaining spots display with real-time updates
    - Add booking summary with clear pricing breakdown for selected option
    - Design mobile-optimized booking flow with progress indicators
    - _Requirements: 3.1, 3.2, 8.1, 8.4, 11.1, 11.2, 11.3, 11.4, 11.5_

  - [ ] 5.3 Implement booking confirmation system
    - Create booking confirmation page with animated elements and booking details
    - Add email notification system for booking confirmations
    - Implement in-app notification display with booking status updates
    - _Requirements: 3.3_

- [ ] 6. Integrate payment gateway with hybrid pricing support
  - [ ] 6.1 Set up payment processing for hybrid bookings
    - Integrate Stripe/PayPal payment gateway with dynamic pricing calculation
    - Create payment intent and processing flow for both private and shared bookings
    - Implement secure payment form with validation and pricing breakdown
    - Add commission calculation for TapNex revenue tracking
    - _Requirements: 3.2, 5.3_

  - [ ] 6.2 Handle payment success and failure scenarios
    - Create payment success page with confirmation details and booking information
    - Implement payment failure handling with retry options and booking preservation
    - Add automatic booking cancellation for failed payments with capacity release
    - Design user-friendly error messages with alternative payment options
    - _Requirements: 3.3, 3.4_

- [ ] 7. Build cafe owner dashboard and game management tools
  - [ ] 7.1 Create cafe owner dashboard
    - Build overview section with daily metrics (revenue, bookings, capacity utilization)
    - Implement live game status display showing current bookings and availability
    - Add quick action buttons for game management and custom slot creation
    - Design responsive dashboard layout with mobile-friendly interface
    - _Requirements: 7.2, 8.1, 8.2_

  - [ ] 7.2 Implement game creation and management interface
    - Create comprehensive game setup form with all required fields
    - Add schedule configuration: opening/closing times, slot duration, available days
    - Implement booking type selection (single vs hybrid) with pricing setup
    - Add form validation for schedule logic and pricing requirements
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ] 7.3 Build custom slot management features
    - Create interface for adding temporary/custom slots outside regular hours
    - Add validation to prevent slot conflicts and overlapping bookings
    - Implement custom slot display alongside auto-generated slots
    - Add bulk slot operations and booking preservation during updates
    - _Requirements: 4.5, 10.3, 10.4, 10.5_

  - [ ] 7.4 Implement booking management and analytics
    - Create booking list with customer details, status, and capacity information
    - Add booking modification and cancellation functionality
    - Implement analytics dashboard with revenue and utilization metrics
    - Remove walk-in booking functionality to enforce online-only policy
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 8. Implement TapNex superuser dashboard and commission management





  - [x] 8.1 Create TapNex superuser dashboard


    - Build commission overview with revenue analytics and financial calculations
    - Implement system-wide analytics showing gross revenue, commission amounts, net payouts
    - Add cafe owner account management interface with password reset functionality
    - Design comprehensive dashboard with commission settings and platform fee configuration
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 8.2 Implement commission and revenue tracking system


    - Create commission calculation engine with configurable rates and platform fees
    - Add detailed revenue reports with breakdown by booking type and time period
    - Implement financial analytics with commission tracking and payout calculations
    - Add system-wide monitoring and cafe owner account management tools
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 9. Add accessibility and performance optimizations
  - [ ] 9.1 Implement accessibility features
    - Add ARIA labels and semantic HTML structure throughout the application
    - Ensure keyboard navigation support for all interactive elements
    - Implement screen reader compatibility with proper heading structure
    - Test color contrast and visual accessibility compliance with WCAG 2.1
    - _Requirements: 8.5_

  - [ ] 9.2 Optimize performance for Vercel deployment
    - Configure static file optimization and compression for faster loading
    - Implement lazy loading for images and components to improve page speed
    - Optimize database queries and add proper indexing for slot and booking queries
    - Set up caching strategies and achieve page load times under 3 seconds
    - _Requirements: 12.1, 12.5_

- [ ]* 10. Testing and quality assurance
  - [ ]* 10.1 Write unit tests for core functionality
    - Create tests for user authentication and role-based authorization
    - Test game model validation and automatic slot generation algorithm
    - Add hybrid booking system tests with capacity validation and conflict resolution
    - Test payment processing with mocked services and commission calculations
    - _Requirements: All core requirements_

  - [ ]* 10.2 Implement integration tests
    - Test complete hybrid booking flow from game selection to payment confirmation
    - Verify real-time updates and capacity tracking across multiple concurrent users
    - Test role-based access control and custom dashboard functionality
    - Add end-to-end tests for slot generation and booking management workflows
    - _Requirements: 3.1-3.5, 7.1-7.4, 11.1-11.5_

- [ ] 11. Deploy and configure production environment
  - [ ] 11.1 Set up Vercel deployment configuration
    - Configure build settings and environment variables for production
    - Set up custom domain and SSL certificate management
    - Implement proper error handling, logging, and monitoring integration
    - Configure Supabase production database with security rules and backup procedures
    - _Requirements: 12.1, 12.2, 12.4_

  - [ ] 11.2 Configure production monitoring and maintenance
    - Set up application monitoring and error tracking with performance metrics
    - Implement backup and recovery procedures for database and file storage
    - Add system health monitoring and automated alerting for critical issues
    - Configure production logging and analytics for system optimization
    - _Requirements: 12.2, 12.3, 12.5_