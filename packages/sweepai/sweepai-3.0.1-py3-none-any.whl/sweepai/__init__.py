import os
os.environ["CLI"] = "true"

from sweepai.config.server import ENV


def main():
    print(f"Hello, world from {os.getcwd()} (ENV={ENV})")
    files = ", ".join(os.listdir("."))
    print(f"I see the following files in this directory: {files}")

if __name__ == "__main__":
    main()
