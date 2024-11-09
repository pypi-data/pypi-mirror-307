import os, sys, platform, subprocess

def get_python_info():
    return {
        "Python Version": platform.python_version(),
        "Python Compiler": platform.python_compiler(),
        "Python Build": platform.python_build(),
        "Python Implementation": platform.python_implementation()
    }
def get_python_paths():
    get_python_paths_return = []
    get_python_paths_dict = {}
    get_python_paths_dict["Python Executable"] = sys.executable
    get_python_paths_return.append(get_python_paths_dict)
    get_python_paths_list = []
    for path in sys.path:
        get_python_paths_list.append(path)
    get_python_paths_dict['Path'] = get_python_paths_list
    get_python_paths_dict["User Site Packages Path"] = f"{os.path.expanduser('~') + '/.local/lib/python{0}.{1}/site-packages'.format(*sys.version_info)}"
    return get_python_paths_return
def get_installed_packages():
    get_installed_packages_return = ""
    try:
        installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "list"], text=True)
        get_installed_packages_return += installed_packages
    except subprocess.CalledProcessError as e:
        return "Error listing installed packages:"
    get_installed_packages_return += "\n"
    return get_installed_packages_return
def get_virtual_env_info():
    venv = os.getenv("VIRTUAL_ENV")
    if venv:
        return f"Virtual Environment Information:\nVirtual Environment Path: {venv}"
    else:
        return "No Virtual Environment Active"

# Run All Functions
if __name__ == "__main__":
    print(get_python_info())
    print(get_python_paths())
    print(get_installed_packages())
    print(get_virtual_env_info())
