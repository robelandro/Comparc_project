#!/usr/bin/env python3
import random, math, json, os


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
    def __init__(self, mapping_technique, cache_size, block_size, main_memory_size=32):
        self.mapping_technique = mapping_technique
        self.cache_size = cache_size
        self.block_size = block_size
        self.main_memory_size = main_memory_size
        self.cache_content = {}
        self.main_memory = {}
        self.file_cache = Store_Jason("cache_content.json")
        self.file_main_memory = Store_Jason("main_memory.json")
        self.cache_content = self.file_cache.load()
        self.main_memory = self.file_main_memory.load()

        if self.info_checker():
            self.specification()
        else:
            if os.path.exists("cache_content.json"):
                os.remove("cache_content.json")
                self.cache_content = {}
            if os.path.exists("main_memory.json"):
                os.remove("main_memory.json")
                self.main_memory = {}
            self.cache_content["Info"] = {"mapping_technique": self.mapping_technique, "cache_size": self.cache_size, "block_size": self.block_size, "main_memory_size": self.main_memory_size}
            self.file_cache.save(self.cache_content)
            self.main_memory["Info"] = {"mapping_technique": self.mapping_technique, "cache_size": self.cache_size, "block_size": self.block_size, "main_memory_size": self.main_memory_size}
            self.file_main_memory.save(self.main_memory)
    
    def specification(self):
        print()
        print("main memory size: {} word".format(self.main_memory_size))
        print("cache size: {} word".format(self.cache_size))
        print("block size: {} word".format(self.block_size))
        print("mapping technique: {}".format(self.mapping_technique))
        print()

    def visualize_cache(self):
        print()
        print("Cache content:")
        for address, block in self.cache_content.items():
            print(f"Block {address}: {block}")
        print()
    
    def visualize_main_memory(self):
        print()
        print("Main memory content:")
        for address, block in self.main_memory.items():
            print(f"Block {address}: {block}")
        print()

    def generate_random_word(self):
        return random.randint(0, self.main_memory_size)

    def check_word_in_cache(self, word):
        block_address = word // self.block_size
        if self.mapping_technique == "direct":
            if str(block_address) in self.cache_content.keys():
                print("Word found in cache. Cache hit.")
                return True
            else:
                print("Word not found in cache. Cache miss.")
                return False
        elif self.mapping_technique == "associative":
            if str(block_address) in self.cache_content.keys():
                print("Word found in cache. Cache hit.")
                return True
            else:
                print("Word not found in cache. Cache miss.")
                return False
        elif self.mapping_technique == "set-associative":
            set_index = math.floor(word % (self.cache_size / (self.block_size * 2)))
            for i in range(set_index * 2, set_index * 2 + 2):
                if i in self.cache_content and word in self.cache_content[i]:
                    print("Word found in cache. Cache hit.")
                    return True
            print("Word not found in cache. Cache miss.")
            return False
        else:
            print("Invalid mapping technique selected.")
            return False

    def bring_word_from_memory(self, word):
        block_address = str(word // self.block_size)
        if block_address in self.main_memory.keys():
            print(f"Word found in main memory. Bringing block {block_address} to cache.")
            return self.main_memory[block_address]
        else:
            print("Word not found in main memory.")
            return None

    def deliver_word_to_processor(self, word):
        block_address = word // self.block_size
        if self.check_word_in_cache(word):
            block_address = word // self.block_size
            print(f"Delivering word {word} from cache block {block_address} to processor.")
        else:
            block = self.bring_word_from_memory(word)
            if block is not None:
                if self.direct_cache_delete(word):
                    self.cache_content[block_address] = block
                elif len(self.cache_content) < (self.cache_size // self.block_size) + 1:
                    self.cache_content[block_address] = block
                else:
                    replacement_technique = repacemnt_memu()
                    content_dic = self.cache_content_dic()
                    if replacement_technique == "FIFO":
                        self.cache_content.pop(content_dic[min(content_dic)])
                        self.cache_content[block_address] = block
                    elif replacement_technique == "LIFO":
                        print(content_dic[max(content_dic)])
                        self.cache_content.pop(content_dic[max(content_dic)])
                        self.cache_content[block_address] = block
                    else:
                        print("Invalid replacement technique selected. or not listed in menu.")
                print(f"Delivering word {word} from main memory block {block_address} to processor.")
            else:
                print(f"Word {word} not found in main memory.")
        
        self.file_cache.save(self.cache_content)
        self.cache_content = self.file_cache.load()

    def fill_main_memory(self):
        if len(self.main_memory) == self.main_memory_size // self.block_size:
            print("Main memory already filled.")
            return
        block_number = self.main_memory_size // self.block_size

        for i in range(block_number):
            block = []
            for j in range(self.block_size):
                block.append(self.generate_random_word())
            self.main_memory[str(i)] = block
        self.file_main_memory.save(self.main_memory)
        self.main_memory = self.file_main_memory.load()
    
    def direct_cache_delete(self, word):
        if self.mapping_technique != "direct":
            return False
        block_address = word // self.block_size
        line_number = block_address % (self.cache_size // self.block_size)
        total_line = self.cache_size // self.block_size
        total_block = self.main_memory_size // self.block_size

        for i in range(line_number, total_block, total_line):
            if i is not block_address and str(i) in self.cache_content.keys():
                self.cache_content.pop(str(i))
                print(f"Block {i} deleted from cache.")
                return True
        return False

    def info_checker(self):
        infos = {"mapping_technique": self.mapping_technique, "cache_size": self.cache_size, "block_size": self.block_size, "main_memory_size": self.main_memory_size}
        try:
            result = all(infos[key] == self.cache_content["Info"][key] for key in infos)
            return result
        except KeyError:
            return False
    
    def print_word_content(self,word):
        for block in self.cache_content.values():
            if word in block:
                print(f"Word {word} found in cache block {self.cache_content.keys()}")
                return
        print(f"Word {word} not found in cache.")
    
    def cache_content_dic(self):
        temp = dict(self.cache_content)
        temp.pop("Info", None)
        return {count: key for count, key in enumerate(temp.keys())}


def menu():
    print("💾Welcome to the cache simulator!")
    print("Please select the mapping technique:")
    print("1. Direct mapping")
    print("2. Associative mapping")
    print("3. Set-associative mapping")
    mapping_technique = input("Your choice: ")
    if mapping_technique == "1":
        mapping_technique = "direct"
    elif mapping_technique == "2":
        mapping_technique = "associative"
    elif mapping_technique == "3":
        mapping_technique = "set-associative"
    else:
        print("Invalid choice. Exiting.")
        exit()

    cache_size = int(input("Please enter the cache size: "))
    block_size = int(input("Please enter the block size: "))
    main_memory_size = int(input("Please enter the main memory size: "))
    cache = Cache(mapping_technique, cache_size, block_size, main_memory_size)
    cache.fill_main_memory()
    cache.visualize_cache()
    cache.visualize_main_memory()

    while True:
        print()
        print("Please select an option:")
        print("1. Deliver word to processor")
        print("2. Visualize cache")
        print("3. Visualize main memory")
        print("4. Exit (Q/q/4)")
        choice = input("Your choice: ")
        if choice == "1":
            word = int(input("Please enter the word: "))
            cache.deliver_word_to_processor(word)
        elif choice == "2":
            cache.visualize_cache()
        elif choice == "3":
            cache.visualize_main_memory()
        elif choice == "Q" or choice == "q" or choice == "4":
            print("Exiting.☠")
            break

def repacemnt_memu():
    print("Please select the replacement technique:")
    print("1. FIFO")
    print("2. LIFO")
    replacement_technique = input("Your choice: ")
    if replacement_technique == "1":
        replacement_technique = "FIFO"
    elif replacement_technique == "2":
        replacement_technique = "LIFO"
    else:
        print("Invalid choice. Exiting.")
        return None
    return replacement_technique

if __name__ == "__main__":
    # Menu
    menu()
