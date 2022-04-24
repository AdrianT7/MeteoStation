#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11   // DHT 11

DHT dht(DHTPIN, DHTTYPE);
 
void setup(){
  Serial.begin(9600);
  dht.begin();
}

void loop(){

  delay(2000);

  float t = dht.readTemperature(); //temperatura
  float h = dht.readHumidity(); //wilgotnosc

  String tmp = String("+T" + String(t));
  String wlg = String("+W" + String(h));

  //Wyslanie przez UART aktualnej temperatury
  //Serial.print("+T"); //+ oznacza początek pakietu danych
  Serial.print(tmp);
  delay(1100); 

  //Wyslanie przez UART aktualnej wilgotnosci
  //Serial.print("+W"); //+ oznacza początek pakietu danych
  Serial.print(wlg);
}
