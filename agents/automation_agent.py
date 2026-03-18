# agents/automation_agent.py
import subprocess
from core.memory import log_event


SAFE_APPS = [
    "Safari", "Chrome", "Firefox",
    "Visual Studio Code", "Terminal", "iTerm",
    "Finder", "Notes", "Calendar",
    "Spotify", "Music"
]


def run_applescript(script: str) -> str:
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() or "Done."
    except subprocess.TimeoutExpired:
        return "Action timed out."
    except Exception as e:
        return f"Automation error: {str(e)}"


def open_app(app_name: str) -> str:
    safe = any(safe.lower() in app_name.lower() for safe in SAFE_APPS)
    if not safe:
        return f"'{app_name}' is not in the safe apps list."
    # use 'open' command — works even when app is closed
    try:
        subprocess.run(["open", "-a", app_name], check=True)
        log_event("automation", f"opened {app_name}")
        return f"Opened {app_name}."
    except subprocess.CalledProcessError:
        return f"Could not open {app_name}. Check the app name is exact."


def show_notification(title: str, message: str) -> str:
    script = f'display notification "{message}" with title "{title}"'
    return run_applescript(script)


def run(user_input: str) -> str:
    text = user_input.lower()

    # Open app
    if "open" in text or "launch" in text:
        for app in SAFE_APPS:
            if app.lower() in text:
                return open_app(app)
        return f"Which app? Safe apps: {', '.join(SAFE_APPS)}"

    # Notification
    if "notify" in text or "notification" in text or "remind" in text:
        return show_notification("SAMEER AI", user_input)

    return "Automation: I can open apps and send notifications. Try 'open VS Code' or 'remind me to take a break'."