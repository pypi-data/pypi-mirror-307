# Beget DNS Authenticator plugin for Certbot

---

## Credentials

```ini
# Beget API token used by Certbot
dns_beget_username = username
dns_beget_password = password 
```

## Examples

```bash
certbot certonly --authenticator beget-plugin \
    --beget-plugin-credentials ~/.secrets/certbot/beget.ini \
    -d domain.com -d *.domain.com
```

```bash
certbot certonly --authenticator beget-plugin \
    --beget-plugin-credentials ~/.secrets/certbot/beget.ini \
    -d xxx.yyy.domain.com -d *.yyy.domain.com
```
