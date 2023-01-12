#include <definitions.h>
#include <properties.c>
//@@//
uint8_t send;
//@@//

inline uint8_t DEVICESTATE(val) {
    return val;
}

inline uint32_t DEVICESTATE(val) {
    return val;
}