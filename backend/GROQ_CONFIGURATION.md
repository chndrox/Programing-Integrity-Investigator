# Groq API Configuration

## ✅ Status: Configured Successfully

Your Groq API key has been configured and is ready to use.

---

## Configuration Details

### API Key
```
Groq API Key: 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
```
**Status:** ✓ Configured in `.env` file  
**Location:** `c:\Users\lenovo\OneDrive\Desktop\PII\backend\.env`

### Model Configuration
```
Model: mixtral-8x7b-32768
```
This is a powerful 8x7B parameter mixture-of-experts model optimized for code and reasoning tasks.

---

## What Was Done

1. ✅ Created `.env` file in backend directory
2. ✅ Added Groq API key to configuration
3. ✅ Configured Groq model (mixtral-8x7b-32768)
4. ✅ Set up additional environment variables
5. ✅ Verified settings load correctly
6. ✅ Restarted backend server
7. ✅ Confirmed Groq service initialization

---

## Environment Variables Configured

The following configuration has been set in `.env`:

```bash
# Groq API Configuration
GROQ_API_KEY=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
GROQ_MODEL=mixtral-8x7b-32768

# Database Configuration
DATABASE_URL=sqlite:///./pii.db

# Security Configuration
SECRET_KEY=your-secret-key-change-this-in-production-to-a-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload Configuration
MAX_FILE_SIZE=10485760
UPLOAD_DIR=./uploads

# Agent Configuration
AGENT_CONCURRENCY_LIMIT=2
AGENT_TIMEOUT_SECONDS=120

# MCP Configuration
USE_MOCK_MCP=True
```

---

## How Groq is Used in Your Backend

The Groq API is used by the AI agents for:

1. **Similarity Analysis** - Detecting code similarities between submissions
2. **Timeline Analysis** - Analyzing git commit histories
3. **Case Report Writing** - Generating investigation reports
4. **Exculpatory Review** - Identifying legitimate explanations

### Code Usage Example

```python
from app.services.groq_service import get_groq_service

# Initialize Groq service
groq_service = get_groq_service()

# Use in agents
response = await groq_service.complete(
    messages=[
        {"role": "system", "content": "You are a code similarity analyst"},
        {"role": "user", "content": "Analyze these two code submissions..."}
    ]
)
```

---

## Verification

### ✓ Configuration Loaded
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\python -c "from app.database import settings; print(f'Groq API Key: {settings.groq_api_key[:20]}...')"
```

Output:
```
Groq API Key: gsk_THNIz7LTrqFa2x4d...
```

### ✓ Service Initialization
```powershell
cd c:\Users\lenovo\OneDrive\Desktop\PII\backend
venv\Scripts\python -c "from app.services.groq_service import get_groq_service; service = get_groq_service(); print('Groq service OK')"
```

Output:
```
Groq service OK
```

### ✓ Backend Running
Server is running with Groq configuration at:
- **URL:** http://127.0.0.1:8000
- **Health:** http://127.0.0.1:8000/health

---

## Security Notes

### ⚠️ Important: API Key Security

1. **DO NOT commit `.env` to git**
   - The `.env` file is in `.gitignore` by default
   - Never share your API key publicly

2. **API Key Rotation**
   - If you need to rotate the key, update it in `.env`
   - Restart the backend server

3. **Production Deployment**
   - Use environment variables instead of `.env` file
   - Store keys in secure secret management systems
   - Update `SECRET_KEY` to a strong random value

---

## Updating the API Key

If you need to change the Groq API key later:

### Method 1: Edit .env file
```powershell
# Open .env file
notepad c:\Users\lenovo\OneDrive\Desktop\PII\backend\.env

# Update the line:
GROQ_API_KEY=your-new-api-key-here

# Restart backend
.\start_backend.ps1
```

### Method 2: Environment Variable (Temporary)
```powershell
$env:GROQ_API_KEY="your-new-api-key-here"
venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

## Testing Groq Integration

Once your backend is running, you can test the Groq integration by:

### 1. Starting an Investigation
```bash
POST /api/investigations/start
```
This will trigger the AI agents which use Groq.

### 2. Check Agent Logs
Watch the backend console output for Groq API calls:
```
INFO: Calling Groq API for similarity analysis...
INFO: Groq response received
```

---

## Groq API Limits

Be aware of Groq API rate limits and quotas:

- **Free Tier:** Check Groq documentation for current limits
- **Rate Limiting:** Built into the Groq client library
- **Error Handling:** Backend has retry logic for transient failures

Monitor usage at: https://console.groq.com

---

## Available Groq Models

You can change the model in `.env`:

| Model | Context | Speed | Best For |
|-------|---------|-------|----------|
| mixtral-8x7b-32768 | 32K tokens | Fast | General reasoning (Current) |
| llama-3.1-8b-instant | 128K tokens | Very Fast | Quick responses |
| llama-3.1-70b-versatile | 128K tokens | Moderate | Complex analysis |
| llama-3.3-70b-versatile | 128K tokens | Moderate | Latest capabilities |

To change:
```bash
# In .env file
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Troubleshooting

### Issue: "Invalid API Key" error

**Solution:**
1. Verify key is correct in `.env`
2. Check for extra spaces or quotes
3. Restart backend server

```powershell
# Verify key
cat .env | Select-String GROQ_API_KEY

# Should show:
GROQ_API_KEY=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
```

### Issue: "Rate limit exceeded"

**Solution:**
- Wait a few seconds between requests
- Consider upgrading Groq plan
- Implement request queuing in application

### Issue: API key not loading

**Solution:**
```powershell
# Check .env exists
Test-Path .env

# Check settings load
venv\Scripts\python -c "from app.database import settings; print(settings.groq_api_key)"

# Restart backend
.\start_backend.ps1
```

---

## Environment File Location

```
c:\Users\lenovo\OneDrive\Desktop\PII\backend\.env
```

**Important:** This file is ignored by git (in `.gitignore`) for security.

---

## Summary

✅ **Groq API Key:** Configured  
✅ **Model:** mixtral-8x7b-32768  
✅ **Backend:** Running with Groq integration  
✅ **AI Agents:** Ready to use Groq for analysis  
✅ **Security:** API key stored in `.env` (not in git)  

Your backend is now fully configured to use Groq for AI-powered plagiarism detection and analysis! 🎉

---

## Next Steps

1. **Test the integration** - Start an investigation to see Groq in action
2. **Monitor usage** - Check Groq console for API usage
3. **Adjust settings** - Tune agent parameters in `.env` if needed

For more information on Groq capabilities, visit: https://console.groq.com/docs
