esp32_ble_tracker: #### Stop the active scan ####
  scan_parameters: 
    active: false

button:
  - platform: template
    name: "Start Scan"
    on_press:
      - esp32_ble_tracker.start_scan:
  
  - platform: template
    name: "Stop Scan"
    on_press:
      - esp32_ble_tracker.stop_scan:

binary_sensor:
- platform: status
  name: "ESP32 Status"
- platform: template
  id: ble_yc01_ble_connected
  icon: mdi:bluetooth-connect
  name: "BLE Connected"

time:
  - platform: homeassistant
    id: homeassistant_time
    on_time:
      # Turn on BLE client every 30 minutes for 2 minutes
      - seconds: 0
        minutes: /30
        then:
          - switch.turn_on: ble_switch
          - delay: 25min
          - switch.turn_off: ble_switch


######################################################
##                                                  ##
##   To initiate to connection with the BLE device  ##
##                                                  ##
######################################################

ble_client: 
  - mac_address: C0:00:00:XX:XX:XX #Use the MAC address of your BLE device
    id: ble_yc01
    on_connect: #### Actions to perform when connecting to the BLE device ####
      then:
      #### Wait until characteristic is discovered ####
        - wait_until:   
            lambda: |-
              esphome::ble_client::BLEClient* client = id(ble_yc01);
            
              auto service_uuid = 0xFF01;
              auto char_uuid = 0xFF02;
              
              //#### When waiting for connection, we extract the available characteristics ####
              esphome::ble_client::BLECharacteristic* chr = client->get_characteristic(service_uuid, char_uuid);
              
              return chr != nullptr;
              
        #### Official connection to the BLE device with the desired characteristic ####
        - lambda: |- 
            ESP_LOGD("ble_client_lambda", "Connected to BLE-YC01");
            id(ble_yc01_ble_connected).publish_state(true);

            esphome::ble_client::BLEClient* client = id(ble_yc01);
            
            auto service_uuid = 0xFF01; 
            auto char_uuid = 0xFF02;
            
            esphome::ble_client::BLECharacteristic* chr = client->get_characteristic(service_uuid, char_uuid);
            
            if (chr == nullptr) {
                ESP_LOGW("ble_client", "[0xFF01] Characteristic not found.  State update can not be written.");
            }
        
    on_disconnect:
      then:
        - lambda: |-
            ESP_LOGD("ble_client", "Disconnected from BLE-YC01");
            id(ble_yc01_ble_connected).publish_state(false);
            
######################################################
##                                                  ##
##     Sensors associated with the BLE device       ##
##                                                  ##
######################################################
            
sensor: #### Template sensor as their values are publish from a lambda or the BLE client ####

  - platform: template    
    name: "BLE-YC01 EC"
    id: ble_yc01_ec_sensor
    unit_of_measurement: "µS/cm"
    accuracy_decimals: 0
    state_class: measurement
    icon: mdi:water-opacity
    
  - platform: template
    name: "BLE-YC01 TDS"
    id: ble_yc01_tds_sensor
    unit_of_measurement: "ppm"
    accuracy_decimals: 0
    state_class: measurement
    icon: mdi:water-opacity
    
  - platform: template
    name: "BLE-YC01 Temperature"
    id: ble_yc01_temperature_sensor
    unit_of_measurement: "F"
    accuracy_decimals: 2
    state_class: measurement
    device_class: temperature
    
  - platform: template
    name: "BLE-YC01 ORP"
    id: ble_yc01_orp_sensor
    unit_of_measurement: "mV"
    accuracy_decimals: 0
    state_class: measurement
    device_class: voltage
    
  - platform: template
    name: "BLE-YC01 pH"
    id: ble_yc01_ph_sensor
    unit_of_measurement: "pH"
    accuracy_decimals: 2
    state_class: measurement
    icon: mdi:ph

  - platform: template
    name: "BLE-YC01 battery"
    id: ble_yc01_battery
    unit_of_measurement: "%"
    accuracy_decimals: 0
    state_class: measurement
    device_class: battery
    icon: mdi:battery


    
  - platform: ble_client ####  Sensor required to manage values coming from the BLE device ####
    ble_client_id: ble_yc01
    type: characteristic
    id: ble_yc01_sensor
    update_interval: 30s
    internal: true
    service_uuid: FF01
    characteristic_uuid: FF02
    notify: true
    #### Lambda to decode values and push to the associated sensors ####
    lambda: |-
    
      if (x.size() == 0) return NAN;
      
      //ESP_LOGD("ble_client.receive", "value received with %d bytes: [%.*s]", x.size(), x.size(), &x[0]); // ####  Useful for debugging ####
 
 
      // ### DECODING ###
      uint8_t tmp = 0;
      uint8_t hibit = 0;
      uint8_t lobit = 0;
      uint8_t hibit1 = 0;
      uint8_t lobit1 = 0;
      auto message = x;
      
      for (int i = x.size() -1 ; i > 0; i--) {
        tmp=message[i];
        hibit1=(tmp&0x55)<<1;
        lobit1=(tmp&0xAA)>>1;
        tmp=message[i-1];	
        hibit=(tmp&0x55)<<1;
        lobit=(tmp&0xAA)>>1;
        
        message[i]=~(hibit1|lobit);
        message[i-1]=~(hibit|lobit1);

      }
      
      //ESP_LOGD("ble_client.receive", "value received with %d bytes: [%.*s]", message.size(), message.size(), &message[0]); // #### For debug ####


      // #### Extraction of individual values ####
      auto temp = ((message[13]<<8) + message[14]);
      auto ph = ((message[3]<<8) + message[4]);
      auto orp = ((message[20]<<8) + message[21]);
      auto battery = ((message[15]<<8) + message[16]);
      auto ec = ((message[5]<<8) + message[6]);
      auto tds = ((message[7]<<8) + message[8]);
      
      // #### Sensors updated with new values
      id(ble_yc01_temperature_sensor).publish_state(((temp/10.0) * (9.0/5.0)) + 32.0);
      id(ble_yc01_ph_sensor).publish_state(ph/100.0);
      id(ble_yc01_orp_sensor).publish_state(orp);
      id(ble_yc01_battery).publish_state(battery/45);// bei uns eher 31.5
      id(ble_yc01_ec_sensor).publish_state(ec);
      id(ble_yc01_tds_sensor).publish_state(tds);
       
      return 0.0; // this sensor isn't actually used other than to hook into raw value and publish to template sensors


switch:  #### To switch on and off the communication with the BLE device ####
  - platform: ble_client
    id: ble_switch
    ble_client_id: ble_yc01
    name: "Enable BLE-YC01"