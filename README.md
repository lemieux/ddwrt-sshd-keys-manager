# DD-WRT SSHD Authorized Keys Manager

[Gregory A. Lussier](https://gregoryalussier.com)

## Introduction

I needed a simple script to update DD-WRT's SSHD Authorized Keys on multiple devices. I am releasing this draft version but will be updating the code structure and scalability.

## How does it work?

### Files

* manager.py: the script itself
* data.json: contains public keys along with information about the user associated to each key

### Algorithm

1. Connect via SSH and execute ``` nvram get sshd_authorized_keys ```
2. Get the current authorized keys from the nvram and store them as an array
3. Build a suitable string (ssh-rsa public key file) from ``` data.json ```
4. Write the string to a text file
5. Upload the text file to the DD-WRT device
6. Remote execute a command on the DD-WRT device to add each public key to its nvram
7. Commit the nvram changes