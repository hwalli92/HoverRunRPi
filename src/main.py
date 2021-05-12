import remote_control
import mqtt
import time


if __name__ == "__main__":
    remote = remote_control.RemoteControl()
    mqtt = mqtt.MQTTServer()
    
    while True:
        payload = remote.read_remote_input()
        
        if payload:
            if payload == "exit":
                exit()
            else:
                mqtt.publish_message(payload)
        
        time.sleep(0.5)
