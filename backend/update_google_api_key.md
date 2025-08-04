# Google API Key Update Guide

## After getting your paid plan API key:

1. **Update your .env file**:
   ```bash
   # In backend/.env
   GOOGLE_API_KEY=your_new_paid_plan_api_key_here
   ```

2. **Test the new key**:
   ```bash
   python test_google_models.py
   ```

3. **Switch back to gemini-1.5-pro** (better model with paid plan):
   ```bash
   # In backend/app/core/config.py, change:
   "google": "gemini-1.5-pro"  # Instead of gemini-1.5-flash
   ```

## Paid Plan Benefits:
- **Higher rate limits**: 15 requests/second vs 1 request/second
- **Higher daily limits**: 1,500 requests/day vs 150 requests/day
- **Better models**: Access to gemini-1.5-pro (more powerful)
- **No rate limiting**: Smooth development experience

## Pricing (Approximate):
- **Input tokens**: $0.00025 / 1K tokens
- **Output tokens**: $0.0005 / 1K tokens
- **Typical cost**: $1-5/month for development
- **Budget alerts**: Set up to avoid surprises 