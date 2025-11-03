## Booking Error Fix - Checklist

### Issue
When clicking "Book Private" or "Book Shared" buttons:
- Error: `Unexpected token '<', '<!DOCTYPE'... is not valid JSON`
- This means the server is returning HTML instead of JSON

### Possible Causes
1. ✅ **URL Mismatch** - FIXED: Changed from `/booking/hybrid-booking/create/` to `/booking/games/book/`
2. ✅ **Authentication Check** - FIXED: Added proper auth checks with JSON responses
3. ✅ **JSON Parsing Error** - FIXED: Added try-catch for JSON decode errors
4. ✅ **Missing Import** - FIXED: Added ValidationError import

### What to Check in Browser
1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Click a "Book Private" button
4. Look at the request to `/booking/games/book/`
5. Check:
   - **Request URL**: Should be `http://localhost:8000/booking/games/book/`
   - **Request Method**: Should be `POST`
   - **Request Headers**: Should include `Content-Type: application/json`
   - **Request Body**: Should be JSON like `{"game_slot_id":"...","booking_type":"PRIVATE","spots_requested":1}`
   - **Response Status**: Check if it's 200, 401, 403, 400, or 500
   - **Response Body**: Should be JSON, not HTML

### Quick Test
1. Make sure you're logged in as a customer
2. Try booking a slot
3. If you see HTML response, check the Response tab in Network panel
4. Look for the actual error message

### If Still Getting HTML Response
Check if:
- CSRF token is being sent correctly
- User is authenticated (check `request.user.is_authenticated`)
- User has customer_profile
- The view is returning JsonResponse, not rendering a template

### Server-Side Debugging
Run the development server and watch the terminal for errors when clicking the book button.

```bash
cd e:/FGC
python manage.py runserver
```

Then in another terminal, test the endpoint:

```bash
curl -X POST http://localhost:8000/booking/games/book/ \
  -H "Content-Type: application/json" \
  -d '{"game_slot_id":"YOUR_SLOT_ID","booking_type":"PRIVATE","spots_requested":1}'
```

This will show if the endpoint is working at all.
