"""
Check system requirements for KrishiMitra
"""
import shutil
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    required = (3, 10)
    recommended = (3, 11)

    if version >= recommended:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    elif version >= required:
        print(f"⚠ Python {version.major}.{version.minor}.{version.micro} (recommended: {recommended[0]}.{recommended[1]}+, but should work)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires {required[0]}.{required[1]}+)")
        return False


def check_command(command, name):
    """Check if a command is available"""
    if shutil.which(command):
        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.split('\n')[0] if result.stdout else "unknown version"
            print(f"✓ {name}: {version}")
            return True
        except Exception:
            print(f"✓ {name}: installed")
            return True
    else:
        print(f"✗ {name}: not found")
        return False


def check_docker():
    """Check Docker and Docker Compose"""
    docker_ok = check_command("docker", "Docker")
    compose_ok = check_command("docker-compose", "Docker Compose")
    return docker_ok and compose_ok


def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file not found (copy from .env.example)")
        return False


def check_venv():
    """Check if running in virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Running in virtual environment")
        return True
    else:
        print("⚠ Not running in virtual environment (recommended)")
        return False


def main():
    """Run all checks"""
    print("KrishiMitra - System Requirements Check")
    print("=" * 50)
    print()

    checks = []

    print("Python:")
    checks.append(check_python_version())
    print()

    print("Virtual Environment:")
    check_venv()  # Warning only, not required
    print()

    print("Required Tools:")
    checks.append(check_command("git", "Git"))
    checks.append(check_docker())
    print()

    print("Optional Tools:")
    check_command("make", "Make")
    print()

    print("Configuration:")
    checks.append(check_env_file())
    print()

    print("=" * 50)
    if all(checks):
        print("✓ All required checks passed!")
        print("\nNext steps:")
        print("  1. Edit .env with your credentials")
        print("  2. Run: docker-compose up -d")
        print("  3. Run: alembic upgrade head")
        print("  4. Run: python src/main.py")
        return 0
    else:
        print("✗ Some checks failed. Please install missing requirements.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
