#!/usr/bin/env python3
import random
import math


class Cache:
    def __init__(self, mapping_technique, cache_size, block_size, replacement_technique=None):
        self.mapping_technique = mapping_technique
        self.cache_size = cache_size
        self.block_size = block_size
        self.replacement_technique = replacement_technique
        self.cache_content = {}
        self.main_memory = {}

    def select_mapping_technique(self):
        if self.mapping_technique == "direct":
            print("Using Direct Mapping technique.")
        elif self.mapping_technique == "associative":
            print("Using Associative Mapping technique.")
        elif self.mapping_technique == "set-associative":
            print("Using Set-Associative Mapping technique.")
        else:
            print("Invalid mapping technique selected.")

    def visualize_cache(self):
        print("Cache content:")
        for address, block in self.cache_content.items():
            print(f"Block {address}: {block}")
    
    def visualize_main_memory(self):
        print("Main memory content:")
        for address, block in self.main_memory.items():
            print(f"Block {address}: {block}")

    def generate_random_word(self):
        return random.randint(0, 100)

    def check_word_in_cache(self, word):
        if self.mapping_technique == "direct":
            block_address = word % (self.cache_size / self.block_size)
            if block_address in self.cache_content:
                print("Word found in cache.")
                return True
            else:
                print("Word not found in cache.")
                return False
        elif self.mapping_technique == "associative":
            for block in self.cache_content.values():
                if word in block:
                    print("Word found in cache.")
                    return True
            print("Word not found in cache.")
            return False
        elif self.mapping_technique == "set-associative":
            set_index = math.floor(word % (self.cache_size / (self.block_size * 2)))
            for i in range(set_index * 2, set_index * 2 + 2):
                if i in self.cache_content and word in self.cache_content[i]:
                    print("Word found in cache.")
                    return True
            print("Word not found in cache.")
            return False
        else:
            print("Invalid mapping technique selected.")
            return False

    def bring_word_from_memory(self, word):
        block_address = word // self.block_size
        if block_address in self.main_memory:
            print(f"Word found in main memory. Bringing block {block_address} to cache.")
            return self.main_memory[block_address]
        else:
            print("Word not found in main memory.")
            return None

    def deliver_word_to_processor(self, word):
        block_address = word // self.block_size
        if self.check_word_in_cache(word):
            block_address = word % (self.cache_size / self.block_size)
            print(f"Delivering word {word} from cache block {block_address} to processor.")
        else:
            block = self.bring_word_from_memory(word)
            if block is not None:
                if len(self.cache_content) < self.cache_size:
                    self.cache_content[block_address] = block
                else:
                    if self.replacement_technique == "FIFO":
                        self.cache_content.pop(next(iter(self.cache_content)))
                        self.cache_content[block_address] = block
                    elif self.replacement_technique == "LRU":
                        self.cache_content.pop(min(self.cache_content, key=self.cache_content.get))
                        self.cache_content[block_address] = block
                    else:
                        print("Invalid replacement technique selected.")
                        print(f"Delivering word {word} from main memory block {block_address} to processor.")
            else:
                print(f"Word {word} not found in main memory.")

    def fill_main_memory(self):
        for i in range(0, 100, self.block_size):
            block = []
            for j in range(self.block_size):
                block.append(self.generate_random_word())
            self.main_memory[i] = block


if __name__ == "__main__":
    while True:
        mapping_technique = input("Select mapping technique: ")
        cache_size = int(input("Select cache size: "))
        block_size = int(input("Select block size: "))
        replacement_technique = input("Select replacement technique: ")
        cache = Cache(mapping_technique, cache_size, block_size, replacement_technique)
        cache.select_mapping_technique()
        cache.fill_main_memory()
        cache.visualize_cache()
        word = int(input("Select word to be delivered to processor: "))
        cache.deliver_word_to_processor(word)
        cache.visualize_cache()
        if input("Continue? (y/n) ") == "n":
            break
