import platform, socket, psutil

def get_system_info():
    return {
        "System": platform.system(),
        "Node": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Processor": platform.processor(),
        "Architecture": platform.architecture(),
        "CPU Count": psutil.cpu_count(logical=True),
        "Physical CPU Count": psutil.cpu_count(logical=False)
    }
def get_cpu_info():
    return {
        "CPU Usage": psutil.cpu_percent(interval=1),
        "CPU Cores Usage": psutil.cpu_percent(interval=1, percpu=True),
        "CPU Frequency": f"{psutil.cpu_freq().current:.2f} MHz"
    }
def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "Total Memory": f"{memory.total / (1024 ** 3):.2f} GB",
        "Available Memory": f"{memory.available / (1024 ** 3):.2f} GB",
        "Used Memory": f"{memory.used / (1024 ** 3):.2f} GB",
        "Memory Usage": f"{memory.percent}"
    }
def get_disk_info():
    get_disk_info_return = []
    for partition in psutil.disk_partitions():
        get_disk_info_dict = {}
        get_disk_info_dict["Device"] = partition.device
        get_disk_info_dict["Mountpoint"] = partition.mountpoint
        get_disk_info_dict["File System Type"] = partition.fstype
        usage = psutil.disk_usage(partition.mountpoint)
        get_disk_info_dict["Total Size"] = f"{usage.total / (1024 ** 3):.2f} GB"
        get_disk_info_dict["Used"] = f"{usage.used / (1024 ** 3):.2f} GB"
        get_disk_info_dict["Free"] = f"{usage.free / (1024 ** 3):.2f} GB"
        get_disk_info_dict["Usage"] = usage.percent
        get_disk_info_return.append(get_disk_info_dict)
    return get_disk_info_return
def get_network_info():
    get_network_info_return = []
    get_network_info_dict = {}
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    get_network_info_dict["Hostname"] = hostname
    get_network_info_dict["Local IP Address"] = local_ip
    net_io = psutil.net_io_counters()
    get_network_info_dict["Total Bytes Sent"] =  f"{net_io.bytes_sent / (1024 ** 2):.2f} MB"
    get_network_info_dict["Total Bytes Received"] = f"{net_io.bytes_recv / (1024 ** 2):.2f} MB"
    get_network_info_return.append(get_network_info_dict)
    for interface, addrs in psutil.net_if_addrs().items():
        get_network = {}
        for addr in addrs:
            if addr.family == socket.AF_INET:
                get_network["Interface"] = interface
                get_network["IP Address"] = addr.address
                get_network["Netmask"] = addr.netmask
                get_network_info_return.append(get_network)
    return get_network_info_return
def get_battery_info():
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            return {
                "Battery Percentage": battery.percent,
                "Power Plugged In": f"{'Yes' if battery.power_plugged else 'No'}"
            }
        else:
            return "No Battery Information Available"
    else:
        return "Battery Information Not Supported on this System"
