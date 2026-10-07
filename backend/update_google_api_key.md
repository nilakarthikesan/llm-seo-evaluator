# Google provider configuration

Set `GOOGLE_API_KEY` in `backend/.env` or the process environment. Keep credentials outside the source files.

From the backend directory, the development script can exercise configured Google models:

```bash
python test_google_models.py
```

The script makes live API requests. Model selection is configured in `app/core/config.py` and the provider adapter. The checked-in defaults are historical; confirm model availability, quotas, and pricing for the configured account before a live run. A paid account can still be rate limited.
