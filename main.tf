locals {
  default_db_node_size = "${terraform.workspace == "staging" ? "1gb" : "2gb"}"
}

# Creating the Galera cluster nodes
resource "digitalocean_droplet" "galera_cluster_node" {
  count              = "${var.db_node_count}"
  image              = "${var.image_slug}"
  name               = "${terraform.workspace}-${var.project}-database-${format("%02d", count.index + 1)}"
  region             = "${var.region}"
  size               = "${var.db_node_size == "" ? local.default_db_node_size : var.db_node_size}"
  private_networking = true
  ssh_keys           = ["${split(",",var.keys)}"]
  tags               = ["${digitalocean_tag.env_tag.id}", "${digitalocean_tag.project_tag.id}", "${digitalocean_tag.resource_role1.id}", "${digitalocean_tag.add_tag.id}"]
  user_data          = "${data.template_file.user_data.rendered}"

  lifecycle {
    # TODO: switch this to true after testing
    prevent_destroy = false
  }

  connection {
    user        = "root"
    type        = "ssh"
    private_key = "${var.private_key_path}"
    timeout     = "2m"
  }
}

# Creating the Galera load balancer nodes
resource "digitalocean_droplet" "galera_loadbalancer" {
  count              = 2
  image              = "${var.image_slug}"
  name               = "${terraform.workspace}-${var.project}-db-loadbalancer-${format("%02d", count.index + 1)}"
  region             = "${var.region}"
  size               = "${var.lb_size}"
  private_networking = true
  ssh_keys           = ["${split(",",var.keys)}"]
  tags               = ["${digitalocean_tag.env_tag.id}", "${digitalocean_tag.project_tag.id}", "${digitalocean_tag.resource_role2.id}", "${digitalocean_tag.add_tag.id}"]
  user_data          = "${data.template_file.user_data.rendered}"

  lifecycle {
    # TODO: switch this to true after testing
    prevent_destroy = false
  }

  connection {
    user        = "root"
    type        = "ssh"
    private_key = "${var.private_key_path}"
    timeout     = "2m"
  }
}

# Passing in user-data to set up Ansible user for configuration
data "template_file" "user_data" {
  template = "${file("${path.root}/config/cloud-config.yaml")}"

  vars {
    public_key   = "${var.public_key}"
    ansible_user = "${var.ansible_user}"
  }
}

resource "digitalocean_floating_ip" "ha_db_fip" {
  region     = "${var.region}"
  droplet_id = "${digitalocean_droplet.galera_loadbalancer.0.id}"
}
