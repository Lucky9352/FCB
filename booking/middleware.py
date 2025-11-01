"""
Middleware to automatically maintain slot availability
Runs background checks without blocking requests
"""
from .auto_slot_generator import check_and_generate_daily_slots
import logging

logger = logging.getLogger(__name__)


class AutoSlotMaintenanceMiddleware:
    """
    Middleware that ensures slots are automatically generated
    Checks once per day on first request
    Runs in background - doesn't slow down user requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check and generate slots in background (once per day)
        # This doesn't block the request - runs in a separate thread
        try:
            check_and_generate_daily_slots()
        except Exception as e:
            # Don't let slot generation errors break the site
            logger.error(f"Error in auto slot maintenance: {str(e)}")
        
        # Process the request normally
        response = self.get_response(request)
        
        return response
