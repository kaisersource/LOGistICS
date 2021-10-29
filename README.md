Build LOGistICS container inside the dir by using:
docker build -t logistics .

Execute in interactive mode in order to enable GUI 
docker run -it -p 102:102 -p 502:502 logistics

In order to cetach the container and avoid its suicide do:
ctrl+p, then ctrl+q 


### v0.1.1
- [x] Merging honeypot setup with a shell script
- [ ] Upload updated version of pyshark-based capture script
- [ ] Check and report deployment differences between Zeek v3 and v4 (Otherwise Security Onion distro is adviced)
- [ ] Docker compose to start all the services, then make the honeypot container a dependency of the capture container 

### v.0.1.0

- [x] S7comm honeypot
- [x] Modbus honeypot 
- [x] tshark replaces pyshark-based capture script  
- [x] S7comm gui template
- [x] Modbus gui template
- [ ] Upload Data Analysis Notebooks & ML trials

If you use *LOGistICS* in a scientific publication, we would appreciate citations using this **BibTex** entry:
``` tex
inproceedings{LOGistICS,
author = {Bistarelli, Stefano and Bosimini, Emanuele and Santini, Francesco},
title = {A Medium-Interaction Emulation and Monitoring System for Operational Technology},
year = {2021},
isbn = {9781450390514},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3465481.3470100},
doi = {10.1145/3465481.3470100},
booktitle = {The 16th International Conference on Availability, Reliability and Security},
articleno = {118},
numpages = {7},
keywords = {Honeypot, Modbus, S7comm, medium interaction., ICS},
location = {Vienna, Austria},
series = {ARES 2021}
}
```



