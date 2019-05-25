 // defines variables
const int sp=150;
const int lsp=50;
long duration;
int val;

void setup() {
Serial.begin(9600); // Serial comm begin at 9600bps
pinMode(7, OUTPUT); 
pinMode(8, OUTPUT); 
pinMode(4, OUTPUT); 
pinMode(5, OUTPUT); 
}
void loop() {
  
  if (Serial.available()){
    val = Serial.read();
    if (val == 'd'){
        right();
      }
    if (val == 'a'){
        left();
      }
    if (val == 'w'){
        forward();
      }
    if (val == 's'){
        backward();
    }
     if (val == 'x'){
        stop();
    }
        
    
    }

}

void forward()
{
digitalWrite(8, HIGH);
digitalWrite(7, LOW);
analogWrite(9, sp);
digitalWrite(5, HIGH);
digitalWrite(4, LOW);
analogWrite(3, sp);
}

void backward()
{  
digitalWrite(7, HIGH);
digitalWrite(8, LOW);
analogWrite(9,sp);
digitalWrite(5, LOW);
digitalWrite(4, HIGH);
analogWrite(3, sp);
}

void left()
{  
digitalWrite(8, HIGH);
digitalWrite(7, LOW);
analogWrite(9,lsp);
digitalWrite(5, LOW);
digitalWrite(4, HIGH);
analogWrite(3, lsp);
}

void right()
{  
digitalWrite(7, HIGH);
digitalWrite(8, LOW);
analogWrite(9,lsp);
digitalWrite(4, LOW);
digitalWrite(5, HIGH);
analogWrite(3, lsp);
}
void stop()
{  

analogWrite(9,0);

analogWrite(3, 0);
}
