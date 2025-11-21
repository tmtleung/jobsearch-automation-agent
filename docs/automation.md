# Automation Guide  
Run the JobSearch AI Agent automatically on macOS, Linux, or Windows.

---

## macOS (launchd)

1. Create a plist file:
```
~/Library/LaunchAgents/com.jobsearch.agent.plist
```

2. Example plist:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>

    <key>EnvironmentVariables</key>
    <dict>
        <key>EMAIL_PASSWORD</key>
        <string>YOUR_APP_PASSWORD</string>
    </dict>

    <key>Label</key>
    <string>com.jobsearch.agent</string>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>9</integer>
        <key>Minute</key><integer>0</integer>
    </dict>

    <key>ProgramArguments</key>
    <array>
        <string>/FULL/PATH/TO/.venv/bin/python</string>
        <string>/FULL/PATH/TO/run_agent.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/FULL/PATH/TO/PROJECT</string>

    <key>StandardOutPath</key>
    <string>/FULL/PATH/TO/logs/agent.log</string>

    <key>StandardErrorPath</key>
    <string>/FULL/PATH/TO/logs/agent_error.log</string>

    <key>RunAtLoad</key>
    <true/>

</dict>
</plist>
```

Load the job:

```
launchctl load ~/Library/LaunchAgents/com.jobsearch.agent.plist
```

Start manually:

```
launchctl start com.jobsearch.agent
```

---

## Linux (cron)

Edit your crontab:
```
crontab -e
```

Daily at 9 AM example:
```
0 9 * * * /usr/bin/python3 /path/to/run_agent.py
```

---

## Windows (Task Scheduler)

1. Open Task Scheduler  
2. Create a task  
3. Action → “Start a Program”  
    - Program: `python.exe`  
    - Arguments: `C:\path\to\run_agent.py`  
4. Set your schedule  
5. Save  
