import visa


def find_instrument(name):
    resource_manager = visa.ResourceManager()
    resource_list = resource_manager.list_resources()

    selected_instrument = ""

#Only one valid input by default
    instrument_list = [resource_manager.open_resource(resource) for resource in resource_list]
    for instrument in instrument_list:
        if instrument.query('*IDN?').find(name) != -1:
            selected_instrument = instrument

    return selected_instrument


