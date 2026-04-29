import platform
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / "scripts"


def main():
    os_name = platform.system()
    print(f"Detected OS: {os_name}")

    if os_name == "Windows":
        script = SCRIPTS_DIR / "setup-windows.ps1"
        print("Running Windows setup...")
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "ByPass", "-File", str(script)],
            check=False,
        )
    elif os_name in ("Linux", "Darwin"):
        script = SCRIPTS_DIR / "setup-linux.sh"
        print("Running Linux/Mac setup...")
        script.chmod(0o755)
        result = subprocess.run(["bash", str(script)], check=False)
    else:
        print(f"Unsupported OS: {os_name}")
        sys.exit(1)

    if result.returncode != 0:
        print("Setup failed. Check the output above for errors.")
        sys.exit(result.returncode)

    print("\nSetup complete.")


if __name__ == "__main__":
    main()
