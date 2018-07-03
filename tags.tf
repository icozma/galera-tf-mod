resource "digitalocean_tag" "env_tag" {
  name = "${basename(path.root)}"
}

resource "digitalocean_tag" "project_tag" {
  name = "${var.project}"
}

resource "digitalocean_tag" "resource_role1" {
  name = "database"
}

resource "digitalocean_tag" "resource_role2" {
  name = "database-loadbalancer"
}

resource "digitalocean_tag" "add_tag" {
  name = "galera"
}
