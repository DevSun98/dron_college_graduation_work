#define ROLL 3    
#define PITCH 5
#define THROTTLE 6
#define YAW 9
#define FLIGHTMODE 10
#define ARM 12

const int PWM_MAX = 253; // PWM 최소 수치
const int PWM_MIN = 113; // PWM 최대 수치 || 2,3그룹 스로틀other 시발점
const int RPY_PWM_IDLE = 186; // 1그룹 롤피치요우는 가운데 값이 시발점이다

boolean beginCOM_ControllerSys = false; // 아두이노에 조종프로그램 연결 유무

struct ProcessField {
  int16_t analogValue;
  int8_t choiceCh;
  int8_t choiceMd;
};

void setup() {
  Serial.begin(9600); //블루투스 시리얼
  
  pinMode(ROLL, OUTPUT); // 4 -> 1채널
  pinMode(PITCH, OUTPUT); // 5 -> 2채널 
  pinMode(THROTTLE, OUTPUT); // 6 -> 3채널
  pinMode(YAW, OUTPUT); // 7 -> 4채널
  pinMode(FLIGHTMODE, OUTPUT); // 8 -> 5채널
  pinMode(ARM, OUTPUT); // 6채널

  analogWrite(ROLL, RPY_PWM_IDLE); // 드론 PWM 기본 세팅
  delay(500);
  analogWrite(PITCH, RPY_PWM_IDLE + 2);
  delay(500);
  analogWrite(YAW, RPY_PWM_IDLE);
  delay(500);
  analogWrite(THROTTLE, PWM_MIN);
  delay(500);
  analogWrite(FLIGHTMODE, PWM_MIN);
  delay(500);
  analogWrite(ARM, PWM_MIN);
  
}

void loop() {
  if (Serial.available()) {
    char buffer[5];
    byte len = Serial.readBytes(buffer, 5);  // 5byte의 버퍼를 수신
    buffer[5] = '\0';

    if (len == 5 && buffer[0] == '#' && buffer[4] == '@') {  // buffer 데이터 에러 검사 -- 정상값: '#???@'    -> 이거 참구문은 의미 없으니 not 반전해서 작성
      
      String str = buffer;  // String 형으로 변환
      str = str.substring(1, 4);  // "#???@" 문자열에서 ???값만 추출
      
      ProcessField processField;
      processField.choiceCh = str[1] - 48;
      processField.choiceMd = str[2] - 48;
      processField.analogValue = str.toInt();  // ???값 정수형으로 변환

      startPinMode(&processField);
    }
  }
}

void startPinMode(ProcessField *processField) {
  if (processField->analogValue - 100 >= 0) {
    analogWrite(THROTTLE, processField->analogValue); // 파이썬에서 들어오는 값으로 아날로그 출력
  }

  else {
    int8_t mdValue = processField->choiceMd;

    switch (processField->choiceCh) {
      case 0:
        if (!beginCOM_ControllerSys) { // 아두이노가 첫 시리얼 연결 일때
          beginCOM_ControllerSys = true;
          analogWrite(ROLL, RPY_PWM_IDLE); // 드론 PWM 기본 세팅
          delay(500);
          analogWrite(PITCH, RPY_PWM_IDLE + 2);
          delay(500);
          analogWrite(YAW, RPY_PWM_IDLE);
          delay(500);
          analogWrite(THROTTLE, PWM_MIN);
          delay(500);
          analogWrite(FLIGHTMODE, PWM_MIN);
          delay(500);
          analogWrite(ARM, PWM_MIN);
          
          Serial.println("#111@");
        }

        else {
          Serial.println("#000@");
        }
        break;
      
      case 1: // Yaw 조작
        if (mdValue == 0) {
          analogWrite(YAW, RPY_PWM_IDLE);
        }

        else if (mdValue == 1) {
          analogWrite(YAW, RPY_PWM_IDLE + 20); 
        }

        else if (mdValue == 2) {
          analogWrite(YAW, RPY_PWM_IDLE - 20);  
        }
        break;

      case 2:  // Pitch 조작
        if (mdValue == 0) {
          analogWrite(PITCH, RPY_PWM_IDLE + 2);
        }

        else if (mdValue == 1) {
          analogWrite(PITCH, RPY_PWM_IDLE + 20);
        }

        else if (mdValue == 2) {
          analogWrite(PITCH, RPY_PWM_IDLE - 20);;
        }
        break;

      case 3:  // Roll 조작
        if (mdValue == 0) {
          analogWrite(ROLL, RPY_PWM_IDLE);
        }

        else if (mdValue == 1) {
          analogWrite(ROLL, RPY_PWM_IDLE + 20);
        }

        else if (mdValue == 2) {
          analogWrite(ROLL, RPY_PWM_IDLE - 20);
        }
        break;

      case 4:  // Arm 조작
        if (mdValue == 0) {  // 시동 off
          analogWrite(THROTTLE, PWM_MIN);
          delay(2000);
          analogWrite(ARM, PWM_MIN);
        }

        else if (mdValue == 1) {  // 시동 on
          analogWrite(THROTTLE, PWM_MIN);
          delay(2000);
          analogWrite(ARM, PWM_MAX);;
        }
        break;

      case 5:  // flightMode 조작
        if (mdValue == 0) {
          analogWrite(FLIGHTMODE, 120);
        }

        else if (mdValue == 1) {
          analogWrite(FLIGHTMODE, 153);
        }

        else if (mdValue == 2) { 
          analogWrite(FLIGHTMODE, 186);
        }

        else if (mdValue == 3) {
          analogWrite(FLIGHTMODE, 219);
        }
        break;
    
    }
  }
}
