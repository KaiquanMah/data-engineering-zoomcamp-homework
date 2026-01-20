## GCP Overview

[Video](https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=2)


### Project infrastructure modules in GCP:
* Google Cloud Storage (GCS): Data Lake
* BigQuery: Data Warehouse

(Concepts explained in Week 2 - Data Ingestion)

### Initial Setup

For this course, we'll use a free version (upto EUR 300 credits). 

1. Create an account with your Google email ID 
2. Setup your first [project](https://console.cloud.google.com/) if you haven't already
    * eg. "DTC DE Course", and note down the "Project ID" (we'll use this later when deploying infra with TF)
3. Setup [service account & authentication](https://cloud.google.com/docs/authentication/getting-started) for this project
    * Grant `Viewer` role to begin with.
    * Download service-account-keys (.json) for auth.
4. Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup
5. Set environment variable to point to your downloaded GCP keys:
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   
   # Refresh token/session, and verify authentication
   gcloud auth application-default login
   ```
   
### Setup for Access
 
1. [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
   * Go to the *IAM* section of *IAM & Admin* https://console.cloud.google.com/iam-admin/iam
   * Click the *Edit principal* icon for your service account.
   * Add these roles in addition to *Viewer* : **Storage Admin** + **Storage Object Admin** + **BigQuery Admin**
   
2. Enable these APIs for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
   
3. Please ensure `GOOGLE_APPLICATION_CREDENTIALS` env-var is set.
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   ```
 
### Terraform Workshop to create GCP Infra
Continue [here](./terraform): `week_1_basics_n_setup/1_terraform_gcp/terraform`

# 2026.01.20 Kai - Use Terraform (WITHOUT VARIABLES) to deploy GCP resources, then delete resources
* Complete `01-docker-terraform\terraform\terraform\terraform_basic\main.tf` following video tutorial
* Place IAM service account key in `01-docker-terraform\terraform\terraform\proud-outrider-483901-c3-2f890d3d3b86.json`
* install terraform
```bash
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/terraform/terraform (main) $ terraform init
bash: terraform: command not found


@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/terraform/terraform (main) $ wget https://releases.hashicorp.com/terraform/1.9.3/terraform_1.9.3_linux_amd64.zip
--2026-01-20 07:36:57--  https://releases.hashicorp.com/terraform/1.9.3/terraform_1.9.3_linux_amd64.zip
Resolving releases.hashicorp.com (releases.hashicorp.com)... 18.67.181.31, 18.67.181.38, 18.67.181.81, ...
Connecting to releases.hashicorp.com (releases.hashicorp.com)|18.67.181.31|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 27024283 (26M) [application/zip]
Saving to: ‘terraform_1.9.3_linux_amd64.zip’

terraform_1.9.3_linux_amd64.zip           100%[=====================================================================================>]  25.77M   125MB/s    in 0.2s    

2026-01-20 07:36:58 (125 MB/s) - ‘terraform_1.9.3_linux_amd64.zip’ saved [27024283/27024283]






@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/terraform/terraform (main) $ unzip terraform_*.zip
Archive:  terraform_1.9.3_linux_amd64.zip
  inflating: LICENSE.txt             
  inflating: terraform               

@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/terraform/terraform (main) $ sudo mv terraform /usr/local/bin/


# After installation, check if Terraform is in your PATH:
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/terraform/terraform (main) $ which terraform
/usr/local/bin/terraform


@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/terraform/terraform (main) $ echo $PATH
/usr/local/rvm/gems/ruby-3.4.7/bin:/usr/local/rvm/gems/ruby-3.4.7@global/bin:/usr/local/rvm/rubies/ruby-3.4.7/bin:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/debugCommand:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/copilotCli:/vscode/bin/linux-x64/585eba7c0c34fd6b30faac7c62a42050bfbc0086/bin/remote-cli:/home/codespace/.local/bin:/home/codespace/.dotnet:/home/codespace/nvm/current/bin:/home/codespace/.php/current/bin:/home/codespace/.python/current/bin:/home/codespace/java/current/bin:/home/codespace/.ruby/current/bin:/home/codespace/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/oryx:/usr/local/go/bin:/go/bin:/usr/local/sdkman/bin:/usr/local/sdkman/candidates/java/current/bin:/usr/local/sdkman/candidates/gradle/current/bin:/usr/local/sdkman/candidates/maven/current/bin:/usr/local/sdkman/candidates/ant/current/bin:/usr/local/rvm/gems/default/bin:/usr/local/rvm/gems/default@global/bin:/usr/local/rvm/rubies/default/bin:/usr/local/share/rbenv/bin:/usr/local/php/current/bin:/opt/conda/bin:/usr/local/nvs:/usr/local/share/nvm/versions/node/v24.11.1/bin:/usr/local/hugo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/share/dotnet:/home/codespace/.dotnet/tools:/usr/local/rvm/bin



@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/terraform/terraform (main) $ terraform --version
Terraform v1.9.3
on linux_amd64

Your version of Terraform is out of date! The latest version
is 1.14.3. You can update by downloading from https://www.terraform.io/downloads.html
```
* Test terraform config
```bash
cd 01-docker-terraform/terraform/terraform/terraform_basic



@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_basic (main) $ terraform init
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/google versions matching "4.51.0"...
- Installing hashicorp/google v4.51.0...
- Installed hashicorp/google v4.51.0 (signed by HashiCorp)


Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.


If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.











@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_basic (main) $ terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "w1-terraform-lesson"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + project                    = "proud-outrider-483901-c3"
      + self_link                  = (known after apply)

      + access (known after apply)
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "w1-terraform-lesson"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "Delete"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 30
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + versioning {
          + enabled = true
        }

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.


# created
#    01-docker-terraform/terraform/terraform/terraform_basic/.terraform/providers/registry.terraform.io/hashicorp/google/4.51.0/linux_amd64/terraform-provider-google_v4.51.0_x5
#    01-docker-terraform/terraform/terraform/terraform_basic/.terraform.lock.hcl












@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_basic (main) $ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "w1-terraform-lesson"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + project                    = "proud-outrider-483901-c3"
      + self_link                  = (known after apply)

      + access (known after apply)
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "w1-terraform-lesson"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "Delete"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 30
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + versioning {
          + enabled = true
        }

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes



google_storage_bucket.data-lake-bucket: Creating...
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=w1_terraform_lesson]


google_bigquery_dataset.dataset: Creating...
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/proud-outrider-483901-c3/datasets/w1_terraform_lesson]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```
* 01-docker-terraform/terraform/terraform/terraform_basic/.terraform.lock.hcl
```hcl
# This file is maintained automatically by "terraform init".
# Manual edits may be lost in future updates.

provider "registry.terraform.io/hashicorp/google" {
  version     = "4.51.0"
  constraints = "4.51.0"
  hashes = [
    "h1:7JFdiV9bvV6R+AeWzvNbVeoega481sJY3PqtIbrwTsM=",
    "zh:001bf7478e495d497ffd4054453c97ab4dd3e6a24d46496d51d4c8094e95b2b1",
    "zh:19db72113552dd295854a99840e85678d421312708e8329a35787fff1baeed8b",
    "zh:42c3e629ace225a2cb6cf87b8fabeaf1c56ac8eca6a77b9e3fc489f3cc0a9db5",
    "zh:50b930755c4b1f8a01c430d8f688ea79de0b0198c87511baa3a783e360d7e624",
    "zh:5acd67f0aafff5ad59e179543cccd1ffd48d69b98af0228506403b8d8193b340",
    "zh:70128d57b4b4bf07df941172e6af15c4eda8396af5cc2b0128c906983c7b7fad",
    "zh:7905fac0ba2becf0e97edfcd4224e57466b04f960f36a3ec654a0a3c2ffececb",
    "zh:79b4cc760305cd77c1ff841f789184f808b8052e8f4faa5cb8d518e4c13beb22",
    "zh:c7aebd7d7dd2b29de28e382500d36fae8b4d8a192cf05e41ea29c66f1251acfc",
    "zh:d8b4494b13ef5af65d3afedf05bf7565918f1e31ad68ae0df81f5c3b12baf519",
    "zh:e6e68ef6881bc3312db50c9fd761f226f34d7834b64f90d96616b7ca6b1daf34",
    "zh:f569b65999264a9416862bca5cd2a6177d94ccb0424f3a4ef424428912b9cb3c",
  ]
}
```
* 01-docker-terraform/terraform/terraform/terraform_basic/terraform.tfstate
```hcl
{
  "version": 4,
  "terraform_version": "1.9.3",
  "serial": 9,
  "lineage": "ac95d89c-c20b-5047-44f4-0499dbb78756",
  "outputs": {},
  "resources": [
    {
      "mode": "managed",
      "type": "google_bigquery_dataset",
      "name": "dataset",
      "provider": "provider[\"registry.terraform.io/hashicorp/google\"]",
      "instances": [
        {
          "schema_version": 0,
          "attributes": {
            "access": [
              {
                "dataset": [],
                "domain": "",
                "group_by_email": "",
                "role": "OWNER",
                "routine": [],
                "special_group": "",
                "user_by_email": "terraform-runner@proud-outrider-483901-c3.iam.gserviceaccount.com",
                "view": []
              },
              {
                "dataset": [],
                "domain": "",
                "group_by_email": "",
                "role": "OWNER",
                "routine": [],
                "special_group": "projectOwners",
                "user_by_email": "",
                "view": []
              },
              {
                "dataset": [],
                "domain": "",
                "group_by_email": "",
                "role": "READER",
                "routine": [],
                "special_group": "projectReaders",
                "user_by_email": "",
                "view": []
              },
              {
                "dataset": [],
                "domain": "",
                "group_by_email": "",
                "role": "WRITER",
                "routine": [],
                "special_group": "projectWriters",
                "user_by_email": "",
                "view": []
              }
            ],
            "creation_time": 1768896005465,
            "dataset_id": "w1_terraform_lesson",
            "default_encryption_configuration": [],
            "default_partition_expiration_ms": 0,
            "default_table_expiration_ms": 0,
            "delete_contents_on_destroy": false,
            "description": "",
            "etag": "rRpDWp0SFZFoBNkutbcWwg==",
            "friendly_name": "",
            "id": "projects/proud-outrider-483901-c3/datasets/w1_terraform_lesson",
            "labels": {},
            "last_modified_time": 1768896005465,
            "location": "US",
            "max_time_travel_hours": "168",
            "project": "proud-outrider-483901-c3",
            "self_link": "https://bigquery.googleapis.com/bigquery/v2/projects/proud-outrider-483901-c3/datasets/w1_terraform_lesson",
            "timeouts": null
          },
          "sensitive_attributes": [],
          "private": "eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoxMjAwMDAwMDAwMDAwLCJkZWxldGUiOjEyMDAwMDAwMDAwMDAsInVwZGF0ZSI6MTIwMDAwMDAwMDAwMH19"
        }
      ]
    },
    {
      "mode": "managed",
      "type": "google_storage_bucket",
      "name": "data-lake-bucket",
      "provider": "provider[\"registry.terraform.io/hashicorp/google\"]",
      "instances": [
        {
          "schema_version": 0,
          "attributes": {
            "autoclass": [],
            "cors": [],
            "custom_placement_config": [],
            "default_event_based_hold": false,
            "encryption": [],
            "force_destroy": true,
            "id": "w1_terraform_lesson",
            "labels": {},
            "lifecycle_rule": [
              {
                "action": [
                  {
                    "storage_class": "",
                    "type": "Delete"
                  }
                ],
                "condition": [
                  {
                    "age": 30,
                    "created_before": "",
                    "custom_time_before": "",
                    "days_since_custom_time": 0,
                    "days_since_noncurrent_time": 0,
                    "matches_prefix": [],
                    "matches_storage_class": [],
                    "matches_suffix": [],
                    "noncurrent_time_before": "",
                    "num_newer_versions": 0,
                    "with_state": "ANY"
                  }
                ]
              }
            ],
            "location": "US",
            "logging": [],
            "name": "w1_terraform_lesson",
            "project": "proud-outrider-483901-c3",
            "public_access_prevention": "inherited",
            "requester_pays": false,
            "retention_policy": [],
            "self_link": "https://www.googleapis.com/storage/v1/b/w1_terraform_lesson",
            "storage_class": "STANDARD",
            "timeouts": null,
            "uniform_bucket_level_access": true,
            "url": "gs://w1_terraform_lesson",
            "versioning": [
              {
                "enabled": true
              }
            ],
            "website": []
          },
          "sensitive_attributes": [],
          "private": "eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsInJlYWQiOjI0MDAwMDAwMDAwMCwidXBkYXRlIjoyNDAwMDAwMDAwMDB9fQ=="
        }
      ]
    }
  ],
  "check_results": null
}

```

* now delete GCP resources
```bash
@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_basic (main) $ terraform destroy
google_bigquery_dataset.dataset: Refreshing state... [id=projects/proud-outrider-483901-c3/datasets/w1_terraform_lesson]
google_storage_bucket.data-lake-bucket: Refreshing state... [id=w1_terraform_lesson]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be destroyed
  - resource "google_bigquery_dataset" "dataset" {
      - creation_time                   = 1768896005465 -> null
      - dataset_id                      = "w1_terraform_lesson" -> null
      - default_partition_expiration_ms = 0 -> null
      - default_table_expiration_ms     = 0 -> null
      - delete_contents_on_destroy      = false -> null
      - etag                            = "rRpDWp0SFZFoBNkutbcWwg==" -> null
      - id                              = "projects/proud-outrider-483901-c3/datasets/w1_terraform_lesson" -> null
      - labels                          = {} -> null
      - last_modified_time              = 1768896005465 -> null
      - location                        = "US" -> null
      - max_time_travel_hours           = "168" -> null
      - project                         = "proud-outrider-483901-c3" -> null
      - self_link                       = "https://bigquery.googleapis.com/bigquery/v2/projects/proud-outrider-483901-c3/datasets/w1_terraform_lesson" -> null
        # (2 unchanged attributes hidden)

      - access {
          - role           = "OWNER" -> null
          - user_by_email  = "terraform-runner@proud-outrider-483901-c3.iam.gserviceaccount.com" -> null
            # (3 unchanged attributes hidden)
        }
      - access {
          - role           = "OWNER" -> null
          - special_group  = "projectOwners" -> null
            # (3 unchanged attributes hidden)
        }
      - access {
          - role           = "READER" -> null
          - special_group  = "projectReaders" -> null
            # (3 unchanged attributes hidden)
        }
      - access {
          - role           = "WRITER" -> null
          - special_group  = "projectWriters" -> null
            # (3 unchanged attributes hidden)
        }
    }

  # google_storage_bucket.data-lake-bucket will be destroyed
  - resource "google_storage_bucket" "data-lake-bucket" {
      - default_event_based_hold    = false -> null
      - force_destroy               = true -> null
      - id                          = "w1_terraform_lesson" -> null
      - labels                      = {} -> null
      - location                    = "US" -> null
      - name                        = "w1_terraform_lesson" -> null
      - project                     = "proud-outrider-483901-c3" -> null
      - public_access_prevention    = "inherited" -> null
      - requester_pays              = false -> null
      - self_link                   = "https://www.googleapis.com/storage/v1/b/w1_terraform_lesson" -> null
      - storage_class               = "STANDARD" -> null
      - uniform_bucket_level_access = true -> null
      - url                         = "gs://w1_terraform_lesson" -> null

      - lifecycle_rule {
          - action {
              - type          = "Delete" -> null
                # (1 unchanged attribute hidden)
            }
          - condition {
              - age                        = 30 -> null
              - days_since_custom_time     = 0 -> null
              - days_since_noncurrent_time = 0 -> null
              - matches_prefix             = [] -> null
              - matches_storage_class      = [] -> null
              - matches_suffix             = [] -> null
              - num_newer_versions         = 0 -> null
              - with_state                 = "ANY" -> null
                # (3 unchanged attributes hidden)
            }
        }

      - versioning {
          - enabled = true -> null
        }
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

google_storage_bucket.data-lake-bucket: Destroying... [id=w1_terraform_lesson]
google_bigquery_dataset.dataset: Destroying... [id=projects/proud-outrider-483901-c3/datasets/w1_terraform_lesson]
google_bigquery_dataset.dataset: Destruction complete after 1s
google_storage_bucket.data-lake-bucket: Destruction complete after 2s

Destroy complete! Resources: 2 destroyed.
```




# 2026.01.20 Kai - Use Terraform (WITH VARIABLES) to deploy GCP resources, then delete resources
```bash
cd 01-docker-terraform/terraform/terraform/terraform_with_variables
# or
@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_basic (main) $ cd ../terraform_with_variables/










@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_with_variables (main) $ terraform init
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/google versions matching "5.6.0"...
- Installing hashicorp/google v5.6.0...
- Installed hashicorp/google v5.6.0 (signed by HashiCorp)
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.










@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_with_variables (main) $ terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "proud-outrider-483901-c3"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)

      + access (known after apply)
    }

  # google_storage_bucket.demo_bucket will be created
  + resource "google_storage_bucket" "demo_bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo_terra_bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "AbortIncompleteMultipartUpload"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 1
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + versioning (known after apply)

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.












@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_with_variables (main) $ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "proud-outrider-483901-c3"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)

      + access (known after apply)
    }

  # google_storage_bucket.demo_bucket will be created
  + resource "google_storage_bucket" "demo_bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo_terra_bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "AbortIncompleteMultipartUpload"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 1
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + versioning (known after apply)

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo_bucket: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 2s [id=projects/proud-outrider-483901-c3/datasets/demo_dataset]
google_storage_bucket.demo_bucket: Creation complete after 2s [id=terraform-demo_terra_bucket]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.













@kaiquanmah0 ➜ .../01-docker-terraform/terraform/terraform/terraform_with_variables (main) $ terraform destroy
google_storage_bucket.demo_bucket: Refreshing state... [id=terraform-demo_terra_bucket]
google_bigquery_dataset.demo_dataset: Refreshing state... [id=projects/proud-outrider-483901-c3/datasets/demo_dataset]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be destroyed
  - resource "google_bigquery_dataset" "demo_dataset" {
      - creation_time                   = 1768897110991 -> null
      - dataset_id                      = "demo_dataset" -> null
      - default_partition_expiration_ms = 0 -> null
      - default_table_expiration_ms     = 0 -> null
      - delete_contents_on_destroy      = false -> null
      - effective_labels                = {} -> null
      - etag                            = "lrD+C93jSlsXGXvpd8n5Iw==" -> null
      - id                              = "projects/proud-outrider-483901-c3/datasets/demo_dataset" -> null
      - is_case_insensitive             = false -> null
      - labels                          = {} -> null
      - last_modified_time              = 1768897110991 -> null
      - location                        = "US" -> null
      - max_time_travel_hours           = "168" -> null
      - project                         = "proud-outrider-483901-c3" -> null
      - self_link                       = "https://bigquery.googleapis.com/bigquery/v2/projects/proud-outrider-483901-c3/datasets/demo_dataset" -> null
      - terraform_labels                = {} -> null
        # (4 unchanged attributes hidden)

      - access {
          - role           = "OWNER" -> null
          - user_by_email  = "terraform-runner@proud-outrider-483901-c3.iam.gserviceaccount.com" -> null
            # (4 unchanged attributes hidden)
        }
      - access {
          - role           = "OWNER" -> null
          - special_group  = "projectOwners" -> null
            # (4 unchanged attributes hidden)
        }
      - access {
          - role           = "READER" -> null
          - special_group  = "projectReaders" -> null
            # (4 unchanged attributes hidden)
        }
      - access {
          - role           = "WRITER" -> null
          - special_group  = "projectWriters" -> null
            # (4 unchanged attributes hidden)
        }
    }

  # google_storage_bucket.demo_bucket will be destroyed
  - resource "google_storage_bucket" "demo_bucket" {
      - default_event_based_hold    = false -> null
      - effective_labels            = {} -> null
      - enable_object_retention     = false -> null
      - force_destroy               = true -> null
      - id                          = "terraform-demo_terra_bucket" -> null
      - labels                      = {} -> null
      - location                    = "US" -> null
      - name                        = "terraform-demo_terra_bucket" -> null
      - project                     = "proud-outrider-483901-c3" -> null
      - public_access_prevention    = "inherited" -> null
      - requester_pays              = false -> null
      - self_link                   = "https://www.googleapis.com/storage/v1/b/terraform-demo_terra_bucket" -> null
      - storage_class               = "STANDARD" -> null
      - terraform_labels            = {} -> null
      - uniform_bucket_level_access = false -> null
      - url                         = "gs://terraform-demo_terra_bucket" -> null

      - lifecycle_rule {
          - action {
              - type          = "AbortIncompleteMultipartUpload" -> null
                # (1 unchanged attribute hidden)
            }
          - condition {
              - age                        = 1 -> null
              - days_since_custom_time     = 0 -> null
              - days_since_noncurrent_time = 0 -> null
              - matches_prefix             = [] -> null
              - matches_storage_class      = [] -> null
              - matches_suffix             = [] -> null
              - num_newer_versions         = 0 -> null
              - with_state                 = "ANY" -> null
                # (3 unchanged attributes hidden)
            }
        }
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

google_storage_bucket.demo_bucket: Destroying... [id=terraform-demo_terra_bucket]
google_bigquery_dataset.demo_dataset: Destroying... [id=projects/proud-outrider-483901-c3/datasets/demo_dataset]
google_bigquery_dataset.demo_dataset: Destruction complete after 0s
google_storage_bucket.demo_bucket: Destruction complete after 1s

Destroy complete! Resources: 2 destroyed.


```

