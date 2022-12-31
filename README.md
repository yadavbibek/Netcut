# Netcut
Disconnect user from wifi( doesn't require wifi password or Connected status to wifi)
This is a script that performs a type of attack known as ARP spoofing. ARP (Address Resolution Protocol) is used to map the IP addresses of devices on a network to their corresponding MAC (Media Access Control) addresses, which are used to physically identify the devices on the network.

In this script, the spoffer function sends fake ARP packets to a target device and a router on the same network. The fake packets contain the attacker's IP and MAC address as the source, and the target's IP and router's IP as the destination. This causes the target and router to update their ARP tables with the attacker's MAC address as the one associated with the target's IP and router's IP, respectively. As a result, the attacker is able to intercept and potentially modify traffic between the target and the router.

The trap_data_in_queue function sets up a netfilter queue, which is a mechanism for intercepting and processing packets traversing the network stack in the Linux kernel. It uses the iptables command to redirect all packets traversing the FORWARD chain (packets going from one device to another on the same network) to the queue. The execute_packet function is then called for each packet in the queue, which simply prints the packet and drops it.

The script also includes a restore function that sends ARP packets to restore the original mapping of IP to MAC addresses in the target's and router's ARP tables. This function is called when the script is interrupted by the user pressing Ctrl+C. The get_mac function is used to obtain the MAC addresses of devices on the network based on their IP addresses.

It's worth noting that ARP spoofing is a type of man-in-the-middle attack, and it can be used for malicious purposes such as intercepting sensitive information or injecting malicious content into the traffic between the target and the router. It's important to secure your network and devices against such attacks.
