terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "exam-reminder-rg"
  location = "norwayeast"

  lifecycle {
    prevent_destroy = true
    ignore_changes  = all
  }
}


# Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "examreminderhkr123"
  resource_group_name = azurerm_resource_group.rg.name
  location            = "norwayeast"
  sku                 = "Basic"
  admin_enabled       = true
}



# Container App Environment
resource "azurerm_container_app_environment" "env" {
  name                = "exam-reminder-env"
  location            = "norwayeast"
  resource_group_name = azurerm_resource_group.rg.name
}

# Container App
resource "azurerm_container_app" "app" {
  name                         = "exam-reminder-app"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  template {
    container {
      name   = "exam-reminder-app"
      image  = "${azurerm_container_registry.acr.login_server}/exam-reminder:latest"
      cpu    = 0.5
      memory = "1Gi"
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8501

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server   = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  
}

output "container_app_url" {
    value = "https://${azurerm_container_app.app.latest_revision_fqdn}"

}