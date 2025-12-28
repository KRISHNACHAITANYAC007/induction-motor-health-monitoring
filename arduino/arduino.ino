#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
String inputString = "";
void setup() {
  lcd.begin(16, 2);        
  Serial.begin(9600);      
  lcd.print("Waiting data...");
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      displayData(inputString);
      inputString = "";
    } else {
      inputString += inChar;
    }
  }
}

void displayData(String data) {
  lcd.clear();
  int tIndex = data.indexOf('T');
  int cIndex = data.indexOf('C');
  int aIndex = data.indexOf('A');
  int mIndex = data.indexOf('M');
  String temp = tIndex != -1 && cIndex != -1 ? data.substring(tIndex + 1, cIndex) : "--";
  String current = cIndex != -1 && aIndex != -1 ? data.substring(cIndex + 1, aIndex) : "--";
  String acc = aIndex != -1 && mIndex != -1 ? data.substring(aIndex + 1, mIndex) : "--";
  String motor = mIndex != -1 ? data.substring(mIndex + 1) : "--";
  lcd.setCursor(0, 0);
  lcd.print("T:" + temp + "C I:" + current);

  lcd.setCursor(0, 1);
  lcd.print("A:" + acc + " M:" + motor);
}
