#import matplotlib.pyplot as plt
import re
def hex_to_base10(hex_value):
    try:
        # Convert hex to base 10
        decimal_value = int(hex_value, 16)
        return decimal_value
    except ValueError:
        return "Invalid hexadecimal value"
    
# Read File Method 
def readMethod(filename):
    # Use a context manager to automatically close the file when done
    with open(filename, "r") as file:
        header = file.readline()  # Read header (if there is one)
        baseValue = 0x090  # Base value (144 in decimal)
        
        # Existing indices lists
        diagnostics_idx     = []
        battery_voltage_idx = []
        module_temp_idx     = []
        cell_temp_idx       = []
        balancing_rate_idx  = []
        
        # New indices lists for additional codes
        overall_params_idx     = []
        cell_voltages_b_idx    = []
        cell_modtemp_b_idx     = []
        cell_temp_b_idx        = []
        cell_balrate_b_idx     = []
        soc_params_idx         = []
        config_params_idx      = []
        login_logout_idx       = []
        set_pass_idx           = []


        # New Lists I made: 

        #Battery Voltage
        min_cell_voltage = []
        max_cell_voltage = []
        average_cell_voltage = []
        total_cell_voltage = []

        #Cell Module Temps
        min_cell_module_temp = []
        max_cell_module_temp = []
        average_cell_module_temp = []

        #Cell Temps
        min_cell_temp = []
        max_cell_temp = []
        average_cell_temp =[]

        #Cell Balacing Rate
        min_cell_bal_rate = []
        max_cell_bal_rate = []
        average_cell_bal_rate = []

        #Indiviual Cell Voltages
            #Group1
        ind_cell_voltage = [] 
        
        


        


        
        # Existing counters
        diag_count = 0
        batt_count = 0
        modt_count = 0
        cellt_count = 0
        bal_count = 0

        # New counters for additional messages
        overall_count  = 0
        cellv_b_count  = 0
        modtemp_b_count= 0
        cellt_b_count  = 0
        balrate_b_count= 0
        soc_count      = 0
        config_count   = 0
        login_count    = 0
        pass_count     = 0

        for line in file:
            # Remove any leading/trailing whitespace
            line = line.strip()
            if not line:
                continue  # skip blank lines

            # Split the line by whitespace. Adjust the separator if needed.
            contents = line.split()
            
            # Ensure there are enough columns; here we expect at least 4:
            # [timestamp, someID, hexCode, measurement]
            if len(contents) < 4:
                continue

            # Convert the third field from hex string to integer.
            try:
                code_val = int(contents[2], 16)
            except ValueError:
                # If conversion fails, skip this line.
                continue

            # Check the code and append the measurement index to the appropriate list.
            if code_val == baseValue + 7:  # Diagnostics code
                diagnostics_idx.append(diag_count)
                diag_count += 1


            elif code_val == baseValue + 1:  # Battery Voltage Overall code

                min_voltage = hex_to_base10(contents[3][0:2])
                min_cell_voltage.append(min_voltage)

                max_voltage = hex_to_base10(contents[3][2:4])
                max_cell_voltage.append(max_voltage)

                avg_voltage = hex_to_base10(contents[3][4:6])
                average_cell_voltage.append(avg_voltage)

                total_voltage = hex_to_base10(contents[3][10:12] + contents[3][12:14] + contents[3][6:8] + contents[3][8:10])
                total_cell_voltage.append(total_voltage)

               
                battery_voltage_idx.append(batt_count) #what does this do?
                batt_count += 1                        #what does this do?

            elif code_val == baseValue + 2:  # Cell Module Temperature Overall code

                min_module_temp = hex_to_base10(contents[3][0:2])
                min_cell_module_temp.append(min_module_temp)
                
                max_module_temp = hex_to_base10(contents[3][2:4])
                max_cell_module_temp.append(max_module_temp)

                avg_module_temp = hex_to_base10(contents[3][4:6])
                average_cell_module_temp.append(avg_module_temp)


                module_temp_idx.append(modt_count) #what does this do?
                modt_count += 1                    #what does this do?

            elif code_val == baseValue + 8:  # Cell Temperature Overall code

                min_cell_temp_val = hex_to_base10(contents[3][0:2])
                min_cell_temp.append(min_cell_temp_val)

                max_cell_temp_val = hex_to_base10(contents[3][2:4])
                max_cell_temp.append(max_cell_temp_val)

                avg_cell_temp_val = hex_to_base10(contents[3][4:6])
                average_cell_temp.append(avg_cell_temp_val)

                cell_temp_idx.append(cellt_count) #what does this do?
                cellt_count += 1                  #what does this do?

            elif code_val == baseValue + 3:  # Cell Balancing Rate Overall code

                min_cell_bal = hex_to_base10(contents[3][0:2])
                min_cell_bal_rate.append(min_cell_bal)

                max_cell_bal = hex_to_base10(contents[3][2:4])
                max_cell_bal_rate.append(max_cell_bal)

                avg_cell_bal = hex_to_base10(contents[3][4:6])
                average_cell_bal_rate.append(avg_cell_bal)

                balancing_rate_idx.append(bal_count) #what does this do?
                bal_count += 1                       #what does this do?

            elif code_val == baseValue + 0:  # Overall Parameters code 
                overall_params_idx.append(overall_count)
                overall_count += 1
            elif code_val == baseValue + 0x0B:  # Individual Cell Voltages – Option B
                cell_voltages_b_idx.append(cellv_b_count)
                cellv_b_count += 1
            elif code_val == baseValue + 0x0C:  # Individual Cell Module Temperatures – Option B
                cell_modtemp_b_idx.append(modtemp_b_count)
                modtemp_b_count += 1
            elif code_val == baseValue + 0x0E:  # Individual Cell Temperatures – Option B
                cell_temp_b_idx.append(cellt_b_count)
                cellt_b_count += 1
            elif code_val == baseValue + 0x0D:  # Individual Cell Balancing Rates – Option B
                cell_balrate_b_idx.append(balrate_b_count)
                balrate_b_count += 1
            elif code_val == baseValue + 5:  # State of Charge parameters

                soc_params_idx.append(soc_count)
                soc_count += 1
            elif code_val == baseValue + 4:  # Configuration Parameters
                config_params_idx.append(config_count)
                config_count += 1
            elif code_val == baseValue + 0x82:  # Log-in & Log-out
                login_logout_idx.append(login_count)
                login_count += 1
            elif code_val == baseValue + 0x83:  # Set New Password
                set_pass_idx.append(pass_count)
                pass_count += 1
            # ---------------------------------------------------
            
            print(code_val)



# Run the method with your CSV file
readMethod("can_log_data.csv")