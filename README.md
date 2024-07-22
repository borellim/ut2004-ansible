# Ansible playbook for UT2004 dedicated server

This playbook / role configures a Linux machine with an instance of the Unreal Tournament 2004 dedicated server. These are the rough steps that it takes:

- prepare the system with common settings;
- configure firewall rules via UFW;
- install required dependencies;
- download and install the UT2004 server via [LinuxGSM](https://linuxgsm.com/);
- copy a custom `ut2k4server.ini` configuration file;
- install cron jobs start the game at boot, and to monitor/restart the game on crash;
- copy some extra custom game data;
- configure the No-IP dynamic DNS service;
- install and configure Nginx as reverse proxy for the UT2004 web admin interface;
- install fail2ban and have it monitor Nginx logs for brute-force attempts;
- enable some SSH hardening options;
- start the game server process.


## Instructions

1. Create the virtual machine with your cloud provider. Note down the public IP and access credentials.
    - An SSH key is required.
    - The default username for Ubuntu server 24.04 is `ubuntu`.
2. If you want a dynamic domain name, create an account on www.noip.com, then create a DNS record and a DDNS key.
    - Otherwise, use `--skip-tags=dyn_dns` later.
3. Modify `hosts.yml` with the parameters of your target host.
4. Modify `secrets.yml` with your desired configuration.
5. Run `ansible-playbook ut2004.yml`. Some useful options:
    - `-vv` for verbose output;
    - `--tags=...` or `--skip-tags=...` to select or exclude steps;
    - `--list-tasks` to list every task that will be run.


## Notes and tips

- The playbook will change the OpenSSH listen port to a custom one (see `secrets.yml`). This is not a sufficient security measure on its own, but can reduce bruteforce attempts and log spam. Use `ssh -p <port>` or `scp -P <port>` to connect to the machine after this playbook has run.
- To manually update the dynamic DNS: `~/noip/noip-duc -g <domain> -u <username> -p <password> -v --once`
- unrealwiki.org has a lot of useful documentation, including [a wiki](https://wiki.unrealadmin.org/Main_Page) and [a reference for ut2k4server.ini](https://unrealadmin.org/server_ini_reference/ut2004)
- Digital Ocean has [an Ansible cheat sheet](https://www.digitalocean.com/community/cheatsheets/how-to-use-ansible-cheat-sheet-guide)
- [See below](#operation) for some useful operative commands

## Operation

### Starting & stopping

The game server will start at boot. To start/stop manually:
```
sudo su - ut2004
./ut2k4server start
./ut2k4server stop
./ut2k4server details
```

### Checking game console

```
./ut2k4server console
# To quit, press "CTRL+b" then "d", NOT "CTRL-C"!
```

### CPU/network usage

```
bashtop
s-tui
```

### Game settings and LinuxGSM settings

Most settings are stored in `~ut2004/serverfiles/System/ut2k4server.ini`. Some settings are passed via command-line arguments, which are stored in `~ut2004/lgsm/config-lgsm/common.cfg`. Files in these folder also contain settings for LinuxGSM, such as monitor settings.

### Logs

LinuxGSM cron jobs:

```
sudo cat ~ut2004/cron.log
sudo tail -f ~ut2004/cron.log
sudo less [-R|-r] ~ut2004/cron.log
```

Fail2ban:

```
sudo systemctl status fail2ban
sudo fail2ban-client status
sudo fail2ban-client status ut2004-webadmin
grep "Ban" /var/log/fail2ban.log
```

Nginx:

```
less /var/log/nginx/access.log
egrep -v "ServerAdmin" /var/log/nginx/access.log
```

SSH server (note that it uses socket-based activation):

```
journalctl -t sshd -f
journalctl -u ssh
```


## Missing features

- skip download and install ut2004 and linuxgsm if already installed
- why fwupd service shows as always changed?
- have a cron job to install security updates daily, but also pin sensitive packages to a specific version.
- have a task dedicated to upgrading system packages, and modify role ubuntu to only upgrade packages when requested explicitly. Also upgrade linuxgsm and noip-duc.
- fail2ban + ssh jail = block ssh spam
- enable AWS EC2 Connect (in case SSH breaks)
- monitor, summarize, alert unauthorized access attempts
- close port 8075 on UFW (we already proxy it on port 80), but only if nginx is configured.
