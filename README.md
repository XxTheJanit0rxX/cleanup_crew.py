# Cleanup_Crew.py V2

Cleanup_Crew.py is a versatile Python script designed to enhance the stealth and efficiency of penetration testing tasks. By dynamically managing user agent strings and providing a streamlined interface for running various enumeration tools, Cleanup_Crew.py aims to reduce the likelihood of detection during security assessments.

## Features

- **Dynamic User Agent Management**: Leverages the `fake-useragent` library to generate random user agent strings, minimizing detection risks associated with static user agent patterns.
- **Fallback User Agent List**: Ensures continued functionality by defaulting to a predefined list of user agents if `fake-useragent` is unavailable due to network issues.
- **Simplified Tool Invocation**: Simplifies the process of running popular security tools with custom user agent strings, including `nmap`, `curl`, `wget`, and more.
- **Advanced Enumeration with Autorecon**: Integrates the powerful `autorecon` tool to conduct thorough enumeration of targets, installing necessary dependencies on the fly.
- **Error Handling and Resilience**: Implements robust error handling mechanisms to improve reliability and user experience.

## Installation

Ensure you have Python 3 installed on your system. Clone the repository or download the script directly:

```
git clone https://github.com/XxTheJanit0rxX/cleanup_crew.py.git
```

Dependencies are managed automatically by the script. However, you may need to install `fake-useragent` manually:

```
pip install fake-useragent
```

## Usage

To use Cleanup_Crew.py, simply run the script from the command line with the desired tool and target:

```
python3 cleanup_crew.py <command> <target>
```

For example, to enumerate a target using `autorecon`:

```
python3 cleanup_crew.py enum example.com
```

Supported commands include `enum` for enumeration and tool names such as `nmap`, `curl`, `wget`, etc., for specific tool execution with a randomized user agent.

## Supported Tools

- `nmap`
- `curl`
- `wget`
- `sqlmap`
- `ffuf`
- `feroxbuster`
- `nikto`
- `gobuster`
- Additional tools can be easily added to the script as needed.

## Contributing

Contributions to Cleanup_Crew.py are welcome! Whether it's adding new features, improving existing functionality, or reporting bugs, feel free to open an issue or submit a pull request.

## License

Cleanup_Crew.py is released under [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the license.

## Disclaimer

Cleanup_Crew.py is developed for educational and ethical penetration testing purposes only. Users are responsible for adhering to applicable laws and obtaining proper permissions before performing security assessments.
