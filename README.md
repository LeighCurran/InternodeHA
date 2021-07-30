[![buy me a coffee](https://img.shields.io/badge/If%20you%20like%20it-Buy%20us%20a%20coffee-green.svg?style=for-the-badge)](https://www.buymeacoffee.com/leighcurran)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
![Maintenance](https://img.shields.io/maintenance/yes/2021.svg?style=for-the-badge)

# Internode for Home Assistant

The Internode integration adds support for retriving data from the Internode API such as:

- internode_history - This is todays usage
- internode_usage - This is the total cumulative usage for the month

Note: To use the internode integration you need a valid account with Internode.

## Configuration
Using *YAML*: add `internode` platform to your sensor configuration in `configuration.yaml`. Example:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: internode
    name: "Internet Usage"
    username: username
    password: Password
    scan_interval:
      hours: 2
```
Note: Name ans scan_interval are optional. If scan_interval is not set a default value of 1 hours will be used. do not include @internode.on.net to your username.

