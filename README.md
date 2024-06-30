# Ansible playbook for UT2004 dedicated server

This playbook and roles configure a Linux machine with an instance of the Unreal Tournament 2004 dedicated server. These are the rough steps that will be taken:

- prepare the system with common settings;
- configure firewall rules via UFW;
- install required dependencies;
- download and install the UT2004 server via [LinuxGSM](https://linuxgsm.com/);
- copy a custom `ut2k4server.ini` configuration file;
- copy some extra custom game data;
- configure the No-IP dynamic DNS service;
- enable some hardening options.

## Instructions

1. Create the virtual machine with your cloud provider. Note down the public IP and access credentials.
    - An SSH key is required.
    - The default username for Ubuntu server 24.04 is `ubuntu`.
2. If you want a dynamic domain name, create an account on www.noip.com, then create a DNS record and a DDNS key.
    - Otherwise, use `--skip-tags=dyn_dns` later.
3. Modify `hosts.yml` with the parameters of your target host.
4. Modify `secrets.yml` with your desired configuration.
5. Run `ansible-playbook ut2004.yml`.
    - Optionally, use `-vv` for verbose output.
    - Optionally, use `--tags=...` or `--skip-tags=...` to select or exclude steps.

## Notes and tips

- The playbook will change the OpenSSH listen port to a custom one (see `secrets.yml`). This is not a sufficient security measure on its own, but can reduce bruteforce attempts and log spam. Use `ssh -p <port>` to connect to the machine after this playbook has run.
- Use `ansible-playbook ut2004.yml --list-tasks`: it's a very useful tree view of all the tasks that will be run.
- To manually update the dynamic DNS: `~/noip/noip-duc -g <domain> -u <username> -p <password> -v --once`
- unrealwiki.org has a lot of useful documentation, including [a wiki](https://wiki.unrealadmin.org/Main_Page) and [a reference for ut2k4server.ini](https://unrealadmin.org/server_ini_reference/ut2004)
- Digital Ocean has [an Ansible cheat sheet](https://www.digitalocean.com/community/cheatsheets/how-to-use-ansible-cheat-sheet-guide)


## Missing features

- skip download and install ut2004 and linuxgsm if already installed
- why fwupd service shows as always changed?
- have a task dedicated to upgrading system packages, and modify role ubuntu to only upgrade packages when requested explicitly. Also upgrade linuxgsm and noip-duc.
- Run ut2k4 server as a service on bootup? (https://docs.linuxgsm.com/configuration/running-on-boot)
- fail2ban + ssh jail = block ssh spam
- fail2ban + reverse proxy + nginx jail = blocks password brute-force guessing on web admin
- monitor, summarize, alert unauthorized access attempts
- add cron job for "./ut2k4server monitor" (to encourage support & development of linuxgsm)
- enable AWS EC2 Connect (in case SSH breaks)
