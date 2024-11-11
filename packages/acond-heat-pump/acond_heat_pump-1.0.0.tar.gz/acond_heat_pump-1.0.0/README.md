# Acond Heat Pump

A unofficial python library to interface with an Acond heat pump
using the Modbus TCP protocol.

### ❗Warning❗
Library is tested only with Acond PRO N heat pump as I don't have access to other models.
If you have a different model and you want to test it, please let me know the results.

## Usage

### Connecting to the Heat Pump

```python
from acond_heat_pump import AcondHeatPump

heat_pump = AcondHeatPump('192.168.1.16')
heat_pump.connect()
```

### Reading Data

```python
response = heat_pump.read_data()
print(response)
```

### Setting Temperatures

```python
heat_pump.set_indoor_temperature(25.0, circuit=1)
heat_pump.set_dhw_temperature(45.0)
heat_pump.set_water_back_temperature(35.0)
heat_pump.set_pool_temperature(28.0)
heat_pump.set_water_cool_temperature(20.0)
```

### Setting Modes

```python
from acond_heat_pump import RegulationMode, HeatPumpMode

heat_pump.set_regulation_mode(RegulationMode.MANUAL)
heat_pump.change_setting(mode=HeatPumpMode.AUTOMATIC)
```

### Closing the Connection

```python
heat_pump.close()
```

## Running Tests

Run the unit tests using `unittest`:

```sh
python -m unittest discover tests
```

## License

This project is licensed under the MIT License.