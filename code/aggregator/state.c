#include <definitions.h>
#include <properties.c>
//@@//
uint8_t pointer = 0;
char payload[64];

uint8_t buffer;
char bpayload[64];
//@@//

inline uint8_t DEVICESTATE(val) {
    return val;
}

inline char DEVICESTATE(val) {
    return val;
}