terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "neural_net" {
  name = "neural-net"
}

resource "docker_image" "orchestrator" {
  name         = "neural-orchestrator:latest"
  keep_locally = true
}

resource "docker_container" "orchestrator" {
  image = docker_image.orchestrator.image_id
  name  = "ai-orchestrator"

  ports {
    internal = 8000
    external = 8000
  }

  networks_advanced {
    name = docker_network.neural_net.name
  }
}
