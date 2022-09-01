# README #


## System Requirements
- CentOS 7
- Enable ISCSI
```shell=
yum install iscsi-initiator-utils
systemctl enable --now iscsid
```
- Install NFS utils
```shell=
yum install nfs-utils
```

<<<<<<< HEAD
=======

>>>>>>> f3d4478c7959641c1cdd3b02d6cfc724ab0d36b9
## Use Persistent Volume
- Due to RWO, strategy of deployment must be Recreate
```yaml
strategy:
  type: Recreate
```

