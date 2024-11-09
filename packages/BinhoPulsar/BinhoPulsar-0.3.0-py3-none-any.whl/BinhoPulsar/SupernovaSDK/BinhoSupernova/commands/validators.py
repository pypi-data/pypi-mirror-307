from .serializers import *
from ..utils.system_message import SystemMessage, SystemModules,RequestValidatorOpcode

#####################################################################
# --------------------- FORMAT VALIDATORS ---------------------------
#####################################################################

MIN_ID_VALUE = 1
MAX_ID_VALUE = 65535

def check_type(value, expected_type):
    return isinstance(value, expected_type)

def check_range(value, expected_type, min_val, max_val):
    return isinstance(value, expected_type) and min_val <= value <= max_val

def check_byte_array(data, max_size):
    if( len(data) > max_size):
        return False
    return all(check_range(value, int, 0x00, 0xFF) for value in data)

def check_valid_id(id):
    return check_range(id, int, MIN_ID_VALUE, MAX_ID_VALUE)

def getRepeatedItems(listOfItems: list):
    """
    Gets the repeated items from listOfItems

    Arguments
    ---------
    listOfItems: List to look into.

    Returns
    -------
    repeated
        List of the items from listOfItems that are repeated.

    """        
    seen = set()
    repeated = set()
    for value in listOfItems:
        if value in seen:
            repeated.add(value)
        else:
            seen.add(value)
    return (list(repeated))

#####################################################################
# ----------------------------- SYSTEM ------------------------------
#####################################################################

def getUsbStringValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = getUsbStringSerializer(metadata["id"], metadata["subcommand"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GET USB STRING requests success")

def setI3cBusVoltageValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.

    requests, response = setI3cBusVoltSerializer(metadata["id"], metadata["i3cBusVoltage"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SET I3C BUS VOLTAGE requests success")

def resetDeviceValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = resetDeviceSerializer(metadata["id"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "RESET DEVICE requests success")

def enterBootModeValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = enterBootModeSerializer(metadata["id"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "ENTER BOOT MODE requests success")

def setI2cSpiUartBusVoltValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.

    requests, response = setI2cSpiUartBusVoltSerializer(metadata["id"], metadata["i2cSpiUartBusVolt"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SET I2C SPI UART BUS VOLTAGE requests success")

def getI3cConnectorsStatusValidator(metadata: dict) :
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "ARGUMENT ERROR: wrong id value")
    requests = None
    response = None

    if (check_valid_id(metadata["id"])):
        requests, response = getI3cConnectorsStatusSerializer(metadata["id"])
        result.opcode = RequestValidatorOpcode.SUCCESS
        result.message = "GET I3C CONNECTORS STATUS requests success"
    
    return requests, response, result

def getAnalogMeasurementsValidator(metadata: dict) :
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "ARGUMENT ERROR: wrong id value")
    requests = None
    response = None

    if (check_valid_id(metadata["id"])):
        requests, response = getAnalogMeasurementsSerializer(metadata["id"])
        result.opcode = RequestValidatorOpcode.SUCCESS
        result.message = "GET ANALOG MEASUREMENTS requests success"
    
    return requests, response, result

def useExternalSourceForI2cSpiUartBusVoltageValidator(metadata: dict) :
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "ARGUMENT ERROR: wrong id value")
    requests = None
    response = None

    if (check_valid_id(metadata["id"])):
        requests, response = useExternalSourceForI2cSpiUartBusVoltageSerializer(metadata["id"])
        result.opcode = RequestValidatorOpcode.SUCCESS
        result.message = "USE EXT SRC I2C-SPI-UART BUS VOLTAGE requests success"
    
    return requests, response, result

def useExternalSourceForI3cBusVoltageValidator(metadata: dict) :
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "ARGUMENT ERROR: wrong id value")
    requests = None
    response = None

    if (check_valid_id(metadata["id"])):
        requests, response = useExternalSourceForI3cBusVoltageSerializer(metadata["id"])
        result.opcode = RequestValidatorOpcode.SUCCESS
        result.message = "USE EXT SRC I3C BUS VOLTAGE requests success"
    
    return requests, response, result

def enterIspModeValidator(metadata: dict) :
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "ARGUMENT ERROR: wrong id value")
    requests = None
    response = None

    if (check_valid_id(metadata["id"])):
        requests, response = enterIspModeSerializer(metadata["id"])
        result.opcode = RequestValidatorOpcode.SUCCESS
        result.message = "ENTER ISP MODE requests success"
    
    return requests, response, result

#####################################################################
# ------------------------------ I2C --------------------------------
#####################################################################

def i2cSetParametersValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i2cSetParametersSerializer(metadata["id"], metadata["cancelTransfer"], metadata["baudrate"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C SET PARAMETERS requests success")

def i2cSetPullUpResistorsValidator(metadata: dict):
    success, result = validateI2cSetPullUpResistors(metadata)
    requests = None
    response = None

    if (success):
        requests, response = i2cSetPullUpResistorsSerializer(metadata["id"], metadata["pullUpResistorsValue"])

    return requests, response, result

def validateI2cSetPullUpResistors(metadata: dict):
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C SET PULL UP RESISTORS requests success")
    success = True

    if (not check_type(metadata["pullUpResistorsValue"], I2cPullUpResistorsValue)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pull up resistors value"
        success = False

    return success, result

def i2cWriteValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i2cWriteSerializer(metadata["id"], metadata["command"], metadata["slaveAddress"], metadata["registerAddress"], metadata["data"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C WRITE requests success")

def i2cWriteNonStopValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i2cWriteSerializer(metadata["id"], metadata["command"], metadata["slaveAddress"], metadata["registerAddress"], metadata["data"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C WRITE NON STOP requests success")

def i2cReadValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i2cReadSerializer(metadata["id"], metadata["command"], metadata["slaveAddress"], metadata["dataLength"], metadata["registerAddress"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C READ requests success")

def i2cReadFromValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i2cReadSerializer(metadata["id"], metadata["command"], metadata["slaveAddress"], metadata["dataLength"], metadata["registerAddress"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C READ FROM requests success")

#####################################################################
# ------------------------------ I3C --------------------------------
#####################################################################

def i3cControllerInitValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cControllerInitSerializer(metadata["id"])
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "INITIALIZE I3C CONTROLLER requests success")
    return requests, response, result

def i3cInitBusValidator(metadata: dict) :
    """
    Validates the targetDeviceTable of the user request. Checks that all I3C devices have a DAA method assigned and that there 
    are no repeated addresses:
    - static address for I2C targets and I3C targets to be initialized with SETAASA
    - static and dynamic addresses for I3C targets to be initialized with SETDASA
    - dynamic addresses for I3C targets to be initialized with ENTDAA

    Arguments
    ---------
    dict: dictionary of metadata that represents the fields for I3cInitBusRequest_t

    Returns
    -------
    requests
        variable of type I3cInitBusRequest_t to later send to the Supernova via USB to request an I3C_INIT_BUS command

    response
        instance of I3cInitBusResponse_t to match the message sent by the Supernova (the response for the command) with the request

    RequestValidatorSuccess
        indicates if the validation was successful or not

    """
    requests = None
    response = None
    result = None

    def verifyI3cDynamicAddressAssignmentMethod(targetDeviceTable: dict):
        """
        Verifies that all I3C entries from the targetDeviceTable have a DAA method assigned.

        Arguments
        ---------
        dict: dictionary of metadata that represents the targetDeviceTable for I3cInitBusRequest_t

        Returns
        -------
        indexOfAddrWithoutMethod
            Index of the entries from targetDeviceTable that does not indicate a DAA method.

        """
        indexOfAddrWithoutMethod = []
        for index, target in targetDeviceTable.items():
            if ((target['i3cFeatures'] & TARGET_TYPE_MASK == TargetType.I3C_DEVICE.value) and 
                ( target['i3cFeatures'] & (ASSIGNMENT_FROM_STATIC_ADDRESS_MASK | DYN_ADDR_ASSIGNMENT_W_ENTDAA_MASK) == 0)):
                indexOfAddrWithoutMethod.append(index)
        return indexOfAddrWithoutMethod

    def getRepeatedAddresses(targetDeviceTable: dict):
        """
        Gets all the repeated addresses from the targetDeviceTable argument.

        Arguments
        ---------
        dict: dictionary of metadata that represents the targetDeviceTable for I3cInitBusRequest_t

        Returns
        -------
        listOfAddresses
           List of Addresses repeated in targetDeviceTable.

        """
        # Address used for SETDASA point to point 
        SETDASA_POINT_TO_POINT_ADDR = 0x01

        listOfAddresses = []

        for target in targetDeviceTable.values():
            if (target['i3cFeatures'] & TARGET_TYPE_MASK == TargetType.I3C_DEVICE.value):  
            
                # If the I3C device supports SETDASA and its static and dynamic addresses are SETDASA_POINT_TO_POINT_ADDR it might refer to a point-to-point SETDASA
                if not((target['i3cFeatures'] & TARGET_SUPPORTS_SETDASA_MASK) and (target['staticAddress'] == SETDASA_POINT_TO_POINT_ADDR) and (target['dynamicAddress'] == SETDASA_POINT_TO_POINT_ADDR)):

                    if ((target['i3cFeatures'] & TARGET_SUPPORTS_SETDASA_MASK) or (target['i3cFeatures'] & DYN_ADDR_ASSIGNMENT_W_ENTDAA_MASK)):  
                        listOfAddresses.append(target['dynamicAddress'])            
                    
                    if (target['i3cFeatures'] & TARGET_SUPPORTS_SETDASA_MASK) or (target['i3cFeatures'] & TARGET_SUPPORTS_SETAASA_MASK): 
                        listOfAddresses.append(target['staticAddress'])  

            if (target['i3cFeatures'] & TARGET_TYPE_MASK == TargetType.I2C_DEVICE.value):  
                listOfAddresses.append(target['staticAddress'])  

        # Return the list of repeated addresses
        return getRepeatedItems(listOfAddresses)
    
    if metadata.get("targetDeviceTable") is not None:
        targetDeviceTable = metadata["targetDeviceTable"]

        listOfTargetsWithoutDaaMethod = verifyI3cDynamicAddressAssignmentMethod(targetDeviceTable)
        if listOfTargetsWithoutDaaMethod:
            targets_str = ', '.join([f"{target_index}" for target_index in listOfTargetsWithoutDaaMethod])
            message = f"I3C INIT BUS failed: target/s in position {targets_str} of the input table not supporting any DAA method"
            result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, message)   
            return requests, response, result  
                  
        listOfRepeatedAddr = getRepeatedAddresses(targetDeviceTable)
        if listOfRepeatedAddr:
            addresses_str = ', '.join([f"0x{addr:02X}" for addr in listOfRepeatedAddr])
            message = f"I3C INIT BUS failed: address/es {addresses_str} repeated"
            result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, message)   
            return requests, response, result

    requests, response = i3cInitBusSerializer(metadata["id"], metadata["targetDeviceTable"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "INITIALIZE I3C BUS requests success")

def i3cGetTargetDeviceTableValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cGetTargetDeviceTableSerializer(metadata["id"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C GET TARGET DEVICE TABLE requests success")

def i3cSetTargetDeviceConfigValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cSetTargetDeviceConfigSerializer(metadata["id"], metadata["entries"])
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C SET TARGET DEVICE CONFIG requests success")
    return requests, response, result    

def i3cChangeDynamicAddressValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cChangeDynamicAddressSerializer(metadata["id"], metadata["currentAddress"], metadata["newAddress"])
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CHANGE DYNAMIC ADDRESS requests success")
    return requests, response, result     

def i3cClearFeatureValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cClearFeatureSerializer(metadata["id"], metadata["selector"], metadata["targetAddress"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CLEAR FEATURE requests success")

def i3cSetFeatureValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cSetFeatureSerializer(metadata["id"], metadata["selector"], metadata["targetAddress"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C SET FEATURE requests success")

def i3cGetCapabilityValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cGetCapabilitySerializer(metadata["id"])
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C GET CAPABILITY requests success")
    return requests, response, result     

def i3cWriteValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cWriteSerializer(metadata["id"], metadata["targetAddress"], metadata["mode"], metadata["pushPullRate"], metadata["openDrainRate"], metadata["registerAddress"], metadata["data"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C WRITE requests success")

def i3cReadValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cReadSerializer(metadata["id"], metadata["targetAddress"], metadata["mode"], metadata["pushPullRate"], metadata["openDrainRate"], metadata["registerAddress"], metadata["length"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C READ requests success")

def i3cSendCccValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cSendCccSerializer(metadata["id"], metadata["commandType"], metadata["isReadOrWrite"],  metadata["targetAddress"], metadata["mode"], metadata["pushPullRate"], metadata["openDrainRate"], metadata["defByte"], metadata["ccc"], metadata["length"], metadata["data"])
    return requests, response, SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C SEND CCC requests success")

def i3cTriggerTargetResetPatternValidator(metadata: dict) :

    '''
    This function validates the data set by the user for the I3C_TRIGGER_TARGET_RESET_PATTERN command and serializes the data into I3cTriggerTargetResetPatternRequest_t using
    i3cTriggerTargetResetPatternSerializer if the validation is successful.

    Arguments
    ---------
    dict: dictionary of metadata that represents the fields for I3cTriggerTargetResetPatternRequest_t

    Returns
    -------
    requests
        variable of type I3cTriggerTargetResetPatternRequest_t to later send to the Supernova via USB to request an I3C_TRIGGER_TARGET_RESET_PATTERN command

    response
        instance of I3cTriggerTargetResetPatternResponse_t to match the message sent by the Supernova (the response for the command) with the request

    RequestValidatorSuccess
        indicates if the validation was successful or not

    '''

    requests, response = i3cTriggerTargetResetPatternSerializer(metadata["id"])
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TRIGGER TARGET RESET PATTERN requests success")
    return requests, response, result  
    
def i3cTriggerExitPatternValidator(metadata: dict) :

    '''
    This function validates the data set by the user for the I3C_TRIGGER_EXIT_PATTERN command and serializes the data into I3cTriggerExitPatternRequest_t using
    i3cTriggerExitPatternSerializer if the validation is successful.

    Arguments
    ---------
    dict: dictionary of metadata that represents the fields for I3cTriggerExitPatternRequest_t

    Returns
    -------
    requests
        variable of type I3cTriggerExitPatternRequest_t to later send to the Supernova via USB to request an I3C_TRIGGER_EXIT_PATTERN command

    response
        instance of I3cTriggerExitPatternResponse_t to match the message sent by the Supernova (the response for the command) with the request

    RequestValidatorSuccess
        indicates if the validation was successful or not

    '''

    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "ARGUMENT ERROR: wrong id value")
    requests = None
    response = None
    
    if (check_valid_id(metadata["id"])):
        requests, response = i3cTriggerExitPatternSerializer(metadata["id"])
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TRIGGER TARGET EXIT PATTERN requests success")
        
    return requests, response, result

def i3cTargetInitValidator(metadata: dict) :

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cTargetInitSerializer(metadata["id"], metadata["memoryLayout"], metadata["uSecondsToWaitForIbi"], metadata["maxReadLength"], metadata["maxWriteLength"], metadata["i3cTargetFeatures"])
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "INITIALIZE I3C PERIPHERAL IN TARGET MODE requests success")
    return requests, response, result

def i3cTargetSetPidValidator(metadata: dict) :

    requests = None
    response = None
    result = None

    # Check if the user sent the right number of bytes as PID
    if (len(metadata["PID"]) is I3C_PID_SIZE):
        requests, response = i3cTargetSetPidSerializer(metadata["id"], metadata["PID"])
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET SET PID requests success")
    else:
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "I3C TARGET SET PID request failed, PID should be 6 bytes")
    
    return requests, response, result

def i3cTargetSetBcrValidator(metadata: dict) :

    requests = None
    response = None
    result = None

    maxDataSpeedTypeCorrect = type(metadata["maxDataSpeedLimit"]) is I3cTargetMaxDataSpeedLimit_t
    ibiReqCapTypeCorrect = type(metadata["ibiReqCapable"]) is I3cTargetIbiCapable_t
    ibiPayloadTypeCorrect = type(metadata["ibiPayload"]) is I3cTargetIbiPayload_t
    offlineCapTypeCorrect = type(metadata["offlineCapable"]) is I3cTargetOfflineCap_t
    virtTargTypeCorrect = type(metadata["virtTargSupport"]) is I3cTargetVirtSupport_t
    deviceRolTypeCorrect = type(metadata["deviceRole"]) is I3cTargetDeviceRole_t
    
    errors = [] 
    isTypeCorrect = [maxDataSpeedTypeCorrect, ibiReqCapTypeCorrect, ibiPayloadTypeCorrect, offlineCapTypeCorrect, virtTargTypeCorrect, deviceRolTypeCorrect]
    isTypeCorrectError = ["maxDataSpeedLimit", "ibiReqCap", "ibiPayload", "offlineCap", "virtTarg", "deviceRol"]
    if all(isTypeCorrect):
        requests, response = i3cTargetSetBcrSerializer(metadata["id"], metadata["maxDataSpeedLimit"], metadata["ibiReqCapable"], metadata["ibiPayload"], metadata["offlineCapable"], metadata["virtTargSupport"], metadata["deviceRole"])
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET SET BCR requests success")
    else:
        for index, element in enumerate(isTypeCorrect):
            if not element:
                errors.append(isTypeCorrectError[index])
        message = f"I3C TARGET SET BCR request failed: {', '.join(errors)} {'type is' if (len(errors) == 1) else 'types are'} not correct"
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, message)

    return requests, response, result

def i3cTargetSetDcrValidator(metadata: dict) :

    requests = None
    response = None
    result = None

    if (type(metadata["dcrValue"]) is I3cTargetDcr_t):
        requests, response = i3cTargetSetDcrSerializer(metadata["id"], metadata["dcrValue"])
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET SET DCR requests success")
    else:
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "I3C TARGET SET DCR request failed, dcrValue type is not correct")
    
    return requests, response, result

def i3cTargetSetStaticAddrValidator(metadata: dict) :

    requests = None
    response = None
    result = None

    i2c_reserved_addresses = list(range(0x00, 0x08)) + list(range(0x78, 0x80))

    # Check if the user 
    if (metadata["staticAddress"] in i2c_reserved_addresses):
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "I3C TARGET SET STATIC ADDRESS request failed, address reserved by I2C protocol")
    else:
        requests, response = i3cTargetSetStaticAddrSerializer(metadata["id"], metadata["staticAddress"])
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET SET STATIC ADDRESS requests success")
    
    return requests, response, result

def i3cTargetSetConfValidator(metadata: dict) :

    '''
    This function validates the data set by the user for the I3C_TARGET_SET_CONFIGURATION command and serializes the data into i3cTargetSetConfSerializer using
    i3cTargetSetConfSerializer if the validation is successful.

    Arguments
    ---------
    dict: dictionary of metadata that represents the fields for I3cTargetSetConfRequest_t

    Returns
    -------
    requests
        variable of type I3cTargetSetConfRequest_t to later send to the Supernova via USB to request an I3C_TARGET_SET_CONFIGURATION command

    response
        instance of I3cTargetSetConfResponse_t to match the message sent by the Supernova (the response for the command) with the request

    RequestValidatorSuccess
        indicates if the validation was successful or not

    '''

    # TODO: Check data validation. Use module inspect and/or try-except block.
    # TODO: Ckeck command value.

    requests, response = i3cTargetSetConfSerializer(metadata["id"], metadata["uSecondsToWaitForIbi"], metadata["maxReadLength"], metadata["maxWriteLength"], metadata["i3cTargetFeatures"])
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SET CONFIGURATION OF SUPERNOVA IN TARGET MODE requests success")
    return requests, response, result

def i3cTargetWriteMemValidator(metadata: dict) :
    '''
    This function validates the data set by the user for the I3C_TARGET_WRITE_MEMORY command and serializes the data into I3cTargetWriteMemRequest_t using
    i3cTargetWriteMemSerializer if the validation is successful.
    It verifies that the address set by the user does not surpass the end of the memory, the request is not even sent to the Supernova thanks to this validation.

    Arguments
    ---------
    dict: dictionary of metadata that represents the fields for I3cTargetWriteMemRequest_t

    Returns
    -------
    requests
        variable of type I3cTargetWriteMemRequest_t to later send to the Supernova via USB to request an I3C_TARGET_WRITE_MEMORY command

    response
        instance of I3cTargetWriteMemResponse_t to match the message sent by the Supernova (the response for the command) with the request

    RequestValidatorSuccess
        indicates if the validation was successful or not

    '''

    requests = None
    response = None
    result = None
    
    # Check memory address value.
    if (metadata["memoryAddr"] is not None):
        
        # Check there is data to be sent.
        if (metadata["data"] is not None) and (len(metadata['data']) > 0):

            # Check if all the data is valid data
            if all(0 <= value <= 0xFF for value in metadata["data"]) == True:
                requests, response = i3cTargetWriteMemSerializer(metadata["id"], metadata["memoryAddr"], metadata["data"])
                result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET WRITE MEMORY requests success")
            else:
                result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "I3C TARGET WRITE MEMORY request failed, invalid data input")
        else:
            result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "I3C TARGET WRITE MEMORY request failed, no data input")
    else:
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "I3C TARGET WRITE MEMORY request failed, no memory address input")

    return requests, response, result

def i3cTargetReadMemValidator(metadata: dict) :
    '''
    This function validates the data set by the user for the I3C_TARGET_READ_MEMORY command and serializes the data into I3cTargetReadMemRequest_t using
    i3cTargetReadMemSerializer if the validation is successful.
    It verifies that the address set by the user does not surpass the end of the memory, the request is not even sent to the Supernova thanks to this validation.

    Arguments
    ---------
    dict: dictionary of metadata that represents the fields for I3cTargetReadMemRequest_t

    Returns
    -------
    requests
        variable of type I3cTargetReadMemRequest_t to later send to the Supernova via USB to request an I3C_TARGET_READ_MEMORY command

    response
        instance of I3cTargetReadMemResponse_t to match the message sent by the Supernova (the response for the command) with the request

    RequestValidatorSuccess
        indicates if the validation was successful or not

    '''

    requests = None
    response = None
    result = None
    # Check memory address value.
    if (metadata["memoryAddr"] is not None):
        # Check read length value.
        if (metadata["length"] is not None) and (metadata["length"] > 0) :
            requests, response = i3cTargetReadMemSerializer(metadata["id"], metadata["memoryAddr"], metadata["length"])
            result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET READ MEMORY requests success")
        else:
            result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "I3C TARGET READ MEMORY request failed, invalid length input")
    else:
        result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, "I3C TARGET READ MEMORY request failed, no memory address input")
    return requests, response, result

#####################################################################
# ------------------------ UART CONTROLLER --------------------------
#####################################################################
    
def uartControllerInitValidator (metadata: dict):
    success, result = validateUartControllerInit(metadata)
    requests = None
    response = None

    if (success):
        requests, response = uartControllerInitSerializer(metadata["id"], metadata["baudRate"], metadata["hardwareHandshake"], metadata["parityMode"], metadata["dataSize"], metadata["stopBitType"])
    
    return requests, response, result
    
def validateUartControllerInit( metadata: dict ):
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "UART CONTROLLER INIT requests success")
    success = True

    if (not check_type(metadata["baudRate"],UartControllerBaudRate)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for baudrate value"
        success = False
    if (not check_type(metadata["hardwareHandshake"],bool)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Hardware Handshake value"
        success = False
    if (not check_type(metadata["parityMode"],UartControllerParity)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Parity Mode value"
        success = False
    if (not check_type(metadata["dataSize"],UartControllerDataSize)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for UART data size value"
        success = False
    if (not check_type(metadata["stopBitType"],UartControllerStopBit)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Stop byte configuration value"  
        success = False  

    return success, result

def uartControllerSetParametersValidator(metadata: dict):
    success, result = validateUartControllerSetParameters( metadata)
    requests = None
    response = None

    if (success):
        requests, response = uartControllerSetParametersSerializer(metadata["id"], metadata["baudRate"], metadata["hardwareHandshake"], metadata["parityMode"], metadata["dataSize"], metadata["stopBitType"])

    return requests, response, result


def validateUartControllerSetParameters( metadata: dict ):
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "UART CONTROLLER SET PARAMETERS requests success")
    success = True

    if (not check_type(metadata["baudRate"],UartControllerBaudRate)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for baudrate value"
        success = False
    if (not check_type(metadata["hardwareHandshake"],bool)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Hardware Handshake value"
        success = False
    if (not check_type(metadata["parityMode"],UartControllerParity)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Parity Mode value"
        success = False
    if (not check_type(metadata["dataSize"],UartControllerDataSize)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for UART data size value"
        success = False
    if (not check_type(metadata["stopBitType"],UartControllerStopBit)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Stop byte configuration value"  
        success = False  

    return success, result

def uartControllerSendMessageValidator(metadata: dict):
    success, result = validateUartSendMessageParameters( metadata )
    requests = None
    response = None
    if (success):
        requests, response = uartControllerSendMessageSerializer(metadata["id"], metadata["data"])
    return requests, response, result

def validateUartSendMessageParameters( metadata: dict ):
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "UART SEND MESSAGE requests success")
    success = True

    if (not check_byte_array(metadata["data"],UART_CONTROLLER_SEND_MAX_PAYLOAD_LENGTH)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: invalid data array"
        success = False

    return success, result

#####################################################################
# ------------------------ SPI CONTROLLER ---------------------------
#####################################################################

def spiControllerInitValidator(metadata: dict) :
    success, result = validateSpiControllerInit(metadata)
    requests, response = None, None

    if success:
        requests, response = spiControllerInitSerializer(metadata["id"], metadata["bitOrder"], metadata["mode"], metadata["dataWidth"], metadata["chipSelect"], metadata["chipSelectPol"], metadata["frequency"])       

    return requests, response, result

def validateSpiControllerInit(metadata: dict):
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SPI CONTROLLER INIT requests success")
    success = True

    if (not check_range(metadata["frequency"],int,SPI_CONTROLLER_MIN_FREQUENCY,SPI_CONTROLLER_MAX_FREQUENCY)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: frequency value out of range"
        success = False
    if (not check_type(metadata["bitOrder"],SpiControllerBitOrder)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for bitOrder value"
        success = False
    if (not check_type(metadata["mode"],SpiControllerMode)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for mode value"
        success = False
    if (not check_type(metadata["dataWidth"],SpiControllerDataWidth)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for dataWidth value"
        success = False
    if (not check_type(metadata["chipSelect"],SpiControllerChipSelect)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for chipSelect value"  
        success = False
    if (not check_type(metadata["chipSelectPol"],SpiControllerChipSelectPolarity)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for chipSelectPol value"  
        success = False

    return success, result

def spiControllerSetParametersValidator(metadata: dict) :
    success, result = validateSpiControllerSetParameters(metadata)
    requests, response = None, None

    if success:
        requests, response = spiControllerSetParametersSerializer(metadata["id"], metadata["bitOrder"], metadata["mode"], metadata["dataWidth"], metadata["chipSelect"], metadata["chipSelectPol"], metadata["frequency"])
    
    return requests, response, result

def validateSpiControllerSetParameters(metadata: dict):
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SPI CONTROLLER SET PARAMETERS requests success")
    success = True

    if (not check_range(metadata["frequency"],int,SPI_CONTROLLER_MIN_FREQUENCY,SPI_CONTROLLER_MAX_FREQUENCY)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: frequency value out of range"
        success = False
    if (not check_type(metadata["bitOrder"],SpiControllerBitOrder)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for bitOrder value"
        success = False
    if (not check_type(metadata["mode"],SpiControllerMode)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for mode value"
        success = False
    if (not check_type(metadata["dataWidth"],SpiControllerDataWidth)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for dataWidth value"
        success = False
    if (not check_type(metadata["chipSelect"],SpiControllerChipSelect)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for chipSelect value"  
        success = False
    if (not check_type(metadata["chipSelectPol"],SpiControllerChipSelectPolarity)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for chipSelectPol value"  
        success = False

    return success, result

def spiControllerTransferValidator(metadata: dict):
    success, result = validateSpiControllerTransfer(metadata)
    requests, response = None, None
    if success:
        requests, response = spiControllerTransferSerializer(metadata["id"], metadata["transferLength"], metadata["payload"])    

    return requests, response, result

def validateSpiControllerTransfer(metadata: dict):
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SPI CONTROLLER TRANSFER requests success")
    success = True

    if (not check_byte_array(metadata["payload"], 1024)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: payload length or data type error"
        success = False
    
    if (not check_type(metadata["payload"], list)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for payload value"
        success = False
    
    if (not check_range(metadata["transferLength"],int,1,1024)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: transferLength value out of range"
        success = False

    return success, result

#####################################################################
# ---------------------------- GPIO --------------------------------
#####################################################################
    
def gpioConfigurePinValidator (metadata: dict):
    success, result = validateGpioConfigurePin(metadata)
    requests = None
    response = None

    if (success):
        requests, response = gpioConfigurePinSerializer(metadata["id"], metadata["pinNumber"], metadata["functionality"])
    
    return requests, response, result
    
def validateGpioConfigurePin( metadata: dict ):
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO CONFIGURE PIN requests success")
    success = True

    if (not check_type(metadata["pinNumber"],GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Pin Number value"
        success = False
    if (not check_type(metadata["functionality"],GpioFunctionality)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Functionality value"
        success = False
    
    return success, result

def gpioDigitalWriteValidator (metadata: dict):
    success, result = validateGpioDigitalWrite(metadata)
    requests = None
    response = None

    if (success):
        requests, response = gpioDigitalWriteSerializer(metadata["id"], metadata["pinNumber"], metadata["logicLevel"])
    
    return requests, response, result
    
def validateGpioDigitalWrite( metadata: dict ):
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO DIGITAL WRITE requests success")
    success = True

    if (not check_type(metadata["pinNumber"],GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Pin Number value"
        success = False
    if (not check_type(metadata["logicLevel"],GpioLogicLevel)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Logic Level value"
        success = False
    
    return success, result

def gpioDigitalReadValidator (metadata: dict):
    success, result = validateGpioDigitalRead(metadata)
    requests = None
    response = None

    if (success):
        requests, response = gpioDigitalReadSerializer(metadata["id"], metadata["pinNumber"])
    
    return requests, response, result
    
def validateGpioDigitalRead( metadata: dict ):
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO DIGITAL READ requests success")
    success = True

    if (not check_type(metadata["pinNumber"],GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Pin Number value"
        success = False
    
    return success, result

def gpioSetInterruptValidator (metadata: dict):
    success, result = validateGpioSetInterruptValidator(metadata)
    requests = None
    response = None

    if (success):
        requests, response = gpioSetInterruptSerializer(metadata["id"], metadata["pinNumber"],metadata["trigger"])
    
    return requests, response, result
    
def validateGpioSetInterruptValidator( metadata: dict ):
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO SET INTERRUPT requests success")
    success = True

    if (not check_type(metadata["pinNumber"],GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Pin Number value"
        success = False
    if (not check_type(metadata["trigger"],GpioTriggerType)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for the Trigger value"
        success = False
    
    return success, result

def gpioDisableInterruptValidator (metadata: dict):
    success, result = validateGpioDisableInterruptValidator(metadata)
    requests = None
    response = None

    if (success):
        requests, response = gpioDisableInterruptSerializer(metadata["id"], metadata["pinNumber"])
    
    return requests, response, result
    
def validateGpioDisableInterruptValidator( metadata: dict ):
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO DISABLE INTERRUPT requests success")
    success = True

    if (not check_type(metadata["pinNumber"],GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for Pin Number value"
        success = False
    
    return success, result