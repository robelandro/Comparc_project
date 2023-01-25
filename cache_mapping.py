#!/usr/bin/python3 
import random, json, os


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
    def __init__(self, mapping_technique, cache_size, block_size, main_memory_size=32, number_of_set=None):
        self.mapping_technique = mapping_technique
        self.cache_size = cache_size
        self.block_size = block_size
        self.main_memory_size = main_memory_size
        self.number_of_set = number_of_set
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
            self.cache_content["Info"] = {"mapping_technique": self.mapping_technique, "cache_size": self.cache_size, "block_size": self.block_size, "main_memory_size": self.main_memory_size, "set": self.number_of_set}
            self.file_cache.save(self.cache_content)
            self.main_memory["Info"] = {"mapping_technique": self.mapping_technique, "cache_size": self.cache_size, "block_size": self.block_size, "main_memory_size": self.main_memory_size, "set": self.number_of_set}
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
        for set_key, cache_list in self.cache_content.items():
            if set_key != "Info":
                for cache_tag, block_list  in cache_list.items():
                    print(f"Set {set_key}, Cache {cache_tag}: {block_list}")
        print()
    
    def visualize_main_memory(self):
        print()
        print("Main memory content:")
        for block_tag, block in self.main_memory.items():
            if block_tag != "Info":
                print(f"Block {block_tag}: {block}")
        print()

    def generate_random_word(self):
        return random.randint(0, self.main_memory_size)

    def check_word_in_cache(self, word):
        block_tag = word // self.block_size
        for set_key, cache_list in self.cache_content.items():
            if set_key != "Info":
                for cache_tag, block_list in cache_list.items():
                    if str(block_tag) == str(block_list[0]):
                        print(f"Word {word} found in cache block {block_tag}. cache hit.")
                        return True
        print(f"Word {word} not found in cache. cache miss.")
        return False

    def bring_word_from_memory(self, word):
        block_tag = str(word // self.block_size)
        if block_tag in self.main_memory.keys():
            print(f"Word found in main memory. Bringing block {block_tag} to cache.")
            return self.main_memory[block_tag]
        else:
            print("Word not found in main memory.")
            return None

    def deliver_word_to_processor(self, word):
        block_tag = word // self.block_size
        total_line = self.cache_size // self.block_size
        if self.check_word_in_cache(word):
            block_tag = word // self.block_size
            print(f"Delivering word {word} from cache block {block_tag} to processor.")
        else:
            block = self.bring_word_from_memory(word)
            if block is not None:
                if self.mapping_technique == "direct":
                    self.direct_mode(block_tag, block, total_line)
                elif self.mapping_technique == "associative":
                    self.associative_mode(block_tag, block, total_line)
                elif self.mapping_technique == "set-associative":
                    self.set_associative_mode(block_tag, block, total_line)
                print(f"Delivering word {word} from main memory block {block_tag} to processor.")
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
    
    def fill_cache(self):
        total_line = self.cache_size // self.block_size
        number_mult = total_line // self.number_of_set
        for i in range(self.number_of_set):
            self.cache_content[i] = {}
            for j in range(number_mult):
                self.cache_content[i][str(i * number_mult + j)] = ["free"]
        self.file_cache.save(self.cache_content)
        self.cache_content = self.file_cache.load()

    def info_checker(self):
        infos = {"mapping_technique": self.mapping_technique, "cache_size": self.cache_size, "block_size": self.block_size, "main_memory_size": self.main_memory_size, "set": self.number_of_set}
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
    
    # def cache_content_dic(self):
    #     temp = dict(self.cache_content)
    #     temp.pop("Info", None)
    #     return {count: key for count, key in enumerate(temp.keys())}

    def direct_mode(self, block_tag, block, total_line):
        cache_number = block_tag % total_line
        if self.cache_content[str(0)][str(cache_number)][0] == "free":
            self.cache_content[str(0)][str(cache_number)] = [block_tag, block]
        else:
            self.cache_content[str(0)][str(cache_number)].clear()
            self.cache_content[str(0)][str(cache_number)].append(block_tag)
            self.cache_content[str(0)][str(cache_number)].append(block)
        
    def associative_mode(self, block_tag, block, total_line):
        cache_number = block_tag % total_line
        number_mult = total_line // self.number_of_set
        # define range where is set_key will be valid
        start_cache = 0 * number_mult
        end_cache = start_cache + number_mult - 1
        for i in range(start_cache, end_cache + 1):
            if self.cache_content[str(0)][str(i)][0] == 'free':
                self.cache_content[str(0)][str(i)].clear()
                self.cache_content[str(0)][str(i)].append(block_tag)
                self.cache_content[str(0)][str(i)].append(block)
                return
        self.replacmnet(block_tag, block, start_cache, end_cache)

    def set_associative_mode(self, block_tag, block, total_line):
        # getting where is the key
        set_key = block_tag % (self.number_of_set)
        number_mult = total_line // self.number_of_set
        # define range where is set_key will be valid
        start_cache = set_key * number_mult
        end_cache = start_cache + number_mult - 1

        # Assosiation implement
        for i in range(start_cache, end_cache + 1):
            if self.cache_content[str(set_key)][str(i)][0] == 'free':
                self.cache_content[str(set_key)][str(i)].clear()
                self.cache_content[str(set_key)][str(i)].append(block_tag)
                self.cache_content[str(set_key)][str(i)].append(block)
                return
        self.replacmnet(block_tag, block, start_cache, end_cache, set_key)

    def replacmnet(self, block_tag, block, start_cache, end_cache, set_key=0):
        replacement_technique = repacemnt_memu()
        if replacement_technique == "FIFO":
            for i in range(start_cache, end_cache + 1):
                if end_cache == i:
                    self.cache_content[str(set_key)][str(end_cache)].clear()
                    self.cache_content[str(set_key)][str(end_cache)] =[block_tag, block]
                else:
                    self.cache_content[str(set_key)][str(i)].clear()
                    self.cache_content[str(set_key)][str(i)].append(self.cache_content[str(set_key)][str(i + 1)][0])
                    self.cache_content[str(set_key)][str(i)].append(self.cache_content[str(set_key)][str(i + 1)][1])
        elif replacement_technique == "LIFO":
            self.cache_content[str(set_key)][str(end_cache)].clear()
            self.cache_content[str(set_key)][str(end_cache)] = [block_tag, block]
        else:
            print("Invalid replacement technique selected. or not listed in menu.")

    def sort_by_key(self):
        info = self.cache_content.pop("Info", None) # remove the "Info" key and store it in a separate variable
        sorted_temp = dict(sorted(self.cache_content.items(), key=lambda x: int(x[0]))) # sort by numerical keys
        self.cache_content.clear()
        self.cache_content["Info"] = info  # add "Info" back in as the first key
        self.cache_content.update(sorted_temp)  # add the sorted keys back in
        


def menu():
    print("💾Welcome to the cache simulator!")
    print("Please select the mapping technique:")
    print("1. Direct mapping")
    print("2. Associative mapping")
    print("3. Set-associative mapping")
    print("L. For load from pervious")
    mapping_technique = input("Your choice: ")
    if mapping_technique == "1":
        mapping_technique = "direct"
        cache = inputer(mapping_technique, 1)
    elif mapping_technique == "2":
        mapping_technique = "associative"
        cache = inputer(mapping_technique, 1)
    elif mapping_technique == "3":
        mapping_technique = "set-associative"
        number_of_set = int(input("Enter Number of Set: "))
        cache = inputer(mapping_technique, number_of_set)
    elif mapping_technique == "L" or mapping_technique == "l":
        loader = Store_Jason("main_memory.json")
        MM_load = loader.load()
        try:
            cache = Cache(MM_load["Info"]["mapping_technique"], 
            int(MM_load["Info"]["cache_size"]), 
            int(MM_load["Info"]["block_size"]), 
            int(MM_load["Info"]["main_memory_size"]), 
            int(MM_load["Info"]["set"]))
        except KeyError:
            print("No previous data found.")
            exit()
    else:
        print("Invalid choice. Exiting.")
        exit()

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

def inputer(mapping_technique, number_of_set=None):
    cache_size = int(input("Please enter the cache size: "))
    block_size = int(input("Please enter the block size: "))
    main_memory_size = int(input("Please enter the main memory size: "))
    cache = Cache(mapping_technique, cache_size, block_size, main_memory_size, number_of_set)
    cache.fill_main_memory()
    cache.fill_cache()
    cache.visualize_cache()
    cache.visualize_main_memory()
    return cache

if __name__ == "__main__":
    # Menu
    menu()
