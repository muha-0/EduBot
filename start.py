import os
import subprocess
import sys


def run_command(command, cwd=None):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, text=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error while executing: {' '.join(command)}")
        print(f"Error details: {e}")
        sys.exit(1)


def main():
    # Get the current working directory
    cwd = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Navigate to backend/server and execute commands
    backend_path = os.path.join(cwd, "backend", "server")
    print(f"Changing to backend directory: {backend_path}")
    if not os.path.exists(backend_path):
        print(f"Backend directory not found: {backend_path}")
        sys.exit(1)

    print("Installing backend dependencies...")
    run_command("pip install -r requirements.txt", cwd=backend_path)

    print("Starting the Python API...")
    subprocess.Popen(f'python "{backend_path}/api.py"', cwd=cwd)

    # Step 2: Navigate to frontend and execute commands
    frontend_path = os.path.join(cwd, "frontend")
    print(f"Changing to frontend directory: {frontend_path}")
    if not os.path.exists(frontend_path):
        print(f"Frontend directory not found: {frontend_path}")
        sys.exit(1)

    print("Installing frontend dependencies...")
    run_command("npm install", cwd=frontend_path)

    print("Starting the frontend...")
    run_command("npm start", cwd=frontend_path)


if __name__ == "__main__":
    main()
