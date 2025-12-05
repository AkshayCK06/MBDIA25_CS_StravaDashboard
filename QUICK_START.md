# Quick Start Guide - Strava Dashboard

This guide will get you up and running in 5 steps with NO hassle!

## Prerequisites
- Python 3.9 or higher installed
- A Strava account with some activities

---

## Step 1: Set Up Virtual Environment

### On Mac/Linux:
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### On Windows:
```bash
# Run setup
setup.bat
```

### Manual Setup (if scripts don't work):
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 2: Register Your Strava Application

1. **Go to**: https://www.strava.com/settings/api

2. **Click**: "Create An App" button

3. **Fill in the form**:
   ```
   Application Name: My Strava Dashboard
   Category: Data Importer (or your choice)
   Club: (leave blank)
   Website: http://localhost:8501
   Authorization Callback Domain: localhost
   ```

4. **Click**: "Create"

5. **Copy these values** (you'll need them next):
   - Client ID (a number like: 123456)
   - Client Secret (a long string like: abc123def456...)

---

## Step 3: Configure Credentials

### Mac/Linux:
```bash
# Copy template
cp .env.example .env

# Edit with your favorite editor
nano .env
# or
vim .env
# or
code .env
```

### Windows:
```bash
# Copy template
copy .env.example .env

# Edit with notepad
notepad .env
```

### Edit the .env file:
Replace the placeholder values with your actual credentials:
```
STRAVA_CLIENT_ID=123456
STRAVA_CLIENT_SECRET=abc123def456...
```

**Save and close** the file.

---

## Step 4: Authenticate with Strava

### Activate virtual environment first:
```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Run authentication:
```bash
python auth.py
```

**What happens:**
1. Your browser will open to Strava's authorization page
2. Click **"Authorize"** to grant access
3. You'll be redirected to a URL like: `http://localhost:8501/?state=&code=XXXXX&scope=...`
4. **Copy the ENTIRE URL** from your browser
5. **Paste it** into the terminal when prompted
6. Press Enter

**Success!** You should see:
```
Authentication successful!
Token saved to cache/strava_token.json
```

---

## Step 5: Fetch Your Data

```bash
python data_manager.py
```

**What happens:**
- Fetches all your Strava activities
- Saves to `data/activities.json` (raw data)
- Saves to `data/activities.csv` (spreadsheet format)
- Shows progress as it downloads

**This may take a minute if you have many activities!**

---

## Verify Everything Works

Test data processing:
```bash
python data_processing.py
```

You should see:
- Summary statistics
- Activity breakdown by type
- Personal records

---

## Troubleshooting

### "Command not found: python"
Try `python3` instead of `python`

### "No module named 'requests'" (or similar)
Make sure virtual environment is activated:
```bash
# Check if (venv) appears in your prompt
# If not, activate it again:
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
```

### "Missing Strava API credentials"
- Make sure `.env` file exists (not `.env.example`)
- Check that you saved the file after editing
- Verify credentials are correct (no extra spaces)

### "Invalid redirect URL"
- Make sure you copied the ENTIRE URL including `http://localhost:8501/?...`
- The URL should start with `http://localhost:8501/?state=&code=`

### Browser doesn't open automatically
- Copy the URL shown in terminal
- Paste it into your browser manually
- Continue with authorization

---

## For Your Teammate (Siddhanth)

To run this project on another computer:

1. **Clone the repository**
2. **Run setup script** (Step 1)
3. **Copy the `.env` file** (you can share this securely - it's just the client ID/secret)
4. **Run authentication** (Step 4) - each person needs to authenticate with their own Strava account
5. **Fetch data** (Step 5)

**Note**: The `.env` file and authentication tokens are in `.gitignore`, so they won't be committed to Git. You'll need to share the `.env` file separately (via secure messaging).

---

## Next Steps

Once you have data:
- Explore the CSV in Excel/Google Sheets: `data/activities.csv`
- Start building the Streamlit dashboard (Week 2)
- Add visualizations with Plotly (Week 2)

---

## Quick Command Reference

```bash
# Activate virtual environment
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Deactivate virtual environment
deactivate

# Re-authenticate
python auth.py

# Refresh data from Strava
python data_manager.py

# View statistics
python data_processing.py

# Check configuration
python config.py
```

---

## Need Help?

Check the detailed [setup_guide.md](setup_guide.md) for more information.
