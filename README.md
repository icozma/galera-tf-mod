## Module Parameters

#### Required
* project: Used for Droplet names in DigitalOcean
* region: data center to use for deployment
* keys: ssh key ids stored in DigitalOcean's system. Retrievable through API
* private_key_path: commonly /home/user/.ssh/id_rsa
* ssh_fingerprint: md5 ssh key fingerprint
* public_key: id_rsa.pub contents
* ansible_user: username which will be used by ansible to connect to remote hosts

#### Optional
* db_node_count -> *(default = 3)*
* db_node_size -> *(default = 4gb)*
* lb_size -> *(default = 4gb)*
* image_slug -> *(default = ubuntu-16-04-x64)*

---

## Example Usage

#### main.tf

    module "galera-cluster" {
      source           = "git::git@bitbucket.org:cmndrsp0ck/galera-cluster.git?ref=v1.0.2"
      db_node_count    = "3"
      db_node_size     = "16gb"
      lb_size          = "c-2"
      project          = "${var.project}"
      region           = "${var.region}"
      keys             = "${var.keys}"
      private_key_path = "${var.private_key_path}"
      ssh_fingerprint  = "${var.ssh_fingerprint}"
      public_key       = "${var.public_key}"
      ansible_user     = "${var.ansible_user}"
    }
