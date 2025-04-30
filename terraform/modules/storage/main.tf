variable "bucket_name_prefix" {
  description = "Prefix for the bucket name. Company standard."
  type        = string
}

variable "location" {
  description = "Bucket location. Defaulted to US-CENTRAL1 per company policy."
  type        = string
  default     = "US-CENTRAL1"
}

variable "env_suffix" {
  description = "Environment suffix (e.g., dev, prod). Drives naming and labeling."
  type        = string
}

variable "data_classification_label" {
  description = "Value for the 'data_classification' label. Company standard."
  type        = string
  default     = "general"
}

resource "google_storage_bucket" "standard_bucket" {
  name                        = "${var.bucket_name_prefix}-bucket-${var.env_suffix}-${random_id.bucket_suffix.hex}"
  location                    = var.location
  uniform_bucket_level_access = true
  storage_class               = "STANDARD"

  versioning {
    enabled = true
  }

  labels = {
    environment         = var.env_suffix
    managed_by          = "terraform-gemini-base"
    cost_allocation_code= "it-infra-001"
    data_classification = var.data_classification_label
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 3 # Shorter suffix for bucket names
}

output "bucket_id" {
  value = google_storage_bucket.standard_bucket.id
}

output "bucket_url" {
  value = google_storage_bucket.standard_bucket.url
}