# Weather-Responsive-Plant-Care-System
The Weather-Responsive Plant Care  System is designed to provide optimal care for plants based on real-time weather conditions. This helps people whom are taking care of plants to have better awareness of the weather.
so this is how the project will work, ive broke it down to 4 requirement so follow this requirement 

Requirement 1(temperature and humidity monitoring):
  equipment: DHT11,OLED
fuction
  - read the temp and humidity
  - show data on oled
  - if themp and humidity is over a certain treshold activate auto watering


Requirement 2(sunlight detection and day and night mode):
  equipment: LDR,OLED,BUTTON
function:
  - if ldr detects sun light, it will run code logic for auto watering(req1) if now it wil got to night mode and you have to use button to water the plant (req 4)


Requirement 3(water level monitoring):
  equipment: ultrasonic,oled and buxxer
function
 - ultrasonic sensor measure the water level in water and display the water level in the oled
 - if too little the buzzer will beep


Requirement 4(manual override):
  equipment:button
function:
  - just press button if u wan manually water the plant 
