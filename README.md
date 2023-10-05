# rekon
`rekon` is an attack surface managent tool that helps to collect basic pubically visible asset information though DNS enumeration and a variety of passive probes. This tool is meant to be able to build an asset inventory from a top-level domain (e.g. acme.com) using free and open source solutions. For an example of the output please see the [example_output](./example_output/) folder in this repository.
 
`rekon` uses a combination of active and passive techinques to gather information. You should only run this tool against sites for which you have permission to run an active scan.

`rekon` is tested against Pyton 3.11.5 on OS X, but is should run anywhere.

# Installation

1. Clone or download this repo:
    
    `git clone https://github.com/yourusername/rekon.git`

1. Navigate to the root of the repo:

    `cd rekon`

1. Install Dependencies

    `pip3 install -r requirements.txt`

# Configuration

Rekon uses a configuration file (rekon-config.json) to specify the scanning parameters and options. You can customize this configuration to meet your needs. Here's how you can configure it:

1. Open `rekon-config.json`
1. Modify the  configuraiton parameters. Explanations are provided in the the sample config file:

```
{
    "root_urls": [      -- Add in a list of domains you want to build a DNS enumeration for.
        "example.com",
        "sample.com"
    ],
    "max_dns_records": 10,  -- This is the max number or records to fetch and scan for each root url. Some sites can have hundreds of records, so start small
    "run_firewall_scan": true, -- Runs the wafw00f tool to figure out what firewall is running
    "run_ip_scan": true, -- Provide a list of associated IP addresses
    "http_status_scan": true, -- Return the HTTP status of the domain
    "sec_headers_scan": true, -- Look for specific missing security headers
    "take_screenshot": true, -- use selenium to snag a screeshot of a valid domain
}
```

# Running rekon

_Running the script over VPN is recommended_.

1. Open a terminal to the root of the /rekon repository.

    `cd path/to/rekon`

1. Run rekon

    `python3 rekon.py`

# Viewing the results

Once Rekon has completed scanning, it will generate a CSV file containing the scan results. The CSV file will be named scan_results_<date>.csv, where <date> is the current date in the "YYYYMMDD" format.

You can open the CSV file with a spreadsheet application or text editor to view the scan results.

# Other reconnisance references

Here are some other references that may be helpful to see how other approach this kind of attack surface reconnisance. 

## How to blogs

* [How to: Recon and Content Discovery](https://www.hackerone.com/ethical-hacker/how-recon-and-content-discovery) - HackerOne


## Useful free browser-based reconnaissance tools

* [crt.sh](https://crt.sh/) -  Certification search, providing DNS enumeration.
* [DNS dumpster](https://dnsdumpster.com/) - Domain research tool with very robust data sets.
* [Shodan.io](https://www.shodan.io/) - Global search engine for internet connected devices.

## Commercial ASM Tools

* [Security Trails](https://securitytrails.com/) - Building DNS and IP realted inventories and monitoring.
* [HackerOne Attack Surface Reviuew](https://www.hackerone.com/attack-surface-review)
* [Security Scorecard](https://securityscorecard.com/solutions/enterprise-risk-management/)

# Open source tools

* [subfinder](https://github.com/projectdiscovery/subfinder) - subdomain discovery tool.
* [sunlist3r](https://github.com/aboul3la/Sublist3r) - DNS enumeration tool
* [wafw00f](https://github.com/EnableSecurity/wafw00f) - Firewall fingerprinting tool.
* [assetfinder](https://github.com/tomnomnom/assetfinder)
* [OWASP Amass](https://github.com/owasp-amass/amass) - Attack surface network mapping.
* [Attack Surface Mapper](https://github.com/superhedgy/AttackSurfaceMapper) - Requires API keys for multiple integrations

[Here's a good blog article](https://blog.yeswehack.com/yeswerhackers/subdomains-tools-review-full-detailed-comparison/) by [Siz2dez](https://twitter.com/Six2dez1) that provides a more comprehensive list of subdomain tools.