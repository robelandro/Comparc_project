#!/usr/bin/python3
# A program that implements Cache mapping techniques:
# a. Direct Mapping
# b. Associative Mapping
# c. Set-Associative Mapping

import random
import sys

# Global variables
cache = []
main_memory = []
cache_size = 0
block_size = 0
cache_type = 0
replacement_type = 0
cache_hit = 0
cache_miss = 0

# Function to generate random words
def generate_random_words():
	global main_memory
	global cache_size
	global block_size
	main_memory = []
	for i in range(cache_size * block_size):
		main_memory.append(random.randint(0, 1000))

# Function to generate random cache
def generate_random_cache():
	global cache
	global cache_size
	global block_size
	global cache_type
	global replacement_type
	cache = []
	if cache_type == 1:
		for i in range(cache_size):
			cache.append([])
			for j in range(block_size):
				cache[i].append(random.randint(0, 1000))
	elif cache_type == 2:
		for i in range(cache_size):
			cache.append([])
			for j in range(block_size):
				cache[i].append(random.randint(0, 1000))
	elif cache_type == 3:
		for i in range(cache_size):
			cache.append([])
			for j in range(block_size):
				cache[i].append(random.randint(0, 1000))

# Function to display cache
def display_cache():
	global cache
	global cache_type
	global cache_size
	global block_size
	if cache_type == 1:
		print("Cache: ")
		for i in range(cache_size):
			print("Block " + str(i) + ": " + str(cache[i]))
	elif cache_type == 2:
		print("Cache: ")
		for i in range(cache_size):
			print("Block " + str(i) + ": " + str(cache[i]))
	elif cache_type == 3:
		print("Cache:")
		for i in range(cache_size):
			print("Set " + str(i) + ": " + str(cache[i]))

# Function to display main memory
def display_main_memory():
	global main_memory
	global cache_size
	global block_size
	print("Main memory: ")
	for i in range(cache_size * block_size):
		print("Block " + str(i) + ": " + str(main_memory[i]))

# Function to display cache hit and miss
def display_cache_hit_miss():
	global cache_hit
	global cache_miss
	print("Cache hit: " + str(cache_hit))
	print("Cache miss: " + str(cache_miss))

# Function to display cache hit ratio
def cache_maping(cache_type):
	global cache
	global main_memory
	global cache_size
	global block_size
	global replacement_type
	global cache_hit
	global cache_miss
	if cache_type == 1:
		for i in range(cache_size * block_size):
			if main_memory[i] in cache[i % cache_size]:
				cache_hit += 1
			else:
				cache_miss += 1
				cache[i % cache_size] = main_memory[i]
	elif cache_type == 2:
		for i in range(cache_size * block_size):
			if main_memory[i] in cache[i % cache_size]:
				cache_hit += 1
			else:
				cache_miss += 1
				cache[i % cache_size].append(main_memory[i])
				if len(cache[i % cache_size]) > block_size:
					cache[i % cache_size].pop(0)
	elif cache_type == 3:
		for i in range(cache_size * block_size):
			if main_memory[i] in cache[i % cache_size]:
				cache_hit += 1
			else:
				cache_miss += 1
				cache[i % cache_size].append(main_memory[i])


if __name__ == "__main__":

	# Get cache size
	cache_size = int(input("Enter cache size: "))

	# Get block size
	block_size = int(input("Enter block size: "))

	# Get cache type
	cache_type = int(input("Enter cache type: "))

	# Get replacement type
	replacement_type = int(input("Enter replacement type: "))

	# Generate random words
	generate_random_words()

	# Generate random cache
	generate_random_cache()

	# Display cache
	display_cache()

	# Display main memory
	display_main_memory()

	# Cache mapping
	cache_maping(cache_type)

	# Display cache hit and miss
	display_cache_hit_miss()
