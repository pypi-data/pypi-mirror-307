# Open5GS API

This package provides a Python API for interacting with Open5GS components and managing PCF configurations.

## Installation

```bash
pip install open5gsapi
```

## Usage

First, import the package and set the configuration path:

```python
from open5gsapi import open5gs

# Set the path to the PCF configuration file
open5gs.set_config_path('/path/to/the/pcf.yaml')
```

If the pcf.yaml file is edited manually after loading:

```python
# Explicitly reload the configuration
open5gs.reload_config()
```

### UE and UPF Operations

#### Getting API URLs

```python
# Get UE API URL
UE_API_URL = open5gs.ue("send")
# Result: "http://10.10.0.132:8080/send"

# Get UPF API URL
UPF_API_URL = open5gs.upf("receive/sensor")
# Result: "http://10.10.0.112:8081/receive/sensor"
```

#### Sending and Receiving Data

```python
# Send data
data = {"sensor_id": 1, "temperature": 25.5, "humidity": 60}
response = open5gs.send_data(UE_API_URL, data)

# Receive data
received_data = open5gs.receive_data(UPF_API_URL)
```

### PCF Configuration Management

#### Listing and Viewing Sessions

```python
# List all sessions
sessions = open5gs.list_sessions()
print("Current sessions:", sessions)

# Get details of a specific session
session_name = "video-streaming"
session_details = open5gs.get_session_details(session_name)
print(f"Details of session '{session_name}':", session_details)
```

#### Modifying Session Parameters

```python
# Modify session parameters
session = open5gs.policy.session('video-streaming')
session.ambr.downlink(value=10000000, unit=1)
session.ambr.uplink(value=20000000, unit=1)
session.qos(index=5)
session.arp(priority_level=7, pre_emption_vulnerability=2, pre_emption_capability=1)

# Modify PCC rule parameters
session.pcc_rule[0].qos(index=3)
session.pcc_rule[0].mbr.downlink(value=2000000, unit=1)
session.pcc_rule[0].gbr.uplink(value=1000000, unit=1)
session.pcc_rule[0].add_flow(direction=2, description="permit out ip from any to assigned")
```

#### Managing Sessions

```python
# Add a new session
new_session = open5gs.policy.add_session('new-session-name')
new_session.ambr.downlink(value=5000000, unit=1)
new_session.ambr.uplink(value=1000000, unit=1)

# Remove a session
open5gs.policy.remove_session('session-to-remove')

# Rename a session
open5gs.rename_session('old-session-name', 'new-session-name')
```

#### Updating Configuration

After making changes to the configuration, you need to call `update_pcf()` to update the PCF YAML file:

```python
open5gs.update_pcf()
```

To tear down existing Docker containers and redeploy them with the new configuration:

```python
open5gs.update_config()
```

To run initialization scripts in the UE and UPF containers and start background processes:

```python
open5gs.run_background_nodes()
```

These methods will:
1. `update_pcf()`: Update the PCF YAML file with the current configuration
2. `update_config()`: Tear down existing Docker containers and redeploy them with the new configuration
3. `run_background_nodes()`: Run initialization scripts in the UE and UPF containers and start background processes (auto-ue-api.py and upf-api.py)

The completion status of these operations can be checked using the following methods:

* `open5gs.is_update_pcf_complete()`: Returns `True` if the `update_pcf()` operation is complete.
* `open5gs.is_update_config_complete()`: Returns `True` if the `update_config()` operation is complete.
* `open5gs.is_run_background_nodes_complete()`: Returns `True` if the `run_background_nodes()` operation is complete.

## API Reference

### UE and UPF Operations

- `open5gs.ue(endpoint: str) -> str`: Get the UE API URL
- `open5gs.upf(endpoint: str) -> str`: Get the UPF API URL
- `open5gs.send_data(url: str, data: Any) -> Dict[str, Any]`: Send data to the specified URL
- `open5gs.receive_data(url: str) -> Any`: Receive data from the specified URL

### PCF Configuration Management

- `open5gs.list_sessions() -> List[str]`: Get a list of all session names
- `open5gs.get_session_details(name: str) -> Dict[str, Any]`: Get details of a specific session
- `open5gs.rename_session(old_name: str, new_name: str)`: Rename a session
- `open5gs.policy.session(name: str) -> Session`: Get or create a session
- `open5gs.policy.add_session(name: str) -> Session`: Add a new session
- `open5gs.policy.remove_session(name: str)`: Remove a session

#### Session Methods

- `session.ambr.downlink(value: int, unit: int)`: Set downlink AMBR
- `session.ambr.uplink(value: int, unit: int)`: Set uplink AMBR
- `session.qos(index: int)`: Set QoS index
- `session.arp(priority_level: int, pre_emption_vulnerability: int, pre_emption_capability: int)`: Set ARP parameters

#### PCC Rule Methods

- `session.pcc_rule[index].qos(index: int)`: Set QoS index for a PCC rule
- `session.pcc_rule[index].mbr.downlink(value: int, unit: int)`: Set downlink MBR for a PCC rule
- `session.pcc_rule[index].mbr.uplink(value: int, unit: int)`: Set uplink MBR for a PCC rule
- `session.pcc_rule[index].gbr.downlink(value: int, unit: int)`: Set downlink GBR for a PCC rule
- `session.pcc_rule[index].gbr.uplink(value: int, unit: int)`: Set uplink GBR for a PCC rule
- `session.pcc_rule[index].add_flow(direction: int, description: str)`: Add a flow to a PCC rule

### Configuration Update

- `open5gs.update_pcf()`: Update the PCF YAML file
- `open5gs.update_config()`: Tear down and redeploy containers with new configuration
- `open5gs.run_background_nodes()`: Run initialization scripts and start background processes in UE and UPF containers

## Error Handling

This API uses custom exception classes to handle various error scenarios. When using the API, you may catch the following exceptions:

### ConfigurationError

Raised when there are issues related to the overall configuration of the Open5GS system. It may occur in the following scenarios:

- The configuration file (pcf.yaml) cannot be found or read.
- There are structural problems with the configuration file.
- Unable to initialize or access necessary components of the Open5GS system.
- Attempting to access or modify a non-existent session.
- Failing to restart the PCF service.

Example usage:
```python
try:
    open5gs.set_config_path('/path/to/pcf.yaml')
except ConfigurationError as e:
    print(f"Configuration error: {e}")
    # Handle the error (e.g., exit the program or use a default configuration)
```

### ValidationError

Raised when the input values provided for specific configuration parameters are invalid or out of the allowed range. It typically occurs when:

- Setting an invalid QoS index.
- Providing an out-of-range value for AMBR.
- Using an incorrect value for ARP parameters.
- Setting an invalid session type.
- Adding an invalid flow direction in PCC rules.

Example usage:
```python
try:
    session = open5gs.policy.session('internet')
    session.qos(index=100)  # 100 is not a valid QoS index
except ValidationError as e:
    print(f"Validation error: {e}")
    # Handle the error (e.g., use a default value or prompt the user for valid input)
```

### CommunicationError

Raised when there are issues communicating with the UE or UPF components. It may occur when:

- Sending data to the UE API fails.
- Receiving data from the UPF API fails.

Example usage:
```python
try:
    response = open5gs.send_data(UE_API_URL, data)
except CommunicationError as e:
    print(f"Communication error: {e}")
    # Handle the error (e.g., retry the operation or log the failure)
```