# Overview 
LOGistICS is a monitoring framework for investigating the security of industrial PLC systems. Diverse processing components and probes with different tasks are included in the architecture. The honeypot node logs S7 and Modbus traffic.

![alt text](https://github.com/kaisersource/LOGistICS/blob/main/Low%20Level%20Design/LLD%20Logistics%20ASIS.svg)

Build LOGistICS container inside the dir by using:
docker build -t logistics .

Execute in interactive mode in order to enable GUI:
docker run -it -p 102:102 -p 502:502 logistics

To detach the container and avoid its suicide do:
ctrl+p, then ctrl+q 

[TODO]

- [x] Ehnancement: deploy LOGistICS by using Compose or Acorn
- [ ] Migrate snap7 from 1.4.0 to 1.4.3
- [ ] Container Hardening
- [ ] Continuous improvement of Python-based Analysis based on ZAT.
- [ ] DTW on collected data
- [ ] Add support of further ICS protocols e.g. DNP3
- [ ] Compile multiple firmware inside the image

### v0.1.1
- [x] Merging honeypot setup with a shell script
- [x] Pyshark update (latest - 0.6)
- [x] Fixed KaiserSniff where live capture couldn't be possible in some circumstances.
- [x] Supervisord integration for proper process management inside a container.
- [x] Moved Python dependencies to requirements.txt
- [x] Multistage Build shrinked image to 700 MB 
- [x] Update image to ubuntu 24.04

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


