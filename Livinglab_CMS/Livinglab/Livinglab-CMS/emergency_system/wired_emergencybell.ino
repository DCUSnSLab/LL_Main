int LED = 3;     //LED 핀 번호
int BUTTON = 2;  //Button 핀 번호

int delayTime = 50; //blink 주기설정

void blinkLED(){        //비상벨 호출알림
  for(int i = 0; i<10; i++){
    digitalWrite(LED, HIGH);
    delay(delayTime);
    digitalWrite(LED, LOW);
    delay(delayTime);
  }
}

//비상벨 초기화 
void setup(){
  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT);
  Serial.begin(9600);
 }

 void loop(){
  int buttonState;
  buttonState = digitalRead(BUTTON); //버튼입력

  if(buttonState == HIGH){ //버튼이 눌렸을 때 blink() 실행
    Serial.println("Event emgerged");
    blinkLED();
  }
  else{
    //Serial.println("Normal State");
  }
 }
