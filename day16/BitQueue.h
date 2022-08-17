//
// Created by jordan on 8/15/22.
//

#ifndef DAY16_BITQUEUE_H
#define DAY16_BITQUEUE_H
#include <vector>
using std::vector;

#include <cstdint>
#include <queue>

#include <string>
using std::string;


#define CURRENT_POS_START 31
#define NUM_BITS 8

class BitQueue {
public:
    BitQueue(uint32_t val);
    BitQueue(const std::string& bytes);
    BitQueue(const vector<uint8_t>& bits_array);

    void add_hex(std::string hex);
    void add(vector<uint8_t> bytes);
    void add(uint8_t val);
    uint32_t get_num_bits(uint8_t amount);
    uint32_t num_bits_left();
    bool pop();

    bool empty();

private:
    std::queue<uint32_t> q;
    uint32_t current_val;
    uint32_t current_pos;
    uint32_t remainder;
    int32_t remainder_pos;
};



#endif //DAY16_BITQUEUE_H
