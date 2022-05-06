# How to verify signed packages

### Download packages from pypi

Download the leetscraper packages and the signature files from [pypi.org](https://pypi.org/project/leetscraper/#files) or use curl with the copied url. 
example: `curl https://copy-pasted-url-to/leetscraper-x.x.x.tar.gz -o leetscraper-x.x.x.tar.gz` 

### Use gpg to verify the signature

Use gpg to verify the packages are signed by [this key](https://github.com/Pavocracy/leetscraper/blob/main/src/leetscraper/leetscraper.py#L2)  
`gpg --verify leetscraper-x.x.x.tar.gz.asc leetscraper-x.x.x.tar.gz`

### Trust this key if you wish

If you wish to trust this key, you can find the [public key here](https://github.com/Pavocracy/Pavocracy/blob/main/pavocracy.pub) or download it with gpg.  

If you downloaded the public key, import it using:  
`gpg --import pavocracy.pub`

Otherwise you can get it with gpg using:  
`gpg --recv-keys 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6`

Set the trust level using:  
`gpg --edit-key Pavocracy`  
`trust`

***NEVER TRUST KEYS YOU ARE NOT CONFIDENT IN. ALWAYS SET APPROPRIATE TRUST LEVELS***
