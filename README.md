## Module Parameters

#### Required
* project
* region
* keys
* private_key_path
* ssh_fingerprint
* public_key
* ansible_user

#### Optional
* db_node_count -> *(default = 3. Recommended value is 5 for production)*
* db_node_size -> *(default = 4gb)*
* lb_size -> *(default = 4gb)*
* image_slug -> *(default = ubuntu-16-04-x64)*

---

## Example Usage

#### main.tf

    module "galera-cluster" {
      source           = "git::git@bitbucket.org:cmndrsp0ck/galera-cluster.git?ref=v1.0.0"
      db_node_count    = "5"
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

**note**: The module *source* path used depends on how you've set up your directory structure.
