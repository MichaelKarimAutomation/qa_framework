import os
import platform
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / 'scripts'
TOOLS_DIR = Path(__file__).parent / 'tools'


def get_base_python_executable() -> Path | None:
    base_prefix = Path(sys.base_prefix)
    if sys.platform == 'win32':
        candidate = base_prefix / 'python.exe'
    else:
        candidate = base_prefix / 'bin' / 'python3'
        if not candidate.exists():
            candidate = base_prefix / 'bin' / 'python'
    return candidate if candidate.exists() else None


def main():
    repo_root = Path(__file__).parent.resolve()
    venv_path = (repo_root / '.venv').resolve()
    current_prefix = Path(sys.prefix).resolve()

    if venv_path.exists() and current_prefix == venv_path:
        base_python = get_base_python_executable()
        if base_python is not None:
            print('Detected active repository .venv. Re-launching setup with the base Python interpreter outside the venv...')

            os.environ.pop('VIRTUAL_ENV', None)
            os.environ.pop('PYTHONHOME', None)

            venv_scripts = (venv_path / ('Scripts' if sys.platform == 'win32' else 'bin')).resolve()
            path_parts = [p for p in os.environ.get('PATH', '').split(os.pathsep) if p and Path(p).resolve() != venv_scripts]
            os.environ['PATH'] = os.pathsep.join(path_parts)

            os.execv(str(base_python), [str(base_python), str(Path(__file__).resolve()), *sys.argv[1:]])

        print('Error: install.py is running from the repository .venv, and the base Python executable could not be located.')
        print('Deactivate the virtual environment and rerun install.py from a fresh shell.')
        sys.exit(1)

    os_name = platform.system()
    print(f'Detected OS: {os_name}')

    if os_name == 'Windows':
        script = SCRIPTS_DIR / 'setup-windows.ps1'
        print('Running Windows setup...')
        result = subprocess.run(
            ['powershell', '-ExecutionPolicy', 'ByPass', '-File', str(script)],
            check=False,
        )
    elif os_name in ('Linux', 'Darwin'):
        script = SCRIPTS_DIR / 'setup-linux.sh'
        print('Running Linux/Mac setup...')
        script.chmod(0o755)
        result = subprocess.run(['bash', str(script)], check=False)
    else:
        print(f'Unsupported OS: {os_name}')
        sys.exit(1)

    if result.returncode != 0:
        print('Setup failed. Check the output above for errors.')
        sys.exit(result.returncode)

    print('\nActivating git hooks...')
    if os_name == 'Windows':
        hook_script = TOOLS_DIR / 'install-hooks.ps1'
        hook_result = subprocess.run(
            ['powershell', '-ExecutionPolicy', 'ByPass', '-File', str(hook_script)],
            check=False,
        )
    else:
        hook_script = TOOLS_DIR / 'install-hooks.sh'
        hook_script.chmod(0o755)
        hook_result = subprocess.run(['bash', str(hook_script)], check=False)

    if hook_result.returncode != 0:
        print('Git hook activation failed. Check the output above for errors.')
        sys.exit(hook_result.returncode)

    print('\nSetup complete.')


if __name__ == '__main__':
    main()
