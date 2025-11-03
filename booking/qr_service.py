"""
QR Code Generation Service for Booking Verification
Fast and efficient QR code generation with unique verification tokens
"""

import qrcode
import secrets
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class QRCodeService:
    """Service for generating and managing booking QR codes"""
    
    @staticmethod
    def generate_verification_token():
        """Generate a secure unique verification token"""
        # Use secrets for cryptographically strong random token
        return secrets.token_urlsafe(32)  # Generates ~43 character string
    
    @staticmethod
    def generate_qr_code(booking):
        """
        Generate QR code for a booking
        
        Args:
            booking: Booking model instance
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate verification token if not exists
            if not booking.verification_token:
                booking.verification_token = QRCodeService.generate_verification_token()
            
            # Create QR code data - JSON format for easy parsing
            qr_data = {
                'booking_id': str(booking.id),
                'token': booking.verification_token,
                'type': 'booking_verification',
                'cafe': 'TapNex Gaming Cafe'
            }
            
            # Convert to string (can be JSON or simple format)
            # Using simple pipe-separated format for faster parsing
            qr_content = f"{booking.id}|{booking.verification_token}|booking"
            
            # Create QR code instance with optimized settings for speed
            qr = qrcode.QRCode(
                version=1,  # Controls size (1 is smallest, auto-adjusts if needed)
                error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium error correction (15%)
                box_size=10,  # Size of each box in pixels
                border=4,  # Border size in boxes
            )
            
            # Add data and generate
            qr.add_data(qr_content)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to BytesIO buffer
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Save to booking model
            filename = f'booking_{booking.id}_qr.png'
            booking.qr_code.save(filename, ContentFile(buffer.read()), save=False)
            
            # Save booking with updated fields
            booking.save(update_fields=['verification_token', 'qr_code'])
            
            logger.info(f"QR code generated successfully for booking {booking.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating QR code for booking {booking.id}: {str(e)}")
            return False
    
    @staticmethod
    def verify_token(token):
        """
        Verify a booking token from QR code scan
        
        Args:
            token: Verification token from QR code
            
        Returns:
            tuple: (success: bool, booking: Booking or None, message: str)
        """
        from .models import Booking
        
        try:
            # Fast database lookup using indexed field
            booking = Booking.objects.select_related(
                'customer', 
                'customer__user', 
                'game', 
                'game_slot'
            ).get(verification_token=token)
            
            # Check if booking is valid for verification
            if booking.status == 'CANCELLED':
                return False, booking, "This booking has been cancelled"
            
            if booking.status == 'COMPLETED':
                return False, booking, "This booking has already been completed"
            
            if booking.status != 'CONFIRMED' and booking.status != 'IN_PROGRESS':
                return False, booking, f"Booking status is {booking.get_status_display()}"
            
            # Check if already verified
            if booking.is_verified and booking.status == 'IN_PROGRESS':
                return True, booking, "Booking already verified and in progress"
            
            return True, booking, "Valid booking"
            
        except Booking.DoesNotExist:
            logger.warning(f"Invalid verification token attempted: {token[:10]}...")
            return False, None, "Invalid QR code or booking not found"
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return False, None, "Verification error occurred"
    
    @staticmethod
    def mark_as_verified(booking, verified_by_user=None):
        """
        Mark booking as verified after successful QR scan
        
        Args:
            booking: Booking instance
            verified_by_user: User who verified (owner/staff)
            
        Returns:
            bool: True if successful
        """
        try:
            booking.is_verified = True
            booking.verified_at = timezone.now()
            booking.verified_by = verified_by_user
            
            # Update status to IN_PROGRESS if currently CONFIRMED
            if booking.status == 'CONFIRMED':
                booking.status = 'IN_PROGRESS'
            
            booking.save(update_fields=['is_verified', 'verified_at', 'verified_by', 'status'])
            
            logger.info(f"Booking {booking.id} marked as verified by {verified_by_user}")
            return True
            
        except Exception as e:
            logger.error(f"Error marking booking as verified: {str(e)}")
            return False
    
    @staticmethod
    def regenerate_qr_code(booking):
        """
        Regenerate QR code for a booking (e.g., if lost or corrupted)
        
        Args:
            booking: Booking instance
            
        Returns:
            bool: True if successful
        """
        try:
            # Delete old QR code if exists
            if booking.qr_code:
                booking.qr_code.delete(save=False)
            
            # Reset verification fields
            booking.verification_token = ''
            booking.qr_code = None
            
            # Generate new QR code
            return QRCodeService.generate_qr_code(booking)
            
        except Exception as e:
            logger.error(f"Error regenerating QR code: {str(e)}")
            return False
