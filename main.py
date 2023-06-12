import random


# Function for reading input file
def read_file(filename):
    f1 = open(filename)
    my_line = f1.readline().strip()
    list1 = []
    while my_line:
        list1.append(my_line)
        my_line = f1.readline().rstrip()
    f1.close()
    return list1


# Input for Cache Size, Block Size, Associativity
cache_size = input("Enter the size of the cache in KB(only the number): ")
cache_size = int(cache_size)
block_size = input("Enter the cache block size : ")
block_size = int(block_size)
way_associative = input("Enter the value of associativity : ")
way_associative = int(way_associative)

# Reading addresses and storing it in a list
address_list = read_file('inst_addr_trace_hex_project_1.txt')

# Initializing variables for Cache Hit and Cache Miss
cache_hit = False
hit_count = 0
miss_count = 0


# Function for calculating power of 2
def calculate_power(x):
    if x == 1:
        return x
    else:
        calculate_power.power_count += 1
        q = x / 2
        calculate_power(q)
    return calculate_power.power_count


# Function for building cache
def build_cache(way):
    sample_list = []
    for j in range(0, total_blocks_in_each_set):
        sample_list.append({"valid": 0, "data": [], "tag": "0", "set": j, "way": way})
    return sample_list


# Function for reading cache
def cache_read(hex_address):
    # Initializing Cache Parameters
    global cache_hit, hit_count, miss_count
    valid_flag = -1

    # Getting binary address from hex_address
    dec_address = int(hex_address, 16)
    bin_address = bin(dec_address)
    bit32_binary = bin_address[2:].zfill(32)

    # Retrieving Tag Bits from Binary Address
    tag = bit32_binary[0:tag_bits]
    print(f"Tag bits = {tag}")

    # Retrieving Set Bits from Binary Address
    _set = bit32_binary[tag_bits:(tag_bits + set_bits)]
    print(f"Set bits = {_set}")
    set_no = int(_set, 2)

    # Retrieving Offset from Binary Address
    offset = bit32_binary[(tag_bits + set_bits):]
    print(f"Block Offset = {offset}")
    offset_int = int(offset, 2)

    # Looping over total number of ways to match data in the cache and main memory
    for _way in range(way_associative):
        # If valid bit for given way and set is 0, it is a cache miss
        if cache_list[_way][set_no]["valid"] == 0:
            cache_hit = False
            valid_flag = _way

            # If valid bit for given way and set is 1 and tag bit is same as retrieved tag, it is a cache hit
        elif cache_list[_way][set_no]["valid"] == 1 and cache_list[_way][set_no]["tag"] == tag:
            cache_hit = True
            break

            # If valid bit for given way and set is 1 and tag bit is different, it is a cache conflict and thus a cache miss
        elif cache_list[_way][set_no]["valid"] == 1 and cache_list[_way][set_no]["tag"] != tag:
            cache_hit = False

        else:
            pass

            # If it is a cache hit, it increases the hit count and returning data as a variable "final"
    if cache_hit:
        hit_count = hit_count + 1
        final = list(cache_list[_way][set_no]["data"][offset_int:(offset_int + 2)])
        print(f"Cache Data in set {set_no} is {cache_list[_way][set_no]['data']}")
        print("Cache hit")
        return final

        # If it is a cache miss, it is retrieving data from a main memory and stores in the cache for given way and set
    # It is also increasing miss count and returns the retrieved data as a variable "final"
    elif not cache_hit:
        mm_block_offset = (dec_address // block_size) * block_size
        cache_data = []
        for data in RAM_list[mm_block_offset:mm_block_offset + block_size]:
            cache_data.append(data)

            # In case of a Cache Conflict
        if valid_flag != -1:
            valid_way = valid_flag
            cache_list[valid_way][set_no]["data"] = hex_address
            final = list(cache_list[valid_way][set_no]["data"][offset_int:(offset_int + 2)])
            cache_list[valid_way][set_no]["valid"] = 1
            cache_list[valid_way][set_no]["tag"] = tag
            print(f"Cache Data in set {set_no} is {cache_list[valid_way][set_no]['data']}")
            print("Cache Missed, Data pushed to the cache line having valid bit 0")

            # In case of a Cache Miss
        elif valid_flag == -1:
            random_way_select = random.randrange(way_associative)
            cache_list[random_way_select][set_no]["data"] = cache_data
            final = list(cache_list[random_way_select][set_no]["data"][offset_int:(offset_int + 2)])
            cache_list[random_way_select][set_no]["valid"] = 1
            cache_list[random_way_select][set_no]["tag"] = tag
            print(f"Cache Data in set {set_no} is {cache_list[random_way_select][set_no]['data']}")
            print("Cache Missed, Data pushed to the cache with valid bit 1 and tag mismatch.")
        miss_count = miss_count + 1
        return final

    else:
        pass


RAM_list = []

# Calculating bits for Cache Block from Block Size
calculate_power.power_count = 0
cache_block_power = calculate_power(block_size)
print(f"Cache block size power 2 = {cache_block_power}")

# Calculating bits for Block Offset
block_offset_bits = cache_block_power
print(f"Block offset bits = {block_offset_bits}")

# Set bits = Cache Size / (Associativity * Block Size)
# Calculating bits for Set from given Cache Size, Associativity and Block Size
calculate_power.power_count = 0
associativity = calculate_power(way_associative)
calculate_power.power_count = 0
set_bits = (10 + calculate_power(cache_size)) - associativity - cache_block_power
print(f"Set bits = {set_bits}")

# Calculating bits for Tag
tag_bits = 32 - (block_offset_bits + set_bits + 2)
print(f"Tag bits = {tag_bits}")

# Calculating total blocks
total_blocks_in_each_set = 2 ** set_bits
print(f"total blocks in caches = {total_blocks_in_each_set}")
print()

# Building Cache as per associativity
cache_list = [[]] * way_associative
for i in range(0, way_associative):
    cache_list[i] = build_cache(i)

# Looping over test addresses to read cache
for i in range(0, len(address_list)):
    final_data = []
    data_read = cache_read(address_list[i])
    final_data = data_read

# Getting Total Cache Access count and Miss Ratio
total_cache_access = hit_count + miss_count
miss_ratio = miss_count / total_cache_access

print()
print("-------------------------------------------------------------------------------")
print()
print(f"Total cache access = {total_cache_access}")
print(f"Total Hit count = {hit_count}")
print(f"Total Miss count = {miss_count}")
print(f"Miss ratio = {miss_ratio}")
