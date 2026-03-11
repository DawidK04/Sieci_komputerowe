ip_value = "12.34.56.78/28"
ip_parts = ip_value.split("/")
ip_addr_str = ip_parts[0].split(".")
int(ip_parts[1])

ip = (int(ip_addr_str[0]) << 24) | (int(ip_addr_str[1]) << 16) | (int(ip_addr_str[2]) << 8) | int(ip_addr_str[3])

mask = int("1" * int(ip_parts[1]) + "0" * (32 -int(ip_parts[1])), 2)

s_ip = ip & mask

r_ip = s_ip | (~mask) 

host_num = max(0, (2 ** (32 - int(ip_parts[1]))) - 2)

first_host_ip = s_ip + 1

last_host_ip = r_ip - 1

def format_ip(ip_int):
    c1 = (ip_int >> 24) 
    c2 = (ip_int >> 16) & 0xFF
    c3 = (ip_int >> 8)  & 0xFF
    c4 = ip_int  & 0xFF

    decimal = f"{c1}.{c2}.{c3}.{c4}"
    binary = f"{c1:08b}.{c2:08b}.{c3:08b}.{c4:08b}"
    return f"{decimal} {binary}"

print(ip_value)
print(format_ip(mask))
print(host_num)
print(format_ip(first_host_ip))
print(format_ip(last_host_ip))
print(format_ip(r_ip))
