# Get IP and record type for domain
import requests
import dns.resolver

def check_ip_addresses(domain):

    ip_addresses = ''

    try:
        answers = dns.resolver.resolve(domain)
        for answer in answers:
            ip_addresses += answer.address + ","

        # Remove the trailing comma
        ip_addresses = ip_addresses.rstrip(',')

    except dns.exception.DNSException:
        print(f"Could not resolve DNS information for {domain}")

    return ip_addresses