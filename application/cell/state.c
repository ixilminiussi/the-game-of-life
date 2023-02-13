#include <definitions.h>
#include <properties.c>
//@@//
uint8_t alive;
uint32_t generation = 0;
uint8_t begin = 1;

uint8_t neighbourUpdates[2] = {0, 0};
uint8_t liveNeighbours[2] = {0, 0};

uint64_t start;

uint32_t cycle = 0;

uint32_t btimer;
uint8_t buffer = 0;
uint8_t balive;
uint8_t bgeneration;
//@@//