variable "vm_name_prefix" {
  description = "Prefix for the VM name. Company standard."
  type        = string
  default     = "vm"
}

variable "project_id" {
  description = "GCP Project ID where the VM will be created."
  type        = string
}

variable "zone" {
  description = "GCP Zone for the VM. Defaulted to us-central1-a per company policy."
  type        = string
  default     = "us-central1-a"
}

variable "machine_type" {
  description = "Machine type for the VM. Company standard default is e2-medium."
  type        = string
  default     = "e2-medium"
}

variable "env" {
  description = "Environment (dev, qa, prod). Drives naming and labeling."
  type        = string
}

variable "boot_disk_image" {
  description = "Boot disk image for the VM. Company standard is Debian 11."
  type        = string
  default     = "debian-cloud/debian-11"
}

variable "custom_tags" {
  description = "Additional custom tags for the VM."
  type        = map(string)
  default     = {}
}

resource "google_compute_instance" "standard_vm" {
  project      = var.project_id
  zone         = var.zone
  name         = "${var.vm_name_prefix}-${var.env}-${random_id.vm_suffix.hex}"
  machine_type = var.machine_type

  boot_disk {
    initialize_params {
      image = var.boot_disk_image
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  labels = merge({
    environment   = var.env
    managed_by    = "terraform-gemini-base"
    cost_center   = "cc123-department-x"
    app_name      = var.vm_name_prefix
    },
    var.custom_tags
  )

  service_account {
    scopes = ["cloud-platform"]
  }

  allow_stopping_for_update = true
}

resource "random_id" "vm_suffix" {
  byte_length = 4
}

output "instance_name" {
  value = google_compute_instance.standard_vm.name
}

output "instance_self_link" {
  value = google_compute_instance.standard_vm.self_link
}

output "instance_public_ip" {
  description = "The public IP address of the VM instance, if available."
  value       = try(google_compute_instance.standard_vm.network_interface[0].access_config[0].nat_ip, "N/A")
}