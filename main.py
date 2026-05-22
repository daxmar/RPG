import os
import sys

from src.core.state_manager import StateManager


def main():
    # Opsional: pastikan path proyek benar
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base_dir)

    manager = StateManager()
    manager.run()


if __name__ == "__main__":
    main()

