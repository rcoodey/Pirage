/**
 *  Pirage
 *
 *  Copyright 2016 Ryan Coodey
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
metadata {
	definition (name: "Pirage", namespace: "rcoodey", author: "Ryan Coodey") {
		capability "Button"
        
        command "toggleGarage"
	}

	tiles {
		standardTile("toggleGarage", "device.button", width: 1, height: 1) {
			state "default", label: "Toggle", icon: "st.Transportation.transportation13", backgroundColor: "#ffffff", action: "toggleGarage"
		} 
	}
}

def toggleGarage()
{
    try {
        log.debug "Toggling $device.name"
        
        //Setup a hub action to make http request
        def getAction = new physicalgraph.device.HubAction(
            method: "GET",
            path: "/ToggleGarage/" + device.deviceNetworkId.replace("Pirage", ""),
            headers: [HOST: "192.168.1.3:80"]
        )
        getAction
        //Dont add any code below here, causes the action to not go through for some reason
    } catch (e) {
        log.debug "Error toggling garage: $e"
    }
}