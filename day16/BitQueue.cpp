//
// Created by jordan on 8/15/22.
//

#include "BitQueue.h"
#include <queue>
#include <algorithm>
#include <stdexcept>
#include <iostream>

BitQueue::BitQueue(uint32_t val) : current_val(val), current_pos(0), remainder(0), remainder_pos(NUM_BITS-1)
{
}

BitQueue::BitQueue(const std::string& bytes) : current_val(0), current_pos(NUM_BITS), remainder(0), remainder_pos(NUM_BITS-1)
{
    add_hex(bytes);
}

BitQueue::BitQueue(const vector<uint8_t>& bits_array) : current_val(0), current_pos(0), remainder(0), remainder_pos(NUM_BITS-1)
{
    std::for_each(bits_array.begin(), bits_array.end(), [this](const uint8_t val)
    {
        q.push(val);
    });

    current_val = q.front();
    q.pop();
    current_pos = 0;
}

bool BitQueue::pop()
{
    if (current_pos >= NUM_BITS)
    {
        current_val = q.front();
        q.pop();
        current_pos = 0;
    }

    bool val = ((current_val << current_pos) & 0x80) > 0;
    current_pos++;
    return val;
}

bool BitQueue::empty()
{
    if (current_pos >= NUM_BITS && q.empty())
        return true;
    return false;
}

void BitQueue::add(uint8_t val)
{
    q.push(val);
}
/*
uint32_t BitQueue::pop_many(uint8_t amount)
{
    if (amount > 32)
    {
        throw std::logic_error("The amount provided is too large. Must be smaller than 32 bits.");
    }
    if (amount > num_bits_left())
    {
        throw std::logic_error("The amount of requested bits is more than are available.");
    }


}*/

uint32_t BitQueue::num_bits_left()
{
    return (q.size() * 8) + (NUM_BITS - current_pos);
}

void BitQueue::add_hex(std::string hex)
{
    if (hex.length() % 2 != 0)
    {
        throw std::logic_error("The hex string provided is not a multiple of two.");
    }

    auto bytes = vector<uint8_t> {};
    bytes.reserve(hex.length() / 2);

    bool high = true;
    uint8_t full_byte = 0;
    for (int i = 0; i < hex.length(); i++)
    {
        uint8_t current = 0;
        uint8_t val = tolower(hex[i]);

        if (val >= 'a' && val <= 'f')
            current = (val - 'a') + 10;
        else if (val >= '0' && val <= '9')
            current = (val - '0');
        else
            throw std::logic_error("The byte at index " + std::to_string(i) + " is not a valid character: " + std::to_string(hex[i]));

        if (high) {
            full_byte = current << 4;
        }
        else
        {
            full_byte |= current;
            q.push(full_byte);
            full_byte = 0;
        }

        high = !high;
    }

}

uint32_t BitQueue::get_num_bits(uint8_t amount)
{
    uint32_t out = 0;
    if (amount > num_bits_left())
    {
        throw std::logic_error("Not enough bits left to retrieve that many bits.");
    }
    if (amount > sizeof(out) * 8)
    {
        throw std::logic_error("Cannot return more than 32 bits.");
    }

    for (int pos = 0; pos < amount; pos++)
    {
        auto val = pop();
        out = (out << 1) | val;

    }
    std::cout << std::endl;
    return out;
}


