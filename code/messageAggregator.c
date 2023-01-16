#include <definitions.h>
//@@//
uint8_t alive;
uint32_t generation;
uint16_t x;
uint16_t y;
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