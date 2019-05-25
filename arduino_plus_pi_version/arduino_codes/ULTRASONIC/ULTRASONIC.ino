const int trigPin = 10;
const int echoPin = 11;
// defines variables

int command = 1;
long duration;
int distance;
void setup() {
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
Serial.begin(9600); // Starts the serial communication
}


void loop() {
// Clears the trigPin
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);
// Calculating the distance
distance= duration*0.034/2;
// Prints the distance on the Serial Monitor
Serial.print("Distance: ");
Serial.println(distance);
if (Serial.available() > 0){
    command = Serial.read();
    Serial.println(command);
    
  }
  else{
    forward(distance);
  }
   

  


send_command(command);



}

void stopped()
{  
analogWrite(9,0);
analogWrite(3, 0);
delay(1000);
command=1;
}

void forward(int distance)
{  
  if (distance>35)
  {
  digitalWrite(8, HIGH);
  digitalWrite(7, LOW);
  analogWrite(9, 200);
  digitalWrite(5, HIGH);
  digitalWrite(4, LOW);
  analogWrite(3, 200);
  }
  else 
  {
    analogWrite(9,0);
    analogWrite(3, 0);
   
  }
  
}

void forward_right()
{
  digitalWrite(8, HIGH);
  digitalWrite(7, LOW);
  analogWrite(9, 50);
  digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
  analogWrite(3, 50);

}

void backward()
{  
  digitalWrite(7, HIGH);
  digitalWrite(8, LOW);
  analogWrite(9, 200);
  digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
  analogWrite(3, 200);
}

void send_command(int command){
  switch (command){

     //reset command
     case 0: stopped(); break;
     case 1: forward(distance);break;
/*
     // single command
     case 1: forward(time); break;
     case 2: reverse(time); break;
     case 3: right(time); break;
     case 4: left(time); break;

     //combination command
     case 6: forward_right(time); break;
     case 7: forward_left(time); break;
     case 8: reverse_right(time); break;
     case 9: reverse_left(time); break;
*/
     default: Serial.print("Inalid Command\n");
    }
}




