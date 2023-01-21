#!/usr/bin/env python3
import random
import math
import json

class Store_Jason:
    def __init__(self, filename):
        self.filename = filename
    
    def load(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    def save(self, data):
        with open(self.filename, 'w') as f:
            try:
                json.dump(data, f)
            except TypeError:
                print("Data type not serializable.")


class Cache:
    def __init__(self, mapping_technique, cache_size, block_size, replacement_technique=None, main_memory_size=32):
        self.mapping_technique = mapping_technique
        self.cache_size = cache_size
        self.block_size = block_size
        self.replacement_technique = replacement_technique
        self.cache_content = {}
        self.main_memory = {}
        self.main_memory_size = main_memory_size
        self.file_cache = Store_Jason("cache_content.json")
        self.file_main_memory = Store_Jason("main_memory.json")
        self.cache_content = self.file_cache.load()
        self.main_memory = self.file_main_memory.load()

    def specification(self):
        print("main memory size: {} word".format(self.main_memory_size))
        print("cache size: {} word".format(self.cache_size))
        print("block size: {} word".format(self.block_size))
        print("mapping technique: {}".format(self.mapping_technique))
        print("replacement technique: {}".format(self.replacement_technique))
        print()

    def visualize_cache(self):
        print("Cache content:")
        for address, block in self.cache_content.items():
            print(f"Block {address}: {block}")
    
    def visualize_main_memory(self):
        print("Main memory content:")
        for address, block in self.main_memory.items():
            print(f"Block {address}: {block}")

    def generate_random_word(self):
        return random.randint(0, self.main_memory_size)

    def check_word_in_cache(self, word):
        if self.mapping_technique == "direct":
            block_address = int(word % (self.cache_size / self.block_size))
            if str(block_address) in self.cache_content.keys():
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
        
        self.file_cache.save(self.cache_content)

    def fill_main_memory(self):
        if len(self.main_memory) == self.main_memory_size // self.block_size:
            print("Main memory already filled.")
            return
        block_number = self.main_memory_size // self.block_size

        for i in range(block_number):
            block = []
            for j in range(self.block_size):
                block.append(self.generate_random_word())
            self.main_memory[i] = block
        self.file_main_memory.save(self.main_memory)


if __name__ == "__main__":
    # while True:
    #     mapping_technique = input("Select mapping technique: ")
    #     cache_size = int(input("Select cache size: "))
    #     block_size = int(input("Select block size: "))
    #     replacement_technique = input("Select replacement technique: ")
    #     cache = Cache(mapping_technique, cache_size, block_size, replacement_technique)
    #     cache.select_mapping_technique()
    #     cache.fill_main_memory()
    #     cache.visualize_cache()
    #     word = int(input("Select word to be delivered to processor: "))
    #     cache.deliver_word_to_processor(word)
    #     cache.visualize_cache()
    #     if input("Continue? (y/n) ") == "n":
    #         break
    cache = Cache("direct", 16, 4)
    cache.specification()
    cache.fill_main_memory()
    cache.visualize_cache()
    cache.visualize_main_memory()
    cache.deliver_word_to_processor(5)
    cache.visualize_cache()
