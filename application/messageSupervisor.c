#include <definitions.h>
//@@//
uint8_t alive;
uint32_t generation;
uint32_t x;
uint32_t y;
uint32_t speed;
uint8_t ping;
//@@//

uint8_t MSG(val) {
    return val;
}

uint16_t MSG(val) {
    return val;
}

uint32_t MSG(val) {
    return val;
}