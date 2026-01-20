terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
# Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
#  credentials = 
  credentials = "proud-outrider-483901-c3-2f890d3d3b86.json"
  project = "proud-outrider-483901-c3"
  region  = "us-central1"
}



resource "google_storage_bucket" "data-lake-bucket" {
  # name          = "<Your Unique Bucket Name>"
  name          = "w1-terraform-lesson"
  location      = "US"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = "w1-terraform-lesson"
  project    = "proud-outrider-483901-c3"
  location   = "US"
}