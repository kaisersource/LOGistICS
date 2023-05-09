# Overview 
LOGistICS is a monitoring framework for investigating the security of industrial PLC systems. Diverse processing components and probes with different tasks are included in the architecture



Build LOGistICS container inside the dir by using:
docker build -t logistics .

Execute in interactive mode in order to enable GUI:
docker run -it -p 102:102 -p 502:502 logistics

In order to detach the container and avoid its suicide do:
ctrl+p, then ctrl+q 

[TODO]
- [x] Deploy proper implementation of pyshark module, enhanced with its latest features
- [x] Step 1: Supervisord integration for proper process management inside a container. Step 2: splitting logistics in microservices, one for each exposed svc.
- [x] Ehnancement: deploy LOGistICS by using Compose or Acorn
- [x] Migrate snap7 to pysnap7
- [x] Container Hardening
- [x] Move GUI to website 
- [x] Migrate template params from csv to ARM/SQL database compliant.   
- [x] Continuous improvement of Python-based Analysis based on ZAT.
- [x] Save internal states of PLC inside a Cache-based DB (eg. Redis).
- [x] Dynamic Time Warping on collected logs in order to check the correlation between events based on time.

### v0.1.1
- [x] Merging honeypot setup with a shell script
- [ ] Upload updated version of pyshark-based capture script
- [ ] Check and report deployment differences between Zeek versions (3.0.8 was used. Otherwise Security Onion distro is adviced)
- [ ] Docker compose to start all the services, then make the honeypot container a dependency of the capture container 
- [ ] Add support of further ICS protocols e.g. DNP3. 
- [x] Moved Python dependencies to requirements.txt

### v.0.1.0

- [x] S7comm honeypot
- [x] Modbus honeypot 
- [x] S7comm gui template
- [x] Modbus gui template


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

``` tex
@article{bistarelli2022identifying,
  title={On Identifying Repeated Patterns of OT Attacks with LOGistICS},
  author={Bistarelli, Stefano and Bosimini, Emanuele and Santini, Francesco},
  year={2022}
}
```


