const int r = 5;             //connect red led at pin 9    
const int g = 6;           //connect yellow led at pin 10
const int sec = 1000;       //seconds defined 
void setup() 
  {
    pinMode(r,OUTPUT);
    pinMode(g,OUTPUT);
    delay(sec);
  }

void loop()
    {
       analogWrite(r,1) ;
        delay(sec*5);
       analogWrite(r,0) ;
        analogWrite(g,1) ;
        delay(sec*5);
        analogWrite(g,0) ;
        
    }
