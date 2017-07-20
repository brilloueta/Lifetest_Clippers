#ifndef linker_oled_data_H
#define linker_oled_data_H

//#include <Arduino.h>



#define OLED_Max_X 		127	//128 Pixels
#define OLED_Max_Y 		63	//64  Pixels

#define PAGE_MODE			01
#define HORIZONTAL_MODE			02


#define OLED_Address		0x3c
#define OLED_Command_Mode		0x80
#define OLED_Data_Mode		0x40
#define OLED_Display_Off_Cmd	0xAE
#define OLED_Display_On_Cmd	0xAF
#define OLED_Normal_Display_Cmd	0xA6
#define OLED_Inverse_Display_Cmd	0xA7
#define OLED_Activate_Scroll_Cmd	0x2F
#define OLED_Dectivate_Scroll_Cmd	0x2E
#define OLED_Set_Brightness_Cmd	0x81

#define Scroll_Left			0x00
#define Scroll_Right			0x01

#define Scroll_2Frames			0x7
#define Scroll_3Frames			0x4
#define Scroll_4Frames			0x5
#define Scroll_5Frames			0x0
#define Scroll_25Frames			0x6
#define Scroll_64Frames			0x1
#define Scroll_128Frames		0x2
#define Scroll_256Frames		0x3


class LinkerOLED {

public:

char addressingMode;


void init(void);

void setNormalDisplay();
void setInverseDisplay();

void sendCommand(unsigned char command);
void sendData(unsigned char Data);

void setPageMode();
void setHorizontalMode();

void setTextXY(unsigned char Row, unsigned char Column);
void clearDisplay();
void setBrightness(unsigned char Brightness);
void putChar(unsigned char c);
void putString(const char *String);
unsigned char putNumber(long n);
unsigned char putFloat(float floatNumber,unsigned char decimal);
unsigned char putFloat(float floatNumber);
void drawBitmap(unsigned char *bitmaparray,int bytes);

void setHorizontalScrollProperties(bool direction,unsigned char startPage, unsigned char endPage, unsigned char scrollSpeed);
void activateScroll();
void deactivateScroll();

};

extern LinkerOLED linkeroled;  // Linker OLED object 

#endif



