# How to verify signed packages

### Download the packages and signatures

Download the leetscraper packages and the signature files from [pypi.org](https://pypi.org/project/leetscraper/#files) or from the [dist folder](https://github.com/Pavocracy/leetscraper/tree/main/dist) in this repo. You could also use curl with the copied url from either source. 
example: `curl https://copy-pasted-url-to/leetscraper-x.x.x.tar.gz -o leetscraper-x.x.x.tar.gz` 

*note: the signature files dont show in the pypi files page, but they are there. add .asc to the end of the download link to get the signatures*

### Use gpg to verify the signature

Use gpg to verify the packages are signed by [this key](https://github.com/Pavocracy/leetscraper/blob/main/.github/workflows/build-and-publish.yml#L49)  
`gpg --verify leetscraper-x.x.x.tar.gz.asc leetscraper-x.x.x.tar.gz`

### Trust this key if you wish

If you wish to trust this key, you can find the [public key here](https://github.com/Pavocracy/Pavocracy/blob/main/pavocracy.pub) or download it with gpg.  

If you downloaded the public key from my github, import it using:  
`gpg --import path/to/pavocracy.pub`

Otherwise you can get it with gpg using:  
`gpg --recv-keys 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6`

*note: make sure this is the same key as what is used to sign the packages*

Set the trust level using:  
`gpg --edit-key Pavocracy`  
`trust`

***NEVER TRUST KEYS YOU ARE NOT CONFIDENT IN. ALWAYS SET APPROPRIATE TRUST LEVELS***
